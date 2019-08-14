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
# and plotting gross and net energy use by scenarios
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
from matplotlib import style
import pickle
#from gurobipy import *

# A note: in being lazy, to plot Gross or Net energy use alone, the path designations must be toggled (path1 is used)
# To plot simultaneously, path1 is GROSS and path3 is NET.
# Perhaps sometime in the future I will clean this up.
path1 = '.../E10_07_08_19/Results'
path2 = <read in list of node names>
path3 = '.../E11_07_08_19/Results'

print path1

full_years = ["1986","1987","1988","1989","1990","1991","1992","1993","1994","1995","1996","1997","1998","1999",
        "2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010"]
years = ["1996","1997","1998","1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010"]
months = ["1","2","3","4","5","6","7","8","9","10","11","12"]
month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

## READ IN SOME DATA ##
hydro_node_in = path2 + "\\" + "Artes Hydro Regions.xlsx"
workbook = xlrd.open_workbook(hydro_node_in, encoding_override="utf_8")
sheet3 = workbook.sheet_by_name("All_Nodes")

# Nodes
nodes = []
node_in = sheet3.col_values(0)
for i in range(len(node_in)):
    name = str(node_in[i])
    nodes.append(name)
nodes.pop(0)

## READ IN MODEL DATA ##
# Create array for reading in files
supp = ["100","90","80","70","60","50","40","30","20","10","0"]
files = []
for j in supp:
    file = ["S", str(j)]
    file_str = "".join(file)
    files.append(file_str)

# Declare Numpy arrays
energy_total = np.zeros((len(files),len(nodes),len(years),len(months)))
energy_import_source = np.zeros((len(files),len(nodes),len(years),len(months)))
energy_gw_source = np.zeros((len(files),len(nodes),len(years),len(months)))
energy_wwtreat = np.zeros((len(files),len(nodes),len(years),len(months)))
energy_conveyance = np.zeros((len(files),len(nodes),len(years),len(months)))
energy_total_net = np.zeros((len(files),len(nodes),len(years),len(months)))
energy_import_source_net = np.zeros((len(files),len(nodes),len(years),len(months)))
energy_gw_source_net = np.zeros((len(files),len(nodes),len(years),len(months)))
energy_wwtreat_net = np.zeros((len(files),len(nodes),len(years),len(months)))
energy_conveyance_net = np.zeros((len(files),len(nodes),len(years),len(months)))
flow = np.zeros((len(files),len(nodes),len(years),len(months)))
energy_intensity = np.zeros((len(files),len(nodes),len(years),len(months)))
ann_avg_ei_bynode = np.zeros((len(files),len(nodes),len(years)))
month_avg_ei_bynode = np.zeros((len(files),len(nodes),len(months)))
month_avg_ei_bynode = np.zeros((len(files),len(nodes),len(months)))

#f1 = open(path2 + "\\Outputs\\" + "Hydro_flows.txt", "a")

### Read in data for results (all scenarios)
# Toggle the path designation to plot either GROSS (E1, E4, E6, E8) or NET (E2, E5, E7, E9) energy use scenarios
for i in range(len(files)):
    f = open(path1 + "\\" + str(files[i]) + "\\energy_total.txt", "r")
    max_rows = []

    for l,line in enumerate(f):
        line = line.strip()
        column = line.split()
        column.pop(0)
        max_rows.append(column)

    k = 0
    for n in range(len(nodes)):
        if nodes[n] in nodes:
            for y in range(len(years)):
                energy_total[i, n, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
            k = k + 1
        else:
            for y in range(len(years)):
                energy_total[i, n, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
    f.close()

for i in range(len(files)):
    f = open(path1 + "\\" + str(files[i]) + "\\energy_import_source.txt", "r")
    max_rows = []

    for l,line in enumerate(f):
        line = line.strip()
        column = line.split()
        column.pop(0)
        max_rows.append(column)

    k = 0
    for n in range(len(nodes)):
        if nodes[n] in nodes:
            for y in range(len(years)):
                energy_import_source[i, n, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
            k = k + 1
        else:
            for y in range(len(years)):
                energy_import_source[i, n, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
    f.close()

for i in range(len(files)):
    f = open(path1 + "\\" + str(files[i]) + "\\energy_gw_source.txt", "r")
    max_rows = []

    for l,line in enumerate(f):
        line = line.strip()
        column = line.split()
        column.pop(0)
        max_rows.append(column)

    k = 0
    for n in range(len(nodes)):
        if nodes[n] in nodes:
            for y in range(len(years)):
                energy_gw_source[i, n, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
            k = k + 1
        else:
            for y in range(len(years)):
                energy_gw_source[i, n, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
    f.close()

for i in range(len(files)):
    f = open(path1 + "\\" + str(files[i]) + "\\energy_ww_treatment.txt", "r")
    max_rows = []

    for l,line in enumerate(f):
        line = line.strip()
        column = line.split()
        column.pop(0)
        max_rows.append(column)

    k = 0
    for n in range(len(nodes)):
        if nodes[n] in nodes:
            for y in range(len(years)):
                energy_wwtreat[i, n, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
            k = k + 1
        else:
            for y in range(len(years)):
                energy_wwtreat[i, n, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
    f.close()

for i in range(len(files)):
    f = open(path1 + "\\" + str(files[i]) + "\\energy_conveyance.txt", "r")
    max_rows = []
    #print files[i]

    for l,line in enumerate(f):
        line = line.strip()
        column = line.split()
        column.pop(0)
        max_rows.append(column)

    k = 0
    for n in range(len(nodes)):
        if nodes[n] in nodes:
            for y in range(len(years)):
                energy_conveyance[i, n, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
            k = k + 1
        else:
            for y in range(len(years)):
                energy_conveyance[i, n, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
    f.close()

# Now read in the files for NET Energy Use model run (E2 or E5)
for i in range(len(files)):
    f = open(path3 + "\\" + str(files[i]) + "\\energy_total.txt", "r")
    max_rows = []
    #print files[i]

    for l,line in enumerate(f):
        line = line.strip()
        column = line.split()
        column.pop(0)
        max_rows.append(column)

    k = 0
    for n in range(len(nodes)):
        if nodes[n] in nodes:
            for y in range(len(years)):
                energy_total_net[i, n, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
            k = k + 1
        else:
            for y in range(len(years)):
                energy_total_net[i, n, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
    f.close()
#
for i in range(len(files)):
    f = open(path3 + "\\" + str(files[i]) + "\\energy_import_source.txt", "r")
    max_rows = []

    for l,line in enumerate(f):
        line = line.strip()
        column = line.split()
        column.pop(0)
        max_rows.append(column)

    k = 0
    for n in range(len(nodes)):
        if nodes[n] in nodes:
            for y in range(len(years)):
                energy_import_source_net[i, n, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
            k = k + 1
        else:
            for y in range(len(years)):
                energy_import_source_net[i, n, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
    f.close()

for i in range(len(files)):
    f = open(path3 + "\\" + str(files[i]) + "\\energy_gw_source.txt", "r")
    max_rows = []

    for l,line in enumerate(f):
        line = line.strip()
        column = line.split()
        column.pop(0)
        max_rows.append(column)

    k = 0
    for n in range(len(nodes)):
        if nodes[n] in nodes:
            for y in range(len(years)):
                energy_gw_source_net[i, n, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
            k = k + 1
        else:
            for y in range(len(years)):
                energy_gw_source_net[i, n, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
    f.close()

for i in range(len(files)):
    f = open(path3 + "\\" + str(files[i]) + "\\energy_ww_treatment.txt", "r")
    max_rows = []

    for l,line in enumerate(f):
        line = line.strip()
        column = line.split()
        column.pop(0)
        max_rows.append(column)

    k = 0
    for n in range(len(nodes)):
        if nodes[n] in nodes:
            for y in range(len(years)):
                energy_wwtreat_net[i, n, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
            k = k + 1
        else:
            for y in range(len(years)):
                energy_wwtreat_net[i, n, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
    f.close()

for i in range(len(files)):
    f = open(path3 + "\\" + str(files[i]) + "\\energy_conveyance.txt", "r")
    max_rows = []
    #print files[i]

    for l,line in enumerate(f):
        line = line.strip()
        column = line.split()
        column.pop(0)
        max_rows.append(column)

    k = 0
    for n in range(len(nodes)):
        if nodes[n] in nodes:
            for y in range(len(years)):
                energy_conveyance_net[i, n, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
            k = k + 1
        else:
            for y in range(len(years)):
                energy_conveyance_net[i, n, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
    f.close()

print "Energy Files Read"

# read in flow volumes for calculating energy intensity
# for i in range(len(files)):
#     f = open(path1 + "\\" + str(files[i]) + "\\supplies.txt", "r")
#     max_rows = []
#
#     for l,line in enumerate(f):
#         line = line.strip()
#         column = line.split()
#         column.pop(0)
#         max_rows.append(column)
#
#     k = 0
#     for n in range(len(nodes)):
#         if nodes[n] in nodes:
#             for y in range(len(years)):
#                 flow[i, n, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
#             k = k + 1
#         else:
#             for y in range(len(years)):
#                 flow[i, n, y, :] = max_rows[n][y * 12:(((y + 1) * 12))]
#     f.close()
#
# print "Flow Files Read"

######### ANALYSIS AND PLOTTING ########

### Plots model runs as designated by path above, either Gross or Net ###

# Summary by Month
# print >> f,"node",' '.join(month_names)
# avg_energy_months = np.zeros((len(files),(len(months))))
# for i in range(len(files)):
#     avg_energy_month = np.sum(energy_total[i, :, :, :], axis=(0, 1))
#     avg_energy_months[i,:] = avg_energy_month/1000000

# Energy Use (Gross/Net), Annual Averages, By Scenario #
avg_ann_energy = np.zeros((len(files)))
avg_ann_energy_import_source = np.zeros((len(files)))
avg_ann_energy_gw_source = np.zeros((len(files)))
avg_ann_energy_wwtreat = np.zeros((len(files)))
avg_ann_energy_conveyance = np.zeros((len(files)))
avg_ann_energy_net = np.zeros((len(files)))
avg_ann_energy_import_source_net = np.zeros((len(files)))
avg_ann_energy_gw_source_net = np.zeros((len(files)))
avg_ann_energy_wwtreat_net = np.zeros((len(files)))
avg_ann_energy_conveyance_net = np.zeros((len(files)))
for i in range(len(files)):
    avg_ann_energy[i] = np.average(np.sum(energy_total[i, :, :, :], axis=(0,2))) / 1000000
    avg_ann_energy_import_source[i] = np.average(np.sum(energy_import_source[i, :, :, :], axis=(0, 2))) / 1000000
    avg_ann_energy_gw_source[i] = np.average(np.sum(energy_gw_source[i, :, :, :], axis=(0, 2))) / 1000000
    avg_ann_energy_wwtreat[i] = np.average(np.sum(energy_wwtreat[i, :, :, :], axis=(0, 2))) / 1000000
    avg_ann_energy_conveyance[i] = np.average(np.sum(energy_conveyance[i, :, :, :], axis=(0, 2))) / 1000000
    avg_ann_energy_net[i] = np.average(np.sum(energy_total_net[i, :, :, :], axis=(0, 2))) / 1000000
    avg_ann_energy_import_source_net[i] = np.average(np.sum(energy_import_source_net[i, :, :, :], axis=(0, 2))) / 1000000
    avg_ann_energy_gw_source_net[i] = np.average(np.sum(energy_gw_source_net[i, :, :, :], axis=(0, 2))) / 1000000
    avg_ann_energy_wwtreat_net[i] = np.average(np.sum(energy_wwtreat_net[i, :, :, :], axis=(0, 2))) / 1000000
    avg_ann_energy_conveyance_net[i] = np.average(np.sum(energy_conveyance_net[i, :, :, :], axis=(0, 2))) / 1000000

# # Plotting, by Scenario
fig, (ax1, ax2) = plt.subplots(1,2,sharex=False)
x = np.arange(1,12)
plt.xticks(x,supp)

#Subplot 1
ax1.stackplot(supp,avg_ann_energy_import_source,avg_ann_energy_gw_source,avg_ann_energy_wwtreat,avg_ann_energy_conveyance)
ax1.set_ylabel('Total Average Consumption (GWh)')
ax1.set_xlabel('% of Imported Water Available')
ax1.set_title('Gross Energy Use',y=1.02)
ax1.set_ylim(0,4500)

#Subplot 2
ax2.stackplot(supp,avg_ann_energy_import_source_net,avg_ann_energy_gw_source_net,avg_ann_energy_wwtreat_net,avg_ann_energy_conveyance_net)
ax2.set_ylabel('Total Average Consumption (GWh)')
ax2.set_xlabel('% of Imported Water Available')
ax2.set_title('Net Energy Use',y=1.02)
ax2.set_ylim(0,4500)

plt.subplots_adjust(bottom=0.3,wspace=0.4)
handles, labels = ax2.get_legend_handles_labels()
fig.legend(('Imported Supply and Treatment','Groundwater Supply and Treatment','Sewage Treatment','Conveyance'),loc='lower center')

fig.set_size_inches(9, 5)
save_path = "C:/Mac Files/Documents/Research/Articles for Publishing/LA Local Water Supply/Energy-Water/Figures/"
fig.savefig(save_path + "Fig 4.png", format='png', dpi=300)

plt.show()

# #### ENERGY USE BY MONTHS #####
# This section uses both Gross and Net energy value to plot simultaneously for comparison
# avg_energy_months = np.zeros((len(files),(len(months))))
# avg_energy_source_months = np.zeros((len(files),(len(months))))
# avg_energy_conveyance_months = np.zeros((len(files),(len(months))))
# avg_energy_months_net = np.zeros((len(files),(len(months))))
# avg_energy_source_months_net = np.zeros((len(files),(len(months))))
# avg_energy_conveyance_months_net = np.zeros((len(files),(len(months))))
# for i in range(len(files)):
#     avg_energy_months[i,:] = (np.average(energy_total[i, :, :, :], axis=(0,1)))/1000
#     #avg_energy_source_months[i,:] = (np.average(energy_source[i, :, :, :], axis=(0,1))) / 1000
#     #avg_energy_conveyance_months[i,:] = (np.average(energy_conveyance[i, :, :, :], axis=(0,1))) / 1000
# for i in range(len(files)):
#     avg_energy_months_net[i,:] = (np.average(energy_total_net[i, :, :, :], axis=(0,1)))/1000
#     #avg_energy_source_months_net[i,:] = (np.average(energy_source_net[i, :, :, :], axis=(0,1))) / 1000
#     #avg_energy_conveyance_months_net[i,:] = (np.average(energy_conveyance_net[i, :, :, :], axis=(0,1))) / 1000
#
# ### Plotting by month and scenario ###
# # X-axis months and labels
# x = np.arange(1,13)
# x_labels = ["J","F","M","A","M","J","J","A","S","O","N","D"]
#
# # Create plot and subplot
# fig, (ax1, ax2) = plt.subplots(1,2,sharex=True)
# #Subplot 1
# for i in range(len(files[1:12])):
#     ax1.plot(x, avg_energy_months[i,:])
# ax1.set_ylabel('Total Average Consumption (MWh)')
# plt.xticks(x,x_labels)
# ax1.set_ylim((0, 1500))
# ax1.set_xlabel('Month')
# ax1.set_title("Gross Energy Use")
#
# #Subplot 2
# for i in range(len(files[1:12])):
#     ax2.plot(x, avg_energy_months_net[i,:])
# ax2.set_ylim((0, 1500))
# ax2.set_xticks(x,x_labels)
# ax2.set_xlabel('Month')
# ax2.set_title("Net Energy Use")
# plt.subplots_adjust(right=0.75,wspace=0.35)
# fig.legend(('100%','90%','80%','70%','60%','50%','40%','30%','20%','10%'),loc='center right',title="% Imported Water")
#
# save_path = "C:/Mac Files/Documents/Research/Articles for Publishing/LA Local Water Supply/Energy-Water/Figures/"
# fig.savefig(save_path + "Fig 3.png", format='png', dpi=300)
#
# plt.show()

####### ENERGY INTENSITY ANALYSIS #######

# Summary  Numbers
# avg_ann_energy = np.zeros((len(files)))
# avg_ann_energy_source = np.zeros((len(files)))
# avg_ann_energy_conveyance = np.zeros((len(files)))
# for i in range(len(files)):
#     avg_ann_energy[i] = np.average(np.sum(energy_total[i, :, :, :], axis=(0,2))) / 1000000
#     avg_ann_energy_source[i] = np.average(np.sum(energy_source[i, :, :, :], axis=(0, 2))) / 1000000
#     avg_ann_energy_conveyance[i] = np.average(np.sum(energy_conveyance[i, :, :, :], axis=(0, 2))) / 1000000
#
# # Energy Intensity Analysis: By Retailer
# for i in range(len(files)):
#     avg_ann_energy[i] = np.average(np.sum(energy_total[i, :, :, :], axis=(0,2))) / 1000000
#     avg_ann_energy_source[i] = np.average(np.sum(energy_import_source[i, :, :, :], axis=(0, 2))) / 1000000
#     avg_ann_energy_source[i] = np.average(np.sum(energy_gw_source[i, :, :, :], axis=(0, 2))) / 1000000
#     avg_ann_energy_source[i] = np.average(np.sum(energy_wwtreat[i, :, :, :], axis=(0, 2))) / 1000000
#     avg_ann_energy_conveyance[i] = np.average(np.sum(energy_conveyance[i, :, :, :], axis=(0, 2))) / 1000000
#
# energy_intensity = np.divide(energy_total,(flow+0.000001))  # in kWh
#
# for i in range(len(files)):
#
#     print str(files[i])
#
#     # Open path for files to calculate energy intensity
#     os.remove(path1 + "\\" + str(files[i]) + "\\" + "energy_int_total_ann_avg.txt")
#     f2 = open(path1 + "\\" + str(files[i]) + "\\" + "energy_int_total_ann_avg.txt", "a")
#     os.remove(path1 + "\\" + str(files[i]) + "\\" + "energy_int_total_month_avg.txt")
#     f3 = open(path1 + "\\" + str(files[i]) + "\\" + "energy_int_total_month_avg.txt", "a")
#     print >> f2, ' '.join(years)
#     print >> f3, ' '.join(month_names)
#
#     ann_avg_ei_bynode[i,:,:] = np.average(energy_intensity[i, :, :, :], axis=(2))
#     month_avg_ei_bynode[i,:,:] = np.average(energy_intensity[i, :, :, :], axis=(1))
#
#     np.savetxt(f2, ann_avg_ei_bynode[i,:,:], fmt="%1.0f", delimiter=' ')
#     np.savetxt(f3, month_avg_ei_bynode[i, :, :], fmt="%1.0f", delimiter=' ')


### Read in ENERGY INTESNITY data from summary_annual.txt sheets for all files (Gross or Net)
# Toggle the path designation to plot either GROSS (E1, E4, E6, E8) or NET (E2, E5, E7, E9) energy use scenarios

# energy_intensity_modout = np.zeros((len(files),len(years)))
#
# for i in range(len(files)):
#     f = open(path1 + "\\" + str(files[i]) + "\\summary_annual.txt", "r")
#     max_rows = []
#
#     for l,line in enumerate(f):
#         line = line.strip()
#         column = line.split()
#         column.pop(0)
#         max_rows.append(column)
#
#     for l in range(0,22):        #length of the current summary_annual file to get to energy intensity readings
#         if l == 21:
#             for y in range(len(years)):
#                 energy_intensity_modout[i, y] = max_rows[l][y]
#     f.close()
#
# avg_energy_intensity_modout = np.mean(energy_intensity_modout, axis=1)
#
# # Plotting Energy Intensity, by Scenario
# f, ax = plt.subplots(1,sharex=True)
# x = np.arange(1,12)
# plt.xticks(x,supp)
# ax.plot(x,avg_energy_intensity_modout,'k-',linewidth=2)
#
# # ax.plot(x,med_max_months,'k-',linewidth=4)
# plt.ylabel('Energy Intensity (kWh)')
# plt.xlabel('% of Imported Water Available')
# # Toggle the title to be either gross or net
# plt.title('Avg. Annual GROSS Energy Intensity for Modeled Water Supply',y=1.02)
# # plt.title('Avg. Annual NET Energy Use for Modeled Water Supply in LA County',y=1.02)
# #plt.legend(('Energy Intensity'),loc='upper right')
# plt.ylim(0,4000)
# plt.show()