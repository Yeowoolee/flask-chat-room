document.addEventListener('DOMContentLoaded', () => {
    // 엔터키로 메시지 전송
    let msg = document.querySelector('#user_message');
    msg.addEventListener('keyup', event => {
        event.preventDefault();
        if (event.keyCode === 13) {
            document.querySelector('#send_message').click();
            
        }
        
    })
})
