(function() {

    function do_search() {
        var req_data = {
            'title': $('#title').val() || '',
            'sort_type': Number($('#sort_type').attr('val') || ''),
        };
        $.ajax({
            type: 'POST',
            contentType: 'application/json; charset=UTF-8',
            url: '/api/note_list',
            data: JSON.stringify(req_data),
            dataType: 'json',
            success: function(res_data) {
                if (res_data.code == 200) {
                    var ele_list = [];
                    for (var i = 0 ; i < res_data.data.length ; i++ ) {
                        var item = res_data.data[i];
                        var $template_note = $($('#template_note').html().trim());
                        var $e1 = $template_note.find('.avatar-container .project');
                        $e1.attr('href', '/note_edit?id=' + item['_id']);
                        $e1.find('div').text(item['title'][0]);
                        var $e2 = $template_note.find('.project-details .project');
                        $e2.attr('href', '/note_edit?id=' + item['_id']);
                        $e2.find('.project-name').text(item['title']);
                        var $e3 = $template_note.find('.controls');
                        $e3.find('.js-timeago').text( 'U' + item['update_datetime'] + ' / ' + 'C' + item['create_datetime']);
                        ele_list.push($template_note);
                    }
                    $('#projects_list').empty().append(ele_list);
                } else {

                }
            },
            error: function(err) {
                $('#res_status').text('Error.');
                $('#p_message').text(err.responseText);
            }
        });
    }
    do_search();
    $('#btn_search').click(function(event){
        event.preventDefault();
        do_search();
    });

    $('#sort-projects-dropdown').click(function(){
        if($(this).attr('aria-expanded') == 'false') {
            $(this).attr('aria-expanded', 'true');
            $(this).closest('div').addClass('open');
        } else {
            $(this).attr('aria-expanded', 'false');
            $(this).closest('div').removeClass('open');
        }
    });

    $('.dropdown-menu').on('click', 'a', function(event){
        event.preventDefault();
        $('#sort-projects-dropdown').click();
        $(this).closest('.dropdown').find('.dropdown-toggle-text').attr('val', $(this).attr('val')).text($(this).text());
    });
})();
