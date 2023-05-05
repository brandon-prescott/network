document.addEventListener('DOMContentLoaded', function() {

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

    // Replace content with editable text area
    document.querySelector(`#content-div-${postID}-saved`).style.display = 'none';
    document.querySelector(`#content-div-${postID}-editing`).style.display = 'block';

    // Replace edit button with save button
    document.querySelector(`#edit-div-${postID}`).style.display = 'none';
    document.querySelector(`#save-div-${postID}`).style.display = 'block';

    // On click, save the post
    document.querySelector(`#save-btn-${postID}`).addEventListener('click', () => savePost(postID));

}


function savePost(postID) {

    const newContent = document.querySelector(`#content-textarea-${postID}`).value;

    // Update database with edited post content
    // Django forbids use of PUT request, so POST request is used with CSRF token for security
    // Helps prevent user from editing another users post
    const csrfToken = Cookies.get('csrftoken'); // From 'js-cookie' library included in head of layout.html
    fetch(`post/${postID}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            content: newContent
        })
    });

    // Close editable text area and update content HTML on current page
    document.querySelector(`#content-div-${postID}-saved`).innerHTML = newContent;
    document.querySelector(`#content-div-${postID}-saved`).style.display = 'block';
    document.querySelector(`#content-div-${postID}-editing`).style.display = 'none';

    // Replace save button with edit button
    document.querySelector(`#edit-div-${postID}`).style.display = 'block';
    document.querySelector(`#save-div-${postID}`).style.display = 'none';


}