import streamlit as st
import json

# Charger le fichier CSV brut
with open('data/sports.csv', 'r') as file:
    sports_data = file.read()


def get_unique_sports(data):
    """
    Extrait les noms de sports uniques de la 9ème colonne du CSV.
    Cette version utilise strip() de manière robuste pour 
    supprimer les guillemets ou apostrophes autour du nom.
    """
    lst_sports = []
    for line in data.splitlines()[1:]:
        if not line.strip():
            continue
        
        try:
            sport = line.split(';')[8]
        except IndexError:
            continue 

    
        sport = sport.strip().strip('\'"')
        sport = sport.replace("\\'", "'")
        
        if sport and sport not in lst_sports:
            lst_sports.append(sport)
            
    return lst_sports


# 1ère standardization de données
def standardize_federation(lst_sports):
    standardized_sports = []
    
    for sport in lst_sports:
        standardized_sport = sport.strip()

        if standardized_sport.startswith("FF de "):
            standardized_sport = standardized_sport[6:]
            
        elif standardized_sport.lower().startswith("ff d'"): 
            standardized_sport = standardized_sport[5:]
            
        elif standardized_sport.startswith("FF"):
            standardized_sport = standardized_sport[2:]
            
        standardized_sports.append(standardized_sport.strip())
        
    return standardized_sports


def lst_to_lower(lst):
    return [item.lower() for item in lst]

lst_sport = get_unique_sports(sports_data)
standardize_sport = standardize_federation(lst_sport)
lst_sport_lower = lst_to_lower(lst_sport)
standardize_sport_lower = lst_to_lower(standardize_sport)

#Exporter en format json -> lst_sport[i] : standardize_sport[i]
with open('data/standardized_sports.json', 'w') as json_file:
    json.dump({lst_sport_lower[i]: standardize_sport_lower[i] for i in range(len(lst_sport_lower))}, json_file, ensure_ascii=False, indent=4)

print(standardize_sport_lower)