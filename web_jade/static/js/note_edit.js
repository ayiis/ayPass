(function() {
    var id = new URLSearchParams(window.location.search).get('id');
    if (!id) return;
    var req_data = {
        'id': id,
    }
    $.ajax({
        type: 'POST',
        contentType: 'application/json; charset=UTF-8',
        url: '/api/note_query',
        data: JSON.stringify(req_data),
        dataType: 'json',
        success: function(res_data) {
            if (res_data.code == 200) {
                console.log(res_data);
                var note_detail = res_data.data
                $('#i_title').val(note_detail.title);
                $('#ta_content').val(note_detail.content);
                $('#ta_content').width(note_detail.width);
                $('#ta_content').height(note_detail.height);
            } else {
                $('#res_status').text('Error.');
                $('#p_message').text(res_data.desc);
            }
        },
        error: function(err) {
            $('#res_status').text('Error.');
            $('#p_message').text(err.responseText);
        }
    });

    // 防止误编辑
    $('#btn_lock_switch').click(function() {
        var $btn_lock_switch = $(this);
        if($btn_lock_switch.attr('locked') == '0') {
            // 解锁
            $btn_lock_switch.attr('locked', '1');
            $btn_lock_switch.contents().filter(function() {
                return this.nodeType === 3;
            }).remove();
            $btn_lock_switch.append('Locked');
            $('#btn_save,#ta_content,#i_title').attr('disabled', true);
            $btn_lock_switch.find('i').removeClass('fa-unlock').addClass('fa-lock');
        } else {
            // 加锁
            $btn_lock_switch.attr('locked', '0');
            $btn_lock_switch.contents().filter(function() {
                return this.nodeType === 3;
            }).remove();
            $btn_lock_switch.append('Unlocked');
            $('#btn_save,#ta_content,#i_title').attr('disabled', null);
            $btn_lock_switch.find('i').removeClass('fa-lock').addClass('fa-unlock');
        }
    });

    $('#btn_save').click(function(event) {
        var req_data = {
            'id': id,
            'title': $('#i_title').val(),
            'content': $('#ta_content').val(),
            'width': $('#ta_content').width(),
            'height': $('#ta_content').height(),
            'ts': (new Date).getTime(),
        }
        event.preventDefault();
        $.ajax({
            type: 'POST',
            contentType: 'application/json; charset=UTF-8',
            url: '/api/note_edit',
            data: JSON.stringify(req_data),
            dataType: 'json',
            success: function(res_data) {
                if (res_data.code == 200) {
                    $('#res_status').text('Success.');
                    $('#p_message').text(res_data.data);
                } else {
                    $('#res_status').text('Failed.');
                    $('#p_message').text(res_data.desc);
                }
            },
            error: function(err) {
                $('#res_status').text('Error.');
                $('#p_message').text(err.responseText);
            }
        });
    });
})();
