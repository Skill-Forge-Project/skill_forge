import subprocess

def run_code(js_code):
    # Use subprocess to run Node.js code
    process = subprocess.Popen(['node', '-e', js_code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    # Decode output from bytes to string
    stdout_str = stdout.decode('utf-8')
    stderr_str = stderr.decode('utf-8')
    print("STDOUT:")
    print(stdout_str)
    print("STDERR:")
    print(stderr_str)
    
    return stdout_str, stderr_str

js_code = """
console.log('Hello, world!');
"""

# Use for debuging porposes only
run_code(js_code)