import pandas as pd
import matplotlib.pyplot as plt

# Importer les fichiers contenant les fonctions utilent
from data_processing import *
from trade_operations import *

def calculate_profit(dataFrame, threshold_profit=1.2):
    # Traiter les données DataFrame
    creat_ema(dataFrame)
    creat_signal(dataFrame)

    # Traiter les trades longues et courtes avec les données DataFrame
    trade_long_df = long_trade(dataFrame)
    trade_short_df = short_trade(dataFrame)

    # Calcule du bénéfice total des trades longues
    total_profit_long = trade_long_df[trade_long_df['Variation_Prix'] >= threshold_profit]['Variation_Prix'].sum()

    # Calcule du bénéfice total des trades courtes
    total_profit_short = trade_short_df[trade_short_df['Variation_Prix'] >= threshold_profit]['Variation_Prix'].sum()

    # Calcule du bénéfice total en combinant les trades longues et courtes
    total_profit = total_profit_long + total_profit_short

    return total_profit


# dataFrame = load_filter_data('/Users/fahad/Documents/Projet/Binance_ETHUSDT_1h.csv')
# print(calculate_profit(dataFrame.head(400)))