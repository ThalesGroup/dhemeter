# =============================================================================
# Copyright 2025 Thales Group
# Licensed under the APACHE 2 License. See LICENSE file in the project root for
# full license information.
# =============================================================================
import os
# create a function to generate a map with this template :
# the file will be called map_<precision>.txt
# content of the file :
# gridtype  = lonlat
# xsize     = 2879
# ysize     = 1441
# xfirst    = -180
# xinc      = 0.125
# yfirst    = -90
# yinc      = 0.125

# precision is the value of xinc and yinc the xsize is calculated by (xfirst + 360) / xinc + 1
# the ysize is calculated by (yfirst + 180) / yinc + 1
def gen_map_world(precision, tmp_dir):
    getxsize = lambda xfirst, xinc: int((xfirst + 360) / xinc + 1)
    getysize = lambda yfirst, yinc: int((yfirst + 180) / yinc + 1)
    xfirst = -180
    yfirst = -90
    xinc = precision
    yinc = precision
    xsize = getxsize(xfirst, xinc)
    ysize = getysize(yfirst, yinc)
    file_name = "map_" + str(precision) + ".txt"
    file = os.path.join(tmp_dir, file_name)
    with open(file, "w") as f:
        f.write("gridtype  = lonlat\n")
        f.write("xsize     = " + str(xsize) + "\n")
        f.write("ysize     = " + str(ysize) + "\n")
        f.write("xfirst    = " + str(xfirst) + "\n")
        f.write("xinc      = " + str(xinc) + "\n")
        f.write("yfirst    = " + str(yfirst) + "\n")
        f.write("yinc      = " + str(yinc) + "\n")
    # return the path of the file
    return file

# generate a map for a specific region given the coordinates of the region
def gen_map_region(precision, xfirst, xlast, yfirst, ylast, tmp_dir):
    getxsize = lambda xfirst, xinc: int((xlast - xfirst) / xinc + 1)
    getysize = lambda yfirst, yinc: int((ylast - yfirst) / yinc + 1)
    xinc = precision
    yinc = precision
    xsize = getxsize(xfirst, xinc)
    ysize = getysize(yfirst, yinc)
    file_name = "map_" + str(precision) + ".txt"
    file = os.path.join(tmp_dir, file_name)
    with open(file, "w") as f:
        f.write("gridtype  = lonlat\n")
        f.write("xsize     = " + str(xsize) + "\n")
        f.write("ysize     = " + str(ysize) + "\n")
        f.write("xfirst    = " + str(xfirst) + "\n")
        f.write("xinc      = " + str(xinc) + "\n")
        f.write("yfirst    = " + str(yfirst) + "\n")
        f.write("yinc      = " + str(yinc) + "\n")
    # return the path of the file
    return file
