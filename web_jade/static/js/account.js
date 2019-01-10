(function(){

    $('#btn_delete_account').click(function(event){
        event.preventDefault();
        var $div_delete = $('#btn_delete_account').closest('div');
        $div_delete.addClass('hidden');
        $div_delete.nextAll().removeClass('hidden');
    });

    $('#btn_ensure_delete').click(function(event){
        event.preventDefault();
        var req_data = {
            'username': $('#username').val(),
            'password': $('#password').val(),
            'ts': (new Date).getTime(),
        }
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: '/api/user_delete',
            data: JSON.stringify(req_data),
            dataType: 'json',
            success: function(res_data) {
                if (res_data.code === 200) {
                    window.location = '/login';
                } else {
                    $('#password').val(null);
                    $('#danger_message').text(res_data.desc);
                }
            },
            error: function(err) {
                $('#password').val(null);
                $('#danger_message').text(err.responseText);
            }
        });
    });

})();
