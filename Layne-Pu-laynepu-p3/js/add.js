$(document).ready(function() {
    $('#add-recipe-form').submit(function () {          //redirect to list.html after submitting
        let searchValue = $('#search-bar-textfield').val();
        document.location.href = "list.html?doPost=true";
        return false;
    });
});