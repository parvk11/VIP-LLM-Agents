import joblib
import pandas as pd
# model = joblib.load('buggy_dataset/bugfixes_test.pkl')

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
idea = "for this code snippet and corresponding error, find the review the code and find corresponding bug in the code and provide a fix for each snippet. Here are the code snippets: \n\n" + snippets_arr[1]
print(idea)