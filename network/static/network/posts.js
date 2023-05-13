document.addEventListener('DOMContentLoaded', function() {

    // Select all buttons with IDs in the format "...-btn-{id}"
    const editBtns = document.querySelectorAll('[id^="edit-btn-"]');
    const likeBtns = document.querySelectorAll('[id^="like-btn-"]');
    const unlikeBtns = document.querySelectorAll('[id^="unlike-btn-"]');

    // Loop through each edit button and listen for click
    editBtns.forEach(function(editBtn) {
        editBtn.addEventListener('click', function() {
            // Get ID of the current post and call editPost
            const postID = editBtn.id.replace('edit-btn-', '');
            editPost(postID);
        });
    });

    // Loop through each like button and listen for click
    likeBtns.forEach(function(likeBtn) {
        likeBtn.addEventListener('click', function() {
            // Get ID of the current post and call likePost
            const postID = likeBtn.id.replace('like-btn-', '');
            likePost(postID);
        });
    });

    // Loop through each unlike button and listen for click
    unlikeBtns.forEach(function(unlikeBtn) {
        unlikeBtn.addEventListener('click', function() {
            // Get ID of the current post and call likePost
            const postID = unlikeBtn.id.replace('unlike-btn-', '');
            unlikePost(postID);
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

    // Post cannot be blank or contain only whitespace
    if (newContent === "" || newContent.trim().length === 0) {
        document.querySelector(`#input-error-${postID}`).style.display = 'block';
    } else {
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
        document.querySelector(`#input-error-${postID}`).style.display = 'none';

        // Replace save button with edit button
        document.querySelector(`#edit-div-${postID}`).style.display = 'block';
        document.querySelector(`#save-div-${postID}`).style.display = 'none';

    }


}


function likePost(postID) {

    // Replace like button with unlike button
    document.querySelector(`#like-div-${postID}`).innerHTML = `<button class="remove-style" id="unlike-btn-${postID}"><i class="fa fa-heart heart-liked"></i></button>`;
    document.querySelector(`#like-div-${postID}`).id = `unlike-div-${postID}`;
    document.querySelector(`#unlike-btn-${postID}`).addEventListener('click', () => unlikePost(postID));

    const csrfToken = Cookies.get('csrftoken');
    fetch(`like/${postID}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            action: "like"
        })
    });

    // Update like count dynamically
    const likesString = document.querySelector(`#likes-div-${postID}`).innerHTML;
    let numberOfLikes = parseInt(likesString.replace("Number of likes: ", ""));
    numberOfLikes++;
    document.querySelector(`#likes-div-${postID}`).innerHTML = `Number of likes: ${numberOfLikes}`;
    

}


function unlikePost(postID) {

    // Replace unlike button with like button
    document.querySelector(`#unlike-div-${postID}`).innerHTML = `<button class="remove-style" id="like-btn-${postID}"><i class="fa fa-heart-o heart-unliked"></i></button>`;
    document.querySelector(`#unlike-div-${postID}`).id = `like-div-${postID}`;
    document.querySelector(`#like-btn-${postID}`).addEventListener('click', () => likePost(postID));

    const csrfToken = Cookies.get('csrftoken');
    fetch(`like/${postID}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            action: "unlike"
        })
    });

    // Update like count dynamically
    const likesString = document.querySelector(`#likes-div-${postID}`).innerHTML;
    let numberOfLikes = parseInt(likesString.replace("Number of likes: ", ""));
    numberOfLikes--;
    document.querySelector(`#likes-div-${postID}`).innerHTML = `Number of likes: ${numberOfLikes}`;

}