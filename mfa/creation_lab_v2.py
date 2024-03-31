import os

'''
    Creation de la trancritpion necessaire pour le mfa en fichier lab.
'''

def create_lab_file(wav_file):
    lab_file = wav_file.replace(".wav", ".lab")
    with open(lab_file, 'w') as f:
        f.write(os.path.splitext(os.path.basename(wav_file))[0])

def explore_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".wav"):
                wav_file = os.path.join(root, file)
                create_lab_file(wav_file)

folder_path = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\use_bdd\test_cut_lab"
explore_folder(folder_path)
