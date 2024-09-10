import psycopg2
from psycopg2 import sql

class conectorDatabase():
    def __init__(self) -> None:
        pass

    def conect_to_database(self, db_name):
        conn = psycopg2.connect(host="localhost", 
                                dbname=db_name,
                                user="newuser",
                                password="postgres",
                                port=5432)
        cur = conn.cursor()
        return cur, conn

class databaseModel(conectorDatabase):
    def __init__(self, db_name) -> None:
        super().__init__()
        self.database_name = db_name

    def create_database(self):
        cur, conn = self.conect_to_database("postgres")
        try:
            cur.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [self.database_name])
            exists = cur.fetchone()
            if not exists:
                cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(self.database_name)))
                print(f"Datenbank '{self.database_name}' databse create sucessfull.")
            else:
                print(f"Datenbank '{self.database_name}' database exist.")
        except Exception as e:
            print(f"Fail by create Database: {e}")
        finally:
            # close conection to database
            cur.close()
            conn.close()

    def create_table(self):
        cur, conn = self.conect_to_database("oaica2")
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
                    prompt VARCHAR(1000),
                    )
                    """)
            cur.execute("""CREATE TABLE IF NOT EXISTS USERKI-RoleChat(
                    ID SERIAL PRIMARY KEY,
                    ID_User INT,
                    ID_KI-Role INT,
                    FOREIGN KEY (ID_User) REFERENCES User(ID),
                    FOREIGN (ID_KI-Role) REFERENCES KI-Role(ID)
                    )
                    """)
            cur.execute("""CREATE TABLE IF NOT EXISTS USER_Message(
                    ID SERIAL PRIMARY KEY,
                    ID_User INT,
                    ID_USERKI-RoleChat,
                    Message VARCHAR(2000),
                    FOREIGN KEY (ID_User) REFERENCES User(ID),
                    FOREIGN KEY (ID_USERKI-RoleChat) REFERENCES USERKI-RoleChat(ID)
                    )
                    """)
            cur.execute("""CREATE TABLE IF NOT EXISTS KIROLE_Message(
                    ID SERIAL PRIMARY KEY,
                    ID_KI-RoleChat INT,
                    ID_USERKI-RoleChat,
                    Message VARCHAR(2000),
                    FOREIGN KEY (ID_KI-RoleChat) REFERENCES  KI-Role(ID),
                    FOREIGN KEY (ID_USERKI-RoleChat) REFERENCES USERKI-RoleChat(ID)
                    
                    )
                    """)
            conn.commit()
        except Exception as e:
            print(f"Exception: {e}")
        finally:
            cur.close()
            conn.close()

    def insert_to_Database(self, table_name, atributes, values):
        cur, conn = self.conect_to_database(self.database_name )
        insert_query = f"INSERT INTO {table_name} ({atributes[0]}"
        for atribute in atributes[1:]:
            insert_query = insert_query + ", " + atribute
        insert_query = f"{insert_query}) VALUES (" + "%s"
        insert_query = f"{insert_query}) VALUES (" + "%s" (", %s") * (len(values)-1) + ")"
        return_message = ""
        try:
            cur.execute(insert_query, values)
            conn.commit()
            return_message = "Successful"
        except Exception as e:
            print(f"Exception: {e}")
            return_message = "Fail"
        finally:
            cur.close()
            conn.close()
            return return_message
    
    def get_information(self, tables, table_with_atributes, search_statement=None, search_value= None,  key_couples=None, order_by=None, how_order= None):
        cur, conn = self.conect_to_database(self.database_name)
        select_query = f"SELECT {table_with_atributes[0]}"
        if len(table_with_atributes) > 1:
            for atribute in table_with_atributes[1]:
                select_query = select_query + f", {atribute}"
        select_query = select_query + f"FROM {tables[0]}"
        if tables > 1:
            x = 1
            for pk, fk in key_couples:
                select_query = select_query + f"LEFT JOIN {tables[0]} on {tables[x]}.{pk} = {tables[0]}.{fk} \n"
                x = x + 1
        if search_statement:
            select_query = select_query + f"WHERE {search_statement} =" + "%s"
        if order_by:
            select_query = select_query + f"ORDER BY {order_by} {how_order}"
        results = ""
        try:
            if search_value:
                cur.execute(select_query, search_value)
            else:
                cur.execute(select_query)
            results = cur.fetchall()
        except Exception as e:
            print("Fail:{e}")
            results = "something is wrong"
        finally:
            cur.close()
            conn.close()
            return results
        # not yet tested
