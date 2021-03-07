from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Slider, Button, DatePicker, Select, RadioButtonGroup, Tabs, Panel
from bokeh.models.widgets.markups import Div
from bokeh.models.widgets.tables import DateFormatter, NumberFormatter, DataTable, TableColumn
from bokeh.plotting import figure
from bokeh.models import BoxZoomTool
from bokeh.core.enums import TextAlign

import inspect
import pandas as pd
from datetime import datetime

from SpiceProvider import SpiceProvider
from models import StandardEphemerisModels


class EphemerisApp:

    to_seconds = dict(Day=86400, Hour=3600, Minute=60, Second=1)

    def __init__(self):

        # app variables
        self.active = True
        self.playAnimation = None
        self.start_epoch = None
        self.stop_epoch = None
        self.current_epoch = None

        # get initial configuration
        self.available_models = inspect.getmembers(StandardEphemerisModels, inspect.isfunction)
        self.ephemeris_model = self.available_models[0][1]()
        self.spice_provider = SpiceProvider()
        self.spice_provider.SPICE_IDS = self.ephemeris_model.objects
        self.spice_provider.SPICE_NAMES = {v: k for k, v in self.ephemeris_model.objects.items()}

        # init data sources
        self.plot_source = self.spice_provider.state_source
        self.table_source = self.spice_provider.ephemeris_source
        self.cum_source = self.spice_provider.cum_source

        # gather options from ephemeris model and spice provider
        allowed_models = [model[0] for model in self.available_models]
        allowed_objects = [self.spice_provider.fromId(name) for name in self.ephemeris_model.objects]
        allowed_frames = self.ephemeris_model.FRAMES
        allowed_corrections = [name for name in SpiceProvider.CORRECTIONS]
        allowed_durations = [str(v) for v in self.ephemeris_model.DURATION_DAYS]
        allowed_intervals = [name for name in SpiceProvider.INTERVALS]

        # set up widgets
        self.model = Select(
            title="Ephemeris Model",
            value=self.ephemeris_model.name,
            options=allowed_models)

        self.center = Select(
            title="Center",
            value=self.ephemeris_model.center,
            options=allowed_objects)

        self.target = Select(
            title="Target",
            value=self.ephemeris_model.target,
            options=allowed_objects)

        self.frames = Select(
            title="Frame",
            value=self.ephemeris_model.frame,
            options=allowed_frames)

        self.planes = RadioButtonGroup(
            labels=['XY', 'YZ', 'XZ'],
            active=0)

        self.vector = Select(
            title='Vector Type',
            value=self.ephemeris_model.vector_type,
            options=allowed_corrections)

        self.epoch = DatePicker(
            title="Select Epoch",
            value=datetime.strftime(self.ephemeris_model.epoch, "%Y-%m-%d"))

        self.offset = Slider(
            title="Days Since Epoch",
            value=self.ephemeris_model.offset,
            start=0,
            end=self.ephemeris_model.duration,
            step=1)

        self.duration = Select(
            title="Duration (Days)",
            value=str(self.ephemeris_model.duration),
            options=allowed_durations)

        self.interval = Select(
            title="Time Step",
            value=str(self.ephemeris_model.step_size),
            options=allowed_intervals)

        # create buttons
        self.play_button = Button(label="Play")
        self.exportRange = Div(text="Start and Stop Epoch: ")
        self.update_button = Button(label="Play")
        self.export_button = Button(label="Export")

        self.infoDiv = Div(text="<hr>All ephemeris data shown on this website was obtained from publicly available "
                                "SPICE files located at <a href='https://naif.jpl.nasa.gov/naif/data.html'>"
                                "https://naif.jpl.nasa.gov/naif/data.html</a>, which is hosted by the  "
                                "Navigation and Ancillary Information Facility (NAIF) at the NASA Jet Propulsion "
                                "Laboratory. The exception is the SPICE kernel for the Parker Solar Probe, which is "
                                "available at <a href='https://sppgway.jhuapl.edu/ancil_products'>"
                                "https://sppgway.jhuapl.edu/ancil_products</a>, hosted by the Johns Hopkins University "
                                "Applied Physics Laboratory. SpiceyPy is being used to process the SPICE files.",
                           sizing_mode='stretch_width')

        # create plot tab objects
        self.plot = figure(match_aspect=True,
                           sizing_mode="stretch_both",
                           title="Astropynamics",
                           tools="hover, pan, reset, save",
                           tooltips=[("name", "@index")])

        self.plot.add_tools(BoxZoomTool(match_aspect=True))
        self.plot.circle('px', 'py', size='radii', source=self.plot_source, line_width=3, line_alpha=0.5, name='XY')
        self.plot.circle('px', 'pz', size='radii', source=self.plot_source, line_width=3, line_alpha=0.5, name='XZ').visible = False
        self.plot.circle('py', 'pz', size='radii', source=self.plot_source, line_width=3, line_alpha=0.5, name='YZ').visible = False
        self.plot.line('px', 'py', source=self.cum_source, line_width=2, line_alpha=0.5, color='red', name='XYOrbit')
        self.plot.line('px', 'pz', source=self.cum_source, line_width=2, line_alpha=0.5, color='red', name='XZOrbit').visible = False
        self.plot.line('py', 'pz', source=self.cum_source, line_width=2, line_alpha=0.5, color='red', name='YZOrbit').visible = False

        self.plotLayout = column(self.plot, self.offset, sizing_mode="stretch_width")
        self.plotTab = Panel(child=self.plotLayout, title="Display")

        # create data table tab objects
        fmt = NumberFormatter(format='0.000', text_align=TextAlign.right)
        columns = [
            TableColumn(field="index", title="Epoch", formatter=DateFormatter(format="%m/%d/%Y %H:%M:%S")),
            TableColumn(field="px", title="PX", formatter=fmt, width=10),
            TableColumn(field="py", title="PY", formatter=fmt),
            TableColumn(field="pz", title="PZ", formatter=fmt),
            TableColumn(field="vx", title="VX", formatter=fmt),
            TableColumn(field="vy", title="VY", formatter=fmt),
            TableColumn(field="vz", title="VZ", formatter=fmt)
        ]

        self.ephemerisTable = DataTable(source=self.table_source, columns=columns, sizing_mode="stretch_both")
        self.ephemerisLayout = column(self.exportRange, self.ephemerisTable, sizing_mode="stretch_width")
        self.dataTab = Panel(child=self.ephemerisLayout, title="Table")

        self.kernels = Div()
        self.kernelTab = Panel(child=self.kernels, title="Kernels")

        self.tabs = Tabs(tabs=[self.plotTab, self.dataTab, self.kernelTab])

        # init data
        self.update_model(None, 0, 'SolarSystem')
        self.update_epochs(None, 0, 0)
        self.update_states(None, 0, 0)

        self.model.on_change('value', self.update_model)
        self.frames.on_change('value', self.update_epochs)
        self.planes.on_change('active', self.update_plot_view)
        self.center.on_change('value', self.update_epochs)
        self.target.on_change('value', self.update_epochs)
        self.offset.on_change('value', self.update_offset)
        self.epoch.on_change('value', self.update_epochs)
        self.duration.on_change('value', self.update_epochs)
        self.interval.on_change('value', self.update_epochs)
        self.update_button.on_click(self.update_onclick)
        self.tabs.on_change('active', self.update_button_type)

        self.inputs = column(self.model,
                             self.frames,
                             self.planes,
                             self.center,
                             self.target,
                             self.epoch,
                             self.duration,
                             self.interval,
                             self.update_button)

    def get_layout(self):
        return column(row([self.inputs, self.tabs]), self.infoDiv, sizing_mode='stretch_width')

    def update_kenerls_tab(self):
        kernels = self.spice_provider.fetch_kernels()
        kernel_text = "<h3>Loaded Spice Kernels:</h3>\n"
        kernel_text += '<table>\n'
        for k in kernels:
            kernel_text += f"<tr><td><b>{k[1]}&emsp;&emsp;</b></td><td>{k[0].split('/')[-1]}</td></tr>\n"
        self.kernels.text = kernel_text + "</table>"

    def update_model(self, attr, old, new):

        # disable callbacks
        self.active = False

        # update model and load new kernel
        self.ephemeris_model = dict(self.available_models)[new]()
        self.spice_provider.set_meta_kernel(self.ephemeris_model.kernel)
        self.spice_provider.setSpiceIds(self.ephemeris_model.objects)

        self.update_kenerls_tab()

        # set widget values
        allowed_objects = [self.spice_provider.fromId(name) for name in self.ephemeris_model.objects]
        allowed_frames = self.ephemeris_model.FRAMES
        allowed_durations = [str(v) for v in self.ephemeris_model.DURATION_DAYS]
        self.target.options = allowed_objects
        self.center.options = allowed_objects
        self.frames.options = allowed_frames
        self.duration.options = allowed_durations

        self.target.value = self.ephemeris_model.target
        self.center.value = self.ephemeris_model.center
        self.frames.value = self.ephemeris_model.frame
        self.planes.active = self.ephemeris_model.plane
        self.epoch.value = datetime.strftime(self.ephemeris_model.epoch, "%Y-%m-%d")
        self.duration.value = str(self.ephemeris_model.duration)
        self.offset.value = self.ephemeris_model.offset
        self.offset.end = self.ephemeris_model.duration
        self.interval.value = self.ephemeris_model.step_size

        # reinstate callbacks
        self.active = True

        # update start and stop epochs and plot
        self.update_epochs(None, 0, 0)

    def update_epochs(self, attr, old, new):

        self.start_epoch = datetime.strptime(self.epoch.value, "%Y-%m-%d")
        self.stop_epoch = self.start_epoch + \
                          pd.Timedelta(seconds=(int(float(self.duration.value) * EphemerisApp.to_seconds['Day'])))

        self.offset.value = 0
        self.offset.end = int(float(self.duration.value) *
                              EphemerisApp.to_seconds['Day'] / EphemerisApp.to_seconds[self.interval.value])
        self.offset.title = f"{self.interval.value}s Since Epoch"
        self.exportRange.text = f"Showing epoch range:\t<b>{self.start_epoch} to {self.stop_epoch}</b>"

        self.update_offset(None, 0, 0)

    def update_offset(self, attr, old, new):

        scale_factor = EphemerisApp.to_seconds[self.interval.value]
        self.current_epoch = self.start_epoch + pd.Timedelta(seconds=(self.offset.value * scale_factor))

        if self.playAnimation is None:
            SpiceProvider.reset_source(self.spice_provider.cum_source)

        self.update_states(None, 0, 0)

    def update_ephemeris(self, attr, old, new):

        self.update_epochs(attr, old, new)

        self.spice_provider.set_center(self.center.value)
        self.spice_provider.frame = self.frames.value
        self.spice_provider.correction = SpiceProvider.CORRECTIONS[self.vector.value]

        if self.active:
            self.spice_provider.fetch_ephemeris_states(
                self.target.value,
                self.start_epoch,
                self.stop_epoch,
                self.interval.value)

    def update_states(self, attr, old, new):

        self.spice_provider.set_center(self.center.value)
        self.spice_provider.frame = self.frames.value
        self.spice_provider.correction = SpiceProvider.CORRECTIONS[self.vector.value]

        if self.active:
            self.spice_provider.fetch_target_states(
                self.ephemeris_model.objects,
                self.current_epoch,
                self.target.value)

    def update_plot_view(self, attr, old, new):

        self.plot.select_one({"name": self.planes.labels[old]}).visible = False
        self.plot.select_one({"name": self.planes.labels[new]}).visible = True

        self.plot.select_one({"name": self.planes.labels[old] + "Orbit"}).visible = False
        self.plot.select_one({"name": self.planes.labels[new] + "Orbit"}).visible = True

    def animate_update(self):

        self.offset.value = 0 if self.offset.value > self.offset.end else self.offset.value + 1
        if self.offset.value == 0:
            SpiceProvider.reset_source(self.spice_provider.cum_source)

    def animate(self, start=True):
        if self.update_button.label == 'Play' and start:
            self.update_button.label = 'Pause'
            self.playAnimation = curdoc().add_periodic_callback(self.animate_update, 50)
        elif self.playAnimation is not None:
            self.update_button.label = 'Play'
            curdoc().remove_periodic_callback(self.playAnimation)
            self.playAnimation = None

    def update_onclick(self):
        if self.tabs.active == 0:
            self.animate()
        elif self.tabs.active == 1:
            self.update_ephemeris(None, 0, 0)
        elif self.tabs.active == 2:
            self.update_kenerls_tab()

    def update_button_type(self, attr, old, new):
        self.animate(False)
        if self.tabs.active == 0:
            self.update_button.label = "Play"
        else:
            self.update_button.label = "Update"
            self.update_ephemeris(None, 0, 0)

