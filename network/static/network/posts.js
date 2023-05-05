document.addEventListener('DOMContentLoaded', function() {

    console.log("DOM Content Loaded!");

    // Select all buttons with IDs in the format "edit-btn-{id}"
    const editBtns = document.querySelectorAll('[id^="edit-btn-"]');

    // Loop through each button and listen for click
    editBtns.forEach(function(editBtn) {
        editBtn.addEventListener('click', function() {
            // Get ID of the current post
            const postID = editBtn.id.replace('edit-btn-', '');

            // Do stuff with the click
            console.log(`Edit Button ${postID} clicked!`);

        });
    });

})

