import os
import subprocess


'''
    Réalisation de la transcription phonétiques avce le mfa en réalisation l'exetuion de chaque commande en invite de commande
'''

# Fonction pour créer un dossier "outputs" dans le dossier donné
def create_outputs_folder(folder_path):
    outputs_folder = os.path.join(folder_path, "outputs")
    os.makedirs(outputs_folder, exist_ok=True)
    return outputs_folder

# Fonction pour exécuter la commande mfa align
def execute_mfa_align(input_folder, output_folder):
    command = f"mfa align --clean {input_folder} dico_v5 french_mfa {output_folder}"
    subprocess.run(command, shell=True)

# Dossier racine
root_folder = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\use_bdd\test_cut_lab"

# Listes pour stocker les chemins des dossiers "05" et des dossiers "outputs"
folders_05 = []
folders_outputs = []

# Parcourir les dossiers et sous-dossiers
for root, dirs, files in os.walk(root_folder):
    for folder in dirs:
        if folder.startswith("04"):
            folder_path = os.path.join(root, folder)
            # Vérifier s'il y a des fichiers WAV dans ce dossier
            wav_files = [file for file in os.listdir(folder_path) if file.lower().endswith(".wav")]
            if wav_files:
                # Créer le dossier "outputs" et obtenir son chemin
                outputs_folder = create_outputs_folder(folder_path)
                # Ajouter les chemins des dossiers "05" et des dossiers "outputs" aux listes
                folders_05.append(folder_path)
                folders_outputs.append(outputs_folder)

# Écrire les commandes dans un fichier batch
with open(r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\commands_04.txt", "w") as bat_file:
    bat_file.write("@echo on\n")
    k = 0
    # Parcourir les dossiers "05" et les dossiers "outputs"
    for folder_05, folder_output in zip(folders_05, folders_outputs):
        k += 1
        bat_file.write(f"rem {k}\n")
        # Écrire la commande correspondante dans le fichier batch
        command = f"mfa align --clean --single_speaker {folder_05} dico_v5 french_mfa {folder_output}\n\n"
        bat_file.write(command)

print("Les commandes ont été écrites dans le fichier commands.bat.")
