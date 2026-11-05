from scx.database import Database

db_fail = False

try:
    # Create a database with a primary key table
    db = Database(
        """
        CREATE TABLE dog_owner (
            Dog_ID INT,
            Owner_ID INT,
            PRIMARY KEY (Dog_ID, Owner_ID)
        );
    """
    )

    # Query with INSERT should execute once and not violate primary key
    db.query("INSERT INTO dog_owner VALUES (1, 1);")

    # Validate row count and contents
    results = db.query("SELECT * FROM dog_owner;")
    if len(results) != 1:
        db_fail = True
    if results != [{"Dog_ID": 1, "Owner_ID": 1}]:
        db_fail = True

    # Validate dict_of_lists return type
    results_dict = db.query(
        "SELECT * FROM dog_owner;", return_type="dict_of_lists"
    )
    if results_dict != {"Dog_ID": [1], "Owner_ID": [1]}:
        db_fail = True

except Exception as e:
    print(f"Exception encountered: {e}")
    db_fail = True

if db_fail:
    print("database/t2.py failed")
    raise Exception("database/t2.py failed")
