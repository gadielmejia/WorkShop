from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>WorkShop Flask App</h1><p>Welcome to the WorkShop application.</p>", 200


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


@app.route("/about")
def about():
    return (
        "<h1>About WorkShop</h1><p>This is a Flask demonstration application.</p>",
        200,
    )
