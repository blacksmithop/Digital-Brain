import os
import glob

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
KNOWLEDGE_DIR = "./knowledge"
GITHUB_DIR = "github"
GITHUB_DATA_DIR = os.path.join(KNOWLEDGE_DIR, GITHUB_DIR)

DEF_PREFIXES = ['def ', 'async def ']
NEWLINE = '\n'

def get_function_name(code):
    """
    Extract function name from a line beginning with 'def' or 'async def'.
    """
    for prefix in DEF_PREFIXES:
        if code.startswith(prefix):
            return code[len(prefix): code.index('(')]


def get_until_no_space(all_lines, i):
    """
    Get all lines until a line outside the function definition is found.
    """
    ret = [all_lines[i]]
    for j in range(i + 1, len(all_lines)):
        if len(all_lines[j]) == 0 or all_lines[j][0] in [' ', '\t', ')']:
            ret.append(all_lines[j])
        else:
            break
    return NEWLINE.join(ret)


def get_functions(filepath):
    """
    Get all functions in a Python file.
    """
    with open(filepath, 'r') as file:
        all_lines = file.read().replace('\r', NEWLINE).split(NEWLINE)
        for i, l in enumerate(all_lines):
            for prefix in DEF_PREFIXES:
                if l.startswith(prefix):
                    code = get_until_no_space(all_lines, i)
                    function_name = get_function_name(code)
                    yield {
                        'code': code,
                        'function_name': function_name,
                        'filepath': filepath,
                    }
                    break


def extract_functions_from_repo(code_directory: str = "./knowledge/github"):
    """
    Extract all .py functions from the repository.
    """
    python_files = glob.glob(os.path.join(code_directory, '**', '*.py'), recursive=True)
    num_files = len(python_files)
    print(f'Total number of .py files: {num_files}')

    if num_files == 0:
        print(f'Verify {code_directory} is set correctly.')
        return None

    all_funcs = []
    
    for code_file in python_files:
        try:
            for func in get_functions(str(code_file)):
                all_funcs.append(func)
        except Exception as e:
            print(e)

    num_funcs = len(all_funcs)
    print(f'Total number of functions extracted: {num_funcs}')

    return all_funcs

if __name__ == "__main__":
    # Extract all functions from the repository
    all_funcs = extract_functions_from_repo(GITHUB_DATA_DIR)