def eval_code(code_str, test_list):
    try:
        exec_globals = {}
        exec(code_str, exec_globals)  # Compile/define the function
    except Exception as e:
        print("❌ Error during code compilation:", e)
        print("Offending code:\n", code_str)
        return False

    for test in test_list:
        try:
            exec(test, exec_globals)
        except AssertionError:
            print(f"❌ Test failed (assertion): {test}")
            return False
        except Exception as e:
            print(f"❌ Error during test execution: {test}\nError: {e}")
            return False

    return True  # All passed

def read_generated_code(file_path):
    with open(file_path, 'r') as f:
        code = f.read()
    return code
import re
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

tests = ["assert swap_List([1,2,3]) == [3,2,1]", "assert swap_List([1,2,3,4,4]) == [4,2,3,4,1]", "assert swap_List([4,5,6]) == [6,5,4]"]
function_definition = extract_func_definition(tests[0])
print("Function definition:", function_definition)
code = read_generated_code("metagpt\\code_generation_mbpp\\test_outputs_c\\case625.py")
passed = eval_code(code, tests)
print(f"Code passed all tests: {passed}")