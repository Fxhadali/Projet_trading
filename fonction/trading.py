# Importation des bibliothèques pandas et matplotlib.pyplot
import pandas as pd
import matplotlib.pyplot as plt
import os

# Chemin vers le fichier CSV d'étude
chemin_fichier_heure_detude = "/Users/fahad/Documents/Projet/Binance_ETHUSDT_1h.csv"

# Chargement du fichier CSV dans un DataFrame
dataFrame = pd.read_csv(chemin_fichier_heure_detude)

# Sélection des données pour l'année 2022 à l'aide de la méthode str.startswith()
dataFrame = dataFrame[dataFrame["Date"].str.startswith("2022")]

# Initialisation de la taille de l'étude pour travailler et effectuer des vérifications sur une plus petite taille de données
size = 2000
dataFrame = dataFrame.tail(size)

# Tri du DataFrame par ordre chronologique en utilisant la colonne 'Date'
dataFrame.sort_values(by='Date', inplace=True)

# Réinitialisation des index pour qu'ils soient séquentiels à partir de zéro
dataFrame.reset_index(drop=True, inplace=True)

#print(dataFrame.iloc[0])

## CREATION DE NOUVELLE COLONNE REPRESENTANT LA MOYENNE MOBILE EXPONENTIELLE

# Calcul de la moyenne mobile exponentielle (EMA) pour la colonne 'Close'
# La méthode .ewm() est utilisée pour calculer l'EMA de chaque ligne de cette colonne, en spécifiant un span de 9 et  25 périodes
dataFrame['EMA_9'] = dataFrame["Close"].ewm(span=9, adjust=False).mean()
dataFrame['EMA_25'] = dataFrame["Close"].ewm(span=25, adjust=False).mean()

# # Remplacement des 9 premiers éléments de la colonne 'EMA_9' par NaN puisqu'il n'y a pas assez d'éléments pour le calcul
# dataFrame.loc[:8, 'EMA_9'] = None
# # De même pour les 25 premiers éléments de la colonne 'EMA_25'
# dataFrame.loc[:24, 'EMA_25'] = None

## CROISEMENT DES MOYENNES MOBILES

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

#print(dataFrame['Signal'])

## VISUALISATION DES SIGNAUX

#Création d'un graphique à partir de la colonne 'Date'
#La colonne 'Date'  est convertie en format datetime à l'aide de pd.to_datetime()


# # Traçage de la courbe de l'EMA_9 en utilisant la colonne "Date" comme axe des x et "EMA_9" comme axe des y
# plt.plot(pd.to_datetime(dataFrame["Date"]), dataFrame['EMA_9'], label='EMA_9', color='yellow')

# # Traçage de la courbe de l'EMA_25 en utilisant la colonne "Date" comme axe des x et "EMA_25" comme axe des y
# plt.plot(pd.to_datetime(dataFrame["Date"]), dataFrame['EMA_25'], label='EMA_25', color='blue')

# #Ajout de titres et étiquettes d'axe
# plt.title('Evolution de l\'EMA_9 et l\'EMA_25 en fonction du temps')
# plt.xlabel('Date')
# plt.legend()
# plt.ylabel('EMA_9 et EMA_25')

# Repérer les croisements à la hausse et à la baisse
croisements_hausse = dataFrame[dataFrame['Signal'] == 1]
croisements_baisse = dataFrame[dataFrame['Signal'] == -1]
# print(croisements_baisse)
# print(croisements_hausse)

#print(croisements_hausse)

# Traçage du deuxième graphique avec les croisements de moyennes mobiles

# # Tracer la courbe EMA_9 en utilisant les dates du DataFrame
# plt.plot(pd.to_datetime(dataFrame["Date"]), dataFrame['EMA_9'], label='EMA_9', color='grey', alpha=0.7)

# # Tracer la courbe EMA_25 en utilisant les dates du DataFrame
# plt.plot(pd.to_datetime(dataFrame["Date"]), dataFrame['EMA_25'], label='EMA_25', color='grey', alpha=0.7)

# # Placer des flèche verts pour les croisements à la hausse de l'EMA_9, en utilisant les dates et les valeurs du DataFrame 'croisements_hausse'
# plt.scatter(pd.to_datetime(croisements_hausse['Date']), croisements_hausse['EMA_9'], color='green', label='Croisement à la hausse', marker='^', s=100)

# # Placer des flèche rouges pour les croisements à la baisse de l'EMA_9, en utilisant les dates et les valeurs du DataFrame 'croisements_baisse'
# plt.scatter(pd.to_datetime(croisements_baisse['Date']), croisements_baisse['EMA_9'], color='red', label='Croisement à la baisse', marker='v', s=100)

# # Ajout de titres et étiquettes d'axe
# plt.legend()
# plt.title('Croisements de moyennes mobiles entre l\'EMA_9 et l\'EMA_25 en fonction du temps')
# plt.xlabel('Date')
# plt.ylabel('EMA_9 et EMA_25')

# #Définition des limites de l'axe des x (l'axe horizontal)
# plt.xlim(pd.to_datetime(dataFrame["Date"].iloc[0]), pd.to_datetime(dataFrame["Date"].iloc[-1]))

# # Création d'un graphique pour les prix de clôture

# plt.figure(figsize=(10, 6))

# # Tracé des prix de clôture en utilisant la colonne "Date" comme axe des x et "Close" comme axe des y
# plt.plot(pd.to_datetime(dataFrame["Date"]), dataFrame['Close'], label='Prix de clôture', color='orange')

# # Ajout des titres et étiquettes d'axe
# plt.title('Prix de clôture au fil du temps')
# plt.xlabel('Date')
# plt.ylabel('Prix de clôture')

# # Légende pour le graphique
# plt.legend()

#Affichage du graphique
# plt.show()

# # CRÉATION DE NOUVELLES DATAFRAME SUR L'ANALYSE DES CROISEMENTS DE MOYENNES MOBILES

# Chargement du deuxième fichier CSV  avec une timeframe à la minute
chemin_fichier_minute = "/Users/fahad/Documents/Projet/Binance_ETHUSDT_2022_minute.csv"
dataFrame_minute = pd.read_csv(chemin_fichier_minute)
dataFrame_minute = dataFrame_minute[dataFrame_minute["Date"].str.startswith("2022")]
#dataFrame_minute = dataFrame_minute.tail(size)
dataFrame_minute.sort_values(by='Date', inplace=True)
dataFrame_minute.reset_index(drop=True, inplace=True)
dataFrame_minute["Date"] = pd.to_datetime(dataFrame_minute["Date"])

#

## ANALYSE DES TRADES LONGS

# Initialisation du tableau pour stocker les informations sur les trades longs
trades_info = []

trade_en_cours = False  # Indicateur pour savoir si une trade longue est en cours
index_ouverture_trade = None  # Index de l'ouverture de la trade longue

# Parcourir les croisements détectés dans le DataFrame
for index, row in dataFrame.iterrows():
    if row['Signal'] == 1 and not trade_en_cours:  # Croisement à la hausse et aucune trade longue en cours
        date_ouverture_trade = row['Date']  # Date d'ouverture de la trade longue
        prix_ouverture_trade = row['Close']  # Prix d'ouverture de la trade longue
        trade_en_cours = True  # Une trade longue est maintenant en cours
        index_ouverture_trade = index  # Enregistrement de l'index de l'ouverture de la trade longue
        #print(f"Trade longue ouverte le {date_ouverture_trade}, prix d'ouverture : {prix_ouverture_trade}")

    # Vérifier si une trade longue est en cours et chercher la fermeture de la trade longue
    if trade_en_cours:
        for minute_index, minute_row in dataFrame_minute.loc[index_ouverture_trade+1:].iterrows():
            if minute_row['Date'] > pd.to_datetime(date_ouverture_trade):
                prix_courant = minute_row['Close']

                # Vérification des conditions de sortie de la trade longue
                if (prix_courant >= prix_ouverture_trade * 1.012) or (prix_courant <= prix_ouverture_trade * 0.96):
                    date_fermeture_trade = minute_row['Date']  # Date de fermeture de la trade longue
                    prix_fermeture_trade = prix_courant  # Prix de fermeture de la trade longue

                    # Calcul de la variation du prix par rapport au prix d'ouverture
                    variation_prix = round((prix_fermeture_trade / prix_ouverture_trade - 1) * 100, 2)

                    # Calcul de la durée de la trade longue en jours, heures et minutes
                    duree_trade = pd.to_datetime(date_fermeture_trade) - pd.to_datetime(date_ouverture_trade)
                    duree_jours = duree_trade.days
                    duree_heures, remainder = divmod(duree_trade.seconds, 3600)
                    duree_minutes, _ = divmod(remainder, 60)

                    # Ajout des informations sur la trade longue à la liste trades_info
                    trades_info.append({
                        'Date_Ouverture': date_ouverture_trade,
                        'Prix_Ouverture': prix_ouverture_trade,
                        'Date_Fermeture': date_fermeture_trade,
                        'Prix_Fermeture': prix_fermeture_trade,
                        'Variation_Prix': variation_prix,
                        'Motif_Fermeture': 'Bénéfice' if variation_prix >= 1.2 else 'Perte',
                        'Duree_Trade': f"{duree_jours} jours, {duree_heures} heures, {duree_minutes} minutes",
                    })

                    # Affichage du message pour chaque fermeture de trade
                    #print(f"Trade longue fermée le {date_fermeture_trade}, prix de fermeture : {prix_fermeture_trade}")

                    # Réinitialiser les variables pour ouvrir une nouvelle trade longue
                    trade_en_cours = False
                    index_ouverture_trade = None
                    break  # Sortir de la boucle interne pour passer au croisement suivant

# Création d'un DataFrame pour stocker les informations sur les trades longues
trades_dataframe = pd.DataFrame(trades_info)

# Affichage du DataFrame contenant les informations sur les trades longues

## ANALYSE DES TRADES COURTS

# Initialisation du tableau pour stocker les informations sur les trades courts
trade_courts_info = []

trade_en_cours = False  # Indicateur pour savoir si une trade courte est en cours
index_ouverture_trade = None  # Index de l'ouverture de la trade courte

# Parcourir les croisements détectés dans le DataFrame
for index, row in dataFrame.iterrows():
    if row['Signal'] == -1 and not trade_en_cours:  # Croisement à la baisse et aucune trade courte en cours
        date_ouverture_trade = row['Date']  # Date d'ouverture de la trade courte
        prix_ouverture_trade = row['Close']  # Prix d'ouverture de la trade courte
        trade_en_cours = True  # Une trade courte est maintenant en cours
        index_ouverture_trade = index  # Enregistrement de l'index de l'ouverture de la trade courte
        #print(f"Trade courte ouverte le {date_ouverture_trade}, prix d'ouverture : {prix_ouverture_trade}")

    # Vérifier si une trade courte est en cours et chercher la fermeture de la trade courte
    if trade_en_cours:
        for minute_index, minute_row in dataFrame_minute.loc[index_ouverture_trade+1:].iterrows():
            if minute_row['Date'] > pd.to_datetime(date_ouverture_trade):
                prix_courant = minute_row['Close']

                # Vérification des conditions de sortie de la trade courte
                if (prix_courant <= prix_ouverture_trade * 0.988) or (prix_courant >= prix_ouverture_trade * 1.04):
                    date_fermeture_trade = minute_row['Date']  # Date de fermeture de la trade courte
                    prix_fermeture_trade = prix_courant  # Prix de fermeture de la trade courte

                    # Calcul de la variation du prix par rapport au prix d'ouverture
                    variation_prix = round((prix_fermeture_trade / prix_ouverture_trade - 1) * 100, 2)

                    # Calcul de la durée de la trade courte en jours, heures et minutes
                    duree_trade = pd.to_datetime(date_fermeture_trade) - pd.to_datetime(date_ouverture_trade)
                    duree_jours = duree_trade.days
                    duree_heures, remainder = divmod(duree_trade.seconds, 3600)
                    duree_minutes, _ = divmod(remainder, 60)

                    # Ajout des informations sur la trade courte à la liste trade_courts_info
                    trade_courts_info.append({
                        'Date_Ouverture': date_ouverture_trade,
                        'Prix_Ouverture': prix_ouverture_trade,
                        'Date_Fermeture': date_fermeture_trade,
                        'Prix_Fermeture': prix_fermeture_trade,
                        'Variation_Prix': variation_prix,
                        'Motif_Fermeture': 'Bénéfice' if variation_prix >= 1.2 else 'Perte',
                        'Duree_Trade': f"{duree_jours} jours, {duree_heures} heures, {duree_minutes} minutes",
                    })

                    # Affichage du message pour chaque fermeture de trade courte
                    #print(f"Trade courte fermée le {date_fermeture_trade}, prix de fermeture : {prix_fermeture_trade}")

                    # Réinitialiser les variables pour ouvrir une nouvelle trade courte
                    trade_en_cours = False
                    index_ouverture_trade = None
                    break  # Sortir de la boucle interne pour passer au croisement suivant

# Création d'un DataFrame pour stocker les informations sur les trades courtes
trade_courts_dataframe = pd.DataFrame(trade_courts_info)


#print(trades_dataframe)
print(trade_courts_dataframe)



#plt.show()

# Convertit les DataFrames en tableaux HTML
table_html_long = trade_courts_dataframe.to_html(index=False)

# Détermine le chemin absolu vers le fichier HTML 
html_file_path = os.path.join("/Users/fahad/Documents/Projet/templates", "short_trade.html")

# Lit le contenu du fichier HTML existant
with open(html_file_path, 'r') as file:
    contenu_html = file.read()

# Remplace le marqueur par le contenu du tableau HTML généré
contenu_html = contenu_html.replace('<!-- TABLE_HAUSSE -->', table_html_long)

# Écrit le contenu HTML modifié dans le fichier HTML
with open(html_file_path, 'w') as file:
    file.write(contenu_html)