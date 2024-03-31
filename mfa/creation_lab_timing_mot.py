import librosa
import numpy as np
import os


'''
    Tentative de création des fichiers lab avec l'indication du début et de la fin de la prononciation du mot.
'''

def generate_lab_with_sound_levels(audio_file, threshold_db=-25):
    # Extraire le nom du fichier sans extension
    name = os.path.splitext(os.path.basename(audio_file))[0]
    
    # Charger le fichier audio
    y, sr = librosa.load(audio_file, sr=None)

    # Convertir l'audio en amplitude en utilisant la transformée de Fourier
    amplitude = np.abs(librosa.stft(y))

    # Calculer l'énergie (puissance) de chaque trame
    energy = librosa.feature.rms(S=amplitude)

    # Convertir l'énergie en décibels
    energy_db = librosa.amplitude_to_db(energy)

    # Trouver les indices des débuts et fins de son en fonction du seuil de silence
    start_index = 0
    end_index = len(y)
    for i in range(len(energy_db[0])):
        if energy_db[0][i] > threshold_db:
            start_index = i * 512  # Convertir l'indice en échantillon
            break
    for i in range(len(energy_db[0])-1, 0, -1):
        if energy_db[0][i] > threshold_db:
            end_index = (i+1) * 512  # Convertir l'indice en échantillon
            break

    # Conversion des indices en millisecondes
    start_time_ms = start_index / sr * 1000
    end_time_ms = end_index / sr * 1000

    # Créer le contenu du fichier .lab avec les intervalles correspondant au niveau sonore détecté
    content = f"{start_time_ms:.6f} {end_time_ms:.6f} {name}\n"
    
    return content

def process_folder_to_lab(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".wav"):
                audio_file = os.path.join(root, file)
                lab_content = generate_lab_with_sound_levels(audio_file)
                output_folder = root
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                output_file = os.path.join(output_folder, os.path.splitext(file)[0] + ".lab")
                with open(output_file, "w") as f:
                    f.write(lab_content)

# Exemple d'utilisation
folder_path = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\segmentation_test\corpus"
process_folder_to_lab(folder_path)
