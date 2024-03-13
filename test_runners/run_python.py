import subprocess
import re

def run_code(python_code, inputs, outputs):
    tests_count = len(inputs)
    successful_tests = 0
    unsuccessful_tests = 0

    for i in range(tests_count):
        current_input = ', '.join([str(element) for element in inputs[i]])  # THIS NEEDS TO BE CHANGED (MAYBE)
        correct_output = str(outputs[i][0])  # THIS NEEDS TO BE CHANGED !!

        function_name = re.findall(r"(?<=def ).*(?=\()", python_code)
        current_python_code = python_code + '\n\n' + f'print({function_name[0]}({current_input}))'

        # Use subprocess to run Python code
        process = subprocess.Popen(['python', '-c', current_python_code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        # Decode output from bytes to string
        stdout_str = stdout.decode('utf-8').replace('\n', '')
        stderr_str = stderr.decode('utf-8')

        if correct_output == stdout_str:
            successful_tests += 1
            # print('YES, IT IS CORRECT, CONGRATS!')
        else:
            unsuccessful_tests += 1
            # print('INCORRECT!')

    print(f'All tests: {tests_count}')
    print(f"You have {successful_tests} successful tests")
    print(f"You have {unsuccessful_tests} unsuccessful tests")
    return successful_tests, unsuccessful_tests


# Example Python code
# python_code = """
# print('Hello, world!')
# """

# # Execute Python code
# stdout, stderr = run_code(python_code)
# print("STDOUT:")
# print(stdout)
# print("STDERR:")
# print(stderr)