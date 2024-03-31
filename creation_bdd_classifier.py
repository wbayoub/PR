import os
import re
import csv
from pydub import AudioSegment
import csv
import parselmouth
import numpy as np


'''
    Creation du fichier csva evc les descripteurs pour les phonemes de la bdd.
'''

def extract_formant_info(audio_file, N=5):
    # Charger l'enregistrement audio avec parselmouth
    audio = parselmouth.Sound(audio_file)

    # Calculer la durée totale de l'audio
    total_duration = audio.get_total_duration()

    # Calculer le time step proportionnel à la durée totale de l'audio
    time_step = total_duration / 1000

    # Extraire les formants avec parselmouth
    formants = audio.to_formant_burg(time_step=time_step, maximum_formant=8000)

    start = formants.t1
    time_step = formants.time_step
    n_frames = formants.nt

    time_intervals = [start + time_step * j for j in range(n_frames)]

    decoup = len(time_intervals) // N

    L_f = {}
    L_b = {}

    # Tracer les courbes des premières, deuxièmes, troisièmes et quatrièmes fréquences de résonance
    for i in range(1, 5):
        formant_frequence_values = [formants.get_value_at_time(i, t) for t in time_intervals]
        formant_bandwidth_values = [formants.get_bandwidth_at_time(i, t) for t in time_intervals]
        A_f = []
        A_b = []
        for j in range(N - 1):
            A_f.append(np.mean(formant_frequence_values[j * decoup:(j + 1) * decoup]))
            A_b.append(np.mean(formant_bandwidth_values[j * decoup:(j + 1) * decoup]))
        A_f.append(np.mean(formant_frequence_values[decoup * (N - 1):]))
        A_b.append(np.mean(formant_bandwidth_values[(N - 1) * decoup:]))
        L_f[i] = A_f
        L_b[i] = A_b

    return L_f, L_b


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

root_folder = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\use_bdd\test_cut_lab\phoneme"

# Définir le chemin de sortie du fichier CSV (NE PAS CHANGER !!!!!!!!!!!!!!)
output_phoneme_path = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\use_bdd\test_cut_lab\phoneme"

name_csv = "analyse_total_test" 
output_csv_path = os.path.join(r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\use_bdd\test_cut_lab\phoneme\analyse", name_csv + ".csv")

seuil = 0.05
N = 5
k_id = 0 
erreur = 0

# with open(output_csv_path, "w", newline="", encoding="utf-8") as csvfile:
#     writer = csv.writer(csvfile)
#     # Créer les titres des colonnes pour L_f et L_b
#     headers = ["Identifiant", "Nom_du_fichier", "Longeur audio", "Classe", "Phoneme", "Mot de provenance du phoneme", "Age de l'enfant", "Annees de l'enfant", "Mois de l'enfant", "Jours de l'enfant", "Position dans le mot", "Chemin d'accees au fichier"]
#     for i in range(1, 5):
#         for j in range(1, N+1):
#             headers.append(f"L_f_{i}_{j}")
#     for i in range(1, 5):
#         for j in range(1, N+1):
#             headers.append(f"L_b_{i}_{j}")
    
#     writer.writerow(headers)
    
#     # Parcourir les dossiers et sous-dossiers
#     for root, dirs, files in os.walk(root_folder):
#         for directory in dirs:
#             dossier_a_parcourir = os.path.join(root, directory)
#             for fichier in os.listdir(dossier_a_parcourir):
#                 if fichier.endswith(".wav"):
#                     k_id += 1
#                     nom_complet = fichier.split('.')[0]
#                     L = nom_complet.split('_')
#                     mot = L[0]
#                     id_enfant = L[1]
#                     age = L[2]
#                     age_ans = age[:2]
#                     age_mois = age[2:4]
#                     age_jours = age[4:]
#                     position = L[-1]

#                     path_file = os.path.join(root, directory, fichier)

#                     try:
#                         L_f, L_b = extract_formant_info(path_file, N)
#                     except Exception as e:
#                         erreur += 1 
#                         continue

                    
#                     # Charger l'enregistrement audio avec parselmouth
#                     audio = parselmouth.Sound(path_file)

#                     # Calculer la durée totale de l'audio
#                     total_duration = audio.get_total_duration()
                    
#                     row_data = [k_id, nom_complet, total_duration,directory, str(S_inv[int(directory)]), mot, age, age_ans, age_mois, age_jours, position, path_file]
                    
#                     # Ajouter les valeurs de L_f et L_b dans les données de la ligne
#                     for i in range(1, 5):
#                         row_data.extend(L_f[i])
#                         row_data.extend(L_b[i])

#                     writer.writerow(row_data)
                    
                    
# Chemin vers le fichier CSV d'entrée
input_csv_path = output_csv_path


name_csv_filtered = name_csv + "_for_train" 

output_csv_filtered_path = os.path.join(r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\use_bdd\test_cut_lab\phoneme\analyse", name_csv_filtered + ".csv")

columns_to_keep = ["Identifiant", "Longeur audio", "Position dans le mot", "Classe","Annees de l'enfant", "Mois de l'enfant", "Jours de l'enfant"]
for i in range(1, 5):
    for j in range(1, N+1):
        columns_to_keep.append(f"L_f_{i}_{j}")
for i in range(1, 5):
    for j in range(1, N+1):
        columns_to_keep.append(f"L_b_{i}_{j}")
columns_to_keep.append("Chemin d'accees au fichier")


# Ouvrir le fichier CSV d'entrée en mode lecture
with open(input_csv_path, "r", newline="", encoding="utf-8") as input_file:
    # Ouvrir le fichier CSV de sortie en mode écriture
    with open(output_csv_filtered_path, "w", newline="", encoding="utf-8") as output_file:
        # Créer un lecteur pour le fichier CSV d'entrée
        reader = csv.DictReader(input_file)
        # Créer un écrivain pour le fichier CSV de sortie
        writer = csv.DictWriter(output_file, fieldnames=columns_to_keep)
        
        # Écrire l'en-tête dans le fichier de sortie
        writer.writeheader()
        
        # Parcourir chaque ligne du fichier CSV d'entrée
        for row in reader:
            # Créer un dictionnaire pour stocker les valeurs des colonnes à garder
            filtered_row = {}
            # Parcourir chaque colonne à garder
            for column in columns_to_keep:
                # Ajouter la valeur de la colonne à garder au dictionnaire
                filtered_row[column] = row[column]
            # Écrire la ligne filtrée dans le fichier de sortie
            writer.writerow(filtered_row)

print("Nombre d'erreur : " + str(erreur))