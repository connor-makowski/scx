from scx.database import Database

# Tables
# - customers.parquet

data_folder = "s3://scx-dev/databases/supermarket/"
db_fail = False

try:
    # Create a database
    db = Database(
        f"""
        CREATE TABLE Customers AS SELECT * FROM read_parquet('{data_folder}customers.parquet');
    """
    )
    # Validate the info
    info = db.get_info()
    if (
        info.get("Customers", {}).get("columns", {}).get("Customer_ID")
        != "NUMBER"
    ):
        db_fail = True

    # Query the database
    if len(db.query("SELECT * FROM Customers LIMIT 1")) != 1:
        db_fail = True

except:
    db_fail = True

if db_fail:
    print("database/t1.py failed")
