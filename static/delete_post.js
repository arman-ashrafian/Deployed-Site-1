/* Runs when 'delete blog' button is clicked */
function delete_post() {
    if(confirm("Are you sure?")) {
        document.forms["deletebutton"].submit();
    }
}
