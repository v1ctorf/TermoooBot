function submitGuess(word) {
    for (let i = 0; i < word.length; i++) {
        document.getElementById('kbd_' + word[i]).click()
    }
    
    document.getElementById('kbd_enter').click();
}

function checkResults() {
    feedback = {}
    let keyboard = document.getElementById('kbd');

    for (key of keyboard.children){
        console.log(key.innerText);    
    }
}

submitGuess('feliz');
checkResults();

