import psycopg2
from db_credentials import host, user, password, db


def connect_to_database(host=host, user=user, password=password, db=db):
    """Connects to a database using the provided credentials"""

    db_connection = psycopg2.connect(f"host={host} dbname={db} user={user} password={password}")
    return db_connection


def execute_query(db_connection=None, query=None, query_params=None):
    """Executes the query on the database using the provided query paramaters

    Args:
        db_connection: The database. Defaults to None.
        query: The query that will be executed on the database. Defaults to None.
        query_params: The parameters for the provided query. Defaults to None.

    Returns:
        [type]: [description]
    """
    if db_connection is None:
        print("No connection to the database found! Have you called connect_to_database() first?")
        return None

    if query is None or len(query.strip()) == 0:
        print("Query is empty. Please enter a valid SQL Query")
        return None

    print(f"Executing {query} using {query_params}")

    cursor = db_connection.cursor()
    cursor.execute(query, query_params)
    db_connection.commit()
    return cursor


if __name__ == "__main__":
    pass
