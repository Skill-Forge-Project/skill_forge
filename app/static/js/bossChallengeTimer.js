var h3 = document.getElementsByTagName("h3");
var challengeId = document.getElementById("challenge_id").value;

var sec         = 15,
    countDiv    = document.getElementById("timer"),
    secpass,
    countDown   = setInterval(function () {
        'use strict';
        secpass();
    }, 1000);

function secpass() {
    'use strict';
    var min     = Math.floor(sec / 60),
        remSec  = sec % 60;
    if (remSec < 10) {
        remSec = '0' + remSec;
    }
    if (min < 10) {
        min = '0' + min;
    }
    countDiv.innerHTML = min + ":" + remSec;
    if (sec > 0) {
        sec = sec - 1;
    } else {
        clearInterval(countDown);
        countDiv.innerHTML = 'Your time is over!';
        // Redirect to the underworld page after the timer ends and update the challenge status to Failed
        window.location.href = '/challenge_timer_over?challenge_id=' + challengeId;
    }
}

