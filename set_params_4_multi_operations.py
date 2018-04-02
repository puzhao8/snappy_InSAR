
from snappy import HashMap
def setParams4MultiOperations(subswath, polarization, burstStart, burstEnd):
    ### Set Params
    params = {
        # TOPSAR-split
        "subswath": subswath,
        "selectedPolarisations": polarization,
        "firstBurstIndex": burstStart,
        "lastBurstIndex": burstEnd,

        # Apply-Orbit-File
        "continuteOnFail": True,
        "orbitType": "Sentinel Precise (Auto Download)",

        # back-Geocoding
        "demResamplingMethod": "BICUBIC_INTERPOLATION",
        "resamplingType": "BISINC_5_POINT_INTERPOLATION",
        "maskOutAreaWithoutElevation": True,
        "outputDerampDemodPhase": True,

        # Interferogram
        "subtractFlatEarthPhase": True,
        "srpPolynomialDegree": 5,  # Order of 'Flat earth phase' polynomial
        "srpNumberPoints": 501,  # Number of points for the 'flat earth phase' polynomial estimation
        "includeCoherence": True,
        "squarePixel": False,
        "Independent Window Sizes": False,
        "cohWinAz": 10,  # Size of coherence estimation window in Azimuth direction
        "cohWinRg": 10,  # Size of coherence estimation window in Range direction

        # TOPSAR-Deburst

        # TopoPhaseRemoval
        "orbitDegree": 3,
        "tileExtensionPercent": '100',
        "outputTopoPhaseBand=": True,  # Output topographic phase band

        # Multilook
        "grSquarePixel": False,
        "nRgLooks": 20,  # Number of Range Looks
        "nAzLooks": 4,  # Number of Azimuth Looks

        # GoldsteinPhaseFiltering
        "alpha": 1.0,  # adaptive filter exponent Valid interval is (0, 1].

        # Terrain-Correction
        "pixelSpacingInMeter": 80.0,
        "outputComplex": True,
        "demName":'SRTM 3Sec',
        "imgResamplingMethod": 'NEAREST_NEIGHBOUR'
    }

    # Parameters Assignments
    parameters = HashMap()
    for a in params:
        # print(a)
        parameters.put(a, params[a])

    return parameters