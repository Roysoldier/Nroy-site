from flask import Flask, jsonify, request, render_template, session, make_response
from os import urandom,path,remove
from lib import sqlitewrap, myLogger,sign
import traceback
import re
import datetime
from werkzeug.utils import secure_filename
from random import randint
import sys
import yaml
import yamlordereddictloader
from apscheduler.schedulers.background import BackgroundScheduler
import threading
import json
import hashlib


ROOT_PATH = path.dirname(path.abspath(__file__)).strip() + "/"

CONFIG = {}

LOCK = threading.Lock()

lien =  r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[\w\-\./?#=&]+'

mydb = sqlitewrap.SqliteWrap(ROOT_PATH + "db/auth.db")

logger = myLogger.MyLogger(path=ROOT_PATH + "logs/messages.log")

debug = False

local = False
USERS = {}
mydb.update_row("users",f"user = 'Noan'",f"status = 'admin'")

###############################################
# Appel de fonction
###############################################

# Définition du nom de mon application Flask
APP_FLASK = Flask(__name__)

APP_FLASK.permanent_session_lifetime = datetime.timedelta(days=1)

# Rechargement des pages WEB automatiquement dès qu'on les change
APP_FLASK.config["TEMPLATES_AUTO_RELOAD"] = True
APP_FLASK.config["SESSION_COOKIE_HTTPONLY"] = False
APP_FLASK.config["REMEMBER_COOKIE_HTTPONLY"] = True
APP_FLASK.config["SESSION_COOKIE_SAMESITE"] = "Strict"
APP_FLASK.config['UPLOAD_FOLDER'] = "./static/data"

# Génération d'un secret de connexion utile à Falsk
APP_FLASK.secret_key = urandom(12)

# Gestion de l'appel à la page base.html
@APP_FLASK.route('/', methods=['GET'])
@APP_FLASK.route('/index.html', methods=['GET'])
def index():
    try:
        listproj = recup_project(3)
        #print(listproj)       
        cook = recup_cook()

        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=cook,debug=debug)
        ires,ierr = mydb.read_row("userinfo",f"name = '{cook}'")
        res,err = mydb.read_row("users",f"user = '{cook}'")
        #print("login : ",isConnect)
        if isConnect:
            render = {"login":isConnect,"pseudo":cook,"img": f"./static/data/{ires[0][3]}","proj":listproj,"status":res[0][7]}
        else:
            render = {"login":isConnect,"proj":listproj}
        #print("render : ",render)
        if debug:
            logger.log("Requête index.html", "DEBUG")
        #renvoie du code source signin.html au navigateur web après traitement
        return render_template('index.html', render=render)
    except:
        logger.log("Erreur inconnue dans index.html", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")

@APP_FLASK.route('/perso.html', methods=['GET'])
def perso():
    try:
        cook = recup_cook()
        #print("cook :",cook)
        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=cook,debug=debug)
        #print("login : ",isConnect)
        ires,ierr = mydb.read_row("userinfo",f"name = '{cook}'")
        res,err = mydb.read_row("users",f"user = '{cook}'")
        if isConnect:
           render = {"login":isConnect,"pseudo":cook,"img": f"./static/data/{ires[0][3]}","status":res[0][7]}
        else:
            render = {"login":isConnect}
        #print("render : ",render)
        if debug:
            logger.log("Requête perso.html", "DEBUG")
        #renvoie du code source perso.html au navigateur web après traitement
        return render_template('perso.html',render=render)
    except:
        logger.log("Erreur inconnue dans perso.html", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")

@APP_FLASK.route('/newproject.html', methods=['GET'])
def new_project():
    try:
        cook = recup_cook()

        #print("cook :",cook)
        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=cook,debug=debug)
        #print("login : ",isConnect)
        ires,ierr = mydb.read_row("userinfo",f"name = '{cook}'")
        res,err = mydb.read_row("users",f"user = '{cook}'")
        if isConnect:
           render = {"login":isConnect,"pseudo":cook,"img": f"./static/data/{ires[0][3]}","status":res[0][7]}
        else:
            render = {"login":isConnect}
        #print("render : ",render)
        if debug:
            logger.log("Requête newproject.html", "DEBUG")
        if res[0][7] != 'admin':
            return index()
        else:
            #renvoie du code source perso.html au navigateur web après traitement
            return render_template('newproject.html',render=render)
    except:
        logger.log("Erreur inconnue dans newproject.html", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")

@APP_FLASK.route('/signin.html', methods=['GET'])
def signin():
    try:
        if debug:
            logger.log("Requête signin.html", "DEBUG")
        #renvoie du code source signin.html au navigateur web après traitement
        return render_template('signin.html')
    except:
        logger.log("Erreur inconnue dans signin.html", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")

@APP_FLASK.route('/signup.html', methods=['GET'])
def signup():
    try:
        if debug:
            logger.log("Requête signup.html", "DEBUG")
        #renvoie du code source signup.html au navigateur web après traitement
        return render_template('signup.html')
    except:
        logger.log("Erreur inconnue dans signup.html", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")

@APP_FLASK.route('/projet.html', methods=['GET'])
def projet():
    try:
        cook = recup_cook()
        #print("cook :",cook)
        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=cook,debug=debug)
        projres ,preojerr = mydb.read_rows('project',["id","owner","name","title","text","date","img","link","like"])

        #print("login : ",isConnect)
        ires,ierr = mydb.read_row("userinfo",f"name = '{cook}'")
        res,err = mydb.read_row("users",f"user = '{cook}'")
        if isConnect:
           render = {"login":isConnect,"pseudo":cook,"img": f"./static/data/{ires[0][3]}","projet":projres,"status":res[0][7]}
        else:
            render = {"login":isConnect,"projet":projres}
        #print("render : ",render)
        if debug:
            logger.log("Requête projet.html", "DEBUG")
        #renvoie du code source projet.html au navigateur web après traitement
        return render_template('projet.html', render=render)
    except:
        logger.log("Erreur inconnue dans projet.html", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")

@APP_FLASK.route('/myproj.html', methods=['GET'])
def myproj():
    try:
        cook = recup_cook()

        #print("cook :",cook)
        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=cook,debug=debug)
        res,err = mydb.read_row("users",f"user = '{cook}'")
        ires,ierr = mydb.read_row("userinfo",f"name = '{cook}'")
        projres ,preojerr = mydb.read_rows('project',["id","owner","name","title","text","date","img","link","like"])
        fproj = []
        for i,v in enumerate(projres):
            #print(v)
            #print(v[1],i)
            if v[1] == cook:
                fproj.append(v)
        #print(projres)
        #print("login : ",isConnect)
        render = {"login":isConnect,"pseudo":cook,"img": f"./static/data/{ires[0][3]}","projet":fproj,"status":res[0][7]}
        #print("render : ",render)
        if debug:
            logger.log("Requête myproj.html", "DEBUG")
        #renvoie du code source projet.html au navigateur web après traitement
        if isConnect:
           return render_template('myproj.html', render=render)
        else:
            return index()
        
    except:
        logger.log("Erreur inconnue dans myproj.html", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")

@APP_FLASK.route('/profil.html', methods=['GET'])
def profil():
    try:
        cook = recup_cook()

        #print("cook :",cook)
        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=cook,debug=debug)
        #print("login : ",isConnect)
        ires,ierr = mydb.read_row("userinfo",f"name = '{cook}'")
        render = {"login":isConnect,"pseudo":cook,"email":ires[0][2],"bio": ires[0][1].replace('"',"'"),"img": f"./static/data/{ires[0][3]}"}
        #print("render : ",render)
        if debug:
            logger.log("Requête profil.html", "DEBUG")
        #renvoie du code source profil.html au navigateur web après traitement
        if isConnect:
           return render_template('profil.html', render=render)
        else:
            return index()
    except:
        logger.log("Erreur inconnue dans profil.html", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")

@APP_FLASK.route('/editprofil.html', methods=['GET'])
def editprofil():
    try:
        cook = recup_cook()

        #print("cook :",cook)
        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=cook,debug=debug)
        #print("login : ",isConnect)
        ires,ierr = mydb.read_row("userinfo",f"name = '{cook}'")
        render = {"login":isConnect,"pseudo":cook,"email":ires[0][2],"bio": ires[0][2].replace('"',"'"),"img": f"./static/data/{ires[0][3]}"}
        #print("render : ",render)
        if debug:
            logger.log("Requête editprofil.html", "DEBUG")
        #renvoie du code source editprofil.html au navigateur web après traitement
        if isConnect:
           return render_template('editprofil.html', render=render)
        else:
            return index()
    except:
        logger.log("Erreur inconnue dans editprofil.html", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")

@APP_FLASK.route('/otherprofile.html', methods=['GET'])
def otherprofile():
    try:
        cook = recup_cook()

        #print('ici')
        ires,ierr = mydb.read_row("userinfo",f"name = '{cook}'")
        oires,oierr = mydb.read_row("userinfo",f"name = '{nameProfile}'")
        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=cook,debug=debug)
        if debug:
            logger.log("Requête otherprofile.html", "DEBUG")
        if isConnect:
           render = {"login":isConnect,"pseudo":cook,"img": f"./static/data/{ires[0][3]}","otherimg": f"./static/data/{oires[0][3]}","otherbio":oires[0][2],"othername":oires[0][0],"otheremail":oires[0][1]}
        else:
            render = {"login":isConnect,"otherimg": f"./static/data/{oires[0][3]}","otherbio":oires[0][2],"othername":oires[0][0],"otheremail":oires[0][1]}

        return render_template('otherprofile.html',render=render)

    except:
        logger.log("Erreur inconnue dans otherprofile.html", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")

@APP_FLASK.route('/projetpres.html', methods=['GET'])

@APP_FLASK.route('/projetpres.html', methods=['GET'])
def projetpres(nameProject):
    try:
        cook = recup_cook()

        #print("cook :",cook)
        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=cook,debug=debug)
        recup_pp(nameProject)
        lres,lerr = mydb.read_row("like",f"user = '{cook}'")
        cres, cerr = mydb.read_row("commentaire",f"project = '{nameProject}'")
        commentaire = []
        responce = []
        for i in cres:
            if i[5] == 0:
                commentaire.append(i)
            else:
                responce.append(i)
        liker = False
        for i in lres:
            if i[1] == cook and i[2] == nameProject and i[3]:
                liker = True

        #print("login : ",isConnect)
        pres,perr = mydb.read_row("project",f"name = '{nameProject}'")
        ires,ierr = mydb.read_row("userinfo",f"name = '{cook}'")
        if isConnect:
           render = {"login":isConnect,"pseudo":cook,"email":ires[0][2],"bio": ires[0][1].replace('"',"'"),"img": f"./static/data/{ires[0][3]}","project":pres[0],"like":liker,"nbrlike":pres[0][8],"commentaire":commentaire,"responce":responce}
        else:
            render = {"login":isConnect,"project":pres[0],"like":False,"nbrlike":pres[0][8],"commentaire":commentaire,"responce":responce}
        #print("render : ",render)
        if debug:
            logger.log("Requête projetpres.html", "DEBUG")
        #renvoie du code source projetpres.html au navigateur web après traitement
        return render_template('projetpres.html', render=render)
    except:
        logger.log("Erreur inconnue dans projetpres.html", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")

@APP_FLASK.route('/chearchfile', methods = ['POST'])
def chearchfile():
    try:
        recup_value = request.form['recup_value']
        #print(recup_value)
        logger.log("Fichier chearchfile", "INFO")
    except Exception as e:
        logger.log(f"Erreur inconnue dans chearchfile: {e}", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()), "DEBUG")
    return projetpres(recup_value)



###############################################
# API
###############################################



@APP_FLASK.route('/api/contact', methods=['POST'])
def api_contact():
    payload = request.json

    return jsonify({'status': "ok","data":{}})


@APP_FLASK.route('/api/like', methods=['POST'])
def api_like():
    try:
        if debug:
            logger.log("Requête api_like", "DEBUG")
        cook = recup_cook()

        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=cook,debug=debug)
        liker = False
        if isConnect:
            payload = request.json
            res,err = mydb.read_row("like",f"user = '{cook}'")
            pres,perr = mydb.read_row("project", f"name = '{payload['name']}'")
            nbrLike = pres[0][8]
            if debug:
                logger.log("Utilisateur connecter pour liker", "DEBUG")
            for i in res:
                #print(i[2])
                if i[1] == cook and i[2] == payload['name'] and i[3]:
                    #print("déja liker")
                    res,err = mydb.update_row("like",f"id = {i[0]}",f"status = 0")
                    res,err = mydb.update_row("project",f"name = '{payload['name']}'",f"like = {nbrLike - 1}")
                    liker = True
                elif i[1] == cook and i[2] == payload['name'] and not i[3]:
                    #print("remise a 1")
                    res,err = mydb.update_row("like",f"id = {i[0]}",f"status = 1")
                    res,err = mydb.update_row("project",f"name = '{payload['name']}'",f"like = {nbrLike + 1}")
                    liker = True
            if not liker:
                maxid,err= mydb.max_index('project',"id")
                
                res,err = mydb.add_row("like",[("id",maxid[0][0] + 1),("user", cook),("project", payload['name']),("status",1)])

                res,err = mydb.update_row("project",f"name = '{payload['name']}'",f"like = {nbrLike + 1}")
               
            return jsonify({"status":"ok","msg":'réussite'})
        else:
            logger.log("Utilisateur non connecter", "ERROR")
            return jsonify({"status":"nok","msg":'error'})
    except:
        logger.log("Erreur inconnue dans api_like", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
        return jsonify({"status":"nok","msg":'error'})

@APP_FLASK.route('/api/signup', methods=['POST'])
def api_signup():
    try:
        if debug:
            logger.log("Requête api_signup", "DEBUG")
            result = sign.signup(logger=logger,mydb=mydb,payload=request.json,debug=debug,bypass=False,verif=CONFIG['scheduler']['enable'],lock=LOCK,path=ROOT_PATH)
        return jsonify(result)
    except:
        logger.log("Erreur inconnue dans api_signup", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
        return jsonify({"status":"nok","msg":'error'})
    

@APP_FLASK.route('/api/checkprofile', methods=['POST'])
def api_checkprofile():
    try:
        
        payload =request.json
        res,err = mydb.read_row("userinfo",f"name = '{payload['name']}'")
        global nameProfile
        nameProfile = payload['name']
        if debug:
            logger.log("Requête checkprofile", "DEBUG")

        return jsonify({"status":"ok","msg":'ok'})
    except:
        logger.log("Erreur inconnue dans checkprofile", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
        return jsonify({"status":"nok","msg":'error'})
    

@APP_FLASK.route('/api/signin', methods=['POST'])
def api_signin():
    try:
       
        if debug:
            logger.log("Requête api_signin", "DEBUG")
        
        result,user = sign.signin(logger=logger,mydb=mydb,email=request.json['email'],pwd=request.json['password'],debug=debug)
        if user['auth']:
            binarykey = bytes(user['user'] + f"nroydevencryptagecookie{randint(1,1000)}", "utf-8")
            hashcook = hashlib.sha256(binarykey).hexdigest()
            res,err = mydb.update_row("users",f"user = '{user['user']}'",f"hashcook = '{hashcook}'")
            res, err = mydb.read_rows("users", ["user","hashcook"])

            resp = make_response(jsonify (result))  
            if not local:
                resp.set_cookie('USER_ID',hashcook,path="/",domain="nroydev.fr", httponly=True, secure=True)  
            else:
                resp.set_cookie('USER_ID',hashcook,path="/", httponly=True, secure=True)  
            
        return resp
    except:
        logger.log("Erreur inconnue dans api_signin", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
        return jsonify({"status":"nok","msg":'error'})
    
@APP_FLASK.route('/api/comment', methods=['POST'])
def api_comment():
    try:

        cook = recup_cook()

        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=cook,debug=debug)
        if isConnect:
            payload = request.json
            maxid,err= mydb.max_index('commentaire',"id")
            res,err = mydb.add_row("commentaire",[("id",maxid[0][0] + 1),("user",cook),("project",payload['projet']),("content",payload['comment']),("img","none"),("rep",payload['status'])])
            return jsonify({"status":"ok","msg":'opérationel'})
        else:
             return jsonify({"status":"nok","msg":'Merci de vous connecter'})  
    except:
        logger.log("Erreur inconnue dans api_commment", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
        return jsonify({"status":"nok","msg":'error'})
    
@APP_FLASK.route('/api/deleteMessage', methods=['POST'])
def api_delete_message():
    try:
        cook = recup_cook()

        payload = request.json
        res,err = mydb.delete_row('commentaire',('id',payload['id']))
        res,err = mydb.delete_row('commentaire',('status',payload['id']))
        
        
        return jsonify({"status":"ok","msg":'opérationel'})
    except:
        logger.log("Erreur inconnue dans  api_delete_message", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
        return jsonify({"status":"nok","msg":'error'})

@APP_FLASK.route('/api/bio', methods=['POST'])
def api_bio():
    try:
        cook = recup_cook()

        #print("cook :",cook)
        payload = request.json
        res,err = mydb.update_row("userinfo",f"name = '{cook}'",f"bio = '{payload['bio']}'")
        
        return jsonify({"status":"ok","data":{'bio':payload['bio']}})
    except:
        logger.log("Erreur inconnue dans api_bio", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
        return jsonify({"status":"nok","msg":'error'})
    
@APP_FLASK.route('/uploader', methods = ['POST'])
def upload_file():
    try:
 
        cook = recup_cook()

        res,err = mydb.read_row("userinfo",f"name = '{cook}'")

        f = request.files['file']
        if f:
            #print(f)
            if res[0][3] != "circle-person.png":
                remove(f"./static/data/{res[0][3]}")
            f.save(path.join(APP_FLASK.config['UPLOAD_FOLDER'],f"{cook}_{f.filename}"))

            res,err = mydb.update_row("userinfo",f"name = '{cook}'",f"img = '{cook}_{f.filename}'")
        logger.log("Fichier uploader", "INFO")
    except:
        logger.log("Erreur inconnue dans upload_file", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
    return editprofil()

@APP_FLASK.route('/uploaderform', methods = ['POST'])
def upload_file_proj():
    try:
        #print("enter")
        cook = recup_cook()

        res,err = mydb.read_row("users",f"user = '{cook}'")
        res,err = mydb.read_row("project",f"owner = '{cook}'")
        res,err = mydb.max_index()
        name = request.form['name'].replace("'","£").replace("'","¤")
        
        title = request.form['titleform'].replace('"',"£").replace("'","¤")

        text = request.form['textform'].replace('"',"£").replace("'","¤")
        link = request.form['link']

        f = request.files['file']
        if f and len(name) > 4 and len(name) < 30 and len(title) > 4 and len(title) < 60 and len(text) > 4 and len(text) < 10000 and re.match(lien,link):
            print("foo")
            f.save(path.join(APP_FLASK.config['UPLOAD_FOLDER'],f"Project_{cook}_{f.filename}"))
            res,err = mydb.max_index('project',"id")
            res,err = mydb.add_row("project",[("id",res[0][0] + 1),("owner",cook),("name",name),("title",title),("text",text),("date",str(datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S"))),("img",f"Project_{cook}_{f.filename}"),("link",link),("like",0)])
        

        # res,err = mydb.update_row("users",f"user = '{cook}'",f"img = '{cook}_{f.filename}'")
        logger.log("Fichier uploader", "INFO")
    except:
        logger.log("Erreur inconnue dans upload_file", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
    return projet()


@APP_FLASK.route('/api/signout', methods = ['POST'])
def api_signout():
    try:
        cook = recup_cook()

        payload = request.json
        sign.sign_out(logger=logger,mydb=mydb,pseudo=cook,debug=debug)
        logger.log(payload["message"],"INFO")
        return jsonify({"status":"ok","msg":'cool'})
    except:
        logger.log("Erreur inconnue dans api/signout", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
        return jsonify({"status":"nok","msg":'error'})

###############################################
# Fonctions
###############################################
def check_account():
    try:
        logger.log("Check périodique", "INFO")
        with LOCK:
            with open(ROOT_PATH +  "account_verif.json","r") as f:
                tmp_account = json.load(f)
            to_remove = []
            for i,v in enumerate(tmp_account):
                if v['verif']:
                    logger.log(f"Création du compte : {v['pseudo']}, après validation", "INFO")
                    result = sign.signup(logger=logger,mydb=mydb,payload=v,debug=debug,bypass=True,verif=False,lock=LOCK,path=ROOT_PATH)
                    to_remove.append(i)
            to_remove.sort(reverse=True)
            for i in to_remove:
                del tmp_account[i]
            with open(ROOT_PATH +  "account_verif.json","w") as f:
                f.write(json.dumps(tmp_account, indent=4))

    except:
        logger.log("Erreur inconnue dans check_account", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")

def recup_project(nbrproj):

    try:
        projres ,preojerr = mydb.read_rows('project',["id","owner","name","title","text","date","img","link","like"])
        listproj = []
        if len(projres) < nbrproj:
            nbrproj = len(projres)
        while len(listproj) < nbrproj:
            nbr = randint(0,len(projres) - 1)
            if  projres[nbr] not in listproj:
                listproj.append(projres[nbr])
        for v in range(len(listproj)):
            listproj.append([listproj[0][2],listproj[0][6],listproj[0][1],listproj[0][8]])
            listproj.pop(0)
        return listproj

    except:
        logger.log("Erreur inconnue dans la fonction recup_projet", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG") 
def recup_pp(proj):
    cres, cerr = mydb.read_row("commentaire",f"project = '{proj}'")
    for i in cres:
      res,err = mydb.read_row("userinfo",f"name = '{i[1]}'")
      res,err = mydb.update_row("commentaire",f"user = '{i[1]}'",f"img = './static/data/{res[0][3]}'")  
    cres, cerr = mydb.read_row("commentaire",f"project = '{proj}'")

def recup_cook():
    cook = request.cookies.get('USER_ID',"")
    if cook and mydb.read_row("users",f"hashcook = '{cook}'") != []:
        cook = mydb.read_row("users",f"hashcook = '{cook}'")[0][0][1]
    return cook
   

###############################################
# Main 
##############################################0
if __name__ == '__main__':
    logger.log("Lancement de l'application ! ", "INFO")
    logger.log("Ouverture du fichier de configuration", "INFO")
    try:
        with open(ROOT_PATH + "config.yaml", "r") as f:
            CONFIG = yaml.load(f, Loader=yamlordereddictloader.Loader)
    except IOError:
        logger.log("Erreur dans le fichier de config", "ERROR")
        sys.exit()
    
    debug = CONFIG.get('debug',False)
    local = CONFIG.get('local',False)
    logger.log("Création de la base de donnée", "INFO")
    mydb.create_table("users",[("id","INTEGER"),("user","TEXT"),("email","TEXT"),("mdp","TEXT"),("lastlog","INTEGER"),("connected","INTEGER"),("hashcook","TEXT"),("status","TEXT")])
    mydb.create_table("userinfo",[("name","TEXT"),("email","TEXT"),("bio","TEXT"),("img","BLOB")])
    mydb.create_table("project",[("id","INTEGER"),("owner","TEXT"),("name","TEXT"),("title","TEXT"),("text","TEXT"),("date","TEXT"),("img","BLOB"),("link","TEXT"),("like","INTEGER"),("comment","INTEGER")])
    mydb.create_table("like",[("id","INTEGER"),("user","TEXT"),("project","TEXT"),("status","INTEGER")])
    mydb.create_table("commentaire",[("id","INTEGER"),("user","TEXT"),("project","TEXT"),("content","TEXT"),('img',"TEXT"),('rep',"INTEGER")])
    if CONFIG['scheduler']['enable']:
        logger.log("Démarrage du scheduler", "INFO")
        scheduler = BackgroundScheduler()
        job = scheduler.add_job(check_account, 'interval', minutes=CONFIG['scheduler']['interval'])
        scheduler.start()
    logger.log("Démarrage du serveur flask", "INFO")
    APP_FLASK.run(ssl_context=(ROOT_PATH + 'ssl/cert.cer',ROOT_PATH + 'ssl/key.key'),host = CONFIG['network']['ip'], port = CONFIG['network']['port'])
    #APP_FLASK.run(host = CONFIG['network']['ip'], port = CONFIG['network']['port'])
