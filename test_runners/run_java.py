import subprocess
import os

def run_code(java_code):
    # Save the Java code to a file
    with open(f"Main.java", "w") as file:
        file.write(java_code)

    # Compile the Java code
    compile_process = subprocess.Popen(['javac', 'Main.java'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    compile_stdout, compile_stderr = compile_process.communicate()

    # Execute the compiled Java program
    if compile_process.returncode == 0:
        execution_process = subprocess.Popen(['java', 'Main'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        execution_stdout, execution_stderr = execution_process.communicate()
        stdout_str = execution_stdout.decode('utf-8')
        stderr_str = execution_stderr.decode('utf-8')
    else:
        stdout_str = ""
        stderr_str = compile_stderr.decode('utf-8')
    
    # Delete the Java file
    os.remove("Main.java")
    os.remove("Main.class")
    return stdout_str, stderr_str

# Example Java code
java_code = """
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, world!");
    }
}
"""


# Use for debuging porposes only
# Execute Java code
# stdout, stderr = run_code(java_code)
# print("STDOUT:")
# print(stdout)
# print("STDERR:")
# print(stderr)