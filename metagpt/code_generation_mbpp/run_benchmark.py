import json
import os
import time
import subprocess
from pathlib import Path
import pandas as pd
import random
import re
from save_text import save_text_to_file
import math
import itertools
import collections
import sympy
import numpy
import bitarray
import pandas


MBPP_FILE = "metagpt\code_generation_mbpp\sanitized-mbpp.json"
NUM_SAMPLES = 10
METAGPT_SCRIPTS = ['metagpt\\code_generation_mbpp\\centralized.py', 'metagpt\\code_generation_mbpp\\hierarchal.py']

def load_tasks(file_path, num_samples=NUM_SAMPLES):
    with open(file_path, 'r') as f:
        tasks = json.load(f)
    random.seed(42)  # For reproducibility
    return random.sample(tasks, NUM_SAMPLES)

def run_meta_gpt(script, task, task_id, tests):

    save_path = "case" + str(task_id) + ".py"
    command = ["python", script, save_path, task]
    start_time = time.time()
    print(f"Running command: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    costs_path ="metagpt\\code_generation_mbpp\\costs\\cost.txt"
    tokens = parse_total_tokens(costs_path)
    
    
    end_time = time.time()
    return result.stdout, end_time - start_time, tokens


def eval_code(code_str, test_list, task_id = "", scriptname = ""):
    try:
        exec_globals = {
            "math": math,
            "re": re,
            "itertools": itertools,
            "collections": collections,
            "sympy" : sympy,
            "numpy": numpy,
            "bitarray": bitarray,
            "pandas": pandas,
            # Add any standard libraries you expect to show up
        }
        exec(code_str, exec_globals)  # Compile/define the function
    except Exception as e:
        print("\nError during code compilation: of task ", task_id, " in script ", scriptname)
        print(f"Error: {e}")
        print("Offending code:\n", code_str)
        return False

    for test in test_list:
        try:
            exec(test, exec_globals)
        except AssertionError:
            print(f"Test failed (assertion) for task {task_id} in script {scriptname}: {test}")
            return False
        except Exception as e:
            print(f"\nError during test execution for task {task_id} in script {scriptname}: {test}")
            print(f"Error: {e}\n")
            return False

    return True  # All passed

def read_generated_code(file_path):
    with open(file_path, 'r') as f:
        code = f.read()
    return code

def count_code_lines(code_str):
    lines = code_str.splitlines()
    return sum(1 for line in lines if line.strip() and not line.strip().startswith("#"))

def extract_code_from_stdout(stdout_text):
    match = re.search(r"```python(.*?)```", stdout_text, re.DOTALL)
    if match:
        code = match.group(1).strip()
        return code
    else:
        print("No code block found!")
        return ""

def extract_func_definition(test):
    match = re.search(r"assert\s+(\w+)\((.*?)\)", test)
    if match:
            func_name = match.group(1)
            args = match.group(2)

            # Estimate number of arguments from commas
            arg_count = args.count(",") + 1 if args.strip() else 0
            arg_names = [f"arg{i}" for i in range(arg_count)]

            return f"def {func_name}({', '.join(arg_names)}):"
    return None

def parse_total_tokens(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    match = re.search(r"Total tokens:\s*(\d+)", content)
    if match:
        return int(match.group(1))
    else:
        raise ValueError("Total tokens not found in file.")


def main():
    try:
        tasks = load_tasks(MBPP_FILE, NUM_SAMPLES)
        results = []
        
        stats = {}
        for script in METAGPT_SCRIPTS:
            stats[script] = {
                'script': script,
                'average_duration': 0,
                'average_tokens': 0,
                'average_lines_of_code': 0,
                'average_productivity': 0,
                'total_passed': 0,
                'total_failed': 0,
                'pass_rate': 0,
                'task_ids': [],
                'passed_tasks': [],
                'failed_tasks': [],
            }
      
        for task in tasks:
            task_id = task['task_id']
            prompt = task['prompt']
            test_list = task['test_list']
            func_def = extract_func_definition(test_list[0])
            if func_def != None:
                full_prompt = f"Write a standalone Python function that follows this function signature{func_def}, **NOT inside a class**, that satisfies the following prompt:\n\n{prompt}\n\n"
            else:
                full_prompt = f"Write a standalone Python function that follows this function signature, **NOT inside a class**, that satisfies the following prompt:\n\n{prompt}\n\n"
            print(f"Running task {task_id}: {full_prompt}")
            name = ""
            for script in METAGPT_SCRIPTS:
                code_file = ""
                if "centralized" in script:
                    code_file = "metagpt\\code_generation_mbpp\\test_outputs_c"
                    name = "Centralized"
                elif "hierarchal" in script:
                    code_file = "metagpt\\code_generation_mbpp\\test_outputs_h"
                    name = "Hierarchical"
                code_file = os.path.join(code_file, "case" + str(task_id) + ".py")

                stdout, duration, tokens = run_meta_gpt(script, full_prompt, task_id, test_list)
                
                if(os.path.exists(code_file)):
                    code = read_generated_code(code_file)
                else:
                    code = extract_code_from_stdout(stdout)
                    save_text_to_file(code_file, code, True)
                    print(f"Generated code:\n{code}")
                lines_of_code = count_code_lines(code)
                passed = eval_code(code, test_list, task_id, script)
                productivity = tokens/lines_of_code
                results.append({
                    'task_id': task_id,
                    'script': name,
                    'duration': duration,
                    'tokens': tokens,
                    'lines_of_code': lines_of_code,
                    'passed': passed,
                    'productivity': productivity,

                })
                stats[script]['average_duration'] += duration
                stats[script]['average_tokens'] += tokens
                stats[script]['average_lines_of_code'] += lines_of_code
                stats[script]['average_productivity'] += productivity
                stats[script]['task_ids'].append(task_id)
                if passed:
                    stats[script]['total_passed'] += 1
                    stats[script]['passed_tasks'].append(task_id)
                else:
                    stats[script]['total_failed'] += 1  
                    stats[script]['failed_tasks'].append(task_id)
        
        print(results)
        for script in METAGPT_SCRIPTS:
            stats[script]['average_duration'] /= NUM_SAMPLES
            stats[script]['average_tokens'] /= NUM_SAMPLES
            stats[script]['average_lines_of_code'] /= NUM_SAMPLES
            stats[script]['average_productivity'] /= NUM_SAMPLES
            stats[script]['pass_rate'] = stats[script]['total_passed'] / (stats[script]['total_passed'] + stats[script]['total_failed']) * 100

        df = pd.DataFrame(stats).T

        df.to_csv('benchmark_results.csv', index=False)
        print("Results saved to benchmark_results.csv")
    except Exception as e:
        df = pd.DataFrame(stats).T
        df.to_csv('benchmark_results.csv', index=False)
        print("Results saved to benchmark_results.csv")
        print("An error occurred:", e)
       
        

        

main()