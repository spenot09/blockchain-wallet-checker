import os
from helpful_scripts import TigergraphAPI
from constants import constants
from dotenv import load_dotenv
from flask import Flask, render_template, request


load_dotenv()

TG_USERNAME = os.getenv("TG_USERNAME")
TG_PASSWORD = os.getenv("TG_PASSWORD")
API_TOKEN = os.getenv("API_TOKEN")


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

        target_wallet = form_data["Target wallet"]
        network = form_data["Network"]

        print(f"Target wallet: {target_wallet}")
        print(f"Checking on the {network} network")

        HOST = constants[network]["host"]
        GRAPH_NAME = constants[network]["graph_name"]

        tg = TigergraphAPI(HOST, GRAPH_NAME, TG_USERNAME, TG_PASSWORD, API_TOKEN)
        score = tg.get_wallet_score(
            wallet=target_wallet, installed_query="TestQuery", network=network
        )

        return render_template("data.html", form_data={target_wallet: score})


app.run(host="localhost", port=5000)
