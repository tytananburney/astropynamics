from bokeh.io import curdoc
from app.EphemerisApp import EphemerisApp

# Builds the entire application
ephemerisApp = EphemerisApp()
curdoc().add_root(ephemerisApp.get_layout())

