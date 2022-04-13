import pyTigerGraph as tg
import functools
import time
import traceback
import sys
import os

from constants import constants


network = "ethereum"
TG_USERNAME = os.getenv("TG_USERNAME")
TG_PASSWORD = os.getenv("TG_PASSWORD")
HOST = constants[network]["host"]
GRAPH_NAME = constants[network]["graph_name"]
SECRET = os.getenv(f"SECRET_{GRAPH_NAME.upper()}_GRAPH")


def timer(func):
    # Timer decorator to check runtime of functions
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        print(f"{func.__name__}() took {elapsed_time:0.4f} seconds to run")
        return value

    return wrapper_timer


class TigergraphAPI:
    """
    Class to interact with TigerGraph API and take care of connections and safety score retrieval.
    """

    def __init__(self, host, graphname, username, password, secret):
        self.host = host
        self.graphname = graphname
        self.username = username
        self.password = password

        graph = tg.TigerGraphConnection(
            host=self.host,
            graphname=self.graphname,
        )
        self.authToken = graph.getToken(secret)[0]

        self.conn = tg.TigerGraphConnection(
            host=self.host,
            graphname=self.graphname,
            username=self.username,
            password=self.password,
            apiToken=self.authToken,
        )

    @timer
    def is_successfully_connected(self):
        return self.conn.getEndpoints() is not None

    @timer
    def query(self, gsql_query):
        """
        A function to write arbitrary gqsl queries to the instantiated graph.
        """
        result = self.conn.gsql(gsql_query)
        return result

    @timer
    def install_query(self, query_to_install, name):
        """
        A function to install a query on the designated graph to allow for faster retrieval speeds in the future.
        Installing a query compiles the procedures described by the query as well as generates a REST endpoint for running the query.
        """
        return self.conn.gsql(
            f"""
            drop query {name}

            {query_to_install}

            install query {name}
            """
        )

    @timer
    def list_installed_queries(self):
        return [key.split("/")[-1] for key in self.conn.getInstalledQueries().keys()]

    @timer
    def is_query_installed(self, installed_query_name):
        return installed_query_name in self.list_installed_queries()

    @timer
    def get_wallet_score(self, installed_query_name: str, query_params: dict):
        """
        Retrieve the target wallet score by injecting it as a parameter into the previously installed query.
        """

        if not self.is_query_installed(installed_query_name):
            print(
                f"{installed_query_name} hasn't been installed yet. Please install chosen query with the install_query(query_to_install, name) method"
            )
            result = f"{installed_query_name} hasn't been installed yet. Please install chosen query with the install_query(query_to_install, name) method"

        try:
            result = self.conn.runInstalledQuery(installed_query_name, query_params)[0]
            return result

        except Exception:
            print(traceback.format_exc())
            # or
            print(sys.exc_info()[2])
            print("Couldn't access query at the moment")
            return


if __name__ == "main":
    tg_instance = TigergraphAPI(HOST, GRAPH_NAME, TG_USERNAME, TG_PASSWORD, SECRET)
    query_params = {
        "v_type": "Wallet",
        "e_type": "sending_payment",
        "re_type": "receiving_payment",
    }
    tg_instance.get_wallet_score("Degree", query_params)
