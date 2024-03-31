import os
import librosa
import soundfile as sf


'''
    Suppression des silences au début et a la fin de chaque audio et enregistrement de ses derniers dans une autre folder.
'''

def cut_wav_with_silence_detection(input_file, output_folder, threshold_db=-25):
    """
    Cuts a WAV file into segments based on silence detection, preserving the directory structure.

    :param input_file: Path to the input WAV file.
    :param output_folder: Path to the output folder where the segments will be saved.
    :param threshold_db: Threshold level for silence detection (in dB).
    """
    # Charger le fichier audio
    y, sr = librosa.load(input_file, sr=None)

    # Convertir l'audio en amplitude en utilisant la transformée de Fourier
    amplitude = librosa.stft(y)

    # Calculer l'énergie (puissance) de chaque trame
    energy = librosa.feature.rms(S=amplitude)

    # Convertir l'énergie en décibels
    energy_db = librosa.amplitude_to_db(energy)

    # Trouver le début et la fin du son en fonction du seuil de silence
    start_index = 0
    end_index = len(y)
    for i in range(len(energy_db[0])):
        if energy_db[0][i] > threshold_db:
            start_index = i * 2048  # Taille de la fenêtre d'analyse de Fourier
            break
    for i in range(len(energy_db[0])-1, 0, -1):
        if energy_db[0][i] > threshold_db:
            end_index = (i+1) * 2048  # Taille de la fenêtre d'analyse de Fourier
            break

    # Découper l'audio en utilisant les indices de début et de fin du son
    trimmed_audio = y[start_index:end_index]

    # Récupérer le chemin relatif du fichier par rapport au dossier d'entrée
    relative_path = os.path.relpath(input_file, input_folder)

    # Générer le chemin de sortie pour le segment découpé
    output_file = os.path.join(output_folder, relative_path)

    # Créer les dossiers nécessaires dans le dossier de sortie
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Écrire le segment découpé dans le fichier de sortie
    sf.write(output_file, trimmed_audio, sr)


def cut_wavs_in_directory_with_silence_detection(input_folder, output_folder, threshold_db=-25):
    """
    Cuts all WAV files in a directory and its subdirectories into segments based on silence detection,
    preserving the directory structure.

    :param input_folder: Path to the input folder containing WAV files.
    :param output_folder: Path to the output folder where the segments will be saved.
    :param threshold_db: Threshold level for silence detection (in dB).
    """
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(".wav"):
                input_file = os.path.join(root, file)
                cut_wav_with_silence_detection(input_file, output_folder, threshold_db)


# Example usage:
input_folder = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\segmentation_test"
output_folder = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka\segmentation_test_cut"
cut_wavs_in_directory_with_silence_detection(input_folder, output_folder)
