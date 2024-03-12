import subprocess
import os

def run_code(csharp_code):
    # Save the C# code to a file
    with open("Program.cs", "w") as file:
        file.write(csharp_code)

    # Compile the C# code
    compile_process = subprocess.Popen(['mono-csc', 'Program.cs'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    compile_stdout, compile_stderr = compile_process.communicate()

    # Execute the compiled C# program
    if compile_process.returncode == 0:
        execution_process = subprocess.Popen(['mono', 'Program.exe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        execution_stdout, execution_stderr = execution_process.communicate()
        stdout_str = execution_stdout.decode('utf-8')
        stderr_str = execution_stderr.decode('utf-8')
    else:
        stdout_str = ""
        stderr_str = compile_stderr.decode('utf-8')

    # Delete the C# file
    os.remove("Program.cs")
    os.remove("Program.exe")
    return stdout_str, stderr_str

# Example C# code
csharp_code = """
using System;
class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Hello World!");
    }
}
"""

# Use for debuging porposes only
# Execute C# code
stdout, stderr = run_code(csharp_code)
print("STDOUT:")
print(stdout)
print("STDERR:")
print(stderr)