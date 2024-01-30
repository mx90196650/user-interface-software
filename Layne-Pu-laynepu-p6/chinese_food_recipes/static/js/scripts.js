$(document).ready(function() {
    $('a.tab').click(function(){
        $('a.tab-selected').attr("class", "tab");
        $(this).attr("class", "tab-selected");
    });

    $('.bookmark-div > img').click(function(){            //click on bookmark icon
        if ($(this).prev().length)
            return;
        let recipe_id = $(this).attr('data-recipe-id');
        let url = $(this).attr('data-ajax-url');

            // Using the core $.ajax() method
        $.ajax({

            // The URL for the request
            url: url,

            // The data to send (will be converted to a query string)
            data: {
                recipe_id: recipe_id
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType: "json",

            headers: {'X-CSRFToken': csrftoken},

            context: this
        })
          // Code to run if the request succeeds (is done);
          // The response is passed to the function
          .done(function( json ) {
              let msg;
              if (json.success == "success") {
                if (json.action == 'collection_saved') {
                    $(this).attr('src', "/static/img/bookmark_solid.png");
                    msg = "<p>Successfully add to your collection!</p>";
                    $(this).attr('class', "selectedBookmarkIcon");
                  } else {
                    $(this).attr('src', "/static/img/bookmark_hollow.png");
                    msg = "<p>Remove from your collection!</p>";
                    $(this).attr('class', "bookmarkIcon");
                  }
                  $(this).before(msg);
                  $(this).prev().fadeOut(1000, function(){
                    $(this).remove();
                  });
              } else {
                alert("Error: " + json.error)
              }
          })
          // Code to run if the request fails; the raw request and
          // status codes are passed to the function
          .fail(function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem!" );
            console.log( "Error: " + errorThrown );
          })
          // Code to run regardless of success or failure;
          .always(function( xhr, status ) {
            // alert( "The request is complete!" );
          });
    });

    $('.bookmark-div img').mouseover(function(){           // enlarge the icon when mouseover
         $(this).css({'transform': 'scale(1.5)'});
    });

    $('.bookmark-div img').mouseout(function(){            // restore the icon when mouseout
     $(this).css({'transform': 'scale(1)'});
    });

    $('.delete-button').mouseover(function(){           // enlarge the icon when mouseover
         $(this).css({'transform': 'scale(1.5)'});
    });

    $('.delete-button').mouseout(function(){            // restore the icon when mouseout
     $(this).css({'transform': 'scale(1)'});
    });

    $(document).on('click','.delete-button', function(){
        if (confirm('Are you sure you want to delete this recipe?')) {
            $(this).parent('form.delete-form').submit()
        }
    });

    $(document).on('click','.editIcon', function(){
        // console.log($(this).attr("homeURL"));
        document.location.href = $(this).attr("url");
    });

    $('.editIcon').mouseover(function(){           // enlarge the icon when mouseover
         $(this).css({'transform': 'scale(1.5)'});
    });

    $('.editIcon').mouseout(function(){            // restore the icon when mouseout
     $(this).css({'transform': 'scale(1)'});
    });

    $('img.recipes-pic').click(function(){          //click to see large recipe pic
        $("#large-pic").attr("src", $(this).attr("src"));
        $("#pop-up-img-div").show();
    });

    $("#pop-up-img-div").click( function () {           //click to hide the large recipe pic
        $(this).hide();
    });
})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');