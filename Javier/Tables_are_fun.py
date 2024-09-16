import psycopg2

def connection():
    return psycopg2.connect(host="localhost", 
                                dbname="postgres",
                                user="postgres",
                                password="postgres",
                                port=5432)

def create_tables():
        
    db_params = connection()
    cur = db_params.cursor()
    # Drop the view before dropping the table
    cur.execute("DROP VIEW IF EXISTS team_names_view")
    
    cur.execute("DROP TABLE IF EXISTS person")
    cur.execute("""CREATE TABLE person(
                ID SERIAL PRIMARY KEY,
                Name VARCHAR(255),
                Age INT,
                Team VARCHAR(255),
                Land VARCHAR(255),
                Position JSON
                )
                """)
    cur.execute("DROP TABLE IF EXISTS land")
    cur.execute("""
                CREATE TABLE IF NOT EXISTS land (
                LandID SERIAL PRIMARY KEY,
                Land VARCHAR(255) UNIQUE NOT NULL,
                FIFA_Rank INT,
                Points DECIMAL
                )"""
                )
    cur.execute("DROP TABLE IF EXISTS teams")
    cur.execute("""
                CREATE TABLE IF NOT EXISTS teams (
                TeamID SERIAL PRIMARY KEY,
                Team VARCHAR(255) UNIQUE NOT NULL,
                Manager VARCHAR(255),
                Stadium VARCHAR(255),
                Location VARCHAR(255),
                Founded VARCHAR(255),
                leagues VARCHAR(255)
                )"""
                )
    cur.execute("""
                CREATE VIEW team_names_view AS
                SELECT Team FROM teams;
                """
                )
    db_params.commit()
    db_params.close()

def insert_person(data):
    conn = None
    cur = None
    try:
        # Connect to PostgreSQL database
        conn = connection()
        cur = conn.cursor()
        
        # SQL query to insert data
        insert_query = """
        INSERT INTO person (Name, Age, Team, Land, Position) VALUES (%s, %s, %s, %s, %s)
        """
        
        # Execute SQL query for each scraped data item
        cur.execute(insert_query, data)
        
        # Commit the transaction
        conn.commit()
        print("Data inserted successfully.")
        # Close cursor and connection
        #cur.close()
        conn.close()

    except Exception as e:
        print(f"An error occurred: {e}")

def insert_land(data):
    conn = None
    cur = None
    try:
        # Connect to PostgreSQL database
        conn = connection()
        cur = conn.cursor()
        
        # SQL query to insert data
        insert_query = """
        INSERT INTO land (Land, FIFA_Rank, Points) VALUES (%s, %s, %s)
        """
        
        # Execute SQL query for each scraped data item
        cur.execute(insert_query, data)
        
        # Commit the transaction
        conn.commit()
        print("Data inserted successfully.")
        # Close cursor and connection
        #cur.close()
        conn.close()

    except Exception as e:
        print(f"An error occurred: {e}")

def insert_team(data):
    conn = None
    cur = None
    try:
        # Connect to PostgreSQL database
        conn = connection()
        cur = conn.cursor()
        
        # SQL query to insert data
        insert_query = """
        INSERT INTO teams (Team, Manager, Stadium, Location, Founded, leagues) VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        # Execute SQL query for each scraped data item
        cur.execute(insert_query, data)
        
        # Commit the transaction
        conn.commit()
        print("Data inserted successfully.")
        # Close cursor and connection
        #cur.close()
        conn.close()

    except Exception as e:
        print(f"An error occurred: {e}")

def check_team(team):
    conn = None
    cur = None
    try:
        # Connect to PostgreSQL database
        conn = connection()
        cur = conn.cursor()
        
        # SQL query to insert data
        insert_query = """
        SELECT EXISTS(SELECT 1 FROM team_names_view WHERE Team = %s)
        """
        
        # Execute SQL query for each scraped data item
        cur.execute(insert_query, (team, ))
        team_exists = cur.fetchone()[0]
        conn.close()
        return team_exists

    except Exception as e:
        print(f"An error occurred: {e}")



if __name__ == "__main__":
    create_tables()
