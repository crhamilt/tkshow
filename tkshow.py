#!/usr/bin/env python3

import os
import argparse
import dicom
import tkinter as tk
import numpy as np
from PIL import Image
from PIL import ImageTk
from skimage import exposure

# TODO:
#  * add cursor readout
#  * add zooming by resizing window
#  *
#

def show_image(data):
    '''
    Get minimal Tkinter GUI and display a pydicom data.pixel_array

    data: object returned from pydicom.read_file()
    '''

    global rawimage
    global pixLabel

    # Callbacks
    def quit_handler():
        frame.quit()

    def motion(event):
        global pixLabel
        x, y = event.x, event.y
        sz = rawimage.shape
        if y < sz[0] and x < sz[1]:
            pixLabel.config(text="%5.1f@[%3dx,%3dy]" % (rawimage[y,x],x,y))


    def brighten_handler():
        global tkimage2  # don't let it get garbage collected
        global rawimage
        img2 = exposure.adjust_gamma(rawimage, 0.98)
        pillowimage2 = Image.frombuffer(mode, size, img2, 'raw', mode, 0, 1)
        tkimage2 = ImageTk.PhotoImage(pillowimage2)
        canvas.itemconfigure(canvasimg, image=tkimage2)
        rawimage = img2

    def darken_handler():
        global tkimage2  # don't let it get garbage collected
        global rawimage
        img2 = exposure.adjust_gamma(rawimage, 1.02)
        pillowimage2 = Image.frombuffer(mode, size, img2, 'raw', mode, 0, 1)
        tkimage2 = ImageTk.PhotoImage(pillowimage2)
        canvas.itemconfigure(canvasimg, image=tkimage2)
        rawimage = img2

    # ~~~~~~~~~~~~~~  main app starts here ~~~~~~~~~~~~~~~~~~~~

    root = tk.Tk()

    # create frame
    frame = tk.Frame(root, background='#000', width=data.Columns, height=data.Rows+50)
    frame.pack(fill=tk.BOTH,expand=tk.YES)

    if 'SeriesDescription' in data and 'InstanceNumber' in data:
        title = ', '.join(('Ser: ' + data.SeriesDescription,
                           'Img: ' + str(data.InstanceNumber)))
    else:
        title = 'dicom image'
    frame.master.title(title)

    # create toplevel menu
    top = frame.winfo_toplevel()
    frame.menuBar = tk.Menu(top)
    top['menu'] = frame.menuBar
    frame.subMenu = tk.Menu(frame.menuBar)
    frame.menuBar.add_cascade(label='File', menu=frame.subMenu)
    frame.subMenu.add_command(label='Quit', command=quit_handler)

    # create a frame to hold controls
    cframe = tk.Frame(frame, background='#077', width=data.Columns, height=50)
    cframe.pack(side=tk.TOP,fill=tk.X,expand=True)

    # create a tkimage holding the input image
    mode = 'I'
    size = (data.Columns,data.Rows)
    rawimage = data.pixel_array.astype(np.int32)

    #  rescale to 0-255
    print('min/max = %8.3f/%8.3f' % (rawimage.min(),rawimage.max()))
    rawimage[:,:] = (rawimage[:,:] - rawimage.min())* 255.0/(rawimage.max()-rawimage.min())
    print('new min/max = %8.3f/%8.3f' % (rawimage.min(),rawimage.max()))

    pillowimage = Image.frombuffer(mode,size, rawimage,'raw',mode,0,1)
    tkimage = ImageTk.PhotoImage(pillowimage)

    #  131,142 = 271
    print("rawimage[142y,131x] = %5.1f" % (rawimage[142,131]))

    # find path to my icons
    iconpath = os.path.dirname(os.path.realpath(__file__))

    # create controls
    qButton = tk.Button(cframe,text="Quit",command=quit_handler)
    qButton.pack(side=tk.LEFT)
    pixLabel = tk.Label(cframe,text="0000.0@000,000",font=("TkTextFont",10),width=16)
    pixLabel.pack(side=tk.LEFT)
    brImage = ImageTk.PhotoImage(file=iconpath+"/brighten.tif")
    brButton = tk.Button(cframe,image=brImage, command=brighten_handler)
    brButton.pack(side=tk.RIGHT)
    dkImage = ImageTk.PhotoImage(file=iconpath+"/darken.tif")
    dkButton = tk.Button(cframe,image=dkImage, command=darken_handler)
    dkButton.pack(side=tk.RIGHT)


    # create frame to hold image
    iframe = tk.Frame(frame, background='#077', width=data.Columns, height=data.Rows)
    iframe.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=tk.YES)

    # put tkimage in canvas
    canvas = tk.Canvas(iframe,highlightthickness=2,width=data.Columns,height=data.Rows)
    canvas.pack(fill=tk.BOTH, expand=tk.YES)
    canvasimg = canvas.create_image(0,0,image=tkimage,anchor=tk.NW)
    canvas.bind('<Motion>', motion)

    frame.mainloop()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="tkshow : display a DICOM image.")
    parser.add_argument("image", type=str,help="filename of DICOM image to display")
    args = parser.parse_args()

    dcm = dicom.read_file(args.image)
    pa = dcm.pixel_array
    show_image(dcm)
