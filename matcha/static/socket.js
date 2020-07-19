window.onload=function() {

    let socket = io.connect('http://' + document.domain + ':5000');
    let socket_notifications = io('http://' + document.domain + ':5000/notification');

    socket.on('connect', function() {
        socket.emit('connect_user', {'username': username});
    })

    $('#wink-b').on('click', function() {
            socket_notifications.emit('notification', { 'recipient': recipient,
                                                            'sender': username,
                                                            'message': " winked at you!"});
        });

    socket_notifications.on('new_wink', function(msg){
        alert(msg)
    });

    $('#send_private_message').on('click', function() {
        let recipient = $('#send_to_username').val();
        let message = $('#private_message').val();

        socket_notifications.emit('private_message', {'recipient': recipient, 'message': message});
    });

    socket_notifications.on('new_private_message', function(msg){
        alert(msg)
    });

    socket_notifications.on('new_match', function(msg){
        alert(msg)
    });

};