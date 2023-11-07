import sqlite3
import utils as ut

def insert_into_reservations_table(data):
    """
    Insert data into reservations table.
    """

    # https://mews-systems.gitbook.io/connector-api/operations/reservations
    # Load config dict
    config = ut.load_config()

    # Connect to SQLite with the database name from the YAML file
    conn = sqlite3.connect(config['db_name'])

    # Create a cursor object using the cursor() method
    cursor = conn.cursor()

    # Create table - USERS
    cursor.execute('''CREATE TABLE IF NOT EXISTS RESERVATIONS
                    (
                        ID                  TEXT PRIMARY KEY     NOT NULL,
                        STATE               TEXT,
                        ORIGIN              TEXT,
                        CREATEDUTC          TEXT,
                        BUSINESSSEGMENTID   TEXT,
                        PURPOSE             TEXT
                   );''')

    # Prepare a SQL query for inserting multiple records
    insert_query = '''INSERT OR IGNORE INTO      RESERVATIONS 
                                                (
                                                    ID, 
                                                    STATE,
                                                    ORIGIN,
                                                    CREATEDUTC,
                                                    BUSINESSSEGMENTID,
                                                    PURPOSE
                                                ) 
                        VALUES                  (?, ?, ?, ?, ?, ?)'''

    # Use executemany() to insert the data; the method takes a sequence of parameters
    cursor.executemany(insert_query, [(item['ID'], 
                                       item['STATE'], 
                                       item['ORIGIN'], 
                                       item['CREATEDUTC'],
                                       item['BUSINESSSEGMENTID'],
                                       item['PURPOSE']
                                       ) for item in data])

    # Commit the changes - it's important to commit the changes to save them to the database.
    conn.commit()

    # Close the connection when done.
    conn.close()

    print("Data inserted successfully!")
