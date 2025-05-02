import asyncio
from metagpt.roles import (
    Architect,
    Engineer,
    ProductManager,
    ProjectManager,
    QaEngineer,

)
from metagpt.team import Team

import pandas as pd
file_path = "metagpt/code_debug/bugfixes_test.pickle"
df = pd.read_pickle(file_path)
sample_snippets = df[['before_merge', 'after_merge']].sample(10, random_state=42)
before_merge_snippets = sample_snippets['before_merge'].tolist()
after_merge_snippets = sample_snippets['after_merge'].tolist()




async def startup(idea: str):
    company = Team()
    company.hire(
        [
            ProductManager(),
            ProjectManager(),
            Architect(),
            Engineer(),
            QaEngineer(),
        ]
    )
    company.invest(investment=3.0)
    company.run_project(idea=idea)

    await company.run(n_round=5)

snippets = "\nsnippet: \n\n".join(before_merge_snippets)

idea = "for each code snippet, find the corresponding bug in the code and provide a fix for each snippet. Here are the code snippets: \n\n" + snippets
print(idea)

async def main():
    await startup(idea= idea )
asyncio.run(main())