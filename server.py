from flask import Flask, jsonify, request, render_template, session, make_response
from os import urandom,path
import smtplib,ssl
from lib import sqlitewrap, myLogger,sign
import traceback
import datetime

ROOT_PATH = path.dirname(path.abspath(__file__)).strip() + "/"

mydb = sqlitewrap.SqliteWrap(ROOT_PATH + "db/auth.db")

logger = myLogger.MyLogger(path=ROOT_PATH + "logs/messages.log")

debug = True

USERS = {}

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

# Génération d'un secret de connexion utile à Falsk
APP_FLASK.secret_key = urandom(12)

# Gestion de l'appel à la page base.html
@APP_FLASK.route('/', methods=['GET'])
@APP_FLASK.route('/index.html', methods=['GET'])
def index():
    try:
        cook = request.cookies.get('USER_ID',"")
        #print("cook :",cook)
        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=cook,debug=debug)
        #print("login : ",isConnect)
        render = {"login":isConnect,"pseudo":cook}
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
        cook = request.cookies.get('USER_ID',"")
        #print("cook :",cook)
        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=cook,debug=debug)
        #print("login : ",isConnect)
        render = {"login":isConnect,"pseudo":cook}
        #print("render : ",render)
        if debug:
            logger.log("Requête perso.html", "DEBUG")
        #renvoie du code source perso.html au navigateur web après traitement
        return render_template('perso.html',render=render)
    except:
        logger.log("Erreur inconnue dans perso.html", "ERROR")
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
        cook = request.cookies.get('USER_ID',"")
        #print("cook :",cook)
        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=cook,debug=debug)
        #print("login : ",isConnect)
        render = {"login":isConnect,"pseudo":cook}
        #print("render : ",render)
        if debug:
            logger.log("Requête projet.html", "DEBUG")
        #renvoie du code source projet.html au navigateur web après traitement
        return render_template('projet.html', render=render)
    except:
        logger.log("Erreur inconnue dans projet.html", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")

@APP_FLASK.route('/profil.html', methods=['GET'])
def profil():
    try:
        cook = request.cookies.get('USER_ID',"")
        #print("cook :",cook)
        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=cook,debug=debug)
        #print("login : ",isConnect)
        res,err = mydb.read_row("users",f"user = '{cook}'")
        render = {"login":isConnect,"pseudo":cook,"email":res[0][2]}
        #print("render : ",render)
        if debug:
            logger.log("Requête profil.html", "DEBUG")
        #renvoie du code source profil.html au navigateur web après traitement
        return render_template('profil.html', render=render)
    except:
        logger.log("Erreur inconnue dans profil.html", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")

@APP_FLASK.route('/editprofil.html', methods=['GET'])
def editprofil():
    try:
        cook = request.cookies.get('USER_ID',"")
        #print("cook :",cook)
        isConnect = sign.is_connected(logger=logger,mydb=mydb,pseudo=cook,debug=debug)
        #print("login : ",isConnect)
        res,err = mydb.read_row("users",f"user = '{cook}'")
        render = {"login":isConnect,"pseudo":cook,"email":res[0][2]}
        #print("render : ",render)
        if debug:
            logger.log("Requête editprofil.html", "DEBUG")
        #renvoie du code source editprofil.html au navigateur web après traitement
        return render_template('editprofil.html', render=render)
    except:
        logger.log("Erreur inconnue dans editprofil.html", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")


###############################################
# API
###############################################
@APP_FLASK.route('/api/contact', methods=['POST'])
def api_contact():
    payload = request.json

    
    return jsonify({'status': "ok","data":{}})

@APP_FLASK.route('/api/signup', methods=['POST'])
def api_signup():
    try:
        if debug:
            logger.log("Requête api_signup", "DEBUG")
        result = sign.signup(logger=logger,mydb=mydb,payload=request.json,debug=debug)
        return jsonify(result)
    except:
        logger.log("Erreur inconnue dans api_signup", "ERROR")
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
            resp = make_response(jsonify (result))  
            resp.set_cookie('USER_ID',user['user'])  
        return resp
    except:
        logger.log("Erreur inconnue dans api_signin", "ERROR")
        if debug:
            logger.log(str(traceback.format_exc()),"DEBUG")
        return jsonify({"status":"nok","msg":'error'})


###############################################
# Main 
###############################################
if __name__ == '__main__':
    logger.log("Lancement de l'application ! ", "INFO")
#Lancement de serveur WEB flask sur l'adresse IP locale et le port 8080
    logger.log("Création de la base de donnée", "INFO")
    mydb.create_table("users",[("id","INTEGER"),("user","TEXT"),("email","TEXT"),("mdp","TEXT"),("lastlog","INTEGER"),("connected","INTEGER"),("bio","TEXT"),("img","BLOB ")])
    logger.log("Démarrage du serveur flask", "INFO")
    APP_FLASK.run(ssl_context=(ROOT_PATH + 'ssl/cert.pem',ROOT_PATH + 'ssl/key.pem'),host = "127.0.0.1", port = 8080)
    
