# TODO LATER: Insert logic for radiometric parameters acquisition (maybe from a weather station)
def get_radiometric_parameters():
    # Default parameters to eventually setup
    Emiss = 0.95 # To enstablish (0.95 according to mastitis literature)
    TRefl = 293.15 # To enstablish
    TAtm = 293.15 # To measure via a weather station
    TAtmC = TAtm - 273.15
    Humidity = 0.55 # To measure via a weather station

    Dist = 2 # To enstablish
    ExtOpticsTransmission = 1 # To enstablish
    ExtOpticsTemp = TAtm
    
    radiometric_parameters = {
        'Emiss': Emiss,
        'TRefl': TRefl,
        'TAtm': TAtm,
        'TAtmC': TAtmC,
        'Humidity': Humidity,
        'Dist': Dist,
        'ExtOpticsTransmission': ExtOpticsTransmission,
        'ExtOpticsTemp': ExtOpticsTemp
        }
    return radiometric_parameters
