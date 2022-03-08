from .config_handler import get_config
from ftplib import FTP
import os
from pathlib import Path

def upload_to_ftp(local_path, ftp_folder):
    # Storing local_path file to an ftp_folder
    config = get_config()
    try:
        HOST = config['FTP']['HOST']
        USER = config['FTP']['USER']
        PASW = config['FTP']['PASW']
        FTP_PATH = config['PATHS']['FTP_PATH']
    except:
        print('Something went wrong while looking for keys in config file')
    
    local_path = Path(local_path)
    with FTP(HOST, USER, PASW) as ftp, open(local_path, 'rb') as file:
        ftp.storbinary(f'STOR {os.path.join(FTP_PATH, ftp_folder, local_path.name)}', file)
    print(f'Upload of {local_path.name} to the ftp completed!')