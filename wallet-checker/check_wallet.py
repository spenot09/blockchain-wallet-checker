import os
import sys
import argparse
import json

from helpful_scripts import TigergraphAPI
from constants import constants
from dotenv import load_dotenv

load_dotenv()

TG_USERNAME = os.getenv("TG_USERNAME")
TG_PASSWORD = os.getenv("TG_PASSWORD")
SECRET = os.getenv("SECRET_KMTEST_GRAPH")

# Create the parser
my_parser = argparse.ArgumentParser(description="Check the safety of a target wallet")

# Add the arguments
my_parser.add_argument(
    "--wallet",
    metavar="W",
    type=str,
    help="the target wallet you want to check",
)

my_parser.add_argument(
    "--network",
    metavar="N",
    default="ethereum",
    type=str,
    help="the chosen network you want to check the wallet on, defaults to ethereum",
)

my_parser.add_argument(
    "--query",
    metavar="Q",
    default="WalletScore_Query",
    type=str,
    help="the query you want to use to retrieve the required score. Refer to the README.md to understand the various scores available",
)


args = vars(my_parser.parse_args())


target_wallet = args["wallet"]
network = args["network"]
query_to_run = args["query"]

"""
example query parameters for the "Degree" query
query_params = {
    "v_type": "Wallet",
    "e_type": "sending_payment",
    "re_type": "receiving_payment",
}
"""

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
        max_score = tg_instance.get_wallet_score("Top1_Wallet", {})["wallet"][0][
            "attributes"
        ]["transaction_count"]
    except:
        max_score = 100

    score = score * 10 / max_score

    print(
        f"The target wallet {target_wallet} has received a score of {score} out of 10.0"
    )
    print(
        "Please refer to Appendix A in the README for an interpretation of this score."
    )
