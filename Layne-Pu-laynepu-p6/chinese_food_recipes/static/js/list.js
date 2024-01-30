$(document).ready(function() {
    // let searchValue = getUrlParam('searchValue');
    // let searchValue = $('h1#category-title').attr('searchValue');
    // let doPost = getUrlParam('doPost');

    // if (searchValue != null && searchValue.length > 0) {            //check if get method used on search bar
    //     if (searchValue === pork'') {
    //         $('h1#category-title').html('Search Results For: "' + searchValue + '"');
    //     } else {
    //         $('h1#category-title').html('No Results For: "' + searchValue + '"');
    //         $('#Hot-recipe').css({'visibility' : 'hidden'});
    //     }
    // }

    // if (doPost === 'true') {        //check if any recipe has been added on add.html
    //     window.onload=function(){alert("You have successfully posted a recipe!")};
    // }

    function getUrlParam(name) {
        let reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        let r = window.location.search.substr(1).match(reg);
        if (r != null)
            return unescape(r[2]);
        return null;
    }
});