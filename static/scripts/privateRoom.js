const toast_container = document.querySelector('.toast-container');
const display = document.querySelector('.display');
const username = document.getElementById('username').value;
const activeUsers = document.getElementById('activeUsers');
const roomname = document.getElementById('roomname').value;
const is_host = document.getElementById('createdOrJoin').value;
const form = document.getElementById('form');

let url = `wss://${window.location.host}/ws/privateRoomConsumer/${username}/${roomname}/False/`
if (is_host == 'True') {
    url = `wss://${window.location.host}/ws/privateRoomConsumer/${username}/${roomname}/True/`
}

const Socket = new WebSocket(url)
Socket.onmessage = (data) => {
    data = JSON.parse(data.data).data
    if (data['data-type'] == 'userDisconnected') {
        activeUsers.innerHTML = data.noOfUsers + ' user active';
        if (data.noOfUsers > 1) activeUsers.innerHTML = data.noOfUsers + ' users active';
    }
    if (data['data-type'] == 'userJoined') {
        let div = document.createElement('div');
        div.classList.add('toast-container');
        div.innerHTML = `
        <div class="toast-container mt-1">
            <div class="d-flex">
                <div class="toast-body">
                ${data.data}
                </div>
            <button type="button" class="btn-close me-2 m-auto" id="close"></button>
            </div>
        </div>
        `;
        activeUsers.innerHTML = data.noOfUsers + ' user active';
        if (data.noOfUsers > 1) activeUsers.innerHTML = data.noOfUsers + ' users active';
        toast_container.appendChild(div)
        setTimeout(() => toast_container.removeChild(div), 3000)
        console.log(data);
    }
    if (data['data-type'] == 'broadcasted_message') {
        console.log(data);
        let Mdata = JSON.parse(data.data)
        console.log(Mdata);
        let html = `
        <div class="toast" style="display: block;">
            <div class="toast-header">
                <strong class="me-auto">${data.sender}</strong>
            </div>
            <div class="toast-body">
                ${Mdata.message}
            </div>
        </div>
        `
        if (Mdata.is_host == 'True') {
            html = `
            <div class="toast" style="display: block;">
            <div class="toast-header">
            <strong class="me-auto">${data.sender}(Host)</strong>
            </div>
            <div class="toast-body">
            ${Mdata.message}
            </div>
            </div>
            `
        }
        display.innerHTML += html;
        console.log(display.scrollHeight);
        display.scrollTop = display.scrollHeight;
    }
}

form.addEventListener('submit', (e) => {
    e.preventDefault();
    let message = document.getElementById('textarea').value;
    Socket.send(JSON.stringify({
        'message': message,
        'is_host': is_host,
    }))
    document.getElementById('textarea').value = '';
});