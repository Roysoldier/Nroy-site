import sqlite3
#création de la class
class SqliteWrap:
    
    # initialization de la class prenant en comptr le nom de la base afin de la crée
    def __init__(self,nameDb=""):
        self.conn = sqlite3.connect(nameDb,check_same_thread=False)
        self.cursor = self.conn.cursor()

    # création d'une fonction permettant de crée une table dans la liste prenant en agrument le nom de la table ainsi qu'une liste de tuple avec le nom et le type de donnée ex : [("id","INTEGER"),("name","TEXT")] 
    def create_table(self, tableName="", listFields = []):
        try:
            myCmd = f"CREATE TABLE {tableName}("
            for i in listFields:
                myCmd += f"{i[0]} {i[1]},"

            myCmd = myCmd[:-1] + ")"
            self.cursor.execute(myCmd)
            self.conn.commit()
            return 1,None
        except Exception as e:
            return 0,e

    # création d'une fonction add_row qui permet  d'ajouter des élément dans une table et qui prend en integration le nom de la table et une liste de tuple avec le nom et l'integration a ajouter 
    def add_row(self,tableName="",listValue=[]):
        try:
            myCmd = f"INSERT INTO {tableName}("
            myValues = " VALUES ("
            for i in listValue:
                myCmd += f"'{i[0]}',"
                if type(i[1]) == str:
                    myValues += f"'{i[1]}',"
                else:
                    myValues += f"{i[1]},"

            myCmd = myCmd[:-1] + ")" + myValues[:-1] + ")"
            self.cursor.execute(myCmd)
            self.conn.commit()
            return 1,None
        except Exception as e:
            return 0,e
    
    # une fonction read_row qui va permettre de "lire" une table dans la base de donnée en lui donnant une liste de tout les champs que l'on veux observer !
    def read_rows(self,tableName="", listFields=[]):
        try:
            myCmd = f"SELECT "
            for i in listFields:
                myCmd += i + ","

            myCmd = myCmd[:-1] + f" FROM {tableName}" 
            return self.cursor.execute(myCmd).fetchall(),None
        except Exception as e:
            return [],e
    
    # une fonction qui va récuperer le max d'un row d'une table INTEGER en ne prenant en compte que le champ et le nom de la table   
    def max_index(self,tableName="",field=""):
        try:
            myCmd = f"SELECT MAX({field}) FROM {tableName}"
            result =  self.cursor.execute(myCmd).fetchall()
            if result[0][0] == None:
                return [(0,)], None
            return result,None
        except Exception as e:
            return [],e
    
    # création d'une fonction read row qui va lire 1 seule condtion en prennant en compte le nom de la table et 1 condition
    def read_row(self,tableName="", condition=""):
        try:
            myCmd = f"SELECT * FROM {tableName} WHERE {condition}"
            result = self.cursor.execute(myCmd).fetchall()
            if len(result) == 0:
                return [], None
            if result[0][0] == None:
                return [], None
            return result,None
        except Exception as e:
            print("read :", e)
            return [],e
    
    def update_row(self,tableName="",condition="",change=""):
        try:
            myCmd = f"UPDATE {tableName} SET {change} WHERE {condition}"
            self.cursor.execute(myCmd)
            self.conn.commit()
            return 1,None
        except Exception as e:
            print("Update : ",e)
            return 0,e


    # création d'une fonction pour reser la table en ne prenant en compte que le nom de la table
    def reset_table(self,tableName=""):
        try:
            self.cursor.execute(f"DELETE FROM {tableName}")
            self.conn.commit()
            return 1,None
        except Exception as e:
            return 0,e

    # création d'une fonction delete_row pour suprimer une condition dans une table en prenant en compte le nom de la table et un tuple avec les conditions concerner
    def delete_row(self,tableName="",condition=()):
        try:
            if type(condition[1]) == str:
                myCmd = f"DELETE FROM {tableName} WHERE {condition[0]} = '{condition[1]}'"
            else:
                myCmd = f"DELETE FROM {tableName} WHERE {condition[0]} = {condition[1]}"
            self.cursor.execute(myCmd)
            self.conn.commit()
            return 1,None
        except Exception as e:
            return 0,e
    # création d'une fonction qui va fermer la base de donnée
    def close_db(self):
        try:
            self.conn.commit()
            self.conn.close()
            return 1,None
        except Exception as e:
            return 0,e
       