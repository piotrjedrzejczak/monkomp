from monkomp.app import app


@app.route("/", methods=["GET"])
def home():
    return 'Hello'