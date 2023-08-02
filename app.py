from flask import Flask, render_template
import os

app = Flask(__name__)

# Récupérer le chemin du répertoire courant du script Python
current_dir = os.path.dirname(os.path.realpath(__file__))

# Combiner le chemin du répertoire courant avec le chemin relatif du répertoire "templates"
template_dir = os.path.join(current_dir, 'templates')

# Définir le répertoire des modèles pour l'application Flask en utilisant le chemin complet
app.template_folder = template_dir

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/moyenne_expo.html')
def Moyenne_expo():
    return render_template('moyenne_expo.html')

@app.route('/analyse.html')
def analyse():
    return render_template('analyse.html')

@app.route('/croisement_moyennes_mobiles.html')
def croisement():
    return render_template('croisement_moyennes_mobiles.html')

if __name__ == '__main__':
    # Utilisation de Gunicorn pour exécuter l'application Flask
    # 'app' fait référence à l'objet Flask défini dans ce fichier (app.py)
    # '-b 0.0.0.0:5000' spécifie l'adresse IP et le port sur lequel Gunicorn écoutera les connexions
    app.run(host='0.0.0.0', port=5000, debug=True)
