import os
import re
import csv

'''
    On a les découpages et on etudie ici le nombre de bon découpage et d'erreures
    Tout ceci fini stockée dans le fichiers csv présent a la fin du text.
'''


# Dossier racine à partir duquel vous souhaitez parcourir les sous-dossiers
root_folder = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\use_bdd\test_cut_lab"

M = "04"
file_name = "output_" + M + ".csv"
# Définir le chemin de sortie du fichier CSV
output_csv_path = os.path.join(root_folder,file_name)

# Initialiser un dictionnaire pour stocker les mots et le comptage de "spn"
mot_compteur_spn = {}
mot_compteur_non_spn = {}


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
                    # Extraire les textes et les compter
                    textes_extraits = re.findall(r'text = "(.*?)"', contenu)
                    k=0
                    if len(textes_extraits) >= 2:  # Vérifier s'il y a assez de textes extraits
                        while textes_extraits[k]=="":
                            k += 1
                        mot = textes_extraits[k]  # Le deuxième texte extrait est le mot
                        if mot == "www":
                            continue
                        # Compter le nombre de "spn"
                        nb_spn = textes_extraits.count("spn")
                        if nb_spn > 0 :
                            # Mettre à jour le compteur de "spn" pour ce mot
                            mot_compteur_spn[mot] = mot_compteur_spn.get(mot, 0) + 1
                        else : 
                            mot_compteur_non_spn[mot] = mot_compteur_non_spn.get(mot, 0) + 1

# Écrire les données dans un fichier CSV
with open(output_csv_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    # Écrire l'en-tête
    writer.writerow(["Mot", "Nombre de Silence","Nombre de Réussite","Total"])
    
    # Obtenir l'ensemble des clés de chaque dictionnaire
    keys_spn = set(mot_compteur_spn.keys())
    keys_non_spn = set(mot_compteur_non_spn.keys())
    
    # Obtenir l'union des deux ensembles de clés
    all_keys = keys_spn.union(keys_non_spn)
    # Parcourir toutes les clés
    for mot in all_keys:
        nb_spn = mot_compteur_spn.get(mot, 0)
        nb_non_spn = mot_compteur_non_spn.get(mot, 0)
        writer.writerow([mot, nb_spn, nb_non_spn,nb_spn+nb_non_spn])

print("Données enregistrées dans", output_csv_path)
