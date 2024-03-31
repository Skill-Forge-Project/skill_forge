import subprocess
import os

def run_code(java_code, inputs, outputs, user_id, username, quest_id):
    tests_count = len(inputs)
    successful_tests = 0
    unsuccessful_tests = 0
    
    # Generate a unique dir and file name for the Java code
    directory = f"{username}_{user_id}_{quest_id}"
    os.makedirs(os.path.join("test_runners/java-files", directory), exist_ok=True)
    os.chdir(os.path.join("test_runners/java-files", directory))
    print(os.getcwd())
    for i in range(tests_count):
        file_path = os.path.join(os.getcwd(), "Main.java")
        class_path = os.path.join(os.getcwd(), "Main.class")
        
        # Save the Java code to a file
        try:
            with open(file_path, "w") as java_file:
                java_file.write(java_code)
        except Exception as e:
            print("Error:", e)
            return 0, tests_count, "Error occurred while saving Java code to file."

        # Compile the Java code
        try:
            compile_process = subprocess.Popen(['javac', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            compile_output, compile_error = compile_process.communicate()
            if compile_error:
                print("Compilation Error:", compile_error.decode('utf-8'))
                return 0, tests_count, f"Compilation Error: {compile_error.decode('utf-8')}"
        except Exception as e:
            print("Error:", e)
            return 0, tests_count, "Error occurred during Java code compilation."

        # Execute the Java code
        try:
            current_input = ' '.join([str(element) for element in inputs[i]]) 
            print(current_input)
            execute_command = ['java', 'Main'] + current_input.split()
            execute_process = subprocess.Popen(execute_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            execute_output, execute_error = execute_process.communicate()
            if execute_error:
                print("Execution Error:", execute_error.decode('utf-8'))
                return 0, tests_count, f"Execution Error: {execute_error.decode('utf-8')}"
            else:
                # Check if output matches expected output
                if execute_output.decode('utf-8').strip() == outputs[i][0]:
                    successful_tests += 1
                else:
                    unsuccessful_tests += 1
        except Exception as e:
            print("Error:", e)
            return 0, tests_count, "Error occurred during Java code execution."
                    
    # Determine message based on test results
    if unsuccessful_tests == 0:
        message = 'Congratulations! Your solution is correct!'
    elif successful_tests > 0 and unsuccessful_tests > 0:
        message = 'Your solution is partially correct! Try again!'
    elif successful_tests == 0 and unsuccessful_tests > 0:
        message = 'Your solution is incorrect! Try again!'

    return successful_tests, unsuccessful_tests, message



# Example Java code
# java_code = """
# public class Main {
#     public static void main(String[] args) {
#         System.out.println("Hello, world!");
#     }
# }
# """


# Use for debuging porposes only
# Execute Java code
# stdout, stderr = run_code(java_code)
# print("STDOUT:")
# print(stdout)
# print("STDERR:")
# print(stderr)