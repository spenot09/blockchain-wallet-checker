from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def form():
    return render_template("form.html")


@app.route("/data/", methods=["POST", "GET"])
def data():
    if request.method == "GET":
        return (
            f"The URL /data is accessed directly. Try going to '/form' to submit form"
        )
    if request.method == "POST":
        # Go and get score from API
        form_data = request.form
        wallet = form_data["Target wallet"]

        

        return render_template("data.html", form_data=wallet)


app.run(host="localhost", port=5000)
