from osgeo import gdal
import numpy as np
import glob
from osgeo import osr
from sys import exit
from gdalconst import *
import os
import sys
import csv
import pandas as pd

def Open1BandTif(filename):
    
    """Open tif file which contain 1 band data only
    input: 
        filename - string
    output:
        dset: tif data - object
        data: data band - array
        cols: number of collumn image - int
        rows: number of rows image - int
        geotransform: geostransform of image - array
        prj: projection of image - array
    """
    
    dset= None
    band = None
    data = None
    dset = gdal.Open(filename)
    geotransform_ = dset.GetGeoTransform()
    prj = dset.GetProjection()
    
    
    if dset is not None:
        band = dset.GetRasterBand(1)
        data = band.ReadAsArray()
    YSize = dset.RasterYSize
    XSize = dset.RasterXSize
            
    return dset, data, XSize, YSize, geotransform_, prj
    

def ClipTiffBySHP (shp, infile, outfile):
    
    """ClipTiffBySHP: Clip tif images by shapefile
        Input:
            shp: input shapefile
            infile: input tif file
        Output:
            outfile: output tif file"""
    
    command = "gdalwarp -dstnodata 255 -cutline {} -crop_to_cutline -of GTiff {} {}".format(shp, infile, outfile)
    os.system(command)
    

def CSVWriteRow(filename, list_data):
    
    """Write data to CSV
    input:
        filename: output filename of CSV file - string
        list_data: data to write to csv - array
    output:
        void
        
    """
    with open(filename, 'w', newline='') as csvfile:
        
        writer = csv.writer(csvfile)
        
        for data in list_data:
            
            writer.writerow(data)
            
def ExtractTiffFromPoint(list_tif, list_index, outfile):
    
    """Extract tiff from x and y
    input:
        list_tiff: list of tif file
        list_index: csv file contains x and y index
        outfile: filename of output
    output:
        void
    """
# =============================================================================
#     list_x = pd.read_csv(list_index, names = ["X","Y"])["X"].values
#     list_y = pd.read_csv(list_index, names = ["X","Y"])["Y"].values
# =============================================================================
    
    list_x = pd.read_csv(list_index)["X"].values
    list_y = pd.read_csv(list_index)["Y"].values
    
    final_data = []
    list_data = []

    for tif in list_tif:
        
        dset, data, cols, rows, geotransform, prj = Open1BandTif(tif)
        for (x, y) in zip(list_x, list_y):
            
            list_data.append(data[int(y)-1][int(x)-1])
            
        final_data.append(list_data)
        
        list_data = []
        del data
        print (tif)
    CSVWriteRow(outfile, np.transpose(np.array(final_data)))
    del final_data