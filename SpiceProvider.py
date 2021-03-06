import spiceypy
import pandas as pd
import datetime as dt
import s3manager

from bokeh.models import ColumnDataSource


class SpiceProvider(object):

    STATE_COLUMNS = ['px', 'py', 'pz', 'vx', 'vy', 'vz']

    CORRECTIONS = dict(Apparent='LT+S', Geometric='None')
    INTERVALS = dict(Day="D", Hour="H", Minute="T", Second="S")

    SPICE_IDS = dict(SUN=10, MERCURY=1, VENUS=2, EARTH=3, EARTH_CENTER=399, MOON=301, MARS=4, JUPITER=5,
                     SATURN=6, URANUS=7, NEPTUNE=8, PLUTO=9, JUNO=-61)
    SPICE_NAMES = {v: k for k, v in SPICE_IDS.items()}

    def __init__(self):

        self.meta_kernel = None
        self.center = '10'
        self.frame = 'J2000'
        self.correction = 'LT+S'

        self.ephemeris_data = pd.DataFrame(columns=SpiceProvider.STATE_COLUMNS)
        self.ephemeris_source = ColumnDataSource()

        self.state_data = pd.DataFrame(columns=SpiceProvider.STATE_COLUMNS+['radii'])
        self.state_source = ColumnDataSource()

        self.cum_data = pd.DataFrame(columns=SpiceProvider.STATE_COLUMNS.append('radii'))
        self.cum_source = ColumnDataSource(self.cum_data)


    def set_meta_kernel(self, kernel):

        if kernel == self.meta_kernel:
            return

        if self.meta_kernel is not None:
            spiceypy.unload(self.meta_kernel)

        if kernel is not None:
            s3manager.get_meta_kernel(kernel)
            spiceypy.furnsh(kernel)

        self.meta_kernel = kernel

    def set_center(self, center):
        self.center = self.fromName(center)

    def get_et(self, utctime):

        if isinstance(utctime, dt.datetime):
            utctime = dt.datetime.strftime(utctime, "%d %b %Y %H:%M:%S")

        return spiceypy.str2et(utctime)

    def fetch_state(self, target, epoch):

        target = self.fromName(target)
        try:
            state, lt = spiceypy.spkezr(str(target), self.get_et(epoch), self.frame, self.correction, str(self.center))
        except spiceypy.utils.exceptions.SpiceSPKINSUFFDATA:
            print(f"Insufficient SPICE data exception was raised for {target} at {epoch}", flush=True)
            state = [None]*6

        return {k: v for k, v in zip(SpiceProvider.STATE_COLUMNS, state)}

    def fetch_ephemeris_states(self, target, epoch_start, epoch_stop, interval):

        if interval not in SpiceProvider.INTERVALS:
            return

        date_range = pd.date_range(epoch_start, epoch_stop, freq=SpiceProvider.INTERVALS[interval])[:500]
        states = {epoch: self.fetch_state(target, epoch) for epoch in date_range}

        self.ephemeris_data = pd.DataFrame.from_dict(states, orient='index')
        self.ephemeris_source.data = self.ephemeris_data.reset_index().to_dict(orient='list')

    def fetch_target_states(self, targets, epoch, prime_target=None):

        states = {self.fromId(target): self.fetch_state(target, epoch) for target in targets}

        self.state_data = pd.DataFrame.from_dict(states, orient='index')

        self.state_data['radii'] = self.fetch_radii(targets)
        self.state_data['radii'] = self.state_data['radii'] / self.state_data['radii'].max() * 12
        self.state_data['radii'] = self.state_data['radii'].apply(lambda r: r if r > 4 else 4)

        self.state_source.data = self.state_data.reset_index().to_dict(orient='list')

        if prime_target is not None:
            self.cum_source.stream(self.state_data[self.state_data.index == prime_target], rollover=2000)

    def fetch_radii(self, targets):
        targets = [self.fromName(t) for t in targets]
        radii = [10] * len(targets)
        for k, target in enumerate(targets):
            try:
                radii[k] = spiceypy.bodvrd(target, 'RADII', 3)[1][0]
            except spiceypy.utils.exceptions.SpiceKERNELVARNOTFOUND:
                pass

        return radii

    def fetch_kernels(self):
        count = spiceypy.ktotal('ALL')
        return [spiceypy.kdata(i, 'ALL') for i in range(count)]

    @staticmethod
    def reset_source(source):
        source.data = pd.DataFrame(columns=SpiceProvider.STATE_COLUMNS)

    def setSpiceIds(self, newIds):
        self.SPICE_IDS = newIds
        self.SPICE_NAMES = {v: k for k, v in newIds.items()}

    def fromId(self, spiceId):
        return self.SPICE_NAMES[spiceId] if spiceId in self.SPICE_NAMES else str(spiceId)

    def fromName(self, name):
        return str(self.SPICE_IDS[name]) if name in self.SPICE_IDS else str(name)




