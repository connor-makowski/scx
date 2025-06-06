import duckdb, type_enforced
from .utils import Error
from pprint import pprint


@type_enforced.Enforcer
class Database(Error):
    def __init__(self, setup_code: str) -> None:
        """
        Create a database

        Arguments:

        - `setup_code`:
            - Type: str
            - What: The SQL code to run that sets up the database

        """
        self.con = duckdb.connect(database=":memory:", read_only=False)
        self.con.execute(setup_code)

    def get_info(self) -> dict[dict[str, dict[str]]]:
        """
        Return a dictionary of the database schema

        Returns a dictionary of the database schema in the following format:
        {
            'Table1': {
                'type': 'table',
                'columns': {
                    'column1': 'type1',
                    'column2': 'type2',
                    ...
                }
            },
            ...
        }
        """
        return {
            table.get("name"): {
                "type": table.get("type"),
                "columns": {
                    desc[0]: desc[1]
                    for desc in self.con.execute(
                        f"SELECT * FROM {table.get('name')} LIMIT 1"
                    ).description
                },
            }
            for table in self.query(
                "SELECT name, type FROM sqlite_master WHERE type='table' OR type='view' ORDER BY name;"
            )
        }

    def show_info(self, pretty: bool = True) -> None:
        """
        Print the database schema

        Optional Arguments:

        - `pretty`:
            - Type: bool
            - Default: True
            - What: Whether to print the schema in a human-readable format
                - If True, print the schema in a human-readable format
                - If False, pretty prints the schema as a dictionary

        Returns None
        """
        if pretty:
            for item, item_data in self.get_info().items():
                print("=" * 25)
                print(f"{item_data.get('type').title()}: {item}")
                for column, dtype in item_data.get("columns").items():
                    print(f"  {column}: {dtype}")
                print()
        else:
            pprint(self.get_info())

    def query(
        self, query: str, return_type: str = "list_of_dicts"
    ) -> [list[dict], dict[list]]:
        """
        Execute a query on the database

        Arguments:

        - `query`:
            - Type: str
            - What: The SQL query to execute

        Optional Arguments:

        - `return_type`:
            - Type: str
            - Default: 'list_of_dicts'
            - What: The format to return the results in
                - 'list_of_dicts': Returns a list of dictionaries, where each dictionary is a row
                - 'dict_of_lists': Returns a dictionary of lists, where each list is a column

        Returns the results of the query in the specified format
        """
        results = self.con.execute(query).fetchall()
        headers = [desc[0] for desc in self.con.execute(query).description]
        if return_type == "list_of_dicts":
            return [dict(zip(headers, row)) for row in results]
        elif return_type == "dict_of_lists":
            return {
                header: [row[i] for row in results]
                for i, header in enumerate(headers)
            }
