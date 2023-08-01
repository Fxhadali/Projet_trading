import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from data_processing import *

def graph_evolution(dataFrame):
    plt.figure(figsize=(10, 6))
    # Traçage de la courbe de l'EMA_9 en utilisant la colonne "Date" comme axe des x et "EMA_9" comme axe des y
    plt.plot(pd.to_datetime(dataFrame["Date"]), dataFrame['EMA_9'], label='EMA_9', color='yellow')

    # Traçage de la courbe de l'EMA_25 en utilisant la colonne "Date" comme axe des x et "EMA_25" comme axe des y
    plt.plot(pd.to_datetime(dataFrame["Date"]), dataFrame['EMA_25'], label='EMA_25', color='blue')

    #Ajout de titres et étiquettes d'axe
    plt.title('Evolution de l\'EMA_9 et l\'EMA_25 en fonction du temps')
    plt.xlabel('Date')
    plt.legend()
    plt.ylabel('EMA_9 et EMA_25')
    #plt.show()

    # Crée un buffer d'octets en mémoire pour stocker l'image du graphique
    img = io.BytesIO()

    # Sauvegarde le graphique dans le buffer d'octets au format PNG
    plt.savefig(img, format='png')

    # Remet le curseur du buffer d'octets au début pour permettre la lecture ultérieure
    img.seek(0)

    # Encode le contenu du buffer d'octets en base64 pour le rendre utilisable en tant qu'URL d'image
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.savefig('graph_evolution.png',format='png', transparent=True)
    # Fermer le graphique pour libérer les ressources
    plt.close()

    # Renvoyer l'image encodée en base64
    return plot_url


def graph_croisement(dataFrame):
    plt.figure(figsize=(10, 6))
    # Repérer les croisements à la hausse et à la baisse
    croisements_baisse, croisements_hausse = data_croisement(dataFrame)

    # Tracer la courbe EMA_9 en utilisant les dates du DataFrame
    plt.plot(pd.to_datetime(dataFrame["Date"]), dataFrame['EMA_9'], label='EMA_9', color='grey', alpha=0.7)

    # Tracer la courbe EMA_25 en utilisant les dates du DataFrame
    plt.plot(pd.to_datetime(dataFrame["Date"]), dataFrame['EMA_25'], label='EMA_25', color='grey', alpha=0.7)

    # Placer des flèche verts pour les croisements à la hausse de l'EMA_9, en utilisant les dates et les valeurs du DataFrame 'croisements_hausse'
    plt.scatter(pd.to_datetime(croisements_hausse['Date']), croisements_hausse['EMA_9'], color='green', label='Croisement à la hausse', marker='^', s=100)

    # Placer des flèche rouges pour les croisements à la baisse de l'EMA_9, en utilisant les dates et les valeurs du DataFrame 'croisements_baisse'
    plt.scatter(pd.to_datetime(croisements_baisse['Date']), croisements_baisse['EMA_9'], color='red', label='Croisement à la baisse', marker='v', s=100)

    # Ajout de titres et étiquettes d'axe
    plt.legend()
    plt.title('Croisements de moyennes mobiles entre l\'EMA_9 et l\'EMA_25 en fonction du temps')
    plt.xlabel('Date')
    plt.ylabel('EMA_9 et EMA_25')
    #plt.show()
    # Crée un buffer d'octets en mémoire pour stocker l'image du graphique
    img = io.BytesIO()

    # Sauvegarde le graphique dans le buffer d'octets au format PNG
    #plt.savefig(img, format='png', transparent=True)

    # Remet le curseur du buffer d'octets au début pour permettre la lecture ultérieure
    img.seek(0)

    # Encode le contenu du buffer d'octets en base64 pour le rendre utilisable en tant qu'URL d'image
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.savefig('graph_croisement.png',format='png', transparent=True)
    # Fermer le graphique pour libérer les ressources
    plt.close()

    # Renvoyer l'image encodée en base64
    return plot_url


# Création d'un graphique pour les prix de clôture
def graph_prix_de_cloture(dataFrame):
    plt.figure(figsize=(10, 6))

    # Tracé des prix de clôture en utilisant la colonne "Date" comme axe des x et "Close" comme axe des y
    plt.plot(pd.to_datetime(dataFrame["Date"]), dataFrame['Close'], label='Prix de clôture', color='orange')

    # Ajout des titres et étiquettes d'axe
    plt.title('Prix de clôture au fil du temps')
    plt.xlabel('Date')
    plt.ylabel('Prix de clôture')

    # Légende pour le graphique
    plt.legend()
    #plt.show()
    # Crée un buffer d'octets en mémoire pour stocker l'image du graphique
    img = io.BytesIO()

    # Sauvegarde le graphique dans le buffer d'octets au format PNG
    plt.savefig(img, format='png')

    # Remet le curseur du buffer d'octets au début pour permettre la lecture ultérieure
    img.seek(0)

    # Encode le contenu du buffer d'octets en base64 pour le rendre utilisable en tant qu'URL d'image
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.savefig('graph_cloture.png',format='png', transparent=True)
    # Fermer le graphique pour libérer les ressources
    plt.close()
    
    # Renvoyer l'image encodée en base64
    return plot_url

dataFrame = load_filter_data('/Users/fahad/Documents/Projet/Binance_ETHUSDT_1h.csv')
creat_ema(dataFrame)
creat_signal(dataFrame)
graph_evolution(dataFrame)
graph_croisement(dataFrame)
graph_prix_de_cloture(dataFrame)