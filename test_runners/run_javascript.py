import subprocess
import re

def run_code(js_code, inputs, outputs):
    tests_count = len(inputs)
    successful_tests = 0
    unsuccessful_tests = 0
    zero_tests = [] # Hold the first example test input and putput
    zero_tests_outputs = [] # Hold the first example after executing the user code (stdout & stderr)
    
    
    for i in range(tests_count):
        current_input = [f'"{element}"' if isinstance(element, str) else str(element) for element in inputs[i]]
        current_input = ', '.join(current_input)
        correct_output = str(outputs[i][0])
        
        function_name = re.findall(r"(?<=function ).*(?=\()", js_code)
        if current_input.isalpha():
            current_js_code = js_code + '\n\n' + f'console.log({function_name[0]}("{current_input}"))'
        else:
            current_js_code = js_code + '\n\n' + f'console.log({function_name[0]}({current_input}))'
        
        # Use subprocess to run JS code
        process = subprocess.Popen(['node', '-e', current_js_code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        # Decode output from bytes to string
        stdout_str = stdout.decode('utf-8').replace('\n', '').replace('undefined', '') # handle undefined output as well
        stderr_str = stderr.decode('utf-8')
        
        # Handle the zero test case
        if i == 0:
            zero_tests.append(current_input)
            zero_tests.append(correct_output)
            zero_tests_outputs.append(stdout_str)
            zero_tests_outputs.append(stderr_str)
        
        if correct_output == stdout_str:
            successful_tests += 1
        else:
            unsuccessful_tests += 1
        
        if unsuccessful_tests == 0:
            message = 'Congratulations! Your solution is correct!'
        elif successful_tests > 0 and unsuccessful_tests > 0:
            message = 'Your solution is partially correct! Try again!'
        elif successful_tests == 0 and unsuccessful_tests > 0:
            message = 'Your solution is incorrect! Try again!'
    return successful_tests, unsuccessful_tests, message, zero_tests, zero_tests_outputs



# js_code = """
# console.log('Hello, world!');
# """

# Use for debuging porposes only
# run_code(js_code)