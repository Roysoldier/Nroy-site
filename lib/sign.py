import traceback
import hashlib
import time
import json


def signup(logger=None,mydb=None,payload=None,debug=False,bypass=False,verif=False,lock=None,path=None):
    try:
        if not verif:
            logger.log("Vérification des comptes désactivé","WARN")

        res,err = mydb.read_row("users",f"email = '{payload['email']}'")
        if len(res) != 0:
            if debug:
                logger.log("Email déja existant","DEBUG")
            return {"status":"nok","msg":'email already exists'}
        else:
            res,err = mydb.read_row("users",f"user = '{payload['pseudo']}'")
            if len(res) != 0:
                if debug:
                    logger.log("Utilisateur déja existant","DEBUG")
                return {"status":"nok","msg":'user already exists'}
            else:
                res,err = mydb.max_index("users","id")
                if len(res) != 0:
                    id = res[0][0] + 1
                    if bypass:
                        hashkey = payload['password']
                    else:
                        binarykey = bytes(payload['password'], "utf-8")
                        hashkey = hashlib.sha256(binarykey).hexdigest()
                    if verif:
                        with lock:
                            with open(path +  "account_verif.json","r") as f:
                                tmp_account = json.load(f)
                            payload['password'] = hashkey
                            payload['verif'] = False
                            tmp_account.append(payload)
                            with open(path +  "account_verif.json","w") as f:
                                f.write(json.dumps(tmp_account, indent=4))
                            return {"status":"ok","msg":'Account will be verified'}
                    else:
                        res,err = mydb.add_row("users",[("id",id),("user",payload["pseudo"]),("email",payload["email"]),("mdp",hashkey),("lastlog",0),("connected",0)])
                        res,err = mydb.add_row("userinfo",[("name",payload["pseudo"]),("email",payload["email"]),('bio',""),("img","circle-person.png")])
                        if res == 1 and not err:

                            logger.log(f"Compte créé : {payload['pseudo']}","INFO")
                            return {"status":"ok","msg":'Account created'}
                        else:
                            logger.log(f"Erreur de création du compte : {payload['pseudo']}","ERROR")
                            return {"status":"nok","msg":'failed to created account'}
                else:
                    logger.log("Erreur inconnue dans la fonction signup","ERROR")
                    return {"status":"nok","msg":'error'}
    except:
        logger.log("Erreur inconnue dans la fonction signup","ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
        return {"status":"nok","msg":'error'}


def signin(logger=None,mydb=None,email="", pwd="",debug=False):
    try:
        res,err = mydb.read_row("users",f"email = '{email}'")
        if not err and len(res) != 0:
            #comparaison des mdp
            binarykey = bytes(pwd, "utf-8")
            hashkey = hashlib.sha256(binarykey).hexdigest()
            if hashkey == res[0][3]:
                logger.log(f"Autentification validé pour : {email}","INFO")
                t = int(time.time())
                mydb.update_row("users",f"email = '{email}'",f"lastlog = {t}, connected = 1")
                return {"status":"ok","msg":'ok'},{'user': res[0][1], 'auth': True}
            else:
                if debug:
                    logger.log("Mot de passe incorect","DEBUG")
                return {"status":"nok","msg":'mdp incorrect'},{'user': "", 'auth': False}
        else:
            logger.log("Erreur inconnue dans la fonction signin","ERROR")
            return {"status":"nok","msg":'error'}, {'user': "", 'auth': False}
    except:
        logger.log("Erreur inconnue dans la fonction signin","ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG") 
        return {"status":"nok","msg":'error'}, {'user': "", 'auth': False}
    

def is_connected(logger=None,mydb=None,pseudo="",maxtime=86400,debug=False):
    try:
        res,err = mydb.read_row("users",f"user = '{pseudo}'")
        if not err and len(res) != 0:
            if res[0][5]:
                if (int(time.time())  - res[0][4]) < maxtime:
                    logger.log(f"{pseudo} est connecté","INFO")
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    except:
        logger.log("Erreur inconnue dans la fonction is_connected","ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG") 
        return False

def sign_out(logger=None,mydb=None,pseudo="",debug=False):
    try:
        res,err = mydb.read_row("users",f"user = '{pseudo}'")
        isConnect = is_connected(logger=logger,mydb=mydb,pseudo=pseudo,debug=debug)
        if isConnect:
            mydb.update_row("users",f"user = '{pseudo}'",f"lastlog = 0, connected = 0")

    except:
        logger.log("Erreur inconnue dans la fonction sign_out","ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG") 
