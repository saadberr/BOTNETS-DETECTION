from flask import Flask, render_template, request, url_for
import pickle

##Creation de l'application web
app = Flask(__name__)
##Importer le modele necessaire pour l'etude
model = pickle.load(open('detection_model.pkl', 'rb'))

##Page d'acceuil
@app.route('/')
def home():
    return render_template("acceuil.html")

##Page de prédiction
@app.route('/predict', methods=['POST'])
def predict():
    ##Importation des features a partir de la page d'acceuil
    features_values = [i for i in request.form.values()]
    nbr_features = len(features_values)
    ##Dictionnaires
    Classes = {0: 'Normal activity ✔️', 1: 'Warning : Malware activity ⚠️'}
    service = {'-': 1, 'dhcp': 2, 'dns': 3, 'ftp': 4, 'ftp-data': 5, 'http': 6, 'irc': 7, 'pop3': 8, 'radius': 9,'smtp': 10, 'snmp': 11, 'ssh': 12, 'ssl': 13}
    state = {'ACC': 1, 'CLO': 2, 'CON': 3, 'FIN': 4, 'INT': 5, 'REQ': 6, 'RST': 7}
    ##Si l utilisateur oublie de saisir une valeur
    for i in range(nbr_features):
        if features_values[i] == "" :
            err = "Veuillez remplir tous les champs s.v.p !"
            return render_template("predict.html", value=err)
    ##Si 'service' et 'state' sont incorrectes
    try:
        features_values[8] = service[features_values[8]]
        features_values[11] = state[features_values[11]]
    except:
        err2 = "Verifier les valeurs des paramètres 'service' ou 'state' !"
        return render_template("predict.html", value=err2)
    else:
        ##Si certains valeurs sont incorrectes
        try:
            features_values = [features_values]
            ##Effectuer la prediction
            prediction = model.predict(features_values)
        except:
            err3 = "Valeurs incorrectes !"
            return render_template("predict.html", value=err3)
        else:
            return render_template("predict.html", value=Classes[prediction[0]])

if __name__ == "__main__":
    app.run(debug=True)
