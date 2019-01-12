(function(){
    $('#btn_save').click(function(event) {
        var req_data = {
            'old_password': $('#old_password').val(),
            'new_username': $('#new_username').val(),
            'new_password': $('#new_password').val(),
            'new_password_confirm': $('#new_password_confirm').val(),
            'ts': (new Date).getTime(),
        }
        if (req_data['new_password'] !== req_data['new_password_confirm']) return $('#span_message').text("Please check your input") && false;
        if ( !(req_data['old_password'] && req_data['new_username'] && req_data['new_password']) ) return $('#span_message').text("Please check your input") && false;
        event.preventDefault();
        $.ajax({
            type: 'POST',
            contentType: 'application/json; charset=UTF-8',
            url: '/api/user_change',
            data: JSON.stringify(req_data),
            dataType: 'json',
            success: function(res_data) {
                if (res_data.code === 200 && res_data.data === true) {
                    $('#span_message').text('Success, redirecting to login in 3 seconds...');
                    setTimeout(function() {
                        window.location = '/login';
                    }, 3000);
                } else {
                    $('#span_message').text(res_data.desc);
                }
            },
            error: function(err) {
                $('#span_message').text(err.responseText);
            }
        });
    });
})();
