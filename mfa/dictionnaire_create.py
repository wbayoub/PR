
'''
    Creation d'un dictionnaire.
'''

# Chemin du fichier texte d'entrée
fichier_entree = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\dico\dico_v1.txt"
# Chemin du fichier texte de sortie
fichier_sortie = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\dico\dico_v5.txt"

space = True

# Ouvrir le fichier d'entrée en mode lecture avec encodage UTF-8
with open(fichier_entree, "r", encoding="utf-8") as entree:
    # Ouvrir le fichier de sortie en mode écriture avec encodage UTF-8
    with open(fichier_sortie, "w", encoding="utf-8") as sortie:
        try:
            # Lire chaque ligne du fichier d'entrée
            for ligne in entree:
                L = ligne.split('/')
                mot = L[0]
                phon = L[1].strip()  # Enlever les retours à la ligne
                
                # Votre code existant pour diviser phon en caractères
                phon = list(phon)
                
                # Vérifier chaque caractère de phon
                for i in range(len(phon)):
                    # Si le caractère est suivi d'un tilde, ne pas ajouter d'espace
                    if i + 1 < len(phon) and phon[i + 1] == '̃':
                        continue
                    else:
                        phon[i] = phon[i] + " "
                
                # Réassembler les caractères de phon en une seule chaîne
                phon = "".join(phon)
                
                ligne_new = str(mot) + "\t" + str(phon)  + "\n"
                
                sortie.write(ligne_new)
        
        finally:
            # Assurez-vous que les fichiers sont fermés même en cas d'erreur
            entree.close()
            sortie.close()

# Affichage de confirmation
print("Le contenu du fichier a été copié avec succès dans le fichier de sortie.")
