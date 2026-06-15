from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def load_posts():
    with open("blog_posts.json", "r") as file:
        return json.load(file)


def save_posts(posts):
    with open("blog_posts.json", "w") as file:
        json.dump(posts, file, indent=4)


@app.route("/")
def index():
    blog_posts = load_posts()
    return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
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
            "content": content
        }

        blog_posts.append(new_post)
        save_posts(blog_posts)

        return redirect(url_for("index"))

    return render_template("add.html")

@app.route("/delete/<int:post_id>")
def delete(post_id):
    blog_posts = load_posts()

    blog_posts = [post for post in blog_posts if post["id"] != post_id]

    save_posts(blog_posts)

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
