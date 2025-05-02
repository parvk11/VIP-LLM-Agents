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
# from metagpt.actions.write_code import PROMPT_TEMPLATE
from metagpt.actions.project_management_an import REFINED_TASK_LIST, TASK_LIST
from metagpt.actions.write_code_plan_and_change_an import REFINED_TEMPLATE
from metagpt.const import BUGFIX_FILENAME, REQUIREMENT_FILENAME
from metagpt.schema import CodingContext, Document, RunCodeResult
from metagpt.utils.common import CodeParser
from metagpt.utils.project_repo import ProjectRepo


# from metagpt.utils import split_10_subtask
class Planner(Role):
    name: str = "Alice"
    profile: str= "Planner"
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # Initialize actions specific to the Planner role
        self.set_actions([CreatePlan]) 
        self._watch({PrepareDocuments})
    async def _think(self) -> bool:
        todo = self.rc.todo
        self.todo_action = any_to_name(self.rc.todo)
        self._set_state(0)
        logger.info(f"{self._setting}: to do action {self.todo_action}")
        return True
    async def _act(self):
        todo = self.rc.todo
        code_text = await todo.run(self.rc.history)
        # logger.info(f"code_text: {code_text}")
        if(type(code_text) == ActionOutput):
            code_text = code_text.instruct_content
        self.rc.env.publish_message(Message(content=str(code_text), cause_by=str(todo)))
        return Message(content=str(code_text), cause_by=todo)

class Coordinator(Role):
    name: str = "Charlie"
    profile: str= "Coordinator"
    action_stack: List[Action] = []
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # Initialize actions specific to the Coordinator role
        self.action_stack = [PrepareDocuments,  ReviewPlan, CoordinatorReviewCode]
        self.set_actions(self.action_stack) 
        # Subscribe to messages
        self._watch({UserRequirement, CreatePlan, WriteCode}) #
   
    async def _act(self):
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo
        code_text = await todo.run(self.rc.history)
        # logger.info(f"code_text: {code_text}")
       
        if(type(code_text) == ActionOutput):
            code_text = code_text.instruct_content
        if(self.get_memories(k=1)[0].cause_by == CoordinatorReviewCode):
            if(self.get_memories(k=1)[0].content == "APPROVED"):
                self.action_stack.pop(0)
        else:
            self.action_stack.pop(0)
        self.set_actions(self.action_stack)
        self.rc.env.publish_message(Message(content=str(code_text), cause_by=str(todo)))
        return Message(content=str(code_text), cause_by=todo)
    
    async def _think(self) -> bool:
        todo = self.rc.todo

        if(len(self.action_stack) > 0):
            self.todo_action = any_to_name(self.action_stack[0])
        self._set_state(0)

        logger.info(f"{self._setting}: to do action {self.todo_action}")

        return True
class CreatePlan(Action):
    PROMPT_TEMPLATE: str = """
    Context: {context}
    Make a plan to fix the bugs in the code given. DO NOT WRITE CODE. Return the plan in the following format:
    1. Identify the bug in the code.
    2. Explain the bug and its impact.
    3. Provide a detailed plan to fix the bug.
    This will be sent to engineer for implementation.
    Return the plan in the following format:
    [CONTENT]
    content here
    [/CONTENT]
    """
    name: str = "CreatePRD"

    async def run(self, context: str, **kwargs):
        prompt = self.PROMPT_TEMPLATE.format(context=context)
        print("prompt", prompt)
        rsp = await self._aask(prompt)
        rsp = rsp.replace("[CONTENT]", "").replace("[/CONTENT]", "").strip()
        
        return rsp
    
class ReviewPlan(Action):
    PROMPT_TEMPLATE: str = """
    Context: {context}
    Please review the plan for the given task and provide feedback. If approved, provide the formatted plan. If not, revise the plan and output it.
    Your output should be in the following format:
    [CONTENT]
    content here
    [/CONTENT]
    """
    name: str = "ReviewPlan"

    async def run(self, context: str, **kwargs):
        prompt = self.PROMPT_TEMPLATE.format(context=context)
        rsp = await self._aask(prompt)
        rsp = rsp.replace("[CONTENT]", "").replace("[/CONTENT]", "").strip()
        
        return rsp

        

class CoordinatorReviewCode(Action):
    PROMPT_TEMPLATE: str = """
    Context: {context}
    Please review the code for the given task and provide feedback. If approved, state APPROVED. If not, provide feedback. 
    Output feedback in the following format:
    [CONTENT]
    content here
    [/CONTENT]
    """
    name: str = "ReviewCode"

    async def run(self, context: str, **kwargs):
        prompt = self.PROMPT_TEMPLATE.format(context=context)
        rsp = await self._aask(prompt)
        rsp = rsp.replace("[CONTENT]", "").replace("[/CONTENT]", "").strip()
        return rsp
    



class WriteSimpleCode(Action):
    PROMPT_TEMPLATE: str = """"
    You are an engineer to fix the bugs in the code. You are given the following context and plan by a Coordinator.
    "Plan and Requirements: {overall_context}\n" 
    "You should write code in Python to fix the bugs. Return the code in the following format:
    ```python
    # your code here
    ```
    
    """


    async def run(self, context, *args, **kwargs):
       prompt = self.PROMPT_TEMPLATE.format(
                overall_context=context,
            )
       rsp = await self._aask(prompt)
       code = CodeParser.parse_code(block="", text=rsp, lang = "python")
       save_text_to_file(sys.argv[1], code)
       return code
       


class EngineerA(Engineer):
    name: str = "Bob"
    profile: str= "Engineer"
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # Initialize actions specific to the Engineer role
        self.set_actions([WriteSimpleCode]) 
        self._watch({ReviewPlan, CoordinatorReviewCode})
        self.code_todos = [WriteCode]
    async def _think(self) -> bool:
        most_recent_message = self.get_memories(k=1)[0].content
        if "APPROVED" in most_recent_message:
            self._set_state(-1)
        else:
            self._set_state(0)
        return True
    async def _act(self):
        todo = self.rc.todo
        coding_context = await todo.run(self.rc.history)
        msg = Message(
                content=coding_context,
                # instruct_content=coding_context,
                role=self.profile,
                cause_by=WriteCode,
            )
        self.rc.env.publish_message(msg)
        return msg


import asyncio
import pandas as pd

file_path = "metagpt/code_debug/bugfixes_test.pickle"
df = pd.read_pickle(file_path)
sample_snippets = df[['before_merge', 'after_merge', 'full_traceback', 'bug type']].sample(3, random_state=45)


before_merge_snippets = sample_snippets['before_merge'].tolist()
# source_code_errs = sample_snippets['source code and errors'].tolist()
full_traceback = sample_snippets['full_traceback'].tolist()
bug_type = sample_snippets['bug type'].tolist()
after_merge_snippets = sample_snippets['after_merge'].tolist()
snippets = ""
snippets_arr = []
for i in range(0,len(after_merge_snippets)):
    snippets += f"-----------------------------------\n\n"
    snippets += f"Code for Review: {before_merge_snippets[i]}\n\n"
    snippets += f"Bug Type: {bug_type[i]}\n\n"
    snippets += f"Full Traceback: {full_traceback[i]}\n\n"
    snippets += f"End of Code for Review\n\n"
    snippets += f"-----------------------------------\n\n"
    snippets_arr.append(snippets)
    snippets = ""
# snippets = "\nsnippet: \n\n".join(before_merge_snippets)
idea = "for this code snippet and corresponding error, find the review the code and find corresponding bug in the code and provide a fix for each snippet. Here are the code snippets: \n\n" + snippets_arr[2]
print(idea)
import os
import sys

def save_text_to_file(name, text):
   
    base_dir = os.path.dirname(os.path.abspath(__file__))  # dir where script lives
    directory = os.path.join(base_dir, "tests_centralized")
    full_path = os.path.join(directory, name)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, 'w') as file:
        file.write(text)

    print(f"Text saved to {full_path}")

context = Context() # Load config2.yaml
env = Environment(context=context)
env.add_roles([Planner(), Coordinator(), EngineerA()]) # Add roles to the environment
env.publish_message(Message(content=idea, send_to=Coordinator, cause_by=UserRequirement)) # Send the user's message to Agent A to start the process.

async def main():
    if len(sys.argv) < 2:
        raise ValueError("Please provide the bugfix filename as a command line argument.")
    # filename = sys.argv[1]
    while not env.is_idle: # `env.is_idle` becomes True only when all agents have no new messages to process.
        await env.run()

asyncio.run(main())








