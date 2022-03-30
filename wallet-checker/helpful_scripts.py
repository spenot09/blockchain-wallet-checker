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
        print(f"{func.__name__} took {elapsed_time:0.4f} seconds to run")
        return value

    return wrapper_timer


class TigergraphAPI:
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
        result = self.conn.gsql(gsql_query)
        return result

    @timer
    def install_query(self, create_query, name):
        return self.conn.gsql(
            f"""
            drop query {name}

            {create_query}

            install query {name}
            """
        )

    @timer
    def get_wallet_score(self, wallet, installed_query, network) -> float:
        try:
            q = self.conn.gsql(f'run query {installed_query}("{wallet}", "{network}")')
            print(
                f"Target wallet has been assigned a score of {q}/10, 0 being the worst safety score, 10 being the highest safety score"
            )
        except:
            q = "Couldn't access query at the moment"
        return q
