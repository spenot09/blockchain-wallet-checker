import pyTigerGraph as tg
import functools
import time


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

    def __init__(self, host, graphname, username, password, apiToken):
        self.host = host
        self.graphname = graphname
        self.username = username
        self.password = password
        self.apiToken = apiToken

        self.conn = tg.TigerGraphConnection(
            host=self.host,
            graphname=self.graphname,
            username=self.username,
            password=self.password,
            apiToken=self.apiToken,
        )

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
    def check_if_query_installed(self, installed_query_name):
        # TODO: Figure out how to check if a query has been installed already
        is_installed = True
        return is_installed

    @timer
    def get_wallet_score(self, wallet, installed_query_name, network):
        """
        Retrieve the target wallet score by injecting it as a parameter into the previously installed query.
        """

        if not self.check_if_query_installed(installed_query_name):

            result = f"{installed_query_name} hasn't been installed yet. Please install chosen query with the install_query(query_to_install, name) method"

        try:
            result = self.conn.gsql(
                f'run query {installed_query_name}("{wallet}", "{network}")'
            )
            print(
                f"Target wallet has been assigned a score of {q}/10, 0 being the worst safety score, 10 being the highest safety score"
            )
        except:
            result = "Couldn't access query at the moment"

        return result
