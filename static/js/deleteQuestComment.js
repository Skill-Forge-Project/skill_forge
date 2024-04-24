// That script handles deleting quests from the quest/quest_id page as Admin

// Add event listener to handle delete comment button click
document.querySelectorAll('.delete-comment').forEach(button => {
    button.addEventListener('click', function() {
        const commentIndex = this.getAttribute('data-comment-id');
        deleteComment(commentIndex);
    });
});

// Function to send AJAX request to delete comment
function deleteComment(commentIndex) {
    const questId = "{{ quest.quest_id }}"; // Replace with actual quest ID
    const formData = new FormData();
    formData.append('quest_id', questId);
    formData.append('comment_index', commentIndex);

    fetch('/delete_comment', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            // Reload the page or update the comments section as needed
            window.location.reload(); // Example: Reload the page
        } else {
            console.error('Failed to delete comment');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}