import pandas as pd
from data_processing import *

def long_trade(dataFrame):
    dataFrame_minute = load_filter_data('/Users/fahad/Documents/Projet/Binance_ETHUSDT_2022_minute.csv')
    # Initialisation du tableau pour stocker les informations sur les trades longs
    trades_info = []

    trade_en_cours = False  # Indicateur pour savoir si une trade longue est en cours
    index_ouverture_trade = None  # Index de l'ouverture de la trade longue

    # Convertir la colonne 'date' du DataFrame dataFrame_minute en objets Timestamp
    dataFrame_minute['Date'] = pd.to_datetime(dataFrame_minute['Date'])


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
    return trades_dataframe

def short_trade(dataFrame):
    dataFrame_minute = load_filter_data('/Users/fahad/Documents/Projet/Binance_ETHUSDT_2022_minute.csv')
    # Initialisation du tableau pour stocker les informations sur les trades courts
    trade_courts_info = []

    trade_en_cours = False  # Indicateur pour savoir si une trade courte est en cours
    index_ouverture_trade = None  # Index de l'ouverture de la trade courte

    # Convertir la colonne 'date' du DataFrame dataFrame_minute en objets Timestamp
    dataFrame_minute['Date'] = pd.to_datetime(dataFrame_minute['Date'])

    # Parcourir les croisements détectés dans le DataFrame
    for index, row in dataFrame.iterrows():
        if row['Signal'] == -1 and not trade_en_cours:  # Croisement à la baisse et aucune trade courte en cours
            date_ouverture_trade = row['Date']  # Date d'ouverture de la trade courte
            prix_ouverture_trade = row['Close']  # Prix d'ouverture de la trade courte
            trade_en_cours = True  # Une trade courte est maintenant en cours
            index_ouverture_trade = index  # Enregistrement de l'index de l'ouverture de la trade courte
            print(f"Trade courte ouverte le {date_ouverture_trade}, prix d'ouverture : {prix_ouverture_trade}")

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

                        #Affichage du message pour chaque fermeture de trade courte
                        print(f"Trade courte fermée le {date_fermeture_trade}, prix de fermeture : {prix_fermeture_trade}")

                        # Réinitialiser les variables pour ouvrir une nouvelle trade courte
                        trade_en_cours = False
                        index_ouverture_trade = None
                        break  # Sortir de la boucle interne pour passer au croisement suivant

    # Création d'un DataFrame pour stocker les informations sur les trades courtes
    trade_courts_dataframe = pd.DataFrame(trade_courts_info)
    return trade_courts_dataframe

dataFrame = load_filter_data('/Users/fahad/Documents/Projet/Binance_ETHUSDT_1h.csv')
creat_ema(dataFrame)
creat_signal(dataFrame)
dataFrame.tail(400)
# print(short_trade(dataFrame.head(400)))

trade_longue = short_trade(dataFrame)

print(trade_longue)

# # Convertit les DataFrames en tableaux HTML
# table_html_long = croisements_hausse.to_html(index=False)

# # Détermine le chemin absolu vers le fichier HTML 
# html_file_path = os.path.join("/Users/fahad/Documents/Projet/templates", "long_trade.html")

# # Lit le contenu du fichier HTML existant
# with open(html_file_path, 'r') as file:
#     contenu_html = file.read()

# # Remplace le marqueur par le contenu du tableau HTML généré
# contenu_html = contenu_html.replace('<!-- TABLE_HAUSSE -->', table_html_long)

# # Écrit le contenu HTML modifié dans le fichier HTML
# with open(html_file_path, 'w') as file:
#     file.write(contenu_html)