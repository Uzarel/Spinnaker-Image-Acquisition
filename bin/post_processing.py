from .config_handler import get_config
import datetime
from .ftp import upload_to_ftp
from matplotlib import pyplot as plt
import numpy as np
import os


def save_ndarray_to_file(ndarray, ftp=True):
    # Saving NDArray to raw file using a timestamp as label, additionally it can store those data to an ftp
    config = get_config()
    try:
        RAW_TEMPERATURES_PATH = config['PATHS']['RAW_TEMPERATURES_PATH']
        THERMAL_IMAGES_PATH = config['PATHS']['THERMAL_IMAGES_PATH']
        VMIN = int(config['THERMAL']['VMIN'])
        VMAX = int(config['THERMAL']['VMAX'])
    except:
        print('Something went wrong while looking for keys in config file')
    timestamp = datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S-%p")
    npy_path = os.path.join(RAW_TEMPERATURES_PATH, f'{timestamp}.npy')
    png_path = os.path.join(THERMAL_IMAGES_PATH, f'{timestamp}.png')
    with open(npy_path, 'wb') as file:
        np.save(file, ndarray)
    plt.imsave(png_path, ndarray, vmin=VMIN, vmax=VMAX, cmap='turbo')
    # Uploads these files to an ftp server according to the config file
    if ftp:
        upload_to_ftp(npy_path, RAW_TEMPERATURES_PATH)
        upload_to_ftp(png_path, THERMAL_IMAGES_PATH)

def get_maximum(ndarray):
    # Retrieves the maximum of a ndarray within the central block according to tolerance
    config = get_config()
    try:
        SHAPE_TOLERANCE = float(config['THERMAL']['SHAPE_TOLERANCE'])
    except:
        print('Something went wrong while looking for keys in config file')
    ndarray_shape = ndarray.shape
    height, width = ndarray_shape
    return np.amax(ndarray[int(height*SHAPE_TOLERANCE/2):height-int(height*SHAPE_TOLERANCE/2)][int(width*SHAPE_TOLERANCE/2):width-int(width*SHAPE_TOLERANCE/2)])