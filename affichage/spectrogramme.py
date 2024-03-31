import numpy as np
import matplotlib.pyplot as plt
import librosa.display
from matplotlib import gridspec


'''
    On affiche le spéctrorgramme pour un fichier wav, on affiche aussi en dessous le spectre en amplitude de ce fichier audio.
'''

# Charger le fichier audio WAV
audio_path = r"C:\Users\wassi\Documents\3A\PR\Champignon.wav"
data, sample_rate = librosa.load(audio_path, sr=None)

# Générer le vecteur de temps
time = np.linspace(0, len(data) / sample_rate, len(data))

# Créer une figure avec une grille spécifique
fig = plt.figure(figsize=(10, 8))
gs = gridspec.GridSpec(2, 3, width_ratios=[10, 1, 1], height_ratios=[3, 1])  # Diviser la figure en 2 lignes et 3 colonnes

# Spectrogramme en puissance
ax1 = plt.subplot(gs[0, :-2])  # Utiliser la première ligne et les deux premières colonnes
S = librosa.feature.melspectrogram(y=data, sr=sample_rate)
S_dB = librosa.power_to_db(S, ref=np.max)
img = librosa.display.specshow(S_dB, sr=sample_rate, x_axis='time', y_axis='mel', ax=ax1)
ax1.set_title('Power Spectrogram')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Frequency (Mel)')

# Barre de couleur
cbar_ax = plt.subplot(gs[0, -2])  # Utiliser la première ligne et la troisième colonne
cbar = plt.colorbar(img, cax=cbar_ax, format='%+2.0f dB')
cbar.set_label('Amplitude')  # Modifier le label de la légende

# Tracer la courbe d'amplitude en fonction du temps
ax2 = plt.subplot(gs[1, :-2])  # Utiliser la deuxième ligne et les deux premières colonnes
ax2.plot(time, data)
ax2.set_title('Amplitude vs Time')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Amplitude')

plt.tight_layout()

plt.show()
