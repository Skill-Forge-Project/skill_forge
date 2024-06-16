// Radio Buttons Script for Edit Reported Quest Form
function changeRadioButtonColors() {
    let inProgressRadioButton = document.getElementById('in_progress_option')
    let inProgressLabel = document.getElementById('in_progress_label')
    inProgressRadioButton.addEventListener('click', changeColorInProgressButtonEvent)

    let resolvedRadioButton = document.getElementById('resolved_option')
    let resolvedLabel = document.getElementById('resolved_label')
    resolvedRadioButton.addEventListener('click', changeColorResolvedButtonEvent)

    function changeColorInProgressButtonEvent(event) {
        inProgressLabel.style.color = '#03e9f4'
        resolvedLabel.style.color = ''
    }

    function changeColorResolvedButtonEvent(event) {
        resolvedLabel.style.color = '#03e9f4'
        inProgressLabel.style.color = ''
    }
}

changeRadioButtonColors()