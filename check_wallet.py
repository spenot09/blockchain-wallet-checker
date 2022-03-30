import os
import sys
import argparse

from walletChecker.helpful_scripts import TigergraphAPI

from dotenv import load_dotenv

load_dotenv()

HOST = "https://5dab72d8cab74eaabdeac665cf8a72e3.i.tgcloud.io"
GRAPH_NAME = "eth"
TG_USERNAME = os.getenv("TG_USERNAME")
TG_PASSWORD = os.getenv("TG_PASSWORD")
API_TOKEN = os.getenv("API_TOKEN")

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

args = vars(my_parser.parse_args())


def check_score(target_wallet=args["wallet"], network=args["network"]):
    print(f"Target wallet: {target_wallet}")
    print(f"Checking on the {network} network")

    tg = TigergraphAPI(HOST, GRAPH_NAME, TG_USERNAME, TG_PASSWORD, API_TOKEN)
    score = tg.get_wallet_score(
        wallet=target_wallet, installed_query="TestQuery", network=network
    )


check_score()
