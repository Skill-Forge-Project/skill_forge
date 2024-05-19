// Function to toggle between content sections in Admin Panel

function toggleContent(sectionId) {
    // Hide all content sections except the one clicked
    var contentSections = document.querySelectorAll('.content');
    contentSections.forEach(function (section) {
        if (section.id === sectionId + 'Content') {
            section.style.display = 'block';
        } else {
            section.style.display = 'none';
        }
    });
}