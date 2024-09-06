import psycopg2
from psycopg2 import sql

def conect_to_database(db_name):
    conn = psycopg2.connect(host="localhost", 
                             dbname="db_name",
                             user="newuser",
                             password="postgres",
                             port=5432)
    cur = conn.cursor()
    return cur, conn

def create_database(dbname):
    cur, conn = conect_to_database("postgres")
    try:
        cur.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [dbname])
        exists = cur.fetchone()
        if not exists:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
            print(f"Datenbank '{dbname}' erfolgreich erstellt.")
        else:
            print(f"Datenbank '{dbname}' existiert bereits.")
    except Exception as e:
        print(f"Fehler beim Erstellen der Datenbank: {e}")
    finally:
        # Schließen des Cursors und der Verbindung
        cur.close()
        conn.close()

def create_table():
    cur, conn = conect_to_database("oaica2")
    try:
        cur.execute("""CREATE TABLE IF NOT EXISTS Articel(
                ID SERIAL PRIMARY KEY,
                Title VARCHAR(100),
                txt TEXT,
                )
                """)
        cur.execute("""CREATE TABLE IF NOT EXISTS User(
                ID SERIAL PRIMARY KEY
                )
                """)
        cur.execute("""CREATE TABLE IF NOT EXISTS KI-Role(
                ID SERIAL PRIMARY KEY,
                Name VARCHAR(50),
                prompt VARCHAR(1000)
                )
                """)
        cur.execute("""CREATE TABLE IF NOT EXISTS USERKI-RoleChat(
                ID SERIAL PRIMARY KEY,
                ID_User INT,
                ID_KI-Role INT,
                )
                """)
        cur.execute("""CREATE TABLE IF NOT EXISTS USER_Message(
                ID SERIAL PRIMARY KEY,
                ID_User INT,
                ID_USERKI-RoleChat,
                Message VARCHAR(2000)
                )
                """)
        cur.execute("""CREATE TABLE IF NOT EXISTS USER_Message(
                ID SERIAL PRIMARY KEY,
                ID_KI-RoleChat INT,
                ID_USERKI-RoleChat,
                Message VARCHAR(2000)
                )
                """)
        conn.commit()
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        cur.close()
        conn.close()

def insert_to_Database():
    pass
 
