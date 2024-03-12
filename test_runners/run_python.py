import subprocess

def run_code(python_code):
    # Use subprocess to run Python code
    process = subprocess.Popen(['python', '-c', python_code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    # Decode output from bytes to string
    stdout_str = stdout.decode('utf-8')
    stderr_str = stderr.decode('utf-8')
    return stdout_str, stderr_str

# Example Python code
python_code = """
print('Hello, world!')
"""

# Execute Python code
# stdout, stderr = run_code(python_code)
# print("STDOUT:")
# print(stdout)
# print("STDERR:")
# print(stderr)