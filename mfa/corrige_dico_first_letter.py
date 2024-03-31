
'''
    Correction du ditionnaire en mettant toute les lettres en minuscules.
'''

def change_first_letter_to_lowercase(file_path):
    """
    Change the first letter of each line in a text file to lowercase.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    modified_lines = []
    for line in lines:
        if line.strip():  # Ignore les lignes vides
            modified_line = line[0].lower() + line[1:]
        else:
            modified_line = line  # Conserver les lignes vides telles quelles
        modified_lines.append(modified_line)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(modified_lines)

# Exemple d'utilisation :
file_path = r"C:\Users\wassi\Documents\MFA\pretrained_models\dictionary\dico_v5.txt"
change_first_letter_to_lowercase(file_path)
