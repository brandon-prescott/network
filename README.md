# Network

## Requirements

Design a Twitter-like social network website for making posts and following users.

* **New Post:** Users who are signed in should be able to write a new text-based post by filling in text into a text area and then clicking a button to submit the post (@00:05).
* **All Posts:** The home page should show posts from all users, with most recent posts first.
* **Profile Page:** Clicking on a username should load that user’s profile page. This page should:
  * Display the number of followers the user has, as well as the number of people that the user follows.
  * Display all of the posts for that user, in reverse chronological order.
  * For any other user who is signed in, this page should also display a “Follow” or “Unfollow” button that will let the current user toggle whether or not they are following this user’s posts. Note that this only applies to any “other” user: a user should not be able to follow themselves.
* **Following:** The “Following” link in the navigation bar should take the user to a page where they see all posts made by users that the current user follows.
* **Pagination:** On any page that displays posts, posts should only be displayed 10 on a page. If there are more than ten posts, a “Next” button should appear to take the user to the next page of posts (which should be older than the current page of posts). If not on the first page, a “Previous” button should appear to take the user to the previous page of posts as well.
* **Edit Post:** Users should be able to click an “Edit” button or link on any of their own posts to edit that post.
* **"Like" and "Unlike":** Users should be able to click a button or link on any post to toggle whether or not they “like” that post.
   
## Preview

https://github.com/brandon-prescott/network/assets/108699186/16906cf2-ee4c-46d3-908e-31d13f04c1e3

## Installation

To set up this project on your computer:
1. Download this project
    ```
    git clone https://github.com/brandon-prescott/network.git
    ```
2. Navigate to the commerce directory
    ```
    cd network
    ```
3. Install all necessary dependencies
    ```
    pip install -r requirements.txt
    ```
4. Make migrations
    ```
    python3 manage.py makemigrations
    ```
5. Migrate
    ```
    python3 manage.py migrate
    ```
