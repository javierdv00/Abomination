import psycopg2
#from "file name" import "function"  # Import the scrape_books function

db_params = psycopg2.connect(host="localhost", 
                             dbname="postgres",
                             user="postgres",
                             password="1190",
                             port=5432)

cur = db_params.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS person(
            ID INT PRIMARY KEY,
            Name VARCHAR(255),
            Age INT,
            Team VARCHAR(255),
            Land VARCHAR(255),
            Possition VARCHAR(255),
            Birthday DATE
            )
            """)


def insert_person(data):
    conn = None
    cur = None
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        
        # SQL query to insert data
        insert_query = """
        INSERT INTO person (Name, Age, Team, Land, Possition, Birthday) VALUAES (%s, %s, %s, %s, %s, %s)
        """
        
        # Execute SQL query for each scraped data item
        for item in data:
            cur.execute(insert_query, item)
        
        # Commit the transaction
        conn.commit()
        print("Data inserted successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close cursor and connection
        cur.close()
        conn.close()

"""if __name__ == "__main__":
    # Get scraped data
    person_data = "function"
    # Insert scraped data into database
    insert_person(person_data)"""