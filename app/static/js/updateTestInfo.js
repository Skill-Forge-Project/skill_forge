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
                $('#message').text(response.message);
                $('#submission_id_info').text(response.submission_id_info);
                $('#results').text(response.results);
                $('#zero-test-input').text('Given Input: ' + response.zero_test_input);
                $('#zero-test-output').text('Expected Output: ' + response.zero_test_output);
                $('#zero-test-stdout').text('Your Output: ' + response.zero_test_result);
                $('#zero-test-stderr').text('Code Errors: ' + '\n' + response.zero_test_error);

                // Dynamic color change based on the successful_tests vs quest_inputs
                if (response.passed === "True") {
                    // If all tests pass, set background to green
                    $('#results').css('color', '#0bf403bd');
                } else {
                    // If not all tests pass, set background to red
                    $('#results').css('color', '#f73333bd');
                }
            },
            error: function (error) {
                console.error(error);
            }
        });
    });
});