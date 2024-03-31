import os
import re
import csv
from pydub import AudioSegment

'''
    Tentative de découpage avec mfa a partir de retranscription textgrid.
'''

def couper_audio(chemin_audio, debut, fin, chemin_sortie):
    # Charger le fichier audio
    audio = AudioSegment.from_wav(chemin_audio)
    
    # Découper l'audio
    audio_coupe = audio[debut:fin]
    
    # Exporter l'audio découpé
    audio_coupe.export(chemin_sortie, format="wav")
    

# Dossier racine à partir duquel vous souhaitez parcourir les sous-dossiers
root_folder = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\use_bdd\test_cut_lab"
S = {'a': 1, 'b': 2, 'd': 3, 'e': 4, 'f': 5, 'i': 6, 'j': 7, 'k': 8, 'l': 9, 'm': 10, 'n': 11, 'o': 12, 'p': 13, 's': 14, 't': 15, 'u': 16, 'v': 17, 'w': 18, 'y': 19, 'z': 20, 'ø': 21, 'œ': 22, 'ɑ̃': 23, 'ɔ': 24, 'ɔ̃': 25, 'ə': 26, 'ɛ': 27, 'ɛ̃': 28, 'ɡ': 29, 'ɥ': 30, 'ɲ': 31, 'ʁ': 32, 'ʃ': 33, 'ʒ': 34}
L = ['a', 'b', 'd', 'e', 'f', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 's', 't', 'u', 'v', 'w', 'y', 'z', 'ø', 'œ', 'ɑ̃', 'ɔ', 'ɔ̃', 'ə', 'ɛ', 'ɛ̃', 'ɡ', 'ɥ', 'ɲ', 'ʁ', 'ʃ', 'ʒ']

M = "05"
# M = "05"
# Définir le chemin de sortie du fichier CSV (NE PAS CHANGER !!!!!!!!!!!!!!)
output_phoneme_path = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\use_bdd\test_cut_lab\phoneme\phoneme_" + M 

seuil = 0.03

# Parcourir les dossiers et sous-dossiers
for root, dirs, files in os.walk(root_folder):
    for directory in dirs:
        if directory == "outputs":
            if not root.split("\\")[-1].startswith(M) : 
                continue
            dossier_a_parcourir = os.path.join(root, directory)
            for fichier in os.listdir(dossier_a_parcourir):
                if not fichier.endswith(".TextGrid"):
                    continue
                chemin_fichier = os.path.join(dossier_a_parcourir, fichier)
                # Ouvrir le fichier en mode lecture
                with open(chemin_fichier, "r", encoding="utf-8") as f:
                    # Lire le contenu du fichier
                    contenu = f.read()
                    # Expression régulière pour rechercher les lignes correspondant aux phonèmes
                    expression = r'intervals \[(\d+)\]:\s*xmin = ([\d.]+)\s*xmax = ([\d.]+)\s*text = "(.*?)"'
                    
                    # Recherche des correspondances dans le contenu
                    correspondances = re.findall(expression, contenu)
                    
                    mot = None
                    k = 0
                    # Affichage des intervalles de temps pour chaque phonème
                    for _,xmin, xmax, phoneme in correspondances:
                        if phoneme == "":
                            continue
                        elif mot == None : 
                            mot = phoneme
                        elif phoneme in L :
                            k += 1 
                            chemin_parent = os.path.dirname(dossier_a_parcourir)
                            nom = fichier.split('.')[0] + ".wav"
                            path_input_wav = os.path.join(chemin_parent,nom)
                            
                            num = str(S[phoneme])
                            path_output_dir_wav = os.path.join(output_phoneme_path,num)
                            
                            age = dossier_a_parcourir.split("\\")[-2]
                            id_enfant = dossier_a_parcourir.split("\\")[-3]
                            name_wav_output = mot + "_" + id_enfant + "_" + age + "_" +str(k) + ".wav"
                            
                            path_output_wav_file = os.path.join(path_output_dir_wav,name_wav_output)
                            
                            x = float(xmin)
                            y=float(xmax)
                            
                            start = (x-(y-x)*seuil)*1000
                            end = (y+(y-x)*seuil)*1000
                            couper_audio(path_input_wav, start, end, path_output_wav_file)
                        else : 
                            print("Erreur dans la detection des phonemes !! ")
                            print(mot)
