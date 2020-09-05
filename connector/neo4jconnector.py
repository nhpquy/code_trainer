import neo4jupyter
from py2neo import Graph, Node


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
    neo4jupyter.init_notebook_mode()
    conn = Neo4jConnection("bolt://localhost:7687", "admin", "123456")
    tx = conn.get_graph().begin()
    nicole = Node("Person", name="Nicole", age=24)
    tx.create(nicole)
    drew = Node("Person", name="Drew", age=20)
    tx.create(drew)
    mtdew = Node("Drink", name="Mountain Dew", calories=9000)
    tx.create(mtdew)
    cokezero = Node("Drink", name="Coke Zero", calories=0)
    tx.create(cokezero)
    coke = Node("Manufacturer", name="Coca Cola")
    tx.create(coke)
    pepsi = Node("Manufacturer", name="Pepsi")
    tx.create(pepsi)
    tx.commit()
    options = {"Person": "name", "Drink": "name", "Manufacturer": "name"}

    neo4jupyter.draw(conn.get_graph(), options)
