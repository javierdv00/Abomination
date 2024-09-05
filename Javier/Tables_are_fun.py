import psycopg2
#from "file name" import "function"  # Import the scrape_books function

db_params = psycopg2.connect(host="localhost", 
                             dbname="postgres",
                             user="postgres",
                             password="postgres",
                             port=5432)

cur = db_params.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS person(
            ID SERIAL PRIMARY KEY,
            Name VARCHAR(255),
            Age INT,
            Team VARCHAR(255),
            Land VARCHAR(255),
            Possition VARCHAR(255)
            )
            """)
db_params.commit()

def insert_person(data):
    conn = None
    cur = None
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(host="localhost", 
                             dbname="postgres",
                             user="postgres",
                             password="postgres",
                             port=5432)
        cur = conn.cursor()
        
        # SQL query to insert data
        insert_query = """
        INSERT INTO person (Name, Age, Team, Land, Possition) VALUES (%s, %s, %s, %s, %s)
        """
        
        # Execute SQL query for each scraped data item
        cur.execute(insert_query, data)
        
        # Commit the transaction
        conn.commit()
        print("Data inserted successfully.")
        # Close cursor and connection
        cur.close()
        conn.close()


    except Exception as e:
        print(f"An error occurred: {e}")

    # finally:
    #     # Close cursor and connection
    #     cur.close()
    #     conn.close()

"""if __name__ == "__main__":
    # Get scraped data
    person_data = "function"
    # Insert scraped data into database
    insert_person(person_data)"""