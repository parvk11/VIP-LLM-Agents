from metagpt.roles import Role, Engineer, Architect, QaEngineer, ProductManager, ProjectManager
from metagpt.actions import WriteTasks, WriteDesign, WritePRD, WriteCode, WriteTest, ActionOutput
from metagpt.actions.prepare_documents import PrepareDocuments
from metagpt.schema import Message
from metagpt.actions import UserRequirement
from typing import List
from metagpt.actions import Action
import re
from metagpt.config2 import Config
from metagpt.context import Context
from metagpt.environment import Environment
from metagpt.logs import logger
from metagpt.utils.common import any_to_name
from metagpt.actions.write_code import PROMPT_TEMPLATE
from metagpt.actions.project_management_an import REFINED_TASK_LIST, TASK_LIST
from metagpt.actions.write_code_plan_and_change_an import REFINED_TEMPLATE
from metagpt.const import BUGFIX_FILENAME, REQUIREMENT_FILENAME
from metagpt.schema import CodingContext, Document, RunCodeResult
from metagpt.utils.common import CodeParser
from metagpt.utils.project_repo import ProjectRepo

class Vote(Action):
    PROMPT_TEMPLATE:str = """"
    # Context {context}"  
    Please review the following action and vote YES if you think this is feasible, correct, and of high quality. 
    Vote NO if you think this is not feasible, incorrect, or of low quality. If you vote NO, please provide a reason. If you vote YES, please provide a reason. If you are unsure, please vote NO.
    """
    async def run(self, context: Context, **kwargs) :
        prompt = self.PROMPT_TEMPLATE.format(context=context)
        rsp:str = await self._aask(prompt)
        if ("YES" in rsp):
            return "YES"
        else:
            return "NO"
class ProductManagerRole(ProductManager):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.set_actions([PrepareDocuments, WritePRD, Vote])
        self._watch({Vote, WriteTasks, WriteDesign, WriteSimpleCode, SimpleWriteTest, UserRequirement})
    async def _think(self):
        most_recent_memory = self.rc.memory.get()[-1].content
        print("most_recent_memory", most_recent_memory, self.rc.memory.get()[-1].cause_by)
        print("caused by userreq? ", self.rc.memory.get()[-1].cause_by == 'metagpt.actions.add_requirement.UserRequirement')
        if("YES" in most_recent_memory):
            self._set_state(-1)
        elif("NO" in most_recent_memory or (self.rc.memory.get()[-1].cause_by == 'metagpt.actions.add_requirement.UserRequirement')):
            self._set_state(0)
        elif("NO" in most_recent_memory or (self.rc.memory.get()[-1].cause_by == 'metagpt.actions.add_requirement.PrepareDocuments')):
            self._set_state(1)
        else:
            self._set_state(2)
        return bool(self.rc.todo)
    async def _act(self):
        todo = self.rc.todo
        rsp = await todo.run(self.rc.history)
        if(type(rsp) == ActionOutput):
            rsp = rsp.instruct_content
        self.rc.env.publish_message(Message(content=(rsp), cause_by=todo))
        return Message(content=(rsp), cause_by=todo)



class ProjManagerRole(ProjectManager):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # Initialize actions specific to the Engineer role
        self.set_actions([CreateTasks, Vote]) 
        self._watch({Vote, WriteDesign, WriteSimpleCode, WritePRD, PrepareDocuments, SimpleWriteTest})
        
    async def _think(self):
        actions = self.actions
        most_recent_memory = self.rc.memory.get()[-1].content
        if("YES" in most_recent_memory):
            self._set_state(-1) #nothing to do
        elif("NO" in most_recent_memory or (self.rc.memory.get()[-1].cause_by == WriteDesign)):
            self._set_state(0) #write Design
        elif(self.rc.memory.get()[-1].cause_by != PrepareDocuments):
            self._set_state(1) #vote
        else:
            self._set_state(-1)
        return bool(self.rc.todo)
    async def _act(self):
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo
        rsp = await todo.run(context=self.context)
        self.rc.env.publish_message(Message(content=str(rsp), cause_by=todo))
        return Message(content=str(rsp), cause_by=todo)
    
        
class CreateTasks(WriteTasks):
    PROMPT_TEMPLATE:str = """"" \
    # Context {context}"
    Based on the system design, please create a task list for the project, this will be forwarded to the software engineer for implementation.
    """
    async def run(self, context: Context, **kwargs) :
        prompt = self.PROMPT_TEMPLATE.format(context=context)
        rsp:str = await self._aask(prompt)
        return rsp  
    
class EngineerRole(Engineer):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # Initialize actions specific to the Engineer role
        self.set_actions([WriteSimpleCode, Vote]) 
        self._watch({Vote, WriteTasks, WriteDesign, WritePRD, PrepareDocuments, SimpleWriteTest})
        
    async def _think(self):
        actions = self.actions
        most_recent_memory = self.rc.memory.get()[-1].content
        if("YES" in most_recent_memory):
            self._set_state(-1) #nothing to do
        elif("NO" in most_recent_memory or (self.rc.memory.get()[-1].cause_by == WriteTasks)):
            self._set_state(0) #write code
        elif(self.rc.memory.get()[-1].cause_by != PrepareDocuments):
            self._set_state(1) #vote #vote
        else:
            self._set_state(-1)
        return bool(self.rc.todo)
    async def _act(self):
        todo = self.rc.todo
        coding_context = await todo.run(self.rc.history)
        print("coding_context", coding_context)
        msg = Message(
                content=coding_context,
                # instruct_content=coding_context,
                role=self.profile,
                cause_by=todo,
            )
        self.rc.env.publish_message(msg)
        return msg

class WriteSimpleCode(Action):

    async def run(self, context, *args, **kwargs):
       bug_feedback = await self.repo.docs.get(filename=BUGFIX_FILENAME)
       
    #    coding_context = CodingContext.loads(self.i_context.content)
    #    test_doc = await self.repo.test_outputs.get(filename="test_" + coding_context.filename + ".json")
       requirement_doc = await self.repo.docs.get(filename=REQUIREMENT_FILENAME)
       summary_doc = None
       logs = ""
    #    if test_doc:
    #         test_detail = RunCodeResult.loads(test_doc.content)
    #         logs = test_detail.stderr
       prompt = PROMPT_TEMPLATE.format(
                overall_context=context,
                design=context,
                task=None,
                code=None,
                logs=logs,
                feedback=bug_feedback.content if bug_feedback else "",
                filename=None,
                summary_log=summary_doc.content if summary_doc else "",
            )
       rsp = await self._aask(prompt)
       code = CodeParser.parse_code(block="", text=rsp, lang = "typescript")
       return code
       
class ArchitectRole(Architect):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # Initialize actions specific to the Engineer role
        self.set_actions([WriteDesign, Vote]) 
        self._watch({Vote, WriteTasks, WriteSimpleCode, WritePRD, PrepareDocuments, SimpleWriteTest})
        
    async def _think(self):
        # actions = self.actions
        most_recent_memory = self.rc.memory.get()[-1].content
        if("YES" in most_recent_memory):
            self._set_state(-1) #nothing to do
        elif("NO" in most_recent_memory or (self.rc.memory.get()[-1].cause_by == WritePRD)):
            self._set_state(0) #write Design
        elif(self.rc.memory.get()[-1].cause_by != PrepareDocuments):
            self._set_state(1) #vote #vote
        else:
            self._set_state(-1)
        return bool(self.rc.todo)
    async def _act(self):
        todo = self.rc.todo
        rsp = await todo.run(context=self.context)
        self.rc.env.publish_message(Message(content=str(rsp), cause_by=todo))
        return Message(content=str(rsp), cause_by=todo)
    
    
class CodeTesterRole(QaEngineer):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # Initialize actions specific to the Engineer role
        self.set_actions([SimpleWriteTest, Vote]) 
        self._watch({Vote, WriteTasks, WriteDesign, WriteSimpleCode, WritePRD})
        
    async def _think(self):
        actions = self.actions
        most_recent_memory = self.rc.memory.get()[-1].content
        if("YES" in most_recent_memory):
            self._set_state(-1) #nothing to do
        elif("NO" in most_recent_memory or (self.rc.memory.get()[-1].cause_by == WriteSimpleCode)):
            self._set_state(0) #write test
        else:
            self._set_state(1) #vote
        return bool(self.rc.todo)
    async def _act(self):
        todo = self.rc.todo
        rsp = await todo.run(context=self.context)
        self.rc.env.publish_message(Message(content=str(rsp), cause_by=todo))
        return Message(content=str(rsp), cause_by=todo)
    

class SimpleWriteTest(Action):
    PROMPT_TEMPLATE: str = """
    Context: {context}
    Write {k} unit tests using jest for the given function, assuming you have imported it.
    Return ```javascript your_code_here ``` with NO other texts,
    your code:
    """

    name: str = "SimpleWriteTest"

    async def run(self, context: str, k: int = 3):
        prompt = self.PROMPT_TEMPLATE.format(context=context, k=k)

        rsp = await self._aask(prompt)

        code_text = self.parse_code(rsp)

        return code_text
    
    @staticmethod
    def parse_code(rsp):
        pattern = r"```javascript(.*)```"
        match = re.search(pattern, rsp, re.DOTALL)
        code_text = match.group(1) if match else rsp
        return code_text
    


import asyncio

context = Context() # Load config2.yaml
env = Environment(context=context)
env.add_roles([ProductManagerRole(), ProjManagerRole(), EngineerRole(), ArchitectRole(), CodeTesterRole()])
env.publish_message(Message(content='make a react to-do app')) # Send the user's message to Agent A to start the process.

async def main():
    while not env.is_idle: # `env.is_idle` becomes True only when all agents have no new messages to process.
        await env.run()

asyncio.run(main())
        