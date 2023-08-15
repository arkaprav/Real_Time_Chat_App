$(document).ready(function(e){
    var members = new Array();
    members.push(creator);
    var clicked = false;
    $('#members').click(function(e){
        e.preventDefault();
        if(clicked == true){
            $('.options').css('display','none');
            clicked = false;
        }
        else{
            $('.options').css('display','block');
            clicked = true;
        }
        var options = $('.options').children();
            options.each(function(i,e){
                $(this).click(function(){
                var text = $(this).text();
                if(members.includes(text)){
                    let i = members.indexOf($(this).text());
                    members.splice(i, 1);
                    $(this).css('background-color','white');
                    $(this).css('color','black');
                }
                else{
                    members.push($(this).text());
                    $(this).css('background-color','skyblue');
                    $(this).css('color','white');
                }
                content = '';
                for(const i in members){
                    if(content == ''){
                        content += String(members[i]);
                    }
                    else{
                        content += ',' + String(members[i]);
                    }
                }
                $('#members').text(content);
            })
        });
    });
    $('#create').click(function(e){
        e.preventDefault();
        console.log(members);
        let name = $('#name').val();
        if(name == '' || name == 'Room Name'){
            $('#error').css('display','block');
            $('#error').text('Invalid room name');
        }
        else if(members.length < 2){
            $('#error').css('display','block');
            $('#error').text('atleast two members should be chosen');
        }
        else{
            $('#error').css('display','none');
            $.ajax({
                type: "POST",
                url: url,
                data: {
                    'csrfmiddlewaretoken':csrf_token,
                    'name': name,
                    'members':members
                },
                success: function(response) {
                    window.location.href = index;
                },
                error: function (response){
                    console.log("Something went wrong");
                }
            });
        }
    });
})
