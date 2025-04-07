$(document).ready(function() {
    $('#chat_form').on('submit', function(e) {
        e.preventDefault(); // Prevent page refresh

        var message = $('.write_msg').val(); // Get user's message
        if (message.trim() === "") return; // Skip empty messages

        // Add user's message to chat history (outgoing)
        var sentMsg = '<div class="outgoing_msg">' +
            '<div class="sent_msg">' +
            '<p>' + message + '</p>' +
            '<span class="time_date">11:01 AM | Today</span>' +
            '</div></div>';
        $('#msg_history').append(sentMsg);

        // Clear input field
        $('.write_msg').val('');

        // Send message to Flask /get endpoint
        $.ajax({
            url: '/get',
            type: 'POST',
            data: { msg: message },
            success: function(response) {
                // Add bot's response to chat history (incoming)
                var receivedMsg = '<div class="incoming_msg">' +
                    '<div class="incoming_msg_img">' +
                    '<img src="https://th.bing.com/th/id/OIP.zNm9xGPtKs65gWJSnOybvwHaLI?w=201&h=303&c=7&r=0&o=5&dpr=1.5&pid=1.7" alt="bot">' +
                    '</div><div class="received_msg">' +
                    '<div class="received_withd_msg">' +
                    '<p>' + response + '</p>' +
                    '<span class="time_date">11:01 AM | Today</span>' +
                    '</div></div></div>';
                $('#msg_history').append(receivedMsg);

                // Scroll to bottom
                $('#msg_history').scrollTop($('#msg_history')[0].scrollHeight);
            },
            error: function() {
                alert('Error sending message!');
            }
        });
    });
});