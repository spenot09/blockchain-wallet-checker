import os
from helpful_scripts import TigergraphAPI
from constants import constants
from dotenv import load_dotenv
from flask import Flask, render_template, request


load_dotenv()

TG_USERNAME = os.getenv("TG_USERNAME")
TG_PASSWORD = os.getenv("TG_PASSWORD")
SECRET = os.getenv("SECRET_KMTEST_GRAPH")

# TG_USERNAME = "tigergraph"
# TG_PASSWORD = "tigergraph"
# SECRET = "5ci5q0oof0bebo3u7p6sqthpkd44rp7v"

application = Flask(__name__)


@application.route("/")
def form():
    return render_template("form.html")


@application.route("/data/", methods=["POST", "GET"])
def data():
    if request.method == "GET":
        return (
            f"The URL /data is accessed directly. Try going to '/form' to submit form"
        )
    if request.method == "POST":
        # Go and get score from API
        form_data = request.form

        target_wallet = form_data["Target wallet"]
        network = form_data["Network"].lower()
        query_to_run = "WalletScore_Query"

        print(f"Target wallet: {target_wallet}")
        print(f"Checking on the {network} network")

        HOST = constants[network]["host"]
        GRAPH_NAME = constants[network]["graph_name"]

        tg_instance = TigergraphAPI(HOST, GRAPH_NAME, TG_USERNAME, TG_PASSWORD, SECRET)
        result_dict = tg_instance.get_wallet_score(
            query_to_run, {"target_wallet": target_wallet}
        )

        try:
            score = result_dict["wallet"][0]["attributes"]["transaction_count"]
        except:
            print(f"{target_wallet} is not available in the current graph")
            quit()

        if query_to_run == "WalletScore_Query":
            try:
                max_score = tg_instance.get_wallet_score("Top1_Wallet", {})["wallet"][
                    0
                ]["attributes"]["transaction_count"]
            except:
                max_score = 100

            score = score * 10 / max_score
            score = f"The target wallet {target_wallet} has received a score of {score} out of 10.0"

        return render_template("data.html", form_data={target_wallet: score})


application.run(host="localhost", port=5000)
