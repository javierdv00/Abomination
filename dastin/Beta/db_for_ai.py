import psycopg2
from psycopg2 import sql
import traceback

""" 
Information:
The empty methods are still being filled in
Each class gets a constructor with a branch 
where either the super is executed or not. 
Reason the last class inherits from all of 
them, and the connector should only be 
inherited once and not x times. 

The hardcoded tables are still removed 
and packed into a Json. The start file 
gets this from and sends it to dbforai
hands over.
"""


class ConectorDatabase():
    def __init__(self) -> None:
        pass

    def conect_to_database(self, db_name):
        conn = psycopg2.connect(host="localhost", 
                                dbname=db_name,
                                user="postgres",
                                password="password",
                                port=5432)
        cur = conn.cursor()
        return cur, conn
   
class QueryDatabase(ConectorDatabase):
    def get_information(self, tables, table_with_atributes, search_statement=None, search_value= None,  key_couples=None, order_by=None, how_order= None):
        cur, conn = self.conect_to_database(self.database_name)
        select_query = f"SELECT {table_with_atributes[0]}"
        if len(table_with_atributes) > 1:
            for atribute in table_with_atributes[1]:
                select_query = select_query + f", {atribute}"
        select_query = select_query + f"FROM {tables[0]}"
        if len(tables) > 1:
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
            print(f"Exception: {e} \nTraceback:\n{traceback.format_exc()} \n ")
            results = "something is wrong"
        finally:
            cur.close()
            conn.close()
            return results
    
class DataDatabse(ConectorDatabase):
    def insert_to_Database(self, table_name, attributes, values):
        cur, conn = self.conect_to_database(self.database_name )
        # insert_query = f"INSERT INTO {table_name} ({atributes[0]}"
        # for atribute in atributes[1:]:
        #     insert_query = insert_query + ", " + atribute
        # #insert_query = f"{insert_query}) VALUES (" + "%s"
        # placeholders = ", ".join(["%s"] * len(values))
        # insert_query = f"{insert_query}) VALUES ({placeholders})"
        # return_message = ""
        insert_query = f"INSERT INTO {table_name} ({', '.join(attributes)}) VALUES ({', '.join(['%s'] * len(values))})"
        try:
            cur.execute(insert_query, values)
            conn.commit()
            return_message = "Successful"
        except Exception as e:
            print(f"Exception: {e} \nTraceback:\n{traceback.format_exc()} \n ")
            return_message = "Fail"
        finally:
            cur.close()
            conn.close()
            return return_message
    
    def delete_Data():
        pass
    
#psql -d user_ki -U newuser -h horst -p 5432

class ViewDatabase(ConectorDatabase):
    def create_view():
        pass

    def drop_view(self):
        pass
    
    def change_view(self):
        pass
    
    def list_view(self):
        pass
      
class BuilderDatabsae(ConectorDatabase):
    def __init__(self, db_name) -> None:
        super().__init__()
        self.database_name = db_name

    def create_database(self):
        cur, conn = self.conect_to_database("postgres")
        conn.autocommit = True
        try:
            cur.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [self.database_name])
            exists = cur.fetchone()
            if not exists:
                cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(self.database_name)))
        except Exception as e:
            print(f"Exception: {e} \nTraceback:\n{traceback.format_exc()} \n ")
        finally:
            # close conection to database
            conn.autocommit = False
            cur.close()
            conn.close()

    def create_table(self):
        cur, conn = self.conect_to_database(self.database_name)
        try:
            cur.execute("""CREATE TABLE IF NOT EXISTS Article(
                    ID SERIAL PRIMARY KEY,
                    Title VARCHAR(100),
                    txt TEXT
                    )
                    """)
            cur.execute("""CREATE TABLE IF NOT EXISTS User_(
                    ID SERIAL PRIMARY KEY,
                    name VARCHAR(20),
                    rank INT
                    )
                    """)
            cur.execute("""CREATE TABLE IF NOT EXISTS KI_Role(
                    ID SERIAL PRIMARY KEY,
                    Name VARCHAR(50),
                    prompt VARCHAR(1000)
                    )
                    """)
            cur.execute("""CREATE TABLE IF NOT EXISTS USERKI_RoleChat(
                    ID SERIAL PRIMARY KEY,
                    ID_User INT,
                    ID_KI_Role INT,
                    FOREIGN KEY (ID_User) REFERENCES User_(ID),
                    FOREIGN KEY (ID_KI_Role) REFERENCES KI_Role(ID)
                    )
                    """)
            cur.execute("""CREATE TABLE IF NOT EXISTS USER_Message(
                    ID SERIAL PRIMARY KEY,
                    ID_User INT,
                    ID_USERKI_RoleChat INT,
                    Message VARCHAR(2000),
                    date,
                    FOREIGN KEY (ID_User) REFERENCES User_(ID),
                    FOREIGN KEY (ID_USERKI_RoleChat) REFERENCES USERKI_RoleChat(ID)
                    )
                    """)
            cur.execute("""CREATE TABLE IF NOT EXISTS KIROLE_Message(
                    ID SERIAL PRIMARY KEY,
                    ID_KI_RoleChat INT,
                    ID_USERKI_RoleChat INT,
                    Message VARCHAR(2000),
                    date,
                    FOREIGN KEY (ID_KI_RoleChat) REFERENCES  KI_Role(ID),
                    FOREIGN KEY (ID_USERKI_RoleChat) REFERENCES USERKI_RoleChat(ID)
                    )
                    """)
            conn.commit()
        except Exception as e:
            print(f"Exception: {e} \nTraceback:\n{traceback.format_exc()} \n ")
        finally:
            cur.close()
            conn.close()
        
# 
class ManagerDatabase(BuilderDatabsae, ViewDatabase, DataDatabse, QueryDatabase, ConectorDatabase):
    def __init__(self, db_name) -> None:
        super().__init__(db_name)
