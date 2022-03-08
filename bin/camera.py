from .post_processing import save_ndarray_to_file, get_maximum
import PySpin
import numpy as np


class IRFormatType:
    LINEAR_10MK = 1
    LINEAR_100MK = 2
    RADIOMETRIC = 3


def acquire_image(cam, nodemap, nodemap_tldevice, chosen_ir_type, radiometric_parameters):
    """
    This function acquires an image from a device.

    :param cam: Camera to acquire images from.
    :param nodemap: Device nodemap.
    :param nodemap_tldevice: Transport layer device nodemap.
    :type cam: CameraPtr
    :type nodemap: INodeMap
    :type nodemap_tldevice: INodeMap
    :return: True if successful, False otherwise.
    :rtype: bool
    """

    sNodemap = cam.GetTLStreamNodeMap()

    # Change bufferhandling mode to NewestOnly
    node_bufferhandling_mode = PySpin.CEnumerationPtr(sNodemap.GetNode('StreamBufferHandlingMode'))

    node_pixel_format = PySpin.CEnumerationPtr(nodemap.GetNode('PixelFormat'))
    node_pixel_format_mono16 = PySpin.CEnumEntryPtr(node_pixel_format.GetEntryByName('Mono16'))
    pixel_format_mono16 = node_pixel_format_mono16.GetValue()
    node_pixel_format.SetIntValue(pixel_format_mono16)

    if chosen_ir_type == IRFormatType.LINEAR_10MK:
        # This section is to be activated only to set the streaming mode to TemperatureLinear10mK
        node_IRFormat = PySpin.CEnumerationPtr(nodemap.GetNode('IRFormat'))
        node_temp_linear_high = PySpin.CEnumEntryPtr(node_IRFormat.GetEntryByName('TemperatureLinear10mK'))
        node_temp_high = node_temp_linear_high.GetValue()
        node_IRFormat.SetIntValue(node_temp_high)
    elif chosen_ir_type == IRFormatType.LINEAR_100MK:
        # This section is to be activated only to set the streaming mode to TemperatureLinear100mK
        node_IRFormat = PySpin.CEnumerationPtr(nodemap.GetNode('IRFormat'))
        node_temp_linear_low = PySpin.CEnumEntryPtr(node_IRFormat.GetEntryByName('TemperatureLinear100mK'))
        node_temp_low = node_temp_linear_low.GetValue()
        node_IRFormat.SetIntValue(node_temp_low)
    elif chosen_ir_type == IRFormatType.RADIOMETRIC:
        # This section is to be activated only to set the streaming mode to Radiometric
        node_IRFormat = PySpin.CEnumerationPtr(nodemap.GetNode('IRFormat'))
        node_temp_radiometric = PySpin.CEnumEntryPtr(node_IRFormat.GetEntryByName('Radiometric'))
        node_radiometric = node_temp_radiometric.GetValue()
        node_IRFormat.SetIntValue(node_radiometric)

    if not PySpin.IsAvailable(node_bufferhandling_mode) or not PySpin.IsWritable(node_bufferhandling_mode):
        print('Unable to set stream buffer handling mode.. Aborting...')
        return False

    # Retrieve entry node from enumeration node
    node_newestonly = node_bufferhandling_mode.GetEntryByName('NewestOnly')
    if not PySpin.IsAvailable(node_newestonly) or not PySpin.IsReadable(node_newestonly):
        print('Unable to set stream buffer handling mode.. Aborting...')
        return False

    # Retrieve integer value from entry node
    node_newestonly_mode = node_newestonly.GetValue()

    # Set integer value from entry node as new value of enumeration node
    node_bufferhandling_mode.SetIntValue(node_newestonly_mode)

    print('*** IMAGE ACQUISITION ***\n')
    try:
        node_acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
        if not PySpin.IsAvailable(node_acquisition_mode) or not PySpin.IsWritable(node_acquisition_mode):
            print('Unable to set acquisition mode to SingleFrame (enum retrieval). Aborting...')
            return False

        # Retrieve entry node from enumeration node
        node_acquisition_mode_singleframe = node_acquisition_mode.GetEntryByName('SingleFrame')
        if not PySpin.IsAvailable(node_acquisition_mode_singleframe) or not PySpin.IsReadable(
                node_acquisition_mode_singleframe):
            print('Unable to set acquisition mode to SingleFrame (entry retrieval). Aborting...')
            return False

        # Retrieve integer value from entry node
        acquisition_mode_singleframe = node_acquisition_mode_singleframe.GetValue()

        # Set integer value from entry node as new value of enumeration node
        node_acquisition_mode.SetIntValue(acquisition_mode_singleframe)

        print('Acquisition mode set to SingleFrame...')

        #  Begin acquiring images
        #
        #  *** NOTES ***
        #  What happens when the camera begins acquiring images depends on the
        #  acquisition mode. Single frame captures only a single image, multi
        #  frame catures a set number of images, and continuous captures a
        #  continuous stream of images.
        #
        #  *** LATER ***
        #  Image acquisition must be ended when no more images are needed.
        cam.BeginAcquisition()

        print('Acquiring images...')

        #  Retrieve device serial number for filename
        #
        #  *** NOTES ***
        #  The device serial number is retrieved in order to keep cameras from
        #  overwriting one another.
        device_serial_number = ''
        node_device_serial_number = PySpin.CStringPtr(nodemap_tldevice.GetNode('DeviceSerialNumber'))
        if PySpin.IsAvailable(node_device_serial_number) and PySpin.IsReadable(node_device_serial_number):
            device_serial_number = node_device_serial_number.GetValue()
            print('Device serial number retrieved as %s...' % device_serial_number)

        # Retrieve Calibration details
        CalibrationQueryR_node = PySpin.CFloatPtr(nodemap.GetNode('R'))
        R = CalibrationQueryR_node.GetValue()
        print('R =', R)

        CalibrationQueryB_node = PySpin.CFloatPtr(nodemap.GetNode('B'))
        B = CalibrationQueryB_node.GetValue()
        print('B =', B)

        CalibrationQueryF_node = PySpin.CFloatPtr(nodemap.GetNode('F'))
        F = CalibrationQueryF_node.GetValue()
        print('F =', F)

        CalibrationQueryX_node = PySpin.CFloatPtr(nodemap.GetNode('X'))
        X = CalibrationQueryX_node.GetValue()
        print('X =', X)

        CalibrationQueryA1_node = PySpin.CFloatPtr(nodemap.GetNode('alpha1'))
        A1 = CalibrationQueryA1_node.GetValue()
        print('alpha1 =', A1)

        CalibrationQueryA2_node = PySpin.CFloatPtr(nodemap.GetNode('alpha2'))
        A2 = CalibrationQueryA2_node.GetValue()
        print('alpha2 =', A2)

        CalibrationQueryB1_node = PySpin.CFloatPtr(nodemap.GetNode('beta1'))
        B1 = CalibrationQueryB1_node.GetValue()
        print('beta1 =', B1)

        CalibrationQueryB2_node = PySpin.CFloatPtr(nodemap.GetNode('beta2'))
        B2 = CalibrationQueryB2_node.GetValue()
        print('beta2 =', B2)

        CalibrationQueryJ1_node = PySpin.CFloatPtr(nodemap.GetNode('J1'))    # Gain
        J1 = CalibrationQueryJ1_node.GetValue()
        print('Gain =', J1)

        CalibrationQueryJ0_node = PySpin.CIntegerPtr(nodemap.GetNode('J0'))   # Offset
        J0 = CalibrationQueryJ0_node.GetValue()
        print('Offset =', J0)

        if chosen_ir_type == IRFormatType.RADIOMETRIC:
            # Object Parameters
            # This section is important when the streaming is set to radiometric and not TempLinear
            # Image of temperature is calculated computer-side and not camera-side
            
            Emiss = radiometric_parameters['Emiss']
            TRefl = radiometric_parameters['TRefl']
            TAtm = radiometric_parameters['TAtm']
            TAtmC = radiometric_parameters['TAtmC']
            Humidity = radiometric_parameters['Humidity']
            Dist = radiometric_parameters['Dist']
            ExtOpticsTransmission = radiometric_parameters['ExtOpticsTransmission']
            ExtOpticsTemp = radiometric_parameters['ExtOpticsTemp']

            H2O = Humidity * np.exp(1.5587 + 0.06939 * TAtmC - 0.00027816 * TAtmC * TAtmC + 0.00000068455 * TAtmC * TAtmC * TAtmC)
            print('H20 =', H2O)

            Tau = X * np.exp(-np.sqrt(Dist) * (A1 + B1 * np.sqrt(H2O))) + (1 - X) * np.exp(-np.sqrt(Dist) * (A2 + B2 * np.sqrt(H2O)))
            print('tau =', Tau)

            # Pseudo radiance of the reflected environment
            r1 = ((1 - Emiss) / Emiss) * (R / (np.exp(B / TRefl) - F))
            print('r1 =', r1)

            # Pseudo radiance of the atmosphere
            r2 = ((1 - Tau) / (Emiss * Tau)) * (R / (np.exp(B / TAtm) - F))
            print('r2 =', r2)

            # Pseudo radiance of the external optics
            r3 = ((1 - ExtOpticsTransmission) / (Emiss * Tau * ExtOpticsTransmission)) * (R / (np.exp(B / ExtOpticsTemp) - F))
            print('r3 =', r3)

            K2 = r1 + r2 + r3
            print('K2 =', K2)

        # Retrieve image
        try:

            #  Retrieve next received image
            #
            #  *** NOTES ***
            #  Capturing an image houses images on the camera buffer. Trying
            #  to capture an image that does not exist will hang the camera.
            #
            #  *** LATER ***
            #  Once an image from the buffer is saved and/or no longer
            #  needed, the image must be released in order to keep the
            #  buffer from filling up.

            image_result = cam.GetNextImage(1000)

            #  Ensure image completion
            if image_result.IsIncomplete():
                print('Image incomplete with image status %d ...' % image_result.GetImageStatus())

            else:

                # Getting the image data as a np array
                image_data = image_result.GetNDArray()

                # Select the desired output first
                if chosen_ir_type == IRFormatType.LINEAR_10MK:
                    # Transforming the data array into a temperature array, if streaming mode is set to TemperatueLinear10mK
                    image_Temp = (image_data * 0.01) - 273.15
                    '''
                    # Displaying an image of temperature when streaming mode is set to TemperatureLinear10mK
                    plt.imshow(image_Temp, cmap='inferno', aspect='auto')
                    plt.colorbar(format='%.2f')
                    '''

                elif chosen_ir_type == IRFormatType.LINEAR_100MK:
                    # Transforming the data array into a temperature array, if streaming mode is set to TemperatureLinear100mK
                    image_Temp = (image_data * 0.1) - 273.15
                    '''
                    # Displaying an image of temperature when streaming mode is set to TemperatureLinear100mK
                    plt.imshow(image_Temp, cmap='inferno', aspect='auto')
                    plt.colorbar(format='%.2f')
                    '''

                elif chosen_ir_type == IRFormatType.RADIOMETRIC:
                    # Transforming the data array into a pseudo radiance array, if streaming mode is set to Radiometric.
                    # and then calculating the temperature array (degrees Celsius) with the full thermography formula
                    image_Radiance = (image_data - J0) / J1
                    image_Temp = (B / np.log(R / ((image_Radiance / Emiss / Tau) - K2) + F)) - 273.15
                    '''
                    # Displaying an image of temperature (degrees Celsius) when streaming mode is set to Radiometric
                    plt.imshow(image_Temp, cmap='inferno', aspect='auto')
                    plt.colorbar(format='%.2f')
                    '''
                    '''
                    # Displaying an image of counts when streaming mode is set to Radiometric
                    plt.imshow(image_data, cmap='inferno', aspect='auto')
                    plt.colorbar(format='%.2f')
                    '''
                    '''
                    # Displaying an image of pseudo radiance when streaming mode is set to Radiometric
                    plt.imshow(image_Radiance, cmap='inferno', aspect='auto')
                    plt.colorbar(format='%.2f')
                    '''
            
            # Saving both raw temperatures and image file according to vmin-vmax range
            save_ndarray_to_file(image_Temp, ftp=True)
            print(f'Maximum temperature: {get_maximum(image_Temp):.1f}')
            #  Release image
            #
            #  *** NOTES ***
            #  Images retrieved directly from the camera (i.e. non-converted
            #  images) need to be released in order to keep from filling the
            #  buffer.
            image_result.Release()

        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            return False

        #  End acquisition
        #
        #  *** NOTES ***
        #  Ending acquisition appropriately helps ensure that devices clean up
        #  properly and do not need to be power-cycled to maintain integrity.
        cam.EndAcquisition()

    except PySpin.SpinnakerException as ex:
        print('Error: %s' % ex)
        return False

    return True


def run_single_camera(cam, chosen_ir_type, radiometric_parameters):
    """
    This function acts as the body of the script; setting up cameras.

    :param cam: Camera to run on.
    :type cam: CameraPtr
    :return: True if successful, False otherwise.
    :rtype: bool
    """
    try:
        result = True

        nodemap_tldevice = cam.GetTLDeviceNodeMap()

        # Initialize camera
        cam.Init()

        # Retrieve GenICam nodemap
        nodemap = cam.GetNodeMap()
        
        # Acquire image
        result &= acquire_image(cam, nodemap, nodemap_tldevice, chosen_ir_type, radiometric_parameters)

        # Deinitialize camera
        cam.DeInit()

    except PySpin.SpinnakerException as ex:
        print('Error: %s' % ex)
        result = False

    return result
