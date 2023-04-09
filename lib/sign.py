import traceback
import hashlib

def signup(logger=None,mydb=None,payload=None,debug=False):
    try:
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
                    binarykey = bytes(payload['password'], "utf-8")
                    hashkey = hashlib.sha256(binarykey).hexdigest()
                    res,err = mydb.add_row("users",[("id",id),("user",payload["pseudo"]),("email",payload["email"]),("mdp",hashkey)])
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


def signin(logger=None,mydb=None,payload=None,debug=False,session=None):
    try:
        res,err = mydb.read_row("users",f"email = '{payload['email']}'")
        if not err and len(res) != 0:
            #comparaison des mdp
            binarykey = bytes(payload['password'], "utf-8")
            hashkey = hashlib.sha256(binarykey).hexdigest()
            if hashkey == res[0][3]:
                session['logged_in'] = True
                logger.log(f"Autentification validé pour : {payload['email']}","INFO")
                return {"status":"ok","msg":'ok'},session
            else:
                session['logged_in'] = False
                if debug:
                    logger.log("Mot de passe incorect","DEBUG")
                return {"status":"nok","msg":'mdp incorrect'},session
        else:
            session['logged_in'] = False
            logger.log("Erreur inconnue dans la fonction signin","ERROR")
            return {"status":"nok","msg":'error'}, session
    except:
        logger.log("Erreur inconnue dans la fonction signin","ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG") 
        return {"status":"nok","msg":'error'}, session