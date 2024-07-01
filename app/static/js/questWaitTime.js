document.addEventListener('DOMContentLoaded', function() {
    var button = document.getElementById('submitSolution');
    var disabledTimestamp = localStorage.getItem('buttonDisabledTimestamp');
    var currentTime = new Date().getTime();
    var thirtySeconds = 30000; // 30 seconds in milliseconds

    // Check if the button should still be disabled based on the stored timestamp
    if (disabledTimestamp && currentTime - disabledTimestamp < thirtySeconds) {
        // Button should still be disabled
        disableButton();
        startTimer(currentTime - disabledTimestamp);
    }

    // Add event listener to handle button click
    button.addEventListener('click', function() {
        // Disable the button
        disableButton();
        startTimer(0);

        // Store the current timestamp in localStorage
        localStorage.setItem('buttonDisabledTimestamp', new Date().getTime());
    });

    // Function to disable the button
    function disableButton() {
        button.disabled = true;
        button.classList.remove('submit-button');
        button.classList.add('inactive-button');
        button.textContent = 'Please wait for 30 seconds.';
    }

    // Function to start the timer
    function startTimer(elapsedTime) {
        var remainingTime = thirtySeconds - elapsedTime;

        // Set a timeout to restore the button's previous state after the remaining time
        setTimeout(function() {
            // Enable the button
            enableButton();
        }, remainingTime);
    }

    // Function to enable the button
    function enableButton() {
        button.disabled = false;
        button.textContent = 'Submit Quest';
        button.classList.remove('inactive-button');
        button.classList.add('submit-button');

        // Remove the stored timestamp from localStorage
        localStorage.removeItem('buttonDisabledTimestamp');
    }
});