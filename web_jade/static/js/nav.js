
(function(){

    $('#sidebar-top-level-items').find('li').filter(function(){
        return $(this).find('>a[href="' + location.pathname + '"]').length > 0;
    }).addClass('active');

    $('#signout').click(function(event){
        event.preventDefault();
        var req_data = {}
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: '/api/user_logout',
            data: JSON.stringify(req_data),
            dataType: 'json',
            success: function(res_data) {
                if (res_data.code === 200) {
                    window.location = '/login';
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
    });

})();
