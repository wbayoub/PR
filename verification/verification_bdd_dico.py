
'''
    Ici on compare la bdd du dcitonnaire pour le mfa et le dictionnaire des lettres possibles dans le modéles du mfa.
'''


L_bdd =  [
            'n',
            'ʃ',
            'w',
            'o',
            'ts',
            'p',
            'ø',
            'ɛ̃',
            'ɟ',
            'ŋ',
            'ɥ',
            'mʲ',
            'm',
            'l',
            'i',
            'ɔ̃',
            'ɛ',
            'v',
            'u',
            'k',
            'ə',
            'e',
            't',
            'ɑ',
            'd',
            'œ',
            'ʎ',
            'j',
            'ɑ̃',
            'ɔ',
            'z',
            'b',
            'tʃ',
            'y',
            'ʒ',
            's',
            'f',
            'ɡ',
            'a',
            'c',
            'ʁ',
            'ɲ',
            'dʒ'
         ]


L_dico =  ['a', 'b', 'd', 'e', 'f', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 's', 't', 'u', 'v', 'w', 'y', 'z', 'ø', 'œ', 'ɑ̃', 'ɔ', 'ɔ̃', 'ə', 'ɛ', 'ɛ̃', 'ɡ', 'ɥ', 'ɲ', 'ʁ', 'ʃ', 'ʒ']


# Caractères présents dans L_dico mais pas dans L_bdd
caracteres_uniquement_L_dico = []
for caractere in L_dico:
    if caractere not in L_bdd:
        caracteres_uniquement_L_dico.append(caractere)

# Caractères présents dans L_bdd mais pas dans L_dico
caracteres_uniquement_L_bdd = []
for caractere in L_bdd:
    if caractere not in L_dico:
        caracteres_uniquement_L_bdd.append(caractere)

print("Caractères présents dans L_dico mais pas dans L_bdd :", caracteres_uniquement_L_dico)
print("Caractères présents dans L_bdd mais pas dans L_dico :", caracteres_uniquement_L_bdd)