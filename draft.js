function submitGuess(word) {
    for (let i = 0; i < word.length; i++) {
        document.getElementById('kbd_' + word[i]).click()
    }
    
    document.getElementById('kbd_enter').click();
}

function checkResults() {
    feedback = {}
    for (key of keyboard.children) {
        if (key.getAttribute('class') != null) {
            feedback[key.innerText] = key.getAttribute('class');
        }
    }
    
    return feedback;
}

submitGuess('feliz');
checkResults();

