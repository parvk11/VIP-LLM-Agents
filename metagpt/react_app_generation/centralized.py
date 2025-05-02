#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 17:45
@Author  : alexanderwu
@File    : write_code.py
@Modified By: mashenquan, 2023-11-1. In accordance with Chapter 2.1.3 of RFC 116, modify the data type of the `cause_by`
            value of the `Message` object.
@Modified By: mashenquan, 2023-11-27.
        1. Mark the location of Design, Tasks, Legacy Code and Debug logs in the PROMPT_TEMPLATE with markdown
        code-block formatting to enhance the understanding for the LLM.
        2. Following the think-act principle, solidify the task parameters when creating the WriteCode object, rather
        than passing them in when calling the run function.
        3. Encapsulate the input of RunCode into RunCodeContext and encapsulate the output of RunCode into
        RunCodeResult to standardize and unify parameter passing between WriteCode, RunCode, and DebugError.
"""

import json

from pydantic import Field
from tenacity import retry, stop_after_attempt, wait_random_exponential

from metagpt.actions.action import Action
from metagpt.actions.project_management_an import REFINED_TASK_LIST, TASK_LIST
from metagpt.actions.write_code_plan_and_change_an import REFINED_TEMPLATE
from metagpt.const import BUGFIX_FILENAME, REQUIREMENT_FILENAME
from metagpt.logs import logger
from metagpt.schema import CodingContext, Document, RunCodeResult
from metagpt.utils.common import CodeParser
from metagpt.utils.project_repo import ProjectRepo

PROMPT_TEMPLATE = """
NOTICE
Role: You are a professional engineer; the main goal is to write google-style, elegant, modular, easy to read and maintain code
Language: Please use the same language as the user requirement, but the title and code should be still in English. For example, if the user speaks Chinese, the specific text of your answer should also be in Chinese.
ATTENTION: Use '##' to SPLIT SECTIONS, not '#'. Output format carefully referenced "Format example".

# Context
## Overall context
{context}
## Design Review
{design}

## Task
Implement Design Review in javascript. 

## Legacy Code
```Code
{code}
```

## Debug logs
```text
{logs}

{summary_log}
```

## Bug Feedback logs
```text
{feedback}
```

# Format example
## Code: {filename}
```javascript
## {filename}
...
```

# Instruction: Based on the context, follow "Format example", write code.

## Code: {filename}. Write code with triple quoto, based on the following attentions and context.
1. Only One file: do your best to implement THIS ONLY ONE FILE.
2. COMPLETE CODE: Your code will be part of the entire project, so please implement complete, reliable, reusable code snippets.
3. Set default value: If there is any setting, ALWAYS SET A DEFAULT VALUE, ALWAYS USE STRONG TYPE AND EXPLICIT VARIABLE. AVOID circular import.
4. Follow design: YOU MUST FOLLOW "Data structures and interfaces". DONT CHANGE ANY DESIGN. Do not use public member functions that do not exist in your design.
5. CAREFULLY CHECK THAT YOU DONT MISS ANY NECESSARY CLASS/FUNCTION IN THIS FILE.
6. Before using a external variable/module, make sure you import it first.
7. Write out EVERY CODE DETAIL, DON'T LEAVE TODO.

"""

from metagpt.roles import Role, Engineer, Architect, QaEngineer, ProductManager, ProjectManager
from metagpt.actions import WriteTasks, WriteDesign, WritePRD, WriteCode, ActionOutput
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


# from metagpt.utils import split_10_subtask

class Coordinator(ProductManager):
    action_stack: List[Action] = []
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # Initialize actions specific to the Coordinator role
        self.action_stack = [PrepareDocuments, WritePRD, CoordinatorReviewArchitecture, CoordinatorReviewCode, CoordinatorReviewTests]
        self.set_actions(self.action_stack) 

        # Subscribe to messages
        self._watch({UserRequirement, PrepareDocuments, WriteDesign, WriteCode, SimpleWriteTest}) #
   
    async def _act(self):
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo
        code_text = await todo.run(self.rc.history)
        logger.info(f"code_text: {code_text}")
       
        temp = code_text
        if(type(code_text) == ActionOutput):
            code_text = code_text.instruct_content
        
        self.action_stack.pop(0)
        self.set_actions(self.action_stack)
        self.rc.env.publish_message(Message(content=str(code_text), cause_by=str(todo)))
        return Message(content=str(code_text), cause_by=todo)
    
    async def _think(self) -> bool:
        todo = self.rc.todo
        # logger.info(f"{self._setting}: memory {self.get_memories(k=3)}")
        self._set_state(0)
        self.todo_action = any_to_name(self.action_stack[0])
        logger.info(f"{self._setting}: to do action {self.todo_action}")
        # logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")

        # return bool(self.rc.todo)
        return True
    #     """Decide what to do"""
    #     if self.git_repo and not self.config.git_reinit:
    #         self._set_state(1)
    #         self.todo_action = any_to_name(self.action_stack[0])

    #     else:
    #         self._set_state(0)
    #         self.config.git_reinit = False
    #         self.todo_action = any_to_name(self.action_stack[0])
    #     logger.info(f"{self._setting}: to do action {self.todo_action}")
    #     # self.set_actions(self.action_stack)
    #     # print("TODO ACTION", self.todo_action)
    #     # print(" ACTION STACK", self.action_stack)
    #     logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
    #     return bool(self.rc.todo)
            
        
class CoordinatorReviewArchitecture(Action):
    PROMPT_TEMPLATE: str = """
    Context: {context}
    Please review the architecture for the given task and provide feedback. If approved, state APPROVED. If not, provide feedback.
    Provide in this format:
    [CONTENT]
    insert content here
    [/CONTENT]
    """
    name: str = "ReviewArchitecture"

    async def run(self, context: str, **kwargs):
        prompt = self.PROMPT_TEMPLATE.format(context=context)

        rsp = await self._aask(prompt)
        # Extract the content between [CONTENT] and [/CONTENT]
        pattern = r"\[CONTENT\](.*?)\[/CONTENT\]"
        match = re.search(pattern, rsp, re.DOTALL)
        if match:
            rsp = match.group(1).strip()
        else:
            rsp = rsp.strip()
        
        
        return rsp
    
class CoordinatorReviewCode(Action):
    PROMPT_TEMPLATE: str = """
    Context: {context}
    Please review the code for the given task and provide feedback. If approved, then provide the code in the format it was recieved.
    If not, provide feedback. and revise the code and output the code in the format it was received.
    Provide in this format:
    [CONTENT]
    insert content here
    [/CONTENT]
    """
    name: str = "ReviewCode"

    async def run(self, context: str, **kwargs):
        prompt = self.PROMPT_TEMPLATE.format(context=context)
        rsp = await self._aask(prompt)
        # Extract the content between [CONTENT] and [/CONTENT]
        pattern = r"\[CONTENT\](.*?)\[/CONTENT\]"
        match = re.search(pattern, rsp, re.DOTALL)
        if match:
            rsp = match.group(1).strip()
        else:
            rsp = rsp.strip()
        code = CodeParser.parse_code(block="", text=rsp, lang = "javascript")
        return code
        return rsp
    
class CoordinatorReviewTests(Action):
    PROMPT_TEMPLATE: str = """
    Context: {context}
    Please review the test cases for the given task and provide feedback. If approved, state APPROVED. If not, provide feedback.
    Provide in this format:
    [CONTENT]
    insert content here
    [/CONTENT]
    """
    name: str = "ReviewResults"

    async def run(self, context: str, **kwargs):
        prompt = self.PROMPT_TEMPLATE.format(context=context)
        rsp = await self._aask(prompt)
        # Extract the content between [CONTENT] and [/CONTENT]
        pattern = r"\[CONTENT\](.*?)\[/CONTENT\]"
        match = re.search(pattern, rsp, re.DOTALL)
        if match:
            rsp = match.group(1).strip()
        else:
            rsp = rsp.strip()
        return rsp
    
# class ArchitectAction(Role):
#     """
#     Make a system design based on the PRD, send to Coordinator for review.
#     """

# class Code(WriteCode):
#     def __init__(self, **kwargs) -> None:
#         super().__init__(**kwargs)
        
#     async def run(self, context: str, **kwargs):


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
    



class ArchitectA(Architect):
    name:str = "Alice"
    profile:str = "Architect"
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # Initialize actions specific to the Architect role
        self.set_actions([WriteDesign]) 
        self._watch({WritePRD, CoordinatorReviewArchitecture}) 
    
    # async def _act(self) -> Message:
    #     todo = self.rc.todo
    #     if
    #     context = self.get_memories()

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
       code = CodeParser.parse_code(block="", text=rsp, lang = "javascript")
       return code
       


class EngineerA(Engineer):
    name: str = "Bob"
    profile: str= "Engineer"
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # Initialize actions specific to the Engineer role
        self.set_actions([WriteSimpleCode]) 
        self._watch({CoordinatorReviewArchitecture})
        self.code_todos = [WriteCode]
    async def _think(self) -> bool:
        self._set_state(0)
        return True
    async def _act(self):
        todo = self.rc.todo
        coding_context = await todo.run(self.rc.history)
        print("coding_context", coding_context)
        msg = Message(
                content=coding_context,
                # instruct_content=coding_context,
                role=self.profile,
                cause_by=WriteCode,
            )
        self.rc.env.publish_message(msg)
        return msg


class CodeTester(Role):
    name:str = "Charlie"
    profile:str = "Code Tester"
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # Initialize actions specific to the Code Reviewer role
        self.set_actions([SimpleWriteTest]) 
        self._watch({CoordinatorReviewCode})



import asyncio
import time

context = Context() # Load config2.yaml
env = Environment(context=context)
env.add_roles([Coordinator(), ArchitectA(), EngineerA(), CodeTester()])
env.publish_message(Message(content='create a simple react todo app to be run locally by one user. no api spec needed. code should be in javascript. DO NOT USE TYPESCRIPT.', send_to=Coordinator)) # Send the user's message to Agent A to start the process.

async def main():
    start_time = time.time()
    while not env.is_idle: # `env.is_idle` becomes True only when all agents have no new messages to process.
        await env.run()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

asyncio.run(main())








