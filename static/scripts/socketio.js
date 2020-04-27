document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://127.0.0.1:5000');

    let room = 'Lobby';
    joinRoom('Lobby');

    socket.on('message', data => {
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const span_timestamp = document.createElement('span');
        const br = document.createElement('br');
        const div = document.createElement('div')
        div.setAttribute("class", "row");
        if (data.username){
            if (data.username === username){
                // 이름이 같을 경우
                
                p.setAttribute("class", "card col-md-5 ml-auto");
                span_username.innerHTML = data.username;
                span_timestamp.innerHTML = data.time_stamp
                p.innerHTML = span_username.outerHTML + br.outerHTML
                                             + data.msg + br.outerHTML + span_timestamp.outerHTML;
                div.innerHTML = p.outerHTML                       
                document.querySelector("#display-message-section").append(div);

            } else{
                p.setAttribute("class", "card col-md-5");
                span_username.innerHTML = data.username;
                span_timestamp.innerHTML = data.time_stamp
                p.innerHTML = span_username.outerHTML + br.outerHTML
                                             + data.msg + br.outerHTML + span_timestamp.outerHTML;
                document.querySelector("#display-message-section").append(p);
            }
        }else{
            printSyMsg(data.msg);
        }
    });

    // 메시지 보내기
    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg': document.querySelector("#user_message").value,
         'username': username, 'room': room});
         // input 내용 지우기
        document.querySelector('#user_message').value = '';
        //스크롤바 내리기
        document.querySelector("#display-message-section").scrollTop = document.querySelector("#display-message-section").scrollHeight;
        
    
    }

    // 채팅 방 변경
    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            if (newRoom == room) {
                msg = `이미 ${room}에 있습니다.`
                printSyMsg(msg);
            }else{
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        }
    });

    function leaveRoom(room){
        socket.emit('leave', {'username' : username, 'room' : room});
    }

    function joinRoom(room){
        socket.emit('join', {'username' : username, 'room' : room});
        //메시지 출력 창 지우기
        document.querySelector('#display-message-section').innerHTML = ''
    }

    // 시스템 메시지 출력
    function printSyMsg(msg){
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
    }

})