import requests

def execute_js_and_test(code, tests):
    url = 'http://192.168.0.169:3000/execute'
    data = {'code': code}
    response = requests.post(url, json=data)
    return response.json()['result']
    # return response.json()

# Example usage
code = 'function add() { console.log("A"); }'
tests = 'describe("Addition tests", () => { test("1 + 1 equals 2", () => { expect(add(1, 1)).toBe(2); }); })'
results = execute_js_and_test(code, tests)
print(results)
