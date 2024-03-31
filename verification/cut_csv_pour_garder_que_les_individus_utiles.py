import csv


'''
    On scan le fichier csv et on ne récupere que les individus qui ont une durée supérieur au treshold seuil, si oui alors on garde sinon on ne garde pas dans la nouvelle bdd csv.
    L'idée est de ne conserver que les individus qui ont des enregistrements suffisament longs pour être analysée par les méthodes de formants.
'''

# Chemin du fichier CSV d'entrée
input_csv_path = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\use_bdd\test_cut_lab\phoneme\analyse\analyse_total_test_for_train.csv"

# Seuil pour le tri des valeurs
seuil = (0.042395833333333334 + 0.05297916666666667)/2

# Chemins des fichiers CSV de sortie
output_csv_sup_seuil = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\use_bdd\test_cut_lab\phoneme\analyse\analyse_total_test_for_train_no_nan.csv"
output_csv_inf_seuil = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\use_bdd\test_cut_lab\phoneme\analyse\analyse_total_test_for_train_with_nan.csv"

# Ouvrir le fichier CSV d'entrée en mode lecture
with open(input_csv_path, "r", newline="", encoding="utf-8") as input_file:
    # Ouvrir les fichiers CSV de sortie en mode écriture
    with open(output_csv_sup_seuil, "w", newline="", encoding="utf-8") as output_file_sup_seuil, \
         open(output_csv_inf_seuil, "w", newline="", encoding="utf-8") as output_file_inf_seuil:
        
        # Créer des lecteurs pour le fichier CSV d'entrée
        reader = csv.reader(input_file)
        
        # Créer des écrivains pour les fichiers CSV de sortie
        writer_sup_seuil = csv.writer(output_file_sup_seuil)
        writer_inf_seuil = csv.writer(output_file_inf_seuil)
        
        # Lire l'en-tête du fichier CSV d'entrée
        header = next(reader)
        
        # Écrire les en-têtes dans les fichiers CSV de sortie
        writer_sup_seuil.writerow(header)
        writer_inf_seuil.writerow(header)
        
        # Parcourir chaque ligne du fichier CSV d'entrée
        for row in reader:
            # Récupérer la valeur de la colonne B
            valeur_b = float(row[1])  # Assurez-vous d'adapter l'indice selon la position de la colonne B dans votre fichier
            
            # Vérifier si la valeur de la colonne B est supérieure ou égale au seuil
            if valeur_b >= seuil:
                # Écrire la ligne dans le fichier CSV de sortie des valeurs supérieures au seuil
                writer_sup_seuil.writerow(row)
            else:
                # Écrire la ligne dans le fichier CSV de sortie des valeurs inférieures au seuil
                writer_inf_seuil.writerow(row)

print("Fichiers CSV créés avec succès !")
