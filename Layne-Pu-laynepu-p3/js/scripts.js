$(document).ready(function() {

    $('#search-bar').submit(function() {            //redirect after searching
        let searchValue = $('#search-bar-textfield').val();
        document.location.href = "list.html?searchValue=" + searchValue;
        return false;
    });

    $('.bookmarkIcon').click(function(){            //click on bookmark icon
        let msg;
        if ($(this).attr("class")!=="selectedBookmarkIcon") {
            $(this).attr('src', "img/bookmark_solid.png");
            $(this).attr('class', "selectedBookmarkIcon");
            msg = "<p>Successfully add to your collection!</p>";
        } else {
            $(this).attr('src', "img/bookmark_hollow.png");
            $(this).attr('class', "bookmarkIcon");
            msg = "<p>Remove from your collection!</p>";
        }
        $(this).before(msg);
        $(this).prev().fadeOut(1000, function(){
            $(this).remove();
        });
    });

    $('.bookmarkIcon').mouseover(function() {           // enlarge the icon when mouseover
         $(this).css({'transform': 'scale(1.5)'});
    });

    $('.bookmarkIcon').mouseout(function() {            // restore the icon when mouseout
     $(this).css({'transform': 'scale(1)'});
    });

    $('img.recipes-pic').click(function(){          //click to see large recipe pic
        $("#large-pic").attr("src", $(this).attr("src"));
        $("#pop-up-img-div").show();
    });

    $("#pop-up-img-div").click( function () {           //click to hide the large recipe pic
        $(this).hide();
    });

        // var terms = [
    //     "Shui Zhu Pork",
    //     "stewed pork rice",
    //     "Braised pork rice",
    //     "sweet and sour pork",
    //     "Pork ribs soup",
    //     "Pork Knuckle Noodle Threads",
    //     "Pork Rice Tamale",
    //     "Pork Sauce Rice",
    //     "shredded pork with garlic sauce",
    //     "Braised Pork with Preserved Mustard",
    //     "Sliced Pork Belly with Garlic Sauce"
    // ];
    //
    // $('#search-bar-textfield').autocomplete({
    //     source: terms
    // });
})