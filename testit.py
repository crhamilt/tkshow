#!/usr/bin/env python

import dicom
import tkshow 

dcm = dicom.read_file('testimgs/MR0044/000001.DCM')

print('dcm.Rows= %d dcm.Columns= %d' % (dcm.Rows,dcm.Columns) )

pa = dcm.pixel_array

print('pa.shape = ', pa.shape)

tkshow.show_image(dcm)
