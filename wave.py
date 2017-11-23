''' Present an interactive function explorer with slider widgets.
Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve wave.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/wave
in your browser.

per avviare il tutto basta includere fra le opzioni del run:
-m bokeh serve --show

'''
from random import Random
from threading import Timer

import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput, Button
from bokeh.plotting import figure
from yahoo_finance import Share


def refresh():

    yahoo = Share('YHOO')
    yahoo.get_open()
    val =  yahoo.get_price()
    yahoo.get_trade_datetime()

    #rndm = Random()
    #val = rndm.randint(0,4)
    x = np.linspace(0, 4 * np.pi, N) + val
    y = np.sin(x) + val
    source.data = dict(x=x, y=y)

# Set up data
N = 200
x = np.linspace(0, 4*np.pi, N)
y = np.sin(x)
source = ColumnDataSource(data=dict(x=x, y=y))


# Set up plot
plot = figure(plot_height=400, plot_width=400, title="my sine wave",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, 4*np.pi], y_range=[-2.5, 2.5])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)


# Set up widgets
text = TextInput(title="title", value='my sine wave')
offset = Slider(title="offset", value=0.0, start=-5.0, end=5.0, step=0.1)
amplitude = Slider(title="amplitude", value=1.0, start=-5.0, end=5.0, step=0.1)
phase = Slider(title="phase", value=0.0, start=0.0, end=2*np.pi)
freq = Slider(title="frequency", value=1.0, start=0.1, end=5.1, step=0.1)
btn = Button(label="refresh")

# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)


def update_data(attrname, old, new):

    # Get the current slider values
    a = amplitude.value
    b = offset.value
    w = phase.value
    k = freq.value

    # Generate the new curve
    x = np.linspace(0, 4*np.pi, N)
    y = a*np.sin(k*x + w) + b

    source.data = dict(x=x, y=y)

for w in [offset, amplitude, phase, freq, btn]:
    if w == btn:
        w.on_click(refresh)
    else:
        w.on_change('value', update_data)


# Set up layouts and add to document
inputs = widgetbox(text, offset, amplitude, phase, freq, btn)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"


