import librosa
import numpy as np
import os

'''
    Création des fichier texgrid pour la transcription necessaire pour le mfa.
'''

def generate_textgrid_with_sound_levels(audio_file, threshold_db=-25):
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

    # Créer le contenu du fichier TextGrid avec les intervalles correspondant au niveau sonore détecté
    content = """File type = "ooTextFile"
Object class = "TextGrid"

xmin = 0
xmax = {}
tiers? <exists>
size = 1
item []:
    item [1]:
        class = "IntervalTier"
        name = "Words"
        xmin = 0
        xmax = {}
        intervals: size = 1
        intervals [1]:
            xmin = {}
            xmax = {}
            text = {}
""".format(len(y)/sr, len(y)/sr, start_index/sr, end_index/sr, name)
    
    return content

def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".wav"):
                audio_file = os.path.join(root, file)
                textgrid_content = generate_textgrid_with_sound_levels(audio_file)
                output_folder = root
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                output_file = os.path.join(output_folder, os.path.splitext(file)[0] + ".TextGrid")
                with open(output_file, "w") as f:
                    f.write(textgrid_content)

# Exemple d'utilisation
folder_path = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\use_bdd\test_cut"
process_folder(folder_path)
