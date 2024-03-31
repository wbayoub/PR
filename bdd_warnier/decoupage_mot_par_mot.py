# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 10:38:41 2024

@author: wassi
"""

import wave
from pydub import AudioSegment
import os
import glob
from tqdm import tqdm


'''
    On découpe les fichiers audios selon la reranscription de la BDD, ce qui nous donne beaucoup de petit fichiers avec la prononciation de chaque mots par les enfants.
'''


def trouver_fichiers_xml(dossier):
    fichiers_xml = []
    # Parcours des dossiers et des fichiers dans le dossier spécifié
    for root, dirs, files in os.walk(dossier):
        # Recherche des fichiers XML dans les fichiers de ce dossier
        fichiers_xml.extend(glob.glob(os.path.join(root, '*.xml')))
    return fichiers_xml

# Chemin vers le fichier XML
fichier_xml = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\Warnier\1903\1903_030112.xml"

chemin_fichier_wav = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\bdd_warnier\1903\0wav\030112.wav"

EPSILON=200
# Définir le chemin du dossier par défaut
dossier_par_defaut = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\test_cut"

# Définir le dossier par défaut
os.chdir(dossier_par_defaut)

def cut_list(path_fichier_xml):

    decoupage = []
    
    # Ouvrir le fichier XML en mode lecture
    with open(path_fichier_xml, 'r', encoding='utf-8') as fichier:
        # Variable pour indiquer si nous sommes à l'intérieur de la balise <orthography>
        dans_orthographe = False
        apres_orthographe = False
        
        # Lire chaque ligne du fichier
        for ligne in fichier:
            # Vérifier si la ligne contient la balise <orthography>
            if "<orthography>" in ligne:
                # Indiquer que nous sommes maintenant à l'intérieur de la balise <orthography>
                dans_orthographe = True
            # Vérifier si nous sommes à l'intérieur de la balise <orthography>
            elif dans_orthographe:
                # Vérifier si la ligne contient la balise <w>
                if "<w>" in ligne:
                    # Extraire le texte de la balise <w>
                    mot = ligne.strip().split(">")[1].split("<")[0]
                # Vérifier si la ligne contient la balise <segment>
                elif "</orthography>" in ligne : 
                    dans_orthographe = False
                    apres_orthographe = True
            elif apres_orthographe : 
                if "<segment" in ligne:
                    # Extraire les attributs de la balise <segment>
                    attributs_segment = ligne.strip().split("<segment ")[1].split(">")[0]
                    L = attributs_segment.split(" ")
                    start = float(L[0].split("=")[-1].strip('"'))
                    fin = start + float(L[1].split("=")[-1].strip('"'))
                    
                    decoupage.append([mot,start,fin])
                    
                    apres_orthographe = False
    return decoupage

def cut_audio(L,chemin_fichier_wav,path_output):
    
    # Charger le fichier audio
    audio = AudioSegment.from_wav(chemin_fichier_wav)
    
    for l in L : 
        name = l[0]
        debut_segment = l[1]
        fin_segment = l[-1]
        if not os.path.exists(path_output):
            # Créer le dossier
            os.makedirs(path_output)
        # Découper le fichier audio en segments
        segment = audio[debut_segment:fin_segment]
        segment.export(path_output + "\\" + name + ".wav", format="wav")

def cut_audio_epsilon(L, chemin_fichier_wav, path_output, epsilon=EPSILON):
    # Charger le fichier audio
    audio = AudioSegment.from_wav(chemin_fichier_wav)
    
    for l in L: 
        name = l[0]
        debut_segment = max(0, float(l[1]) - epsilon)  # Ajout d'un epsilon avant le début du segment
        fin_segment = min(len(audio), float(l[-1]) + epsilon)  # Ajout d'un epsilon après la fin du segment
        
        if not os.path.exists(path_output):
            # Créer le dossier s'il n'existe pas
            os.makedirs(path_output)
        
        # Découper le fichier audio en segments
        segment = audio[debut_segment:fin_segment]
        segment.export(os.path.join(path_output, name + ".wav"), format="wav")        


def trouver_fichiers_xml(dossier):
    fichiers_xml = []
    # Parcours des dossiers et des fichiers dans le dossier spécifié
    for root, dirs, files in os.walk(dossier):
        # Recherche des fichiers XML dans les fichiers de ce dossier
        fichiers_xml.extend(glob.glob(os.path.join(root, '*.xml')))
    return fichiers_xml

def supprimer_audios(dossier):
    # Parcourir tous les éléments (fichiers et dossiers) dans le dossier spécifié et ses sous-dossiers
    for root, dirs, files in os.walk(dossier):
        for fichier in files:
            chemin_fichier = os.path.join(root, fichier)
            # Vérifier si le fichier est un fichier audio avec l'extension .wav
            if fichier.endswith(".wav"):
                # Supprimer le fichier audio
                os.remove(chemin_fichier)


# M = cut_list(fichier_xml)
# nom_enregistrement = "030112"
# cut_audio(M,chemin_fichier_wav,nom_enregistrement)

# Utilisation de la fonction pour trouver les fichiers XML dans un dossier spécifique
dossier = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\Warnier"

fichiers_xml = trouver_fichiers_xml(dossier)

# supprimer_audios(dossier_output)

# Utilisation de tqdm pour afficher la barre de progression
for file in tqdm(fichiers_xml, desc="Chargement des fichiers XML"): 
    fichier_xml = file 
    # # Partie wav
    C = file.split(".")
    total_c = C[0].split("\\")
    total_c_output = total_c.copy()
    
    
    indice_a_remplacer = total_c.index("Warnier")  
    total_c[indice_a_remplacer] = "bdd_warnier"  
    total_c_output[indice_a_remplacer] = "test_cut"
    
    total_c.insert(-1,"0wav")
    name = total_c[-1].split("_")[1]
    
    total_c[-1] = name
    total_c[-1] = name + ".wav"
    total_c_output.pop()
    total_c_output.append(name)
    
    total_c_output_epsilon = total_c_output.copy()
    total_c_output_epsilon[indice_a_remplacer] = "cut_epsilon" + "_" + str(EPSILON)
    
    path_fichier_wav = "//".join(total_c)
    path_output = "//".join(total_c_output)
    path_output_epislon = "//".join(total_c_output_epsilon)

    
    list_cut = cut_list(fichier_xml)
    cut_audio(list_cut,path_fichier_wav,path_output)
    cut_audio_epsilon(list_cut,path_fichier_wav,path_output_epislon)
    
# print(path_fichier_wav)
# print(path_output)
# print(path_output_epislon)

    



