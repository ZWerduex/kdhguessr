import os, typing, sqlite3

import dotenv

env = dotenv.dotenv_values('.env')

class Database:
    """Abstract base class for database interfaces
    """

    def __init__(self):
        """Requires QUERIES_DIR variable set to the path to the queries directory in .env file
        """
        assert env['QUERIES_DIR'], 'QUERIES_DIR must be set in .env file'
        self.queries_dir: str = env['QUERIES_DIR'] # type: ignore

    def get_query(self, query_name: str) -> str:
        """Returns the content of a query found in queries directory

        Args:
            query_name (str): The filename of the SQL query

        Returns:
            str: The content of the identified SQL file
        """
        with open(os.path.join(self.queries_dir, f'{query_name}.sql'), 'r') as f:
            return f.read()

    def select(self,
        query_name: str,
        params: typing.Optional[tuple|dict]
    ) -> list[tuple]:
        """Runs a SELECT query identified by its name

        Args:
            query_name (str): The name of the query to run
            params (typing.Optional[tuple | dict]): Any params that query may requires. They can be named depending on the query.

        Returns:
            list[tuple]: The results of the SELECT query
        """
        raise NotImplementedError('select method must be implemented by subclass')

    def exec(self,
        query_name: str,
        params: typing.Optional[list[tuple|dict]]
    ) -> list[tuple]:
        """Runs a query that modifies the database (INSERT, UPDATE, DELETE) identified by its name.
        
        This method should handle connecting to the database, running the query, committing the transaction and closing the connection.

        Args:
            query_name (str): The name of the query to run
            params (typing.Optional[list[tuple | dict]]): Any params that query may requires. They can be named depending on the query.

        Returns:
            list[tuple]: The results of the query ran
        """
        raise NotImplementedError('exec method must be implemented by subclass')

class SQLite3Database(Database):
    """Interface for SQLite3 databases
    """

    def __init__(self):
        """Requires KDH_DATABASE variable set in .env file to the path of the SQLite3 database file.
        """
        super().__init__()
        assert env['KDH_DATABASE'], 'KDH_DATABASE must be set in .env file'
        self.path: str = env['KDH_DATABASE'] # type: ignore
 
    def select(self,
        query_name: str,
        params: typing.Optional[tuple|dict]
    ) -> list[tuple]:
        query = self.get_query(query_name)
        params = params or [] # type: ignore
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params) # type: ignore
            return cursor.fetchall()

    def exec(self,
        query_name: str,
        params: typing.Optional[list[tuple|dict]]
    ) -> list[tuple]:
        query = self.get_query(query_name)
        params = params or []
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params)
            conn.commit()
            return cursor.fetchall()