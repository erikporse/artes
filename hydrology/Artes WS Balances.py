__author__ = 'eporse'

import xlrd
import xlwt
from xlutils.copy import copy
from xlwt import easyxf
import tablib
import xlutils
import sys
import os
import math
import numpy
import pickle
from gurobipy import *

path = '...Artes Regions'

print path

# Set up arrays for re-arranging data (values in ac-ft)
hydro_name = []  # changing list of files based on hydrologic regions
precip = [] # precipitation
surface_storage = [] # surface storage inflow volume
et = [] # evapotranspiration
gw_storage = [] # groundwater storage
infiltration = [] # infiltration volume
surface_outflow = [] #surface outflow volume
gw_outflow = [] # groundwater outflow volume
gw_inflow = [] # groundwater inflow volume
actgw_inflow = [] # active groundwater inflow volume


precip = []

year = ["1986","1987","1988","1989","1990","1991","1992","1993","1994","1995","1996","1997","1998","1999",
        "2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012"]
month = ["1","2","3","4","5","6","7","8","9","10","11","12"]
day = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]

# Read in filenames, which are the WSIDs, by watersheds
# Do one at a time, comment out other watersheds
fname_in = path + "/" + "Hydro Regions v8Jun16.xlsx"
workbook = xlrd.open_workbook(fname_in, encoding_override="utf_8")
sheet2 = workbook.sheet_by_name("Names")

## Hydrologic Regions ##
hydro_name_in = sheet2.col_values(0)
for i in range(len(hydro_name_in)):
    name = str(hydro_name_in[i])
    hydro_name.append(name)

for k in range(len(hydro_name)):
    print hydro_name_in[k]

    fname_in2 = path + "/Watershed Totals/" + str(hydro_name[k]) + ".xlsx"
    print fname_in2
    workbook2 = xlrd.open_workbook(fname_in2, encoding_override="utf_8")

    sheet2 = workbook2.sheet_by_name("Formatted")

    precip_fin = sheet2.row_values(3,start_colx=1, end_colx=None)
    precip.append(precip_fin)
    f1 = open(path + "/Watershed Balances/" + "precipitation", "ab")
    for i in range(len(precip)):
        precip_write = []
        for j in range(len(precip[i])):
            precip_write.append(precip[i][j])
    print >> f1, str(precip_write).strip("[]")

    surf_stor_fin = sheet2.row_values(4,start_colx=1, end_colx=None)
    surface_storage.append(surf_stor_fin)
    f2 = open(path + "/Watershed Balances/" + "surface_storage", "ab")
    for i in range(len(surface_storage)):
        surface_storage_write = []
        for j in range(len(surface_storage[i])):
            surface_storage_write.append(surface_storage[i][j])
    print >> f2, str(surface_storage_write).strip("[]")

    gw_storage_fin = sheet2.row_values(5,start_colx=1, end_colx=None)
    gw_storage.append(gw_storage_fin)
    f4 = open(path + "/Watershed Balances/" + "gw_storage", "ab")
    for i in range(len(gw_storage)):
        gw_storage_write = []
        for j in range(len(gw_storage[i])):
            gw_storage_write.append(gw_storage[i][j])
    print >> f4, str(gw_storage_write).strip("[]")

    surface_outflow_fin = sheet2.row_values(6,start_colx=1, end_colx=None)
    surface_outflow.append(surface_outflow_fin)
    f6 = open(path + "/Watershed Balances/" + "surface_outflow", "ab")
    for i in range(len(surface_outflow)):
        surface_outflow_write = []
        for j in range(len(surface_outflow[i])):
            surface_outflow_write.append(surface_outflow[i][j])
    print >> f6, str(surface_outflow_write).strip("[]")

    gw_outflow_fin = sheet2.row_values(7,start_colx=1, end_colx=None)
    gw_outflow.append(gw_outflow_fin)
    f7 = open(path + "/Watershed Balances/" + "gw_outflow", "ab")
    for i in range(len(gw_outflow)):
        gw_outflow_write = []
        for j in range(len(gw_outflow[i])):
            gw_outflow_write.append(gw_outflow[i][j])
    print >> f7, str(gw_outflow_write).strip("[]")

    et_fin = sheet2.row_values(8,start_colx=1, end_colx=None)
    et.append(et_fin)
    f3 = open(path + "/Watershed Balances/" + "evapotranspiration", "ab")
    for i in range(len(et)):
        et_write = []
        for j in range(len(et[i])):
            et_write.append(et[i][j])
    print >> f3, str(et_write).strip("[]")

    infil_fin = sheet2.row_values(9,start_colx=1, end_colx=None)
    infiltration.append(infil_fin)
    f5 = open(path + "/Watershed Balances/" + "infiltration", "ab")
    for i in range(len(infiltration)):
        infiltration_write = []
        for j in range(len(infiltration[i])):
            infiltration_write.append(infiltration[i][j])
    print >> f5, str(infiltration_write).strip("[]")

    gw_inflow_fin = sheet2.row_values(10,start_colx=1, end_colx=None)
    gw_inflow.append(gw_inflow_fin)
    f8 = open(path + "/Watershed Balances/" + "gw_inflow", "ab")
    for i in range(len(gw_inflow)):
        gw_inflow_write = []
        for j in range(len(gw_inflow[i])):
            gw_inflow_write.append(gw_inflow[i][j])
    print >> f8, str(gw_inflow_write).strip("[]")

    actgw_inflow_fin = sheet2.row_values(11,start_colx=1, end_colx=None)
    actgw_inflow.append(actgw_inflow_fin)
    f8 = open(path + "/Watershed Balances/" + "active_gw_inflow", "ab")
    for i in range(len(actgw_inflow)):
        actgw_inflow_write = []
        for j in range(len(actgw_inflow[i])):
            actgw_inflow_write.append(actgw_inflow[i][j])
    print >> f8, str(actgw_inflow_write).strip("[]")





