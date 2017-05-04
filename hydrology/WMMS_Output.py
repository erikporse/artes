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
from gurobipy import *

sys.path.append('.../Output')
path = '.../Output'
path2 = '.../Full Run 1986-2011'
path3 = '.../Artes Regions'


print path

# Set up arrays for re-arranging data
filename = []
year = ["1996","1997","1998","1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012"]
month = ["1","2","3","4","5","6","7","8","9","10","11","12"]
day = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]

# Read in filenames, which are the WSIDs, by watersheds
# Do one at a time, comment out other watersheds
fname_in = path + "/" + "WSID_List.xlsx"
workbook = xlrd.open_workbook(fname_in, encoding_override="utf_8")

# Ballona
# sheet1 = workbook.sheet_by_name("Ballona")
# ballona_fin = sheet1.col_values(0)
# for i in range(len(ballona_fin)):
#     file = str(ballona_fin[i])
#     filename.append(file[:4])

# Dominguez
# sheet1 = workbook.sheet_by_name("Dominguez")
# dominguez_fin = sheet1.col_values(0)
# for i in range(len(dominguez_fin)):
#     file = str(dominguez_fin[i])
#     filename.append(file[:4])

# LA River
# sheet1 = workbook.sheet_by_name("LARiver")
# lariver_fin = sheet1.col_values(0)
# for i in range(len(lariver_fin)):
#     file = str(lariver_fin[i])
#     filename.append(file[:4])

# Malibu
# sheet1 = workbook.sheet_by_name("Malibu")
# malibu_fin = sheet1.col_values(0)
# for i in range(len(malibu_fin)):
#     file = str(malibu_fin[i])
#     filename.append(file[:4])

# San Gabriel
sheet1 = workbook.sheet_by_name("SanGab")
sangab_fin = sheet1.col_values(0)
for i in range(len(sangab_fin)):
    file = str(sangab_fin[i])
    filename.append(file[:4])

data_sws = dict.fromkeys(filename)
data_vals = dict.fromkeys(filename)

for n in filename:
    f = open(path + "/" + n + ".out", "r")
    columns = []

    for l,line in enumerate(f):
        line = line.strip()
        column = line.split()
        if l > 25:
            columns.append(column)

    f.close()
    data_sws[n] = columns

# Create arrays for values
values_by_day = dict.fromkeys(filename)
values_by_month_full = dict.fromkeys(filename)
values_by_month = dict.fromkeys(filename)

for n in filename:
    params1 = []
    prec = []
    surs = []
    agws = []
    suro = []
    agwo = []
    infil = []
    agwi = []
    vol = []
    for l in range(len(columns)):
        y = data_sws[n][l][1]
        m = data_sws[n][l][2]
        d = data_sws[n][l][3]
        v1 = data_sws[n][l][6]  # for precip
        v2 = data_sws[n][l][7]  # for surface storage
        v3 = data_sws[n][l][8]  # for groundwater storage
        v4 = data_sws[n][l][9]  # for surface outflow
        v5 = data_sws[n][l][10]  # for groundwater outflow
        v6 = data_sws[n][l][11]  # for infiltration from surface to aquifer
        v7 = data_sws[n][l][12]  # active groundwater inflow vol
        v8 = data_sws[n][l][13]  # total volume in reach
        params1.append([y,m,d])
        prec.append(v1)
        surs.append(v2)
        agws.append(v3)
        suro.append(v4)
        agwo.append(v5)
        infil.append(v6)
        agwi.append(v7)
        vol.append(v8)
    values_by_day[n] = [params1,prec,surs,agws,suro,agwo,infil,agwi,vol]

f = open(path + "/Formatted/" "sangabriel.txt", "ab")
for n in filename:
    params2 = []
    for y in year:
        for m in month:
            params2.append([y,m])
            month_prec_sum = 0
            month_surs_sum = 0
            month_agws_sum = 0
            month_suro_sum = 0
            month_agwo_sum = 0
            month_infil_sum = 0
            month_agwi_sum = 0
            month_vol_sum = 0
            for l in range(len(values_by_day[n][0])):
                #print l,y,m,month_sum, values_by_day[n][0][l], values_by_day[n][1][l][0]
                if y == values_by_day[n][0][l][0] and m == values_by_day[n][0][l][1]:
                    #print n,y,m,month_agwo_sum,values_by_day[n][0][l],float(values_by_day[n][5][l])
                    month_prec_sum = month_prec_sum + float(values_by_day[n][1][l])
                    month_surs_sum = month_surs_sum + float(values_by_day[n][2][l])
                    month_agws_sum = month_agws_sum + float(values_by_day[n][3][l])
                    month_suro_sum = month_suro_sum + float(values_by_day[n][4][l])
                    month_agwo_sum = month_agwo_sum + float(values_by_day[n][5][l])
                    month_infil_sum = month_infil_sum + float(values_by_day[n][6][l])
                    month_agwi_sum = month_agwi_sum + float(values_by_day[n][7][l])
                    month_vol_sum = month_vol_sum + float(values_by_day[n][8][l])

            values_by_month_full[n] = [params2,month_prec_sum,month_surs_sum,month_agws_sum,
                                       month_suro_sum,month_agwo_sum,month_infil_sum,month_agwi_sum,month_vol_sum]
            print >> f,n,y,m,values_by_month_full[n][-8],values_by_month_full[n][-7],values_by_month_full[n][-6],values_by_month_full[n][-5],values_by_month_full[n][-4],\
                values_by_month_full[n][-3],values_by_month_full[n][-2],values_by_month_full[n][-1]
