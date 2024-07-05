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
    
    os.open(os.path.join(directory, 'Textes'), exit_Ok = True )
    os.open(os.path.join(directory, 'Images'), exit_Ok = True )
    os.open(os.path.join(directory, 'Audio'), exit_Ok = True )
    os.open(os.path.join(directory, 'Html'), exit_Ok = True )
    
    for filename in os.listdir(directory):
        file_path =  os.path.join(directory, filename)
        
        if os.path.isfile(file_path): 
            file_extention = os.path.splitext(filename)
            
            if file_extention == '.html':
                  new_file_path = os.path.join(directory, 'Html', filenamle)
            elif file_extention == '.txt':
                  new_file_path = os.path.join(directory, 'Texte', filenamle)
            elif file_extention in ('.mp3',  '.wav'):
                  new_file_path = os.path.join(directory, 'Audio', filenamle)
            elif file_extention in ('.jpg', '.png'):
                  new_file_path = os.path.join(directory, 'Image', filenamle)
                  os.replace(file_path, new_file_path)
                
           
                
                
            