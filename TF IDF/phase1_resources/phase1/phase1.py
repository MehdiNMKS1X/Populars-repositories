import os
import zipfile
def decompress_archive(zip_path: str, extract_to: str) -> None: 
    """ Decompresse l’archive ZIP specifiee dans le chemin zip_path vers le repertoire extract_to.
    :param zip_path: Chemin vers le fichier ZIP a decompresser :param extract_to: Repertoire de destination pour les fichiers
    extraits.
    """ 
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        



def organize_files(directory: str) -> None:
    """
    Organise les fichiers dans le repertoire specifie en les classant dans des sous-dossiers selon leur type.
    :param directory: Chemin du repertoire contenant les fichiers a organiser.
    """
    
    os.makedirs(os.path.join(directory, 'Textes'), exist_ok = True )
    os.makedirs(os.path.join(directory, 'Images'), exist_ok = True )
    os.makedirs(os.path.join(directory, 'Audio'), exist_ok = True )
    os.makedirs(os.path.join(directory, 'Html'), exist_ok = True )
    
    for filename in os.listdir(directory):
      file_path =  os.path.join(directory, filename)
        
      if os.path.isfile(file_path): 
            file_extention = os.path.splitext(filename)
                        
            if file_extention[1] == '.html':
                  new_file_path = os.path.join(directory, 'Html', filename)
                  os.rename(file_path, new_file_path)
            elif file_extention[1] == '.txt':
                  new_file_path = os.path.join(directory, 'Textes', filename)
                  os.rename(file_path, new_file_path)
            elif file_extention[1] in ('.mp3',  '.wav'):
                  new_file_path = os.path.join(directory, 'Audio', filename)
                  os.rename(file_path, new_file_path)
            elif file_extention[1] in ('.jpg', '.png'):
                  new_file_path = os.path.join(directory, 'Images', filename)
                  os.rename(file_path, new_file_path)

decompress_archive("./phase1_resources.zip", ".")

organize_files("./phase1_resources")
            