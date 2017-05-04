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
import numpy as np
from gurobipy import *

sys.path.append('.../Output')
path = '.../Output'
path2 = '.../Full Run 1986-2011'
path3 = '.../Artes Regions'

print path

# Set up arrays for re-arranging data
hydro_name = []  # changing list of files based on hydrologic regions
sws = []  # list of # of SWS's in each hydro region
year = ["1986","1987","1988","1989","1990","1991","1992","1993","1994","1995","1996","1997","1998","1999",
        "2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012"]
month = ["1","2","3","4","5","6","7","8","9","10","11","12"]
day = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]

# Read in filenames, which are the WSIDs, by watersheds
# Do one at a time, comment out other watersheds
fname_in = path3 + "/" + "Artes Hydro Regions v8Jun16.xlsx"
workbook = xlrd.open_workbook(fname_in, encoding_override="utf_8")
sheet2 = workbook.sheet_by_name("Names")

## Hydrologic Regions ##
hydro_name_in = sheet2.col_values(0)
sws_fin = sheet2.col_values(2)
for i in range(len(hydro_name_in)):
    name = str(hydro_name_in[i])
    sws_f = str(sws_fin[i])
    hydro_name.append(name)
    sws.append(sws_f)

for k in range(len(hydro_name)):
    print hydro_name_in[k]
    data_hydro = dict.fromkeys(hydro_name)

    file = str(sws[k])
    filename = file[:4]

    f = open(path3 + "/WS Outflows/" + str(hydro_name[k]), "r")
    columns = []

    for l,line in enumerate(f):
        line = line.strip()
        column = line.split()
        columns.append(column)

    f.close()
    data_hydro[k] = columns

    # Create arrays for values
    values_by_month_full = dict.fromkeys(hydro_name)
    values_by_month = dict.fromkeys(hydro_name)

    f = open(path3 + "/WS Outflows/" + "RO Totals", "ab")
    params1 = []
    ro = []
    for l in range(len(columns)):
        #print hydro_name[n],data_hydro[n][l][1],data_hydro[n][l][2],data_hydro[n][l][3]

        y = data_hydro[k][l][1]
        m = data_hydro[k][l][2]
        v = data_hydro[k][l][3]  # for total outflow, including upstream

        #print len(columns),l,hydro_name[k],data_hydro[k][l][1],data_hydro[k][l][2],v

        params1.append([y,m])
        ro.append(v)
    values_by_month[k] = [params1,ro]

    print >> f, filename, (" ".join(ro))