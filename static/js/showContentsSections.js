// JavaScript script to handle the show/hide of the contents sections in the Admin Panel


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