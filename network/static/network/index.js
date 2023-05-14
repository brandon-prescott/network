document.addEventListener('DOMContentLoaded', function() {

    // Check for post input error and display error message if invalid
    const postBtn = document.querySelector('#post-btn');
    postBtn.addEventListener('click', function() {
        const postContent = document.querySelector('#create-textarea').value;
        if (postContent === "" || postContent.trim().length === 0) {
            document.querySelector('#create-error').style.display = 'block';
            document.querySelector('#create-error').innerHTML = 'Post cannot be blank.';
        }
    });
    
});