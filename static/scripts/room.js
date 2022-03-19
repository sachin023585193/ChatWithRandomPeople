const username = document.getElementById('username').value;
const url = `ws://${window.location.host}/ws/consumer/${username}/`;
let Socket = new WebSocket(url);
const form = document.querySelector('#form');
const display = document.querySelector('.display');
const nextBtn = document.getElementById('next');
const sendBtn = document.getElementById('send');
const textarea = document.getElementById('textarea');
let Connected = false;

form.addEventListener('submit', (e) => {
    e.preventDefault()
    value = document.querySelector('#textarea').value;
    Socket.send(JSON.stringify({
        'message': value
    }))
    document.querySelector('#textarea').value = "";
})

Socket.onmessage = (data) => {
    data = JSON.parse(data.data)
    console.log(data);
    if (data['data-type'] == 'broadcasted_message') {
        display.innerHTML += `
        <div class="toast" style="display: block;">
            <div class="toast-header">
                <strong class="me-auto">${data.sender}</strong>
            </div>
            <div class="toast-body">
                ${data.data.message}
            </div>
        </div>
        `
        display.scrollTop = display.scrollHeight;
    }
    if (data['data-type'] === 'waitingForUser') {
        document.querySelector('.info').classList.remove('display-none')
    }
    if (data['data-type'] === 'connectedToUser' && Connected == false) {
        Connected = true;
        document.querySelector('.info').innerHTML = `<div class='ml-1'>Connected to ${data.sender}</div>`
    }
    if (data['data-type'] === 'userDisconnected') {
        document.querySelector('.info').innerHTML = `<div class='text-danger px-1'>!!!${data.data}</div>`
        document.querySelector('.block').classList.remove('block');
        nextBtn.classList.add('block');
    }
}
nextBtn.addEventListener('click', () => {
    Socket.close();
    window.location.reload();
});