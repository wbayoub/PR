import parselmouth
import numpy as np


'''
    Creation de la bdd des phonemes avec les descripteurs pour les classifieur.
'''


def extract_formant_info(audio_file, N=5):
    # Charger l'enregistrement audio avec parselmouth
    audio = parselmouth.Sound(audio_file)

    # Calculer la durée totale de l'audio
    total_duration = audio.get_total_duration()

    # Calculer le time step proportionnel à la durée totale de l'audio
    time_step = total_duration / 1000

    # Extraire les formants avec parselmouth
    formants = audio.to_formant_burg(time_step=time_step, maximum_formant=8000)

    start = formants.t1
    time_step = formants.time_step
    n_frames = formants.nt

    time_intervals = [start + time_step * j for j in range(n_frames)]

    decoup = len(time_intervals) // N

    L_f = {}
    L_b = {}

    # Tracer les courbes des premières, deuxièmes, troisièmes et quatrièmes fréquences de résonance
    for i in range(1, 5):
        formant_frequence_values = [formants.get_value_at_time(i, t) for t in time_intervals]
        formant_bandwidth_values = [formants.get_bandwidth_at_time(i, t) for t in time_intervals]
        A_f = []
        A_b = []
        for j in range(N - 1):
            A_f.append(np.mean(formant_frequence_values[j * decoup:(j + 1) * decoup]))
            A_b.append(np.mean(formant_bandwidth_values[j * decoup:(j + 1) * decoup]))
        A_f.append(np.mean(formant_frequence_values[decoup * (N - 1):]))
        A_b.append(np.mean(formant_bandwidth_values[(N - 1) * decoup:]))
        L_f[i] = A_f
        L_b[i] = A_b

    return L_f, L_b

# Exemple d'utilisation de la fonction
audio_file = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\use_bdd\test_cut_lab\phoneme\phoneme_05\25\champignon_1933_050215_6.wav"
N = 5
L_f, L_b = extract_formant_info(audio_file, N)

print("Valeurs de L frequence : ", L_f)
print("Valeurs de L bandwidth : ", L_b)
