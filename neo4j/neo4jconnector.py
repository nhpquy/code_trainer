from py2neo import Graph


class Neo4jConnection:

    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__graph = None
        try:
            self.__graph = Graph(host=self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self.__graph is not None:
            self.__graph = None

    def get_graph(self):
        if self.__graph is not None:
            return self.__graph

    def query(self, query, db=None):
        assert self.__graph is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.__graph.session(database=db) if db is not None else self.__graph.session()
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response


if __name__ == '__main__':
    conn = Neo4jConnection("bolt://localhost:7687", "admin", "123456")
