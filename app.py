"""
Flask Blog Application

This application allows users to create, read, update, and delete blog posts.

"""

import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def json_database():
    """
    Read the blog post data from the JSON file.

    Returns:
        list: List of blog post dictionaries.
    """
    with open("database.json", "r", encoding="utf-8") as fileobj:
        data = json.load(fileobj)
    return data


def generate_id():
    """
    Generate a new unique ID for a blog post.

    Returns:
        int: Unique ID for the blog post.
    """
    data = json_database()
    counter = len(data) + 1
    return counter


@app.route('/')
def index():
    """
    Render the home page with the list of blog posts.

    Returns:
        str: Rendered HTML template.
    """
    blog_post = json_database()
    return render_template("index.html", post=blog_post)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Add a new blog post.

    If a POST request is received, the form data is used to create a new blog post.
    If a GET request is received, the add form is rendered.

    Returns:
        str: Rendered HTML template or redirect to home page.
    """
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        new_post = {"id": generate_id(),
                    "author": author,
                    "title": title,
                    "content": content}

        data = json_database()
        data.append(new_post)

        with open("database.json", "w", encoding="utf-8") as fileobj:
            json.dump(data, fileobj)

        return redirect(url_for('index'))

    return render_template('add.html', title="Add form")


@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete(post_id):
    """
    Delete a blog post.

    Args:
        post_id (int): ID of the blog post to delete.

    Returns:
        str: Redirect to home page.
    """
    data = json_database()
    for blog_post in data:
        if blog_post['id'] == post_id:
            data.remove(blog_post)
            break
    with open("database.json", "w", encoding="utf-8") as fileobj:
        json.dump(data, fileobj)
    return redirect('/')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Update a blog post.

    If a POST request is received, the form data is used to update the blog post.
    If a GET request is received, the update form is rendered.

    Args:
        post_id (int): ID of the blog post to update.

    Returns:
        str: Rendered HTML template or redirect to home page.
    """
    posts = json_database()
    post = None

    for check_post in posts:
        if check_post['id'] == post_id:
            post = check_post
            break

    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post in the JSON file
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        post['author'] = author
        post['title'] = title
        post['content'] = content

        with open("database.json", "w", encoding="utf-8") as fileobj:
            json.dump(posts, fileobj)

        return redirect(url_for('index'))

    # It's a GET request, display the update.html page
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
