// Redirect to tasks
function pythonTasks() {
    window.location.href = "{{ url_for('python_tasks') }}";
}

function jsTasks() {
    window.location.href = "{{ url_for('js_tasks') }}";
}

function javaTasks() {
    window.location.href = "{{ url_for('java_tasks') }}";
}

function csharpTasks() {
    window.location.href = "{{ url_for('c_sharp_tasks') }}";
}