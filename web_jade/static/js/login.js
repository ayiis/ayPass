(function() {
    $('#btn_submit').click(function(event) {
        event.preventDefault();
        var req_data = {
            'username': $('#username').val(),
            'password': $('#password').val(),
            'remember_me': $('#remember_me').val(),
            'ts': (new Date).getTime(),
        }
        if(req_data.username && req_data.password) {
            $.ajax({
                type: 'POST',
                contentType: 'application/json',
                url: '/api/user_login',
                data: JSON.stringify(req_data),
                dataType: 'json',
                success: function(res_data) {
                    if (res_data.code === 200) {
                        window.location = '/note_list' ;
                    } else {
                        $('#password').val(null);
                        $('#error_message').text(res_data.desc);
                    }
                },
                error: function(err) {
                    $('#password').val(null);
                    $('#error_message').text(err.responseText);
                }
            });
        } else {
            $('#error_message').text('Input an username and a password.');
        }
    });
    $('#sign_up').click(function(event) {
        event.preventDefault();
        var req_data = {
            'username': $('#username').val(),
            'password': $('#password').val(),
            'ts': (new Date).getTime(),
        }
        if(req_data.username && req_data.password) {
            $.ajax({
                type: 'POST',
                contentType: 'application/json',
                url: '/api/user_create',
                data: JSON.stringify(req_data),
                dataType: 'json',
                success: function(res_data) {
                    if (res_data.code === 200) {
                        $('#error_message').text('Success, redirecting to user center in 3 seconds...');
                        setTimeout(function() {
                            $('#btn_submit').click();
                        }, 3000);
                    } else {
                        $('#password').val(null);
                        $('#error_message').text(res_data.desc);
                    }
                },
                error: function(err) {
                    $('#password').val(null);
                    $('#error_message').text(err.responseText);
                }
            });
        } else {
            $('#error_message').text('Input an username and a password.');
        }
    });
})();
