// Redirect to Register page
function register() {
    window.location.href = "{{ url_for('register') }}";
}
function login(){
    window.location.href = "{{ url_for('login') }}";
}

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

function showContent(sectionId) {
    // Hide all content sections
    var contentSections = document.querySelectorAll('.content');
    contentSections.forEach(function(section) {
        section.style.display = 'none';
    });

    // Show the selected content section
    var selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.style.display = 'block';
    }
}