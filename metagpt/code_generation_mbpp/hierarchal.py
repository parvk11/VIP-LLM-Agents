import asyncio
from metagpt.roles import (
    Architect,
    Engineer,
    ProductManager,
    ProjectManager,
    QaEngineer,

)
from metagpt.team import Team
import os
from metagpt.actions import WriteCode
import pandas as pd
from metagpt.logs import logger
from metagpt.utils.common import CodeParser
import sys
from metagpt.utils.common import any_to_name

idea = sys.argv[2]

def save_text_to_file(name, text):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # dir where script lives
    directory = os.path.join(base_dir, "test_outputs_h")
    full_path = os.path.join(directory, name)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, 'w') as file:
        file.write(text)

    print(f"Text saved to {full_path}")

class CustomEngineer(Engineer):
    name: str = "Peter"
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.set_actions([WriteCustomCode])
        self.next_todo_action = any_to_name(WriteCustomCode)

class WriteCustomCode(WriteCode):
    
    async def write_code(self, prompt) -> str:
        logger.info("Prompt: " + prompt)
        code_rsp = await self._aask(prompt)
        code = CodeParser.parse_code(block="", text=code_rsp)
        save_text_to_file(sys.argv[1], code)
        return code
async def startup(idea: str):
    company = Team()
    company.hire(
        [
            ProductManager(),
            ProjectManager(),
            Architect(),
            CustomEngineer(),
            QaEngineer(),
        ]
    )
    company.invest(investment=3.0)
    company.run_project(idea=idea)

    await company.run(n_round=5)

import time
async def main():
    start_time = time.time()
    await startup(idea= idea )
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")
asyncio.run(main())