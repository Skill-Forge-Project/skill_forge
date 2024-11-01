function reportReasonHandle() {
    const firstReportButton = document.getElementById('reportQuestWithTextarea');
    const secondReportButton = document.getElementById('reportQuest');
    const reportReasonTextarea = document.getElementById('report-reason');
    const reportUrl = document.getElementById('report-url').dataset.url; // Get the base report URL

    firstReportButton.addEventListener('click', function() {
        reportReasonTextarea.style.display = 'block'; // Show the textarea
        firstReportButton.style.display = 'none'; // Hide the first button
        secondReportButton.style.display = 'block'; // Show the submit report button
        reportReasonTextarea.focus(); // Focus the textarea
    });

    secondReportButton.addEventListener('click', function() {
        const reportReason = reportReasonTextarea.value.trim();

        // Validate the input
        if (reportReason.length < 20) {
            alert('Please provide a report reason with at least 20 characters length.');
        } else {
            // Redirect with the report reason
            location.href = reportUrl + encodeURIComponent(reportReason);
        }
    });
}

// Call the function after the DOM is fully loaded
document.addEventListener('DOMContentLoaded', reportReasonHandle);