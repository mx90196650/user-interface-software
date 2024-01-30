$(document).ready(function() {

    $(document).on('click','.comment-edit-button', function(){
        console.log('click icon url = ' + $(this).parents('.comment-box').attr('edit-url'))
        let content = $(this).parents('.comment-box').find('p.comment').text();
        $(this).parents('.comment-box').find('p.comment').remove();
        $(this).parents('.comment-box').find('div.comment-box-img').after('<form id="edit-comment-form" method="post" action="'+ $(this).parents('.comment-box').attr('edit-url') + '">' +
            '<textarea name="edit-comment-field" id="edit-comment-field" >' + content + '</textarea>' +
            '<input name="submit-edit-comment" id="submit-edit-comment" type="button" value="Confirm Edit">' +
            '</form>')
    });

    $( '#comment-section' ).on( "mouseover", ".comment-edit-button", function( event ) {
        $(this).css({'transform': 'scale(1.2)'});
    });

    $( '#comment-section' ).on( "mouseout", ".comment-edit-button", function( event ) {
        $(this).css({'transform': 'scale(1)'});
    });

    $( '#comment-section' ).on( "mouseover", ".comment-delete-button", function( event ) {
        $(this).css({'transform': 'scale(1.2)'});
    });

    $( '#comment-section' ).on( "mouseout", ".comment-delete-button", function( event ) {
        $(this).css({'transform': 'scale(1)'});
    });

    $('.comment-delete-button').click(function(){
        if (confirm('Are you sure you want to delete this comment?')) {
            let comment_id = $(this).attr('comment_id');
            let url = $(this).attr('delete-ajax-url');
            $.ajax({
                url: url,
                data: {
                    comment_id: comment_id
                },
                type: "POST",
                dataType: "json",
                headers: {'X-CSRFToken': csrftoken},
                context: this
            })
              .done(function( json ) {
                  if (json.success === "success") {
                      $(this).parents('.comment-box').remove()
                      alert('You have successfully deleted the comment!')
                  } else {
                    alert("Error: " + json.error)
                  }
              })
              .fail(function( xhr, status, errorThrown ) {
                alert( "Sorry, there was a problem!" );
                console.log( "Error: " + errorThrown );
              })
        }
    });

    $('input#submit-comment').click(function(){
        let form = $(this).parents('form#comment-form')
        $.ajax({
            url: form.attr('action'),
            data: form.serialize(),
            type: form.attr('method'),
            dataType: "json",
            headers: {'X-CSRFToken': csrftoken},
            context: this
        })
          .done(function( json ) {
              if (json.success === "success") {
                  $('.comment-box').eq(0).after(
                      '<div class="comment-box" edit-url="/chinese_food_recipes/comment-edit/' + json.comment_id + '">' +
                          '<div class="image-comment">' +
                              '<div class="comment-box-img">' +
                                  '<img src="/static/img/hacker_anonymous_icon.png" alt="user-pic">' +
                                      '<a href="{{ comment.user.details.get_absolute_url }}">' + json.comment_user + '</a>' +
                              '</div>' +
                              '<p class="comment">' + json.comment_content + '</p>' +
                          '</div>' +
                          '<div class="comment-right-sec">' +
                              '<div class="comment-man-div">' +
                                  '<img src="/static/img/edit_icon.png" alt="icon" class="comment-edit-button"' +
                                       'url="{% url \'chinese_food_recipes:recipes_edit_page\' recipe_id=recipe.id %}">' +
                                      '<img src="/static/img/delete-icon.png" class="comment-delete-button"' +
                                           'comment_id="{{ comment.id }}"' +
                                           'delete-ajax-url={% url \'chinese_food_recipes:comment_delete\' %}>' +
                              '</div>' +
                              '<p class="comment-date">few seconds ago</p>' +
                          '</div>' +
                      '</div>'
                  )
                  $('#comment-text-field').val('');
                  alert('You have successfully added the comment!')
              } else {
                alert("Error: " + json.error)
              }
          })
          .fail(function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem!" );
            console.log( "Error: " + errorThrown );
          })
    });

    $( '#comment-section' ).on( "click", "input#submit-edit-comment", function( event ) {
        let form = $(this).parents('form#edit-comment-form')
        console.log('url = ' + form.attr('action'))
        $.ajax({
            url: form.attr('action'),
            data: form.serialize(),
            type: form.attr('method'),
            dataType: "json",
            headers: {'X-CSRFToken': csrftoken},
            context: this
        })
          .done(function( json ) {
              if (json.success === "success") {
                  $(this).parents('form#edit-comment-form').before('<p class="comment">' + json.comment_content + '</p>')
                  $(this).parents('form#edit-comment-form').remove();
                  alert('You have successfully edited the comment!')
              } else {
                alert("Error: " + json.error)
              }
          })
          .fail(function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem!" );
            console.log( "Error: " + errorThrown );
          })
    });
})