from astropynamics.models.EphemerisModel import EphemerisModel
from datetime import datetime


def GeometricSolarSystem():

    SolarSystemModel = EphemerisModel()
    SolarSystemModel.name = "The Solar System"
    SolarSystemModel.kernel = "solarsystem.tm"
    SolarSystemModel.objects = dict(SUN=10, MERCURY=1, VENUS=2, EARTH=3, MARS=4, JUPITER=5, SATURN=6, URANUS=7,
                                    NEPTUNE=8)
    SolarSystemModel.center = 'SUN'
    SolarSystemModel.target = 'EARTH'
    SolarSystemModel.frame = 'J2000'
    SolarSystemModel.plane = 0
    SolarSystemModel.vector_type = 'Geometric'
    SolarSystemModel.epoch = datetime.now()
    SolarSystemModel.offset = 0
    SolarSystemModel.duration = 730
    SolarSystemModel.step_size = 'Day'

    return SolarSystemModel


def ApparentSolarSystem():

    SolarSystemModel = EphemerisModel()
    SolarSystemModel.name = "Apparent Solar System"
    SolarSystemModel.kernel = "solarsystem.tm"
    SolarSystemModel.objects = dict(SUN=10, MERCURY=1, VENUS=2, EARTH=3, MARS=4, JUPITER=5, SATURN=6, URANUS=7,
                                    NEPTUNE=8)
    SolarSystemModel.center = 'SUN'
    SolarSystemModel.target = 'EARTH'
    SolarSystemModel.frame = 'J2000'
    SolarSystemModel.plane = 0
    SolarSystemModel.vector_type = 'Apparent'
    SolarSystemModel.epoch = datetime.now()
    SolarSystemModel.offset = 0
    SolarSystemModel.duration = 730
    SolarSystemModel.step_size = 'Day'

    return SolarSystemModel


def SunEarthMoon():

    SunEarthMoonModel = EphemerisModel()
    SunEarthMoonModel.name = "Sun Earth-Moon System"
    SunEarthMoonModel.kernel = "solarsystem.tm"
    SunEarthMoonModel.objects = dict(SUN=10, EARTH=399, MOON=301)
    SunEarthMoonModel.center = 'EARTH'
    SunEarthMoonModel.target = 'MOON'
    SunEarthMoonModel.frame = 'ECLIPJ2000'
    SunEarthMoonModel.plane = 0
    SunEarthMoonModel.vector_type = 'Geometric'
    SunEarthMoonModel.epoch = datetime.now()
    SunEarthMoonModel.offset = 0
    SunEarthMoonModel.duration = 365
    SunEarthMoonModel.step_size = 'Day'

    return SunEarthMoonModel


def JunoTransferTrajectory():

    JunoHeliocentricModel = EphemerisModel()
    JunoHeliocentricModel.name = "Juno Heliocentric Trajectory"
    JunoHeliocentricModel.kernel = "juno.tm"
    JunoHeliocentricModel.objects = dict(JUNO=-61, SUN=10, EARTH=3, JUPITER=5)
    JunoHeliocentricModel.center = 'SUN'
    JunoHeliocentricModel.target = 'JUNO'
    JunoHeliocentricModel.frame = 'J2000'
    JunoHeliocentricModel.plane = 0
    JunoHeliocentricModel.vector_type = 'Geometric'
    JunoHeliocentricModel.epoch = datetime.strptime('2011-08-05', "%Y-%m-%d")
    JunoHeliocentricModel.offset = 0
    JunoHeliocentricModel.duration = 730
    JunoHeliocentricModel.step_size = 'Day'

    return JunoHeliocentricModel


def JunoJovianTrajectory():

    JunoHeliocentricModel = EphemerisModel()
    JunoHeliocentricModel.name = "Juno Jovian Trajectory"
    JunoHeliocentricModel.kernel = "juno.tm"
    JunoHeliocentricModel.objects = dict(JUNO=-61, JUPITER=599, IO=516, EUROPA=515, GANYMEDE=514, CALLISTO=505,
                                         AMALTHEA=504, THEBE=503, ADRASTEA=502, METIS=501)
    JunoHeliocentricModel.center = 'JUPITER'
    JunoHeliocentricModel.target = 'JUNO'
    JunoHeliocentricModel.frame = 'ECLIPJ2000'
    JunoHeliocentricModel.plane = 1
    JunoHeliocentricModel.vector_type = 'Geometric'
    JunoHeliocentricModel.epoch = datetime.strptime('2016-08-26', "%Y-%m-%d")
    JunoHeliocentricModel.offset = 0
    JunoHeliocentricModel.duration = 60
    JunoHeliocentricModel.step_size = 'Hour'

    return JunoHeliocentricModel


def JwstHaloOrbitModel():

    JunoHeliocentricModel = EphemerisModel()
    JunoHeliocentricModel.name = "JWST Halo Orbit"
    JunoHeliocentricModel.kernel = "l2lagrange.tm"
    JunoHeliocentricModel.objects = dict(JWST=-170, L2=392, EARTH_BARYCENTER=3, EARTH=399, MOON=301, SUN=10)
    JunoHeliocentricModel.center = 'L2'
    JunoHeliocentricModel.target = 'JWST'
    JunoHeliocentricModel.frame = 'RLP'
    JunoHeliocentricModel.plane = 0
    JunoHeliocentricModel.vector_type = 'Geometric'
    JunoHeliocentricModel.epoch = datetime.strptime('2018-10-01', "%Y-%m-%d")
    JunoHeliocentricModel.offset = 0
    JunoHeliocentricModel.duration = 730
    JunoHeliocentricModel.step_size = 'Day'

    return JunoHeliocentricModel

def Mars2020Model():

    JunoHeliocentricModel = EphemerisModel()
    JunoHeliocentricModel.name = "MARS 2020"
    JunoHeliocentricModel.kernel = "mars2020.tm"
    JunoHeliocentricModel.objects = dict(PERSEVERANCE=-168, MARS=4, EARTH=399, SUN=10)
    JunoHeliocentricModel.center = 'SUN'
    JunoHeliocentricModel.target = 'PERSEVERANCE'
    JunoHeliocentricModel.frame = 'J2000'
    JunoHeliocentricModel.plane = 0
    JunoHeliocentricModel.vector_type = 'Geometric'
    JunoHeliocentricModel.epoch = datetime.strptime('2020-07-01', "%Y-%m-%d")
    JunoHeliocentricModel.offset = 0
    JunoHeliocentricModel.duration = 365
    JunoHeliocentricModel.step_size = 'Day'

    return JunoHeliocentricModel

