import os
import unicodedata


'''
    Nom explicite, ici on supprime les accents dans les fichiers de transcription pour mfa.
'''

def remove_accents(text):
    """
    Remove accents from a given text.
    """
    return ''.join(char for char in unicodedata.normalize('NFD', text)
                   if unicodedata.category(char) != 'Mn')

def process_lab_file(file_path):
    """
    Process a .lab file and remove accents from its content.
    """
    with open(file_path, 'r', encoding='latin-1') as file:
        content = file.read()
    content_without_accents = remove_accents(content)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content_without_accents)


def process_directory(directory):
    """
    Recursively process a directory and its subdirectories.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.lab'):
                file_path = os.path.join(root, file)
                process_lab_file(file_path)

# Chemin du répertoire à traiter
directory_path = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\use_bdd\test_cut_lab"

# Appel de la fonction pour traiter le répertoire
process_directory(directory_path)
