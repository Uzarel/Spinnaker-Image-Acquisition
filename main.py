import argparse
from bin import camera, ext_parameters
import PySpin


RAW_TEMPERATURES_PATH = 'raw_temperatures'
THERMAL_IMAGES_PATH = 'thermal_images'


def main(chosen_ir_type, radiometric_parameters = None):
    """
    Preparing and cleaning up the system.

    :return: True if successful, False otherwise.
    :rtype: bool
    """
    result = True

    # Retrieve singleton reference to system object
    system = PySpin.System.GetInstance()

    # Get current library version
    version = system.GetLibraryVersion()
    print('Library version: %d.%d.%d.%d' % (version.major, version.minor, version.type, version.build))

    # Retrieve list of cameras from the system
    cam_list = system.GetCameras()

    num_cameras = cam_list.GetSize()

    print('Number of cameras detected: %d' % num_cameras)

    # Finish if there are no cameras
    if num_cameras == 0:

        # Clear camera list before releasing system
        cam_list.Clear()

        # Release system instance
        system.ReleaseInstance()

        print('Not enough cameras!')
        print('Done!')
        return False

    # Run script on the first camera
    print('Running script for camera 0...')

    cam = cam_list[0]
    result &= camera.run_single_camera(cam, chosen_ir_type, radiometric_parameters)
    print('Camera 0 script complete... \n')

    # Release reference to camera
    # NOTE: Unlike the C++ scripts, we cannot rely on pointer objects being automatically
    # cleaned up when going out of scope.
    # The usage of del is preferred to assigning the variable to None.
    del cam

    # Clear camera list before releasing system
    cam_list.Clear()

    # Release system instance
    system.ReleaseInstance()

    print('Done!')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Takes a single image from a A700 FLIR camera")
    parser.add_argument("--ir_type", type=int, default=2, help="Chosen IR type for acquisition: '1' for LINEAR_10MK, '2' for LINEAR_100MK and '3' for RADIOMETRIC")
    args = parser.parse_args()
    
    chosen_ir_type = args.ir_type
    if args.ir_type == 3:
        radiometric_parameters = ext_parameters.get_radiometric_parameters()
        main(chosen_ir_type, radiometric_parameters)
    else:
        main(chosen_ir_type)
