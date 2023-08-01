import pandas as pd
import os

# Chargement, filtrage et traitement d'un fichier CSV pour récupérer les données de l'année 2022, avec une réduction de la taille et un tri chronologique.
def load_filter_data(path):
    chemin_fichier_heure_detude = path

    # Chargement du fichier CSV dans un DataFrame
    dataFrame = pd.read_csv(chemin_fichier_heure_detude)

    # Sélection des données pour l'année 2022 à l'aide de la méthode str.startswith()
    dataFrame = dataFrame[dataFrame["Date"].str.startswith("2022")]

    # # Initialisation de la taille de l'étude pour travailler et effectuer des vérifications sur une plus petite taille de données
    # dataFrame = dataFrame.tail()

    # Tri du DataFrame par ordre chronologique en utilisant la colonne 'Date'
    dataFrame.sort_values(by='Date', inplace=True)

    # Réinitialisation des index pour qu'ils soient séquentiels à partir de zéro
    dataFrame.reset_index(drop=True, inplace=True)
    dataFrame["Date"] = pd.to_datetime(dataFrame["Date"])

    return dataFrame

# Séparation des données d'un DataFrame en deux sous-ensembles distincts : les croisements à la baisse et les croisements à la hausse, en fonction de la valeur de la colonne 'Signal'.
def data_croisement(dataFrame):
    croisements_hausse = dataFrame[dataFrame['Signal'] == 1]
    croisements_baisse = dataFrame[dataFrame['Signal'] == -1]
    return croisements_baisse, croisements_hausse


# Calcule des moyennes mobiles exponentielles pour la colonne 'Close' du DataFrame donné avec des fenêtres de 9 et 25 périodes.

def creat_ema(dataframe):
    # Calcul de la moyenne mobile exponentielle (EMA) pour la colonne 'Close'
    # La méthode .ewm() est utilisée pour calculer l'EMA de chaque ligne de cette colonne, en spécifiant un span de 9 et  25 périodes
    dataframe['EMA_9'] = dataframe["Close"].ewm(span=9, adjust=False).mean()
    dataframe['EMA_25'] = dataframe["Close"].ewm(span=25, adjust=False).mean()


# Calcule des signaux des 'EMA_9' et 'EMA_25', en enregistrant les signaux de croisement détectés dans une colonne 'Signal'.

def creat_signal(dataFrame):
    # Calcul des signaux de croisement : lorsque EMA_9 croise EMA_25

    # Initialisation du signal a 0 : Aucun croisement
    dataFrame['Signal'] = 0

    # Utilisation de shift(1) pour comparer les valeurs actuelles avec les valeurs précédentes et détecter les croisements.
    # Si EMA_9 est supérieure à EMA_25 actuellement, mais était inférieure dans la période précédente, alors c'est un croisement à la hausse (Signal = 1).
    # Si EMA_9 est inférieure à EMA_25 actuellement, mais était supérieure dans la période précédente, alors c'est un croisement à la baisse (Signal = -1).
    # Pour les croisements à la hausse
    dataFrame.loc[(dataFrame['EMA_9'] > dataFrame['EMA_25']) & (dataFrame['EMA_9'].shift(1) < dataFrame['EMA_25'].shift(1)), 'Signal'] = 1

    # Pour les croisements à la baisse
    dataFrame.loc[(dataFrame['EMA_9'] < dataFrame['EMA_25']) & (dataFrame['EMA_9'].shift(1) > dataFrame['EMA_25'].shift(1)), 'Signal'] = -1



dataFrame = load_filter_data('/Users/fahad/Documents/Projet/Binance_ETHUSDT_1h.csv')
creat_ema(dataFrame)
creat_signal(dataFrame)

# Détermine le chemin absolu vers le fichier HTML dans le répertoire "mon_repertoire_html"
html_file_path = os.path.join("/Users/fahad/Documents/Projet/templates", "signal_baisse.html")

# Appelle la fonction pour obtenir les DataFrames de croisements
croisements_baisse, croisements_hausse = data_croisement(dataFrame)

collone_a_garder = ['Date', 'Close']
croisements_baisse = croisements_baisse[collone_a_garder]
#croisements_hausse = croisements_hausse.transpose()

# Convertit les DataFrames en tableaux HTML
table_html_hausse = croisements_hausse.to_html(index=False)
table_html_baisse = croisements_baisse.to_html(index=False)

# Lit le contenu du fichier HTML existant
with open(html_file_path, 'r') as file:
    contenu_html = file.read()

# Remplace le marqueur par le contenu du tableau HTML généré
contenu_html = contenu_html.replace('<!-- TABLE_HAUSSE -->', table_html_baisse)

# Écrit le contenu HTML modifié dans le fichier HTML
with open(html_file_path, 'w') as file:
    file.write(contenu_html)


# print(dataFrame)