$(document).ready(function () {
    $('#submitSolution').click(function () {
        // Get the current contents of the CodeMirror editor
        var userCode = editor.getValue();

        // Update the user_code input field with the current contents
        $('#editor').val(userCode);
        // Make an AJAX request to the Flask route
        $.ajax({
            url: '/submit-solution',
            type: 'POST',
            data: $('#submit_form').serialize(),
            success: function (response) {
                // Update the divs with the returned test results
                $('#successful_tests').text('Successful Tests: ' + response.successful_tests);
                $('#unsuccessful_tests').text('Unsuccessful Tests: ' + response.unsuccessful_tests);
                $('#message').text(response.message);
                $('#zero-test-input').text('Given Input: ' + response.zero_test_input);
                $('#zero-test-output').text('Expected Output: ' + response.zero_test_output);
                $('#zero-test-stdout').text('Your Output: ' + response.zero_test_result);
                $('#zero-test-stderr').text('Code Errors: ' + '\n' + response.zero_test_error);
            },
            error: function (error) {
                console.error(error);
            }
        });
    });
});