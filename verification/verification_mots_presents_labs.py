import glob
import re


'''
    On récuperer la liste des mots présent dans les fichiers lab.
'''

def extract_words_from_lab_files(folder_path):
    # Utiliser glob pour trouver tous les fichiers .lab dans le dossier spécifié
    lab_files = glob.glob(folder_path + "/*.lab")

    # Initialiser un ensemble pour stocker tous les mots
    all_words = set()

    # Parcourir chaque fichier .lab
    for lab_file in lab_files:
        # Lire le contenu du fichier .lab
        with open(lab_file, 'r', encoding='utf-8') as file:
            content = file.read()

        # Utiliser une expression régulière pour extraire tous les mots (séparés par des espaces)
        words = re.findall(r'\b\w+\b', content)

        # Ajouter les mots à l'ensemble des mots
        all_words.update(words)

    return all_words

# Exemple d'utilisation :
folder_path = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\use_bdd\test_cut_lab\1903\050114"
all_words = extract_words_from_lab_files(folder_path)
print("Tous les mots présents dans les fichiers .lab du dossier :", all_words)
