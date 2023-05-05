document.addEventListener('DOMContentLoaded', function() {

    console.log("DOM Content Loaded!");

    // Select all buttons with IDs in the format "edit-btn-{id}"
    const editBtns = document.querySelectorAll('[id^="edit-btn-"]');

    // Loop through each button and listen for click
    editBtns.forEach(function(editBtn) {
        editBtn.addEventListener('click', function() {
            // Get ID of the current post and call editPost
            const postID = editBtn.id.replace('edit-btn-', '');
            editPost(postID);
        });
    });
})


function editPost(postID) {
    console.log(`Post ${postID} clicked!`);

    document.querySelector(`#content-div-${postID}-saved`).style.display = 'none';
    document.querySelector(`#content-div-${postID}-editing`).style.display = 'block';

}