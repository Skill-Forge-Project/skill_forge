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
    }

    // Function to start the timer with dynamic countdown
    function startTimer(elapsedTime) {
        var remainingTime = thirtySeconds - elapsedTime;
        updateButtonText(Math.ceil(remainingTime / 1000));

        // Use setInterval to update the button text every second
        var interval = setInterval(function() {
            remainingTime -= 1000;
            if (remainingTime <= 0) {
                clearInterval(interval);
                enableButton(); // Re-enable the button when the time is up
            } else {
                updateButtonText(Math.ceil(remainingTime / 1000));
            }
        }, 1000);
    }

    // Function to update button text with the remaining seconds
    function updateButtonText(seconds) {
        button.textContent = `Wait for ${seconds} second${seconds > 1 ? 's' : ''}`;
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
