#!/usr/bin/env python3

import tkinter as tk
import numpy as np
import dicom
from PIL import Image
from PIL import ImageTk


def show_image(data, block=True, master=None):
    '''
    Get minimal Tkinter GUI and display a pydicom data.pixel_array

    data: object returned from pydicom.read_file()
    block: if True run Tk mainloop() to show the image
    master: use with block==False and an existing Tk widget as parent widget

    '''
    mode = 'I'
    size = (data.Columns,data.Rows)

    # create frame
    frame = tk.Frame(master=master, background='#000', width=data.Columns, height=data.Rows)
    if 'SeriesDescription' in data and 'InstanceNumber' in data:
        title = ', '.join(('Ser: ' + data.SeriesDescription,
                           'Img: ' + str(data.InstanceNumber)))
    else:
        title = 'dicom image'
    frame.master.title(title)

    # create a tkimage
    pillowimage = Image.frombuffer(mode,size,data.pixel_array.astype(np.int32),'raw',mode,0,1)
    tkimage = ImageTk.PhotoImage(pillowimage)

    # put tkimage in canvas
    canvas = tk.Canvas(frame)
    canvas.create_image(0,0,image=tkimage,anchor=tk.NW)

    canvas.grid()
    frame.grid()
    frame.grid_propagate(0)

    if block:
        frame.mainloop()
