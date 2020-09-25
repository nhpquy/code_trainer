from py2neo import Graph


class Neo4jConnection:

    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__graph = None
        try:
            self.__graph = Graph(uri=self.__uri, user=self.__user, password=self.__pwd)
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self.__graph is not None:
            self.__graph = None

    def get_graph(self):
        if self.__graph is not None:
            return self.__graph
