from bs4 import BeautifulSoup
import requests
import os
from urllib.parse import urljoin, urlparse


'''
    On précise l'url et on télécharge tout les fichiers présents en conservant l'architecture sur le serveur.
'''

ban = ["Name","Last modified","Size","Description","Parent Directory"]

def download_audio_from_folder_recursive(url, destination):
    """
    Télécharge les fichiers audio de manière récursive à partir d'un dossier racine donné.

    Args:
        url: URL du dossier racine.
        destination: Emplacement de destination des fichiers audio téléchargés.

    Returns:
        None
    """

    # Téléchargement des fichiers audio du dossier actuel
    download_audio_from_folder(url, destination)

    # Analyse du contenu de la page web
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Téléchargement des fichiers audio de chaque sous-dossier
    for link in soup.find_all('a', href=True):
        text = link.text.strip()  # Récupérer le texte de la balise <a>
        href = link['href']
        full_url = urljoin(url, href)
        if is_directory(full_url):
            if not text in ban:
                subdir_name = extract_folder_name(href)  # Extraire le nom du dossier
                subdir_destination = os.path.join(destination, subdir_name)
                print(f"Téléchargement du dossier : {subdir_name}")
                print(text)
                download_audio_from_folder_recursive(full_url, subdir_destination)

def extract_folder_name(href):
    """
    Extrait le nom du dossier à partir d'un lien relatif.

    Args:
        href: Lien relatif du dossier.

    Returns:
        str: Nom du dossier extrait.
    """
    url_parts = urlparse(href)
    folder_name = os.path.basename(url_parts.path.rstrip('/'))
    return folder_name



def download_audio_from_folder(url, destination):
    """
    Télécharge les fichiers audio d'un dossier à partir d'une URL.

    Args:
        url: URL du dossier à télécharger.
        destination: Emplacement de destination des fichiers audio téléchargés.

    Returns:
        None
    """

    # Création du dossier de destination
    if not os.path.exists(destination):
        os.makedirs(destination)

    # Téléchargement du contenu de la page web
    response = requests.get(url)

    # Si la requête est réussie
    if response.status_code == 200:
        # Analyse du contenu de la page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Téléchargement des fichiers audio
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(url, href)
            if is_audio_file(full_url):
                download_file(full_url, destination)

def is_audio_file(url):
    """
    Vérifie si l'URL pointe vers un fichier audio (MP3 ou WAV).

    Args:
        url: L'URL à vérifier.

    Returns:
        bool: True si le fichier est un fichier audio, False sinon.
    """
    parsed_url = urlparse(url)
    # Vérifie si l'URL pointe vers un fichier MP3 ou WAV
    return parsed_url.path.endswith(('.mp3', '.wav'))

def is_directory(url):
    """
    Vérifie si l'URL pointe vers un dossier.

    Args:
        url: L'URL à vérifier.

    Returns:
        bool: True si l'URL pointe vers un dossier, False sinon.
    """
    parsed_url = urlparse(url)
    # Vérifie si l'URL se termine par un '/'
    return parsed_url.path.endswith('/')

def download_file(url, destination):
    """
    Télécharge un fichier à partir d'une URL vers une destination donnée.

    Args:
        url: URL du fichier à télécharger.
        destination: Emplacement de destination du fichier téléchargé.

    Returns:
        None
    """
    response = requests.get(url)
    filename = os.path.basename(urlparse(url).path)
    with open(os.path.join(destination, filename), 'wb') as f:
        f.write(response.content)
    print(f"Téléchargement de {filename} terminé.")  # Ajout de l'instruction d'impression

# Exemple d'utilisation
url = 'https://media.talkbank.org/phon/French/Warnier/'
destination = r"C:\Users\wassi\Documents\Pcloud_files\Ecole\Cours\3A\Projet_recherche\BDD\Eureka"

download_audio_from_folder_recursive(url, destination)
