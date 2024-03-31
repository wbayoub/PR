import parselmouth
import librosa
import matplotlib.pyplot as plt
import numpy as np


'''
    Affichage de 4 frequences les plus présentes dans chaque trame sous formesde courbes.
'''

# Charger l'enregistrement audio
audio_file = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\use_bdd\test_cut_lab\phoneme\test\2\bibliotheque_1903_050114_1.wav"

# Charger l'enregistrement audio avec parselmouth
audio = parselmouth.Sound(audio_file)

# Calculer la durée totale de l'audio
total_duration = audio.get_total_duration()

# Calculer le time step proportionnel à la durée totale de l'audio
time_step = total_duration / 1000

# Extraire les formants avec parselmouth
formants = audio.to_formant_burg(time_step=time_step, maximum_formant=8000)

# Initialiser une liste pour stocker les couleurs des courbes
colors = ['b', 'g', 'r', 'c']

start = formants.t1
time_step = formants.time_step
n_frames = formants.nt
print("time_step : " + str(time_step))

time_intervals = [ start + time_step * j for j in range(n_frames)]

L= {}
# Tracer les courbes des premières, deuxièmes, troisièmes et quatrièmes fréquences de résonance
for i in range(1,5):
    formant_values = [formants.get_value_at_time(i,t) for t in time_intervals]
    decoup = len(formant_values)//5
    A = []
    for j in range(4):
        A.append(np.mean(formant_values[j*decoup:(j+1)*decoup]))
    A.append(np.mean(formant_values[decoup*4:]))
    L[i] = A
    
    plt.plot(time_intervals, formant_values, color=colors[i-1], label=f'Formant {i}')

# Ajouter des titres et des légendes
plt.xlabel('Temps (s)')
plt.ylabel('Fréquence (Hz)')
plt.title('Évolution des formants au cours du temps')
plt.legend()

# Afficher le graphique
plt.show()

print("Valeurs de L : ", L)
# audio_data, sample_rate = librosa.load(audio_file)
# # Obtenir la durée totale de l'audio en secondes
# total_duration = librosa.get_duration(y=audio_data, sr=sample_rate)

# # Créer un vecteur de temps pour l'axe x
# time = librosa.samples_to_time(np.arange(len(audio_data)), sr=sample_rate)

# # Afficher la courbe d'amplitude dans le temps
# plt.figure(figsize=(10, 4))
# plt.plot(time, audio_data)
# plt.xlabel('Temps (s)')
# plt.ylabel('Amplitude')
# plt.title('Courbe d\'amplitude dans le temps')
# plt.grid(True)
# plt.show()

