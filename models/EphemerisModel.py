import numpy as np
from datetime import datetime


class EphemerisModel:

    FRAMES = ['J2000', 'ECLIPJ2000', 'GSE', 'RLP']
    DURATION_DAYS = [0.5, 1, 7, 14, 30, 60, 90, 365, 730, 1825]

    def __init__(self):

        self.name = ''

        self.objects = []
        self.center = ''
        self.target = ''

        self.frame = ''
        self.plane = ''
        self.vector_type = ''

        self.epoch = datetime.now()
        self.offset = -1
        self.duration = -1
        self.step_size = ''


class OrbitState:

    def __init__(self, position, velocity=None, attitude=None, rate=None, epoch=None):

        self.epoch = None
        self.px = None
        self.py = None
        self.pz = None
        self.vx = None
        self.vy = None
        self.vz = None
        self.qs = None
        self.qx = None
        self.qy = None
        self.qz = None
        self.rx = None
        self.ry = None
        self.rz = None

        if position is None:
            print("Error: Position cannot be None")
            return

        self.setPosition(position)

        if velocity is not None:
            self.setVelocity(velocity)

        if attitude is not None:
            self.setAttitude(attitude)

        if rate is not None:
            self.setRate(rate)

        if epoch is not None:
            self.setEpoch(epoch)

    def setPosition(self, position):
        # Check position has 3 elements
        if len(position) != 3:
            print("Error: Position must an array with 3 elements.")
            return

        self.px = position[0]
        self.py = position[1]
        self.pz = position[2]

    def setVelocity(self, velocity):
        # Check velocity has 3 elements
        if len(velocity) != 3:
            print("Error: Velocity must an array with 3 elements.")
            return

        self.vx = velocity[0]
        self.vy = velocity[1]
        self.vz = velocity[2]

    def setAttitude(self, attitude):
        # Check that attitude has 4 elements
        if len(attitude) != 4:
            print("Error: Attitude must an array with 4 elements.")
            return

        # Check that attitude is a unit quaternion
        if np.linalg.norm(attitude) != 1:
            print("Warning: Input quaternion is not a unit quaternion. Normalizing input...")
            attitude /= np.linalg.norm(attitude)

        # Set attitude
        self.qs = attitude[0]
        self.qx = attitude[1]
        self.qy = attitude[2]
        self.qz = attitude[3]

    def setRate(self, rate):
        # Check rate has 3 elements
        if len(rate) != 3:
            print("Error: Rate must an array with 3 elements.")
            return

        self.rx = rate[0]
        self.ry = rate[1]
        self.rz = rate[2]

    def setEpoch(self, epoch):
        if isinstance(epoch, int) or isinstance(epoch, float):
            self.epoch = datetime.fromtimestamp(float(epoch))
        elif isinstance(epoch, str):
            self.epoch = datetime.fromisoformat(epoch)
        elif isinstance(epoch, datetime):
            self.epoch = epoch
        else:
            print('Error: Epoch not set. Epoch must be a UTC timestamp, ISO Format date string, or datetime object.')

    def getPosition(self):
        return [self.px, self.py, self.pz]

    def getVelocity(self):
        return [self.vx, self.vy, self.vz]

    def getAttitude(self):
        return [self.qs, self.qx, self.qy, self.qz]

    def getRate(self):
        return [self.rx, self.ry, self.rz]

    def getEpoch(self):
        return self.epoch
