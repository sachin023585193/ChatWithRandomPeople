// let textarea = document.getElementById('textarea');

textarea.addEventListener('keyup', (e) => {
    if (e.key == 'Enter') {
        sendBtn.click()
    }
});