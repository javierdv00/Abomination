
import os
from pyfiglet import Figlet
import time
from ai_action_abomination import Oaica2
import json
from db_for_ai import databaseModel
from stringcolor import *

class abominationTerminalView():
    def __init__(self) -> None:
        self.obj_ai = Oaica2()
        self.obj_dat = databaseModel("userki43")
    
    def show_table(self):
        print("def show_table():")
        cursor, conn =  self.obj_ai.conect_to_database("userki43")
        cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
        tables = cursor.fetchall()
        index = 0
        print("choice your table")
        for table in tables:
            print(f"{index}: {table[0]}")
            index = index + 1
        table = int(input())
        print(tables[table][0])
        obj_1 = databaseModel("userki43")
        output = obj_1.get_information([tables[table][0]], ["*"])
        outpu2 = [row[0] for row in output]
        for idx, row in enumerate(output, start=1):
            print(f"\nIndex: {idx}")
            for attr, value in zip(outpu2, row):
                print(f"{attr}: {value}")
            input("Press Enter to continue...")

        #output = self.obj_ai.get_information(tables[table][0], ["*"])
        print(output)
        input("press enter")

    # def get_information(self, tables, table_with_atributes, search_statement=None, search_value= None,  key_couples=None, order_by=None, how_order= None):    
    def create_article(self):
        result = self.obj_ai.get_text_response(input(
            """What topic would you like an article about? 
            Feel free to describe exactly what you want 
            to include and how many words it should be, minimum and maximum.\n"""), decision_maker=0)
        print(f"raw: {result} \n")
        # result = result.strip()
        # result = result.replace('\n', '\\n').replace('\r', '\\r')
        # result = result.replace("'", '"')
        data = json.loads(result)
        print(f"""{data["Title"]}


        {data["Body"]} 

        """

        )
        self.obj_dat.insert_to_Database("Article", ["Title", "txt"], [data["Title"],data["Body"]])
        #self.obj_ai.insert_to_Database()
        #def insert_to_Database(self, table_name, attributes, values):

    def chat_with(self):
        cursor, conn =  self.obj_ai.conect_to_database("userki43")
        cursor.execute("""
                SELECT KI_Role.ID, KI_Role.Name, KI_Role.prompt
                FROM KI_Role
            """)
        Atributes = cursor.fetchall()
        index = 1
        print("Choice one of the Chatpartner")
        for Atribute in Atributes[1:-1]:
            print(f"{index}: {Atribute[1]}")
            index = index + 1
        result = int(input())
        mesage = []
        print("Hello welcome in the Chatroom. Write your first Mesage")
        mesage.append({"role": "system", "content": Atributes[result][2]})
        while True:
            user_mesage = input(cs("USER:", "green"))
            mesage.append({"role": "user", "content": user_mesage})
            ki_answer = self.obj_ai.get_chating(mesage)
            print(cs(ki_answer, "red"))
            mesage.append({"role": "assistant", "content": ki_answer})
            if (input(cs("write 0 and press enter for break", "blue"))) == "0":
                break


    def intro(self):
        def slow_print(text, delay=0.05):
            for char in text:
                print(char, end='', flush=True)
                time.sleep(delay)
            print()  
        fig = Figlet()
        project_banner = fig.renderText('Abomination')
        author_banner = fig.renderText('Authors:')
        quote_banner = fig.renderText('Quote of the Day')
        authors = "Javierdv, Buggican, Lyssa1101, StudentDastin, Sepehrsprr"

        slow_print(project_banner, delay=0.02)
        time.sleep(1) 
        slow_print(author_banner, delay=0.02)
        slow_print(authors, delay=0.02)
        time.sleep(1)  
        slow_print(quote_banner, delay=0.02)

    def menue(self):
        main_menue = """
            shose one of this with his number
            1: show_table
            2: create Arctile
            3: chat with
            x: ending the program
        """
        result = { "main_menue": main_menue }
        return result


    def main(self):
        self.intro()
        ending_mesage_ur = "press Enter for To continue "
        wrong_message = "Some thing is wronge"
        ending_mesage = ending_mesage_ur
        input(ending_mesage)
        os.system("clear")
        while True:
            choice = int(input(self.menue()["main_menue"]))
            if choice == 1:
                self.show_table()
            elif choice == 2:
                self.create_article()
            elif choice == 3:
                self.chat_with()
            elif (choice == "x") or (choice ==  "X"):
                break
            else:
                ending_mesage = wrong_message + ending_mesage_ur
            input(ending_mesage)
            os.system("clear")




obj = abominationTerminalView()
obj.main()
    
