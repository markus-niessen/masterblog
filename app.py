from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def load_posts():
    """Load all blog posts from the JSON file."""
    with open("blog_posts.json", "r") as file:
        return json.load(file)


def save_posts(posts):
    """Save all blog posts to the JSON file."""
    with open("blog_posts.json", "w") as file:
        json.dump(posts, file, indent=4)


@app.route("/")
def index():
    """Display all blog posts on the home page."""
    blog_posts = load_posts()
    return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    """Display the add form and create new blog posts."""
    if request.method == "POST":
        blog_posts = load_posts()

        title = request.form.get("title")
        author = request.form.get("author")
        content = request.form.get("content")

        new_id = max(post["id"] for post in blog_posts) + 1 if blog_posts else 1

        new_post = {
            "id": new_id,
            "title": title,
            "author": author,
            "content": content,
            "likes": 0
        }

        blog_posts.append(new_post)
        save_posts(blog_posts)

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/delete/<int:post_id>")
def delete(post_id):
    """Delete a blog post by its ID."""
    blog_posts = load_posts()

    blog_posts = [post for post in blog_posts if post["id"] != post_id]

    save_posts(blog_posts)

    return redirect(url_for("index"))


def fetch_post_by_id(post_id):
    """Return a blog post matching the given ID."""
    blog_posts = load_posts()

    for post in blog_posts:
        if post["id"] == post_id:
            return post

    return None


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    """Display the update form and save edited posts."""
    blog_posts = load_posts()
    post = fetch_post_by_id(post_id)

    if post is None:
        return "Post not found", 404

    if request.method == "POST":
        post["title"] = request.form.get("title")
        post["author"] = request.form.get("author")
        post["content"] = request.form.get("content")

        for index, blog_post in enumerate(blog_posts):
            if blog_post["id"] == post_id:
                blog_posts[index] = post
                break

        save_posts(blog_posts)

        return redirect(url_for("index"))

    return render_template("update.html", post=post)


@app.route("/like/<int:post_id>")
def like(post_id):
    """Increase the like counter of a blog post."""
    blog_posts = load_posts()

    for post in blog_posts:
        if post["id"] == post_id:
            post["likes"] += 1
            break

    save_posts(blog_posts)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
