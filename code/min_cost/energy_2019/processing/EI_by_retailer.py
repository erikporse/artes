##################################################################################
#
# Artes: Modeling Water Management in Los Angeles for Local Water Supplies
#
# Copyright: Erik Porse
# California Center for Sustainability Communities at UCLA
# July 2019
#
# http://waterhub.ucla.edu
#
# Permission and use permitted with attribution.
# Creative Commons Attribution 4.0 International License
#
# Please cite the reference below when using or adapting code:
#
# Porse, Erik C., Kathryn B. Mika, Elizabeth Litvak, Kim Manago, Kartiki Naik,
#  Madelyn Glickfeld, Terri Hogue, Mark Gold, Diane Pataki, and Stephanie Pincetl.
#  Systems Analysis and Optimization of Local Water Supplies in Los Angeles.
#  Journal of Water Resources Planning and Management. (2017)
#
# This is some short code for processing outputs from the energy use model 
# and plotting energy intensity of modeled scenarios
#
##################################################################################

__author__ = 'eporse'

import xlrd
from xlutils.copy import copy
import xlutils
import sys
import os
import math
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import pickle
#from gurobipy import *

# A note: to plot Gross or Net energy use alone, the path designations must be toggled (path1 is used for plotting)
# To plot simultaneously, path1 is GROSS and path3 is NET.
path2 = '.../E10_07_08_19/Results'
path1 = '.../E11_07_08_19/Results'
path3 = '.../Water-Energy Model\data'

full_years = ["1986","1987","1988","1989","1990","1991","1992","1993","1994","1995","1996","1997","1998","1999",
        "2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010"]
years = ["1996","1997","1998","1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010"]
months = ["1","2","3","4","5","6","7","8","9","10","11","12"]
month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
time_steps = 300

## READ IN SOME DATA ##
node_in = path3 + "\LACounty_EnergyIntensities_Artes_USE.xlsx"
print node_in
workbook = xlrd.open_workbook(node_in, encoding_override="utf_8")
sheet3 = workbook.sheet_by_name("All_Nodes")

# Nodes
nodes = []
node_in = sheet3.col_values(0)
for i in range(len(node_in)):
    name = str(node_in[i])
    nodes.append(name)

demand_node_in = path3 + "\\" + "\LACounty_EnergyIntensities_Artes_USE.xlsx"
workbook = xlrd.open_workbook(demand_node_in, encoding_override="utf_8")
sheet1 = workbook.sheet_by_name("Demand_Nodes")

# Demand Nodes
demand_nodes = []
node_in = sheet1.col_values(0)
for i in range(len(node_in)):
    name = str(node_in[i])
    demand_nodes.append(name)

# Energy Intensity Coefficients of Sources and Flows
sheet2 = workbook.sheet_by_name("EI_to_retailers")

#imported Energy Intensity
ei_imported = []
ei_imported_in = sheet2.col_values(1)
for i in range(len(ei_imported_in)):
    name = str(ei_imported_in[i])
    ei_imported.append(name)
ei_imported.pop(0)

# groundwater Energy Intensity
ei_gw = []
ei_gw_in = sheet2.col_values(2)
for i in range(len(ei_gw_in)):
    name = str(ei_gw_in[i])
    ei_gw.append(name)
ei_gw.pop(0)

#sewage treatment Energy Intensity
ei_ww = []
ei_ww_in = sheet2.col_values(3)
for i in range(len(ei_ww_in)):
    name = str(ei_ww_in[i])
    ei_ww.append(name)
ei_ww.pop(0)

#conveyance Energy Intensity
ei_convey= []
ei_convey_in = sheet2.col_values(4)
for i in range(len(ei_convey_in)):
    name = str(ei_convey_in[i])
    ei_convey.append(name)
ei_convey.pop(0)

## READ IN MODEL RESULTS DATA ##
# Create array for reading in files
supp = ["100","90","80","70","60","50","40","30","20","10","0"]
files = []
for j in supp:
    file = ["S", str(j)]
    file_str = "".join(file)
    files.append(file_str)

# Read in flows data by source and scenario
imported_supply = np.zeros((len(files),len(demand_nodes),len(years),len(months)))
gw_supply = np.zeros((len(files),len(demand_nodes),len(years),len(months)))
ww_treatment_supply = np.zeros((len(files),len(demand_nodes),len(years),len(months)))
conveyance_supply = np.zeros((len(files),len(demand_nodes),len(years),len(months)))

for i in range(len(files)):
    f = open(path1 + "\\" + str(files[i]) + "\\supplies_imports_month.txt", "r")
    max_rows = []

    for l,line in enumerate(f):
        line = line.strip()
        column = line.split()
        column.pop(0)
        max_rows.append(column)

    k = 0
    for n in range(len(nodes)):
        if nodes[n] in demand_nodes:
            for y in range(len(years)):
                imported_supply[i, k, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
            k = k + 1
    f.close()

for i in range(len(files)):
    f = open(path1 + "\\" + str(files[i]) + "\\supplies_gw_month.txt", "r")
    max_rows = []

    for l,line in enumerate(f):
        line = line.strip()
        column = line.split()
        column.pop(0)
        max_rows.append(column)

    k = 0
    for n in range(len(nodes)):
        if nodes[n] in demand_nodes:
            for y in range(len(years)):
                gw_supply[i, k, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
            k = k + 1
    f.close()

for i in range(len(files)):
    f = open(path1 + "\\" + str(files[i]) + "\\exports.txt", "r")
    max_rows = []

    for l,line in enumerate(f):
        line = line.strip()
        column = line.split()
        column.pop(0)
        max_rows.append(column)

    k = 0
    for n in range(len(nodes)):
        if nodes[n] in demand_nodes:
            for y in range(len(years)):
                ww_treatment_supply[i, k, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
            k = k + 1
    f.close()

for i in range(len(files)):
    f = open(path1 + "\\" + str(files[i]) + "\\supplies.txt", "r")
    max_rows = []

    for l,line in enumerate(f):
        line = line.strip()
        column = line.split()
        column.pop(0)
        max_rows.append(column)

    k = 0
    for n in range(len(nodes)):
        if nodes[n] in demand_nodes:
            for y in range(len(years)):
                conveyance_supply[i, k, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
                data = max_rows[n][y * 12:(((y + 1) * 12))]
            k = k + 1
    f.close()

    
######## COMMENT OUT SECTION 1 OR 2 DEPENDING ON IF PLOTTING GROSS OR NET ENERGY USE ########

# 1) Calculate Annual Average Energy Intensity from All Sources, attributed to Retailers
# imported_energy = np.zeros((len(files),len(demand_nodes),len(years),len(months)))
# gw_energy = np.zeros((len(files),len(demand_nodes),len(years),len(months)))
# ww_treatment_energy = np.zeros((len(files),len(demand_nodes),len(years),len(months)))
# conveyance_energy = np.zeros((len(files),len(demand_nodes),len(years),len(months)))
# energy_total = np.zeros((len(files),len(demand_nodes),len(years),len(months)))
# avg_ann_ei_retailer = np.zeros((len(files),len(demand_nodes)))
# avg_ann_supply_retailer = np.zeros((len(files),len(demand_nodes),len(years)))
#
# for i in range(len(files)):
#     if files[i] == "S0":
#         for n in range(len(demand_nodes)):
#             for y in range(len(years)):
#                 for t in range(len(months)):
#                     imported_energy[i,n,y,t] = np.multiply(float(imported_supply[i, n, y, t]),float(ei_imported[n]))
#                     gw_energy[i, n, y, t] = np.multiply(float(gw_supply[i, n, y, t]), float(ei_gw[n]))
#                     ww_treatment_energy[i, n, y, t] = np.multiply(float(ww_treatment_supply[i, n, y, t]), float(ei_ww[n]))
#                     conveyance_energy[i, n, y, t] = np.multiply(float(conveyance_supply[i, n, y, t]), float(ei_convey[n]))
#                     energy_total[i, n, y, t] = imported_energy[i,n,y,t] + gw_energy[i, n, y, t] + ww_treatment_energy[i, n, y, t] + conveyance_energy[i, n, y, t]
#
#             avg_ann_ei_retailer[i,n] = np.average(np.sum(energy_total[i, n, :, :], axis=(1)) / np.sum(conveyance_supply[i, n, :, :], axis=(1)))
#             print files[i],demand_nodes[n],avg_ann_ei_retailer[i,n]

# 2) Calculate Monthly Average Energy Intensity from All Sources, attributed to Retailers
imported_energy = np.zeros((len(files),len(demand_nodes),len(years),len(months)))
gw_energy = np.zeros((len(files),len(demand_nodes),len(years),len(months)))
ww_treatment_energy = np.zeros((len(files),len(demand_nodes),len(years),len(months)))
conveyance_energy = np.zeros((len(files),len(demand_nodes),len(years),len(months)))
energy_total = np.zeros((len(files),len(demand_nodes),len(years),len(months)))
avg_monthly_ei_retailer = np.zeros((len(files),len(demand_nodes),len(months)))
avg_ann_supply_retailer = np.zeros((len(files),len(demand_nodes),len(years)))

for i in range(len(files)):
    if files[i] == "S0":
        for n in range(len(demand_nodes)):
            for y in range(len(years)):
                for t in range(len(months)):
                    imported_energy[i,n,y,t] = np.multiply(float(imported_supply[i, n, y, t]),float(ei_imported[n]))
                    gw_energy[i, n, y, t] = np.multiply(float(gw_supply[i, n, y, t]), float(ei_gw[n]))
                    ww_treatment_energy[i, n, y, t] = np.multiply(float(ww_treatment_supply[i, n, y, t]), float(ei_ww[n]))
                    conveyance_energy[i, n, y, t] = np.multiply(float(conveyance_supply[i, n, y, t]), float(ei_convey[n]))
                    energy_total[i, n, y, t] = imported_energy[i,n,y,t] + gw_energy[i, n, y, t] + ww_treatment_energy[i, n, y, t] + conveyance_energy[i, n, y, t]

for i in range(len(files)):
    if files[i] == "S0":
        for n in range(len(demand_nodes)):
            for t in range(len(months)):
                if t == 7:
                    avg_monthly_ei_retailer[i,n,t] = np.average(np.sum(energy_total[i, n, :, t], axis=(0)) / np.sum(conveyance_supply[i, n, :, t], axis=(0)))
                    print files[i],demand_nodes[n],months[t],avg_monthly_ei_retailer[i,n,t]


