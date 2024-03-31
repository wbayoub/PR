import os
import re
import csv
from pydub import AudioSegment
import csv


'''
    Creation de la bdd des phonemes pour connaitre les infos standards pour chaque phonemes.
'''

def couper_audio(chemin_audio, debut, fin, chemin_sortie):
    # Charger le fichier audio
    audio = AudioSegment.from_wav(chemin_audio)
    
    # Découper l'audio
    audio_coupe = audio[debut:fin]
    
    # Exporter l'audio découpé
    audio_coupe.export(chemin_sortie, format="wav")
    

# Dossier racine à partir duquel vous souhaitez parcourir les sous-dossiers
S = {'a': 1, 'b': 2, 'd': 3, 'e': 4, 'f': 5, 'i': 6, 'j': 7, 'k': 8, 'l': 9, 'm': 10, 'n': 11, 'o': 12, 'p': 13, 's': 14, 't': 15, 'u': 16, 'v': 17, 'w': 18, 'y': 19, 'z': 20, 'ø': 21, 'œ': 22, 'ɑ̃': 23, 'ɔ': 24, 'ɔ̃': 25, 'ə': 26, 'ɛ': 27, 'ɛ̃': 28, 'ɡ': 29, 'ɥ': 30, 'ɲ': 31, 'ʁ': 32, 'ʃ': 33, 'ʒ': 34}
S_inv = {1: 'a', 2: 'b', 3: 'd', 4: 'e', 5: 'f', 6: 'i', 7: 'j', 8: 'k', 9: 'l', 10: 'm', 11: 'n', 12: 'o', 13: 'p', 14: 's', 15: 't', 16: 'u', 17: 'v', 18: 'w', 19: 'y', 20: 'z', 21: 'ø', 22: 'œ', 23: 'ɑ̃', 24: 'ɔ', 25: 'ɔ̃', 26: 'ə', 27: 'ɛ', 28: 'ɛ̃', 29: 'ɡ', 30: 'ɥ', 31: 'ɲ', 32: 'ʁ', 33: 'ʃ', 34: 'ʒ'}
L = ['a', 'b', 'd', 'e', 'f', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 's', 't', 'u', 'v', 'w', 'y', 'z', 'ø', 'œ', 'ɑ̃', 'ɔ', 'ɔ̃', 'ə', 'ɛ', 'ɛ̃', 'ɡ', 'ɥ', 'ɲ', 'ʁ', 'ʃ', 'ʒ']

M = "05"
root_folder = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\use_bdd\test_cut_lab\phoneme\phoneme_" + M

# Définir le chemin de sortie du fichier CSV (NE PAS CHANGER !!!!!!!!!!!!!!)
output_phoneme_path = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\use_bdd\test_cut_lab\phoneme\phoneme_" + M 

name_csv = "analyse_" + M
output_csv_path = os.path.join(r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\use_bdd\test_cut_lab\phoneme\analyse", name_csv + ".csv")

seuil = 0.05

k_id = 0 

with open(output_csv_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    # Écrire l'en-tête
    writer.writerow(["Identifiant","Nom_du_fichier", "Classe", "Phoneme", "Mot de provenance du phoneme", "Age de l'enfant", "Annees de l'enfant", "Mois de l'enfant", "Jours de l'enfant", "Position dans le mot", "Chemin d'accées au fichier"])
    # Parcourir les dossiers et sous-dossiers
    for root, dirs, files in os.walk(root_folder):
        for directory in dirs : 
            dossier_a_parcourir = os.path.join(root, directory)
            for fichier in os.listdir(dossier_a_parcourir):
                k_id += 1 
                nom_complet = fichier.split('.')[0]
                L = nom_complet.split('_')
                mot = L[0]
                id_enfant = L[1]
                age = L[2]
                age_ans = age[:2]
                age_mois = age[2:4]
                age_jours = age[4:]
                position = L[-1]
                
                path_file = os.path.join(root,directory,fichier)
                writer.writerow([k_id, nom_complet, directory, str(S_inv[int(directory)]), mot, age, age_ans, age_mois, age_jours, position, path_file])
                
        
        
