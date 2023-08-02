from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Get the absolute path of the 'templates' folder and render the 'index.html' file.
    template_dir = os.path.abspath('/Users/fahad/Documents/Projet/templates/')
    return render_template('index.html', template_folder=template_dir)

@app.route('/moyenne_expo.html')
def Moyenne_expo():
    template_dir = os.path.abspath('/Users/fahad/Documents/Projet/templates/')
    return render_template('moyenne_expo.html', template_folder=template_dir)

@app.route('/analyse.html')
def analyse():
    template_dir = os.path.abspath('/Users/fahad/Documents/Projet/templates/')
    return render_template('analyse.html', template_folder=template_dir)

@app.route('/croisement_moyennes_mobiles.html')
def croisement():
    template_dir = os.path.abspath('/Users/fahad/Documents/Projet/templates/')
    return render_template('croisement_moyennes_mobiles.html', template_folder=template_dir)

if __name__ == '__main__':
    app.run(debug=True)
