(function() {
    var req_data = {};
    var log_type = {
        'SIGN_IN': {'icon': 'fa-key', 'text': 'Signed in'},
        'SIGN_OUT': {'icon': 'fa-key', 'text': 'Signed out'},
        'SIGN_UP': {'icon': 'fa-key', 'text': 'Signed up'},
        'CREATE_TEXT': {'icon': 'fa-pencil-square', 'text': 'Create text'},
        'CREATE_NOTE': {'icon': 'fa-pencil-square', 'text': 'Create note'},
        'EDIT_TEXT': {'icon': 'fa-pencil-square-o', 'text': 'Edit text'},
        'EDIT_NOTE': {'icon': 'fa-pencil-square-o', 'text': 'Edit note'},
    }
    $.ajax({
        type: 'POST',
        contentType: 'application/json; charset=UTF-8',
        url: '/api/log_list',
        data: JSON.stringify(req_data),
        dataType: 'json',
        success: function(res_data) {
            if (res_data.code == 200) {
                var ele_list = [];
                for (var i = 0 ; i < res_data.data.length ; i++ ) {
                    console.log(1);
                    var item = res_data.data[i];
                    var $template_note = $($('#template_log').html().trim());
                    var $e1 = $template_note.find('.description');
                    var log_content = log_type[item['log_type']];
                    $e1.find('i').addClass(log_content['icon']);
                    $e1.find('.log_type').text(log_content['text']);
                    $e1.find('.target').text(item['target']).attr('href', '/note_edit?id=' + item['target']);
                    $template_note.find('.ip').text(item['userip']);
                    $template_note.find('.js-timeago').text(item['create_datetime']);
                    ele_list.push($template_note);
                }
                $('#log_list').append(ele_list);
            } else {
            }
        },
        error: function(err) {
            $('#res_status').text('Error.');
            $('#p_message').text(err.responseText);
        }
    });
})();
