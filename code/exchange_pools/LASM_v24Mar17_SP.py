##################################################################################
#
# Artes: Modeling Water Management in Los Angeles for Local Water Supplies
#
# © Erik Porse, 2016-18
# California Center for Sustainability Communities at UCLA
#
# http://waterhub.ucla.edu
#
# Use permitted with attribution.
# Please cite the reference below when using or adapting code:
#
# Porse, Erik C., Kathryn B. Mika, Elizabeth Litvak, Kim Manago, Kartiki Naik,
#  Madelyn Glickfeld, Terri Hogue, Mark Gold, Diane Pataki, and Stephanie Pincetl. (2017).
#  “Systems Analysis and Optimization of Local Water Supplies in Los Angeles.”
#  Journal of Water Resources Planning and Management. 143(9)
#
# Porse, Erik, Kathryn B. Mika, Rhianna Williams, Mark Gold, William Blomquist, Stephanie Pincetl, 
#  "Groundwater Exchange Pools and Urban Water Supply Sustainability: Modeling Directed and Undirected Networks"
#  Journal of Water Resources Planning and Management (In Press).
#
# This model version has Groundwater Exchange Pools (SP)
#
##################################################################################

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
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


from gurobipy import *

fname_in = '/Users/eporse/Documents/Research/Ecology_Energy_Climate/Water Resources/Countries and Regions/California/Southern California/Systems Analysis/Artes Model/Model Runs/B3_03_30_17/LASM_Data_D100_S0_SP_B3.xlsx'
fname_out1 = '/Users/eporse/Documents/Research/Ecology_Energy_Climate/Water Resources/Countries and Regions/California/Southern California/Systems Analysis/Artes Model/Output/LASM_FlowsRaw_Out.xlsx'
fname_out2 = '/Users/eporse/Documents/Research/Ecology_Energy_Climate/Water Resources/Countries and Regions/California/Southern California/Systems Analysis/Artes Model/Output/LASM_StoragesRaw_Out.xlsx'
fname_out3 = '/Users/eporse/Documents/Research/Ecology_Energy_Climate/Water Resources/Countries and Regions/California/Southern California/Systems Analysis/Artes Model/Output/LASM_Supplies_Out.xlsx'
fname_out4 = '/Users/eporse/Documents/Research/Ecology_Energy_Climate/Water Resources/Countries and Regions/California/Southern California/Systems Analysis/Artes Model/Output/Shadows.xlsx'
path = '/Users/eporse/Documents/Research/Ecology_Energy_Climate/Water Resources/Countries and Regions/California/Southern California/Systems Analysis/Artes Model/Output'

# Initialize dictionaries (arrays) and vectors
nodes = []
demand_nodes = []
month_nodes = []
calib_nodes = []
gw_nodes = []
spreading_nodes = []
recycled_nodes = []
purple_nodes = []
surface_nodes = []
inflows_in = []
calib_inflows_in = []
sur_calib_inflows_in = []
month_demands_in = []
loss_rates_in = []
storage_nodes = []
local_sources = []
origins = []
terminals = []
origins2 = []
terminals2 = []
origins3 = []
terminals3 = []
capacity_value = []
links = []
links = tuplelist(links)
msg_import_links = []
msg_import_links = tuplelist(msg_import_links)
surface_supply_links = []
surface_supply_links = tuplelist(surface_supply_links)
storage_pool_links_in = []
storage_pool_links_in = tuplelist(storage_pool_links_in)
storage_pool_links_out = []
storage_pool_links_out = tuplelist(storage_pool_links_out)
storage_pool_balances = []
storage_pool_balances = tuplelist(storage_pool_balances)
purple_pipes = []
purple_pipes = tuplelist(purple_pipes)
times = []
years = []
calib_years = []
months = []
storage_pumpers = []
storage_pool_nodes_out = ["GSO_CEN","GSO_CHI","GSO_HOL","GSO_MSG","GSO_PUE","GSO_RAY","GSO_SFE",
            "GSO_SIX","GSO_SMC","GSO_SPA","GSO_SYL","GSO_VER","GSO_WCS"]
storage_pool_nodes_in = ["GSI_CEN","GSI_CHI","GSI_HOL","GSI_MSG","GSI_PUE","GSI_RAY","GSI_SFE",
            "GSI_SIX","GSI_SMC","GSI_SPA","GSI_SYL","GSI_VER","GSI_WCS"]

# For scenarios
demand_mult = 0.8 # Demand multiplier, for reducing demands (i.e. conservation)

# initialize Excel file
workbook = xlrd.open_workbook(fname_in, encoding_override="utf_8")
sheet1 = workbook.sheet_by_name("GUROBI Nodes")
sheet2 = workbook.sheet_by_name("GUROBI Links")
sheet3 = workbook.sheet_by_name("GUROBI Demand Nodes")
sheet4 = workbook.sheet_by_name("GUROBI Storage Nodes")
sheet5 = workbook.sheet_by_name("GUROBI Local Sources")
sheet6 = workbook.sheet_by_name("GUROBI Years")
sheet7 = workbook.sheet_by_name("GUROBI Months")
sheet8 = workbook.sheet_by_name("GUROBI Monthly Capacities")
sheet9 = workbook.sheet_by_name("GUROBI Month Nodes")
sheet10 = workbook.sheet_by_name("GUROBI Calibration Nodes")
sheet11 = workbook.sheet_by_name("GUROBI Groundwater")
sheet12 = workbook.sheet_by_name("GUROBI Recycled")
sheet13 = workbook.sheet_by_name("GUROBI Spreading")
sheet14 = workbook.sheet_by_name("GUROBI Surface")
sheet15 = workbook.sheet_by_name("GUROBI Calib Years")
sheet16 = workbook.sheet_by_name("GUROBI Losses")
sheet17 = workbook.sheet_by_name("GUROBI Purple")
sheet18 = workbook.sheet_by_name("GUROBI GW Pool Links Out")
sheet19 = workbook.sheet_by_name("GUROBI Storage Pumpers")
sheet20 = workbook.sheet_by_name("GUROBI GW Pool Links In")

######### READ DATA FROM EXCEL FILE ##########

#Creates index for years & calibration years, turns them into strings
years_in = sheet6.col_values(1)
for i in range(len(years_in)):
    year = str(years_in[i])
    years.append(year[:4])
calib_years_in = sheet15.col_values(1)
for i in range(len(calib_years_in)):
    calib_year = str(calib_years_in[i])
    calib_years.append(calib_year[:4])
#Creates index for months and turns it into a string
months_in = sheet7.col_values(1)
for i in range(len(months_in)):
    month = months_in[i].encode('utf-8')
    months.append(month)

## GET NODES DATA ##
# Read in nodes
nodes_in = sheet1.col_values(1)
for i in range(len(nodes_in)):
    node = nodes_in[i].encode('utf-8')
    nodes.append(node)

# Read in groundwater nodes and operating safe yields
gw_nodes_in = sheet11.col_values(1)
for i in range(len(gw_nodes_in)):
    gw_node = gw_nodes_in[i].encode('utf-8')
    gw_nodes.append(gw_node)
gw_opyield_in = sheet11.col_values(2)

# Annual and monthly demands
ann_demand_in = sheet1.col_values(2)
for i in range(len(nodes)):
    month_demand_in = sheet1.row_values(i, start_colx=3, end_colx=15)
    month_demands_in.append(month_demand_in)

# Read in upper and lower storage bounds for nodes
storage_lower_in = sheet1.col_values(15)
storage_upper_in = sheet1.col_values(16)

# Reads in inflows and re-arranges array to be 3-D
for i in range(len(nodes)):
    #inflow_in = sheet1.row_values(i,start_colx=17, end_colx=None)
    inflow_in = sheet1.row_values(i,start_colx=137, end_colx=None)
    inflows_in.append(inflow_in)
inflows_3d = numpy.zeros(shape=(len(nodes),len(years),len(months)))

for i in range(len(nodes)):
    m = 0
    for j in range(len(years)):
        for k in range(len(months)):
            inflows_3d[i][j][k] = inflows_in[i][m]
            m = m+1

# Reads in lists of nodes with demands and storage capacity
demand_nodes_in = sheet3.col_values(1)
for i in range(len(demand_nodes_in)):
    demand_node = demand_nodes_in[i].encode('utf-8')
    demand_nodes.append(demand_node)

for i in range(len(nodes)):
    loss_rate = sheet16.row_values(i,start_colx=2, end_colx=None)
    loss_rates_in.append(loss_rate)

storage_nodes_in = sheet4.col_values(1)
for i in range(len(storage_nodes_in)):
    storage_node = storage_nodes_in[i].encode('utf-8')
    storage_nodes.append(storage_node)
storage_delta_in = sheet4.col_values(3)

# Reads in list of nodes that are "local" sources of water
local_sources_in = sheet5.col_values(1)
for i in range(len(local_sources_in)):
    local = local_sources_in[i].encode('utf-8')
    local_sources.append(local)

# Reads in list of nodes that are calibration nodes- gauges and WWTPs
calib_node_in = sheet10.col_values(1)
for i in range(len(calib_node_in)):
    calib = calib_node_in[i].encode('utf-8')
    calib_nodes.append(calib)

# Reads in list of nodes for recycled water sources, reuse capacities, and purple pipe
recycled_nodes_in = sheet12.col_values(1)
for i in range(len(recycled_nodes_in)):
    recycled_node = recycled_nodes_in[i].encode('utf-8')
    recycled_nodes.append(recycled_node)
reuse_cap_in = sheet12.col_values(2)

purple_nodes_in = sheet17.col_values(1)
for i in range(len(purple_nodes_in)):
    purple_node = purple_nodes_in[i].encode('utf-8')
    purple_nodes.append(purple_node)

# Reads in additional node lists for calculating output metrics
spreading_nodes_in = sheet13.col_values(1)
for i in range(len(spreading_nodes_in)):
    spreading_node = spreading_nodes_in[i].encode('utf-8')
    spreading_nodes.append(spreading_node)

surface_nodes_in = sheet14.col_values(1)
for i in range(len(surface_nodes_in)):
    surface_node = surface_nodes_in[i].encode('utf-8')
    surface_nodes.append(surface_node)

storage_pumpers_in = sheet19.col_values(1)
for i in range(len(storage_pumpers_in)):
    storage_pumper = storage_pumpers_in[i].encode('utf-8')
    storage_pumpers.append(storage_pumper)

# Reads in calibration flows and re-arranges array to be 3-D
# CALIBRATION YEARS INCLUDE 1996-2010 (Years with Full Historical Flow Data Surface Watersheds)
####
# For Calibration with 1996-2010 for WWTPs
for i in range(len(calib_nodes)):
    calib_inflow_in = sheet10.row_values(i,start_colx=2, end_colx=None)
    calib_inflows_in.append(calib_inflow_in)
calib_inflows_3d = numpy.zeros(shape=(len(nodes),len(calib_years),len(months)))

for i in range(len(calib_nodes)):
    m = 0
    for j in range(len(calib_years)):
        for k in range(len(months)):
            calib_inflows_3d[i][j][k] = calib_inflows_in[i][m]
            m = m+1
###

###
# For Calibration with Surface Watersheds, 1986-2010
for i in range(len(surface_nodes)):
    sur_calib_inflow_in = sheet14.row_values(i,start_colx=2, end_colx=None)
    sur_calib_inflows_in.append(sur_calib_inflow_in)
sur_calib_inflows_3d = numpy.zeros(shape=(len(nodes),len(years),len(months)))

for i in range(len(surface_nodes)):
    m = 0
    for j in range(len(years)):
        for k in range(len(months)):
            sur_calib_inflows_3d[i][j][k] = sur_calib_inflows_in[i][m]
            m = m+1
###

## GET LINKS DATA ##
# Read data for origin and terminal nodes of each link
origins_in = sheet2.col_values(1)
for i in range(len(origins_in)):
    origin = origins_in[i].encode('utf-8')
    origins.append(origin)

terminals_in = sheet2.col_values(2)
for i in range(len(terminals_in)):
    terminal = terminals_in[i].encode('utf-8')
    terminals.append(terminal)

# Link capacities- annual
capacity_in = sheet2.col_values(3)
# Link capacities- monthly, for selected facilities (WRPs and Spreading Basins)
month_nodes_in = sheet9.col_values(1)
for i in range(len(month_nodes_in)):
    month_node = month_nodes_in[i].encode('utf-8')
    month_nodes.append(month_node)
month_capacity_dry_in = sheet8.col_values(2)
month_capacity_wet_in = sheet8.col_values(3)

# Rinse and repeat for groundwater storage pools
# Pool Outflow Links
origins_in2 = sheet18.col_values(1)
for i in range(len(origins_in2)):
    origin2 = origins_in2[i].encode('utf-8')
    origins2.append(origin2)
terminals_in2 = sheet18.col_values(2)
for i in range(len(terminals_in2)):
    terminal2 = terminals_in2[i].encode('utf-8')
    terminals2.append(terminal2)

# Pool Inflow Links
origins_in3 = sheet20.col_values(1)
for i in range(len(origins_in3)):
    origin3 = origins_in3[i].encode('utf-8')
    origins3.append(origin3)
terminals_in3 = sheet20.col_values(2)
for i in range(len(terminals_in3)):
    terminal3 = terminals_in3[i].encode('utf-8')
    terminals3.append(terminal3)

# Storage pool annual extraction and recharge capacities
capacity_in2 = sheet18.col_values(3)
capacity_in3 = sheet20.col_values(3)

## ASSIGN KEYS ##
# Gives keys (indices) of nodes/links for lists of lists
ann_demand = dict.fromkeys(nodes, )
month_demand = dict.fromkeys(nodes, )
demand_upper = dict.fromkeys(nodes, )
demand_lower = dict.fromkeys(nodes, )
loss_rates = dict.fromkeys(nodes, )
inflow = dict.fromkeys(nodes, )
calib_inflow = dict.fromkeys(calib_nodes, )
sur_calib_inflow = dict.fromkeys(surface_nodes, )
storage_lower = dict.fromkeys(nodes, )
storage_upper = dict.fromkeys(nodes, )
storage_delta = dict.fromkeys(storage_nodes, )
capacity = dict.fromkeys(links, )
pool_capacity_out = dict.fromkeys(storage_pool_links_out)
pool_capacity_in = dict.fromkeys(storage_pool_links_in)
month_capacity_dry = dict.fromkeys(month_nodes, )
month_capacity_wet = dict.fromkeys(month_nodes, )
reuse_capacity = dict.fromkeys(recycled_nodes, )
gw_opyield = dict.fromkeys(gw_nodes, )

# Create the dictionaries with values for demands/storage (by node)
# and capacities (by link- origin to terminal node)
for i in range(len(origins)):
    link = (origins[i],terminals[i])
    links.append(link)

msg_import_link = (('MWD_SGV','SUR_SDM'),('MWD_SGV','SUR_BDM'),('MWD_USG','SUR_SGU'),('MWD_THV','SPG_LIT'))
for i in range(len(msg_import_link)):
    msg_import_links.append(msg_import_link[i])

surface_supply_link = (('SUR_ASE','CTY_PAS'),('SUR_SAU','CTY_SIE'),('SUR_SDM','IOU_GSM'),('SUR_SGU','CTY_AZU'),('SUR_SGU','MWC_COV'),('SUR_SGU','IOU_CAW'))
for i in range(len(surface_supply_link)):
    surface_supply_links.append(surface_supply_link[i])

for node in range(len(nodes)):
    ann_demand[nodes[node]] = ann_demand_in[node] * 1

for node in range(len(nodes)):
    for month in range(len(months)):
        month_demand[nodes[node],months[month]] = month_demands_in[node][month] * 1

for node in range(len(nodes)):
    for month in range(len(months)):
        loss_rates[nodes[node],months[month]] = loss_rates_in[node][month] * 1

for node in range(len(nodes)):
    for year in range(len(years)):
        for month in range(len(months)):
            inflow[nodes[node],years[year],months[month]] = inflows_3d[node][year][month] * 1

# Create separate dictionaries for groundwater storage exchange pools

for i in range(len(origins2)):
    storage_pool_link_out = (origins2[i],terminals2[i])
    storage_pool_links_out.append(storage_pool_link_out)

for i in range(len(origins3)):
    storage_pool_link_in = (origins3[i],terminals3[i])
    storage_pool_links_in.append(storage_pool_link_in)

for i in range(len(storage_pool_nodes_out)):
    storage_pool_balance = (storage_pool_nodes_out[i],storage_pool_nodes_in[i])
    storage_pool_balances.append(storage_pool_balance)

# Create separate dictionary for purple pipe networks of recycled water
for i in range(len(recycled_nodes)):
    for j in range(len(purple_nodes)):
        if [(x,y) for x,y in links if x == recycled_nodes[i] and y == purple_nodes[j]]:
            purple_pipe = (recycled_nodes[i],purple_nodes[j])
            purple_pipes.append(purple_pipe)

# For Calibration of 1996-2010, WWTPs and Surface Watersheds
for node in range(len(calib_nodes)):
    for year in range(len(calib_years)):
        for month in range(len(months)):
            calib_inflow[calib_nodes[node],calib_years[year],months[month]] = calib_inflows_3d[node][year][month] * 1

# For Calibration of 1986-2010, Surface Watersheds
for node in range(len(surface_nodes)):
    for year in range(len(years)):
        for month in range(len(months)):
            sur_calib_inflow[surface_nodes[node],years[year],months[month]] = sur_calib_inflows_3d[node][year][month] * 1

for node in range(len(nodes)):
    storage_lower[nodes[node]] = storage_lower_in[node] * 1

for node in range(len(gw_nodes)):
    gw_opyield[gw_nodes[node]] = gw_opyield_in[node] * 1

for node in range(len(nodes)):
    storage_upper[nodes[node]] = storage_upper_in[node] * 1

for node in range(len(storage_nodes)):
    storage_delta[storage_nodes[node]] = storage_delta_in[node] * 1

for node in range(len(recycled_nodes)):
    reuse_capacity[recycled_nodes[node]] = reuse_cap_in[node] * 1

for link in range(len(links)):
    capacity[links[link]] = capacity_in[link] * 1

for link in range(len(storage_pool_links_out)):
    pool_capacity_out[storage_pool_links_out[link]] = capacity_in2[link] * 1

for link in range(len(storage_pool_links_in)):
    pool_capacity_in[storage_pool_links_in[link]] = capacity_in3[link] * 1

for node in range(len(month_nodes)):
    month_capacity_dry[month_nodes[node]] = month_capacity_dry_in[node] * 1

for node in range(len(month_nodes)):
    month_capacity_wet[month_nodes[node]] = month_capacity_wet_in[node] * 1

##################### CREATE OPTIMIZATION MODEL #######################
m = Model('local_reliance')

# Create variables
flow = {}
for i,j in links:
    for y in years:
        for t in months:
            flow[i,j,y,t] = m.addVar(ub=capacity[i,j],obj=1.0,
                                       name='flow-%s-%s-%s-%s' % (i,j,y,t))

storage = {}
for j in nodes:
    for y in years:
        for t in months:
            storage[j,y,t] = m.addVar(ub=storage_upper[j],lb=storage_lower[j],obj=1.0,
                                    name='storage-%s-%s-%s' % (j,y,t))

losses = {}
for j in nodes:
    for y in years:
        for t in months:
            losses[j,y,t] = m.addVar(lb=0,obj=1.0,name='losses-%s-%s-%s' % (j,y,t))

penalty = {}
for j in nodes:
    for y in years:
        for t in months:
            penalty[j,y,t] = m.addVar(lb=0,obj=1.0,name='penalty-%s-%s-%s' % (j,y,t))

shortage = {}
for j in nodes:
    for y in years:
        for t in months:
            shortage[j,y,t] = m.addVar(obj=1.0,name='supplies-%s-%s-%s' % (j,y,t))

direct_supply = {}
for j in nodes:
    for y in years:
        for t in months:
            direct_supply[j,y,t] = m.addVar(obj=1.0,name='direct_supply-%s-%s-%s' % (j,y,t))

storage_penalty = {}
for j in storage_nodes:
    for y in years:
        for t in months:
            storage_penalty[j,y,t] = m.addVar(obj=1.0,name='supplies-%s-%s-%s' % (j,y,t))

local_supplies = {}
for j in nodes:
    for y in years:
        for t in months:
            local_supplies[j,y,t] = m.addVar(obj=1.0,name='local_supplies-%s-%s-%s' % (j,y,t))

gw_ann_produced = {}
for j in gw_nodes:
    for y in years:
        gw_ann_produced[j,y] = m.addVar(ub=gw_opyield[j],lb=0,
                                        obj=1.0,name='gw_produced-%s-%s' % (j,y))

# Update the model with variables
m.update()

## Constraints ##
# Network flow conservation
for j in nodes:
    for y in years:
        for t in months:
            if t == 'Jan':
                #if y == '1986':
                if y == '1996':
                    # sums flows when its January of the first year
                    m.addConstr(
                        quicksum(flow[i,j,y,t] for i,j in links.select('*',j)) + inflow[j,y,t] ==
                        quicksum(flow[j,k,y,t] for j,k in links.select(j,'*')) + storage[j,y,t] + losses[j,y,t],
                            'node-%s-%s-%s' % (j,y,t))
                else:
                    # sums flows when its January but not the first year- reaches back to Dec previous year
                    m.addConstr(
                        quicksum(flow[i,j,y,t] for i,j in links.select('*',j)) + inflow[j,y,t] +
                        storage[j,years[years.index(y)-1],months[months.index(t)+11]] ==
                        quicksum(flow[j,k,y,t] for j,k in links.select(j,'*')) + storage[j,y,t] + losses[j,y,t],
                            'node-%s-%s-%s-%s' % (i,j,y,t))
            else:
                # sums flows when its all months other than January of any year- reaches back to previous month
                m.addConstr(
                    quicksum(flow[i,j,y,t] for i,j in links.select('*',j)) + inflow[j,y,t] +
                    storage[j,y,months[months.index(t)-1]] ==
                    quicksum(flow[j,k,y,t] for j,k in links.select(j,'*')) + storage[j,y,t] + losses[j,y,t],
                    'node-%s-%s-%s-%s' % (i,j,y,t))

# Link capacity constraints
for i,j in links:
    if j in demand_nodes:
        for y in years:
            for t in months:
                m.addConstr(
                    quicksum(flow[i,j,y,t] for t in months) <= capacity[i,j],'cap-%s-%s-%s-%s' % (i,j,y,t))

# Link minimum flow constraints
for i,j in links:
    for y in years:
        for t in months:
            m.addConstr(flow[i,j,y,t] >= 0,'cap-%s-%s-%s-%s' % (i,j,y,t))

# For nodes, losses are at least equal to empirical minimums
# Losses include:
# 1) Demand nodes- irrigation and distribution systems,
# 2) Reservoirs- evaporation and seepage (assumed 3%)
# 3) surface nodes- evapotranspiration and groundwater recharge
for j in nodes:
    for y in years:
        for t in months:
            m.addConstr(
                quicksum(flow[i,j,y,t] for i,j in links.select('*',j)) * loss_rates[j,t] <= losses[j,y,t],
                    'loss_rate-%s-%s-%s' % (j,y,t))

# Storage node constraints (primarily for groundwater and surface water storage nodes)
for j in nodes:
    for y in years:
        for t in months:
            m.addConstr(storage[j,y,t] <= storage_upper[j],'us-%s-%s-%s' % (j,y,t))

for j in nodes:
    for y in years:
        for t in months:
            m.addConstr(storage[j,y,t] >= storage_lower[j],'ls-%s-%s-%s' % (j,y,t))

# Node demand constraints and calculations- not used if incorporating shortages
# for j in demand_nodes:
#     for y in years:
#         for t in months:
#             m.addConstr(
#                 quicksum(flow[i,j,y,t] for i,j in links.select('*',j)) >= (month_demand[j,t] * demand_mult),
#                 'demand-%s-%s-%s' % (j,y,t))

# Groundwater pumping restrictions based on annual basin operating safe yields
for i in gw_nodes:
    for y in years:
        for t in months:
            m.addConstr(
                quicksum(flow[i,j,y,t] for i,j in links.select(i,'*') for t in months) == gw_ann_produced[i,y],
                    'gw-ann_prod-%s-%s' % (i,y))

# Flow constraints into WWTPs and spreading basins
for j in month_nodes:
    for y in years:
        for t in months:
            # sets monthly flow capacities based on dry (Apr-Sept) or wet (Oct-Mar) weather flows
            if any([t == 'Oct', t == 'Nov', t == 'Dec', t == 'Jan', t == 'Feb', t == 'Mar']):
                m.addConstr(
                    quicksum(flow[i,j,y,t] for i,j in links.select('*',j)) <= month_capacity_wet[j],
                        'eng_capacities-%s-%s-%s-%s' % (i,j,y,t))
            else:
                m.addConstr(
                    quicksum(flow[i,j,y,t] for i,j in links.select('*',j)) <= month_capacity_dry[j],
                        'eng_capacities-%s-%s-%s-%s' % (i,j,y,t))

# Water Reuse Capacities in Purple Pipe Networks
for i in recycled_nodes:
    for y in years:
        for t in months:
            m.addConstr(
                quicksum(flow[i,j,y,t] for i,j in purple_pipes.select(i,'*')) <= reuse_capacity[i],
                    'reuse-%s-%s-%s-%s' % (i,j,y,t))

# Local Use Calculations
for j in local_sources:
    for y in years:
        for t in months:
            m.addConstr(
                local_supplies[j,y,t] == quicksum(flow[i,j,y,t] for i,j in links.select('*',j)),
                    'local_supplies-%s-%s-%s-%s' % (i,j,y,t))

# Constraints to limit reservoir additions or withdrawls
for i in storage_nodes:
    for y in years:
        for t in months:
            m.addConstr(
                quicksum(flow[i,j,y,t] for i,j in links.select(i,"*")) <= 300000,
                        'storage_change-%s-%s-%s-%s' % (i,j,y,t))

############## STORAGE POOL CALCULATIONS AND CONSTRAINTS #######################

# Annual storage and pumping limits to/from storage pools
for i,j in storage_pool_links_out:
    for y in years:
        for t in months:
            m.addConstr(
                quicksum(flow[i,j,y,t] for t in months) <= capacity[i,j],
                    'pool-supply_constr-%s-%s' % (i,y))
for i,j in storage_pool_links_in:
    for y in years:
        for t in months:
            m.addConstr(
                quicksum(flow[i,j,y,t] for t in months) <= capacity[i,j],
                    'pool-supply_constr-%s-%s' % (i,y))

# Storage pool activity must follow >> total inputs = total ouputs
for a,b in storage_pool_balances:
    for y in years:
        for t in months:
            m.addConstr(
                quicksum(flow[a,b,y,t] for a,b in storage_pool_links_in.select('*',b) for y in years for t in months) ==
                quicksum(flow[a,b,y,t] for a,b in storage_pool_links_out.select(a,'*') for y in years for t in months),
                'pools_mbal-%s-%s-%s' % (b,y,t))

############## END STORAGE POOL CALCULATIONS AND CONSTRAINTS #######################

############## PENALTY FUNCTION CONSTRAINTS #######################

# The shortage function that regulates nodes meeting demands is hacked to prevent duplicated undirected network flows from being counted as supplies
for j in demand_nodes:
    for y in years:
        for t in months:
            m.addConstr(
                shortage[j,y,t] == (month_demand[j,t] * demand_mult) - quicksum(flow[i,j,y,t] for i,j in links.select('*',j)),
                                    # quicksum(flow[j,k,y,t] for j,k in storage_pool_links_in.select(j,'*')),
                                    'shortage-%s-%s-%s' % (j,y,t))

for j in local_sources:
    for y in years:
        for t in months:
            m.addConstr(
                penalty[j,y,t] == losses[j,y,t],
                    'penalty-%s-%s-%s' % (j,y,t))

################# END OF PENALTY CONSTRAINTS ########################

################# CALIBRATION CONSTRAINTS ########################

# Surface node calibration constraints
for i in surface_nodes:
    for y in years:
        for t in months:
            if i == "SUR_PAC":
                 b = 0  # dummy fill to make it skip the calibration step for Pac Ocean inflows- calibrated below
            else:
                m.addConstr(
                    quicksum(flow[i,j,y,t] for i,j in links.select(i,'*')) >= 0.75 * sur_calib_inflow[i,y,t],
                        'calib2-inflow_low-%s-%s-%s' % (i,y,t))
                m.addConstr(
                    quicksum(flow[i,j,y,t] for i,j in links.select(i,'*')) <= 1.25 * sur_calib_inflow[i,y,t],
                        'calib2-inflow_high-%s-%s-%s' % (i,y,t))

# Constrain Pacific Ocean inflows from Ballona, LA River, and SG River
pac_river_inflows = ["SUR_BAC","CAL_319","SUR_SGO"] # major river outflows with data
for y in years:
   for i in pac_river_inflows:
       for j in surface_nodes:
           if j == 'SUR_PAC':
               for t in months:
                   m.addConstr(
                       quicksum(flow[i,j,y,t] for i,j in links.select(i,j) for t in months for i in pac_river_inflows) >= 0.75 * sur_calib_inflow[j,y,t],
                           'calib2-inflow_low-%s-%s-%s' % (j,y,t))
                   m.addConstr(
                       quicksum(flow[i,j,y,t] for i,j in links.select(i,j) for t in months for i in pac_river_inflows) <= 1.25 * sur_calib_inflow[j,y,t],
                           'calib2-inflow_high-%s-%s-%s' % (j,y,t))

# WWTP calibration node constraints
for i in calib_nodes:
    for y in calib_years:
        for t in months:
            m.addConstr(
                quicksum(flow[i,j,y,t] for i,j in links.select(i,'*')) >= 0.05 * calib_inflow[i,y,t],
                    'calib-inflow_low-%s-%s-%s' % (i,y,t))
            m.addConstr(
                quicksum(flow[i,j,y,t] for i,j in links.select(i,'*')) <= 3.0 * calib_inflow[i,y,t],
                    'calib-inflow_high-%s-%s-%s' % (i,y,t))

################# END OF CALIBRATION CONSTRAINTS ########################

#### Objective Functions ####

# Minimize Shortages
# m.setObjective((quicksum((shortage[j,y,t]) for j in demand_nodes for y in years for t in months)) +
#               quicksum(penalty[j,y,t] for j in nodes for y in years for t in months) -
#               quicksum(local_supplies[j,y,t] for j in nodes for y in years for t in months),
#               GRB.MINIMIZE)
#m.setObjective(shortage[j,y,t], GRB.MINIMIZE)

# Set Objective: Maximize use of Local Sources with Perfect Foresight
m.setObjective(quicksum(local_supplies[j,y,t] for j in nodes for y in years for t in months) -
                quicksum(penalty[j,y,t] for j in nodes for y in years for t in months) -
                (100 * quicksum(shortage[j,y,t] for j in nodes for y in years for t in months)),
                GRB.MAXIMIZE)
# m.setObjective(quicksum(local_supplies[j,y,t] for j in nodes for y in years for t in months) -
#                quicksum(penalty[j,y,t] for j in nodes for y in years for t in months),
#                GRB.MAXIMIZE)

# Feasibility tolerance parameter to work through a model on edge of feasibility #
#m.setParam(GRB.Param.FeasibilityTol, 1e-05)

m.optimize()

############## END OF OPTIMIZATION ALGORITHM #######################

############### WRITE SOLUTIONS ##################

## If Feasible Solution ##
#m.write("model.rlp")

## If Infeasible Solution ##
m.computeIIS()
m.write("model.ilp")

# Read output variables
solution = m.getAttr('X', flow)
storages = m.getAttr('X', storage)
losses = m.getAttr('X', losses)
shortages = m.getAttr('X', shortage)
constraint = m.getConstrs()

shadows = tablib.Dataset()
for i in range(len(constraint)):
    shadow = [constraint[i].getAttr("ConstrName"),constraint[i].getAttr("Pi"),constraint[i].getAttr("IISConstr")]
    shadows.append(shadow)

###### Print out text files #######

# Calculate storage pool allocations
pool_supplies = {}
for j in storage_pumpers:
    for y in years:
        for t in months:
            pool_value = (quicksum(solution[i,j,y,t] for i,j in storage_pool_links_out.select('*',j)) -
                            quicksum(solution[j,k,y,t] for j,k in storage_pool_links_in.select(j,'*')))
            pool_supplies[j,y,t] = pool_value.getValue()

# Reconfigure solution and write text files
os.remove(path + "/" + "demands.txt")
os.remove(path + "/" + "inflows.txt")
os.remove(path + "/" + "supplies.txt")
os.remove(path + "/" + "exports.txt")
os.remove(path + "/" + "prev_storage.txt")
os.remove(path + "/" + "curr_storage.txt")
os.remove(path + "/" + "losses.txt")
os.remove(path + "/" + "shortages.txt")
os.remove(path + "/" + "summary_annual.txt")
os.remove(path + "/" + "summary_monthly.txt")
os.remove(path + "/" + "gw_storage_pool.txt")

f1 = open(path + "/" + "demands.txt", "ab")
f2 = open(path + "/" + "inflows.txt", "ab")
f3 = open(path + "/" + "supplies.txt", "ab")
f4 = open(path + "/" + "exports.txt", "ab")
f5 = open(path + "/" + "prev_storage.txt", "ab")
f6 = open(path + "/" + "curr_storage.txt", "ab")
f7 = open(path + "/" + "losses.txt", "ab")
f8 = open(path + "/" + "shortages.txt", "ab")
f11 = open(path + "/" + "summary_annual.txt", "ab")
f12 = open(path + "/" + "summary_monthly.txt", "ab")
f13 = open(path + "/" + "gw_storage_pool.txt", "ab")

for j in nodes:
    demands = []
    inflows_txt = []
    supplies_txt = []
    exports = []
    prev_storages = []
    curr_storages = []
    losses_txt = []
    shortages_txt = []
##############################

    for y in years:
        for t in months:
            value_in = quicksum(solution[i,j,y,t] for i,j in links.select('*',j))
            value_out = quicksum(solution[j,k,y,t] for j,k in links.select(j,'*'))
            if t == 'Jan':
                #if y == '1986':
                if y == '1996':
                    demand = month_demand[j,t] * demand_mult
                    demands.append(demand)
                    inflow_txt = inflow[j,y,t]
                    inflows_txt.append(inflow_txt)
                    supply_txt = value_in.getValue()
                    supplies_txt.append(supply_txt)
                    export = value_out.getValue()
                    exports.append(export)
                    prev_storage = 0
                    prev_storages.append(prev_storage)
                    curr_storage = storages[j,y,t]
                    curr_storages.append(curr_storage)
                    loss_txt = losses[j,y,t]
                    losses_txt.append(loss_txt)
                    shortage_txt = shortages[j,y,t]
                    shortages_txt.append(shortage_txt)

                else:
                    demands.insert(len(demands),month_demand[j,t] * demand_mult)
                    inflows_txt.insert(len(inflows_txt),inflow[j,y,t])
                    supplies_txt.insert(len(supplies_txt),value_in.getValue())
                    exports.insert(len(exports),value_out.getValue())
                    prev_storages.insert(len(prev_storages),storages[j,years[years.index(y)-1],months[months.index(t)+11]])
                    curr_storages.insert(len(curr_storages),storages[j,y,t])
                    losses_txt.insert(len(losses_txt),losses[j,y,t])
                    shortages_txt.insert(len(shortages_txt),shortages[j,y,t])

            else:
                demands.insert(len(demands),month_demand[j,t] * demand_mult)
                inflows_txt.insert(len(inflows_txt),inflow[j,y,t])
                supplies_txt.insert(len(supplies_txt),value_in.getValue())
                exports.insert(len(exports),value_out.getValue())
                prev_storages.insert(len(prev_storages),storages[j,y,months[months.index(t)-1]])
                curr_storages.insert(len(curr_storages),storages[j,y,t])
                losses_txt.insert(len(losses_txt),losses[j,y,t])
                shortages_txt.insert(len(shortages_txt),shortages[j,y,t])

    demands_str = ' '.join(map(str, demands))
    inflows_txt_str = ' '.join(map(str, inflows_txt))
    supplies_txt_str = ' '.join(map(str, supplies_txt))
    exports_str = ' '.join(map(str, exports))
    prev_storages_str = ' '.join(map(str, prev_storages))
    curr_storages_str = ' '.join(map(str, curr_storages))
    losses_str = ' '.join(map(str, losses_txt))
    shortages_str = ' '.join(map(str, shortages_txt))
    print >> f1,j,demands_str
    print >> f2,j,inflows_txt_str
    print >> f3,j,supplies_txt_str
    print >> f4,j,exports_str
    print >> f5,j,prev_storages_str
    print >> f6,j,curr_storages_str
    print >> f7,j,losses_str
    print >> f8,j,shortages_str

# Write to Storage Pool File
for i,j in storage_pool_links_out:
    gw_pool_imps_txt = []
    for y in years:
        for t in months:
            value_in = (solution[i,j,y,t])
            if t == 'Jan':
                #if y == '1986':
                if y == '1996':
                    gw_pool_imp_txt = value_in
                    gw_pool_imps_txt.append(gw_pool_imp_txt)

                else:
                    gw_pool_imps_txt.insert(len(gw_pool_imps_txt),value_in)

            else:
                gw_pool_imps_txt.insert(len(gw_pool_imps_txt),value_in)

    gw_pool_imps_txt_str = ' '.join(map(str, gw_pool_imps_txt))
    print >> f13,i,j,gw_pool_imps_txt_str

for i,j in storage_pool_links_in:
    gw_pool_imps_txt = []
    for y in years:
        for t in months:
            value_in = (solution[i,j,y,t])
            if t == 'Jan':
                #if y == '1986':
                if y == '1996':
                    gw_pool_imp_txt = value_in
                    gw_pool_imps_txt.append(gw_pool_imp_txt)

                else:
                    gw_pool_imps_txt.insert(len(gw_pool_imps_txt),value_in)

            else:
                gw_pool_imps_txt.insert(len(gw_pool_imps_txt),value_in)

    gw_pool_imps_txt_str = ' '.join(map(str, gw_pool_imps_txt))
    print >> f13,i,j,gw_pool_imps_txt_str

## Some Output Calculations ##
gw_pumping = []
gw_pumping_month = []
gw_recharge = []
gw_recharge_month = []
sw_capture = []
sw_capture_month = []
recycled = []
recycled_month = []
reuse = []
reuse_month = []
hyperion_recycled = []
swp_to_lacity = []
barrier_injection = []
msg_import_recharge = []
surface_supplies = []
imported_supply = []
imported_supply_month = []
imported_use = []
imported_use_month = []
ocean_inflows = []
ocean_inflows_month = []
shortages_file = []
gw_pools_exchange = []
gw_pools_exchange_month = []

## Annual Summed Values ##
for y in years:
    value_sum = 0
    for i in gw_nodes:
        for t in months:
            value = quicksum(flow[i,j,y,t] for i,j in links.select(i,"*") for t in months)
        value_sum = value.getValue() + value_sum
    gw_pumping.append(value_sum)

for y in years:
    value_sum = 0
    for j in gw_nodes:
        for t in months:
            value = quicksum(flow[i,j,y,t] for i,j in links.select("*",j) for t in months)
        value_sum = value.getValue() + value_sum
    gw_recharge.append(value_sum)

for y in years:
    value_sum = 0
    for j in demand_nodes:
        for t in months:
            value = quicksum(shortage[j,y,t] for t in months)
        value_sum = value.getValue() + value_sum
    shortages_file.append(value_sum)

for y in years:
    value_sum = 0
    for j in spreading_nodes:
        for t in months:
            value = quicksum(flow[i,j,y,t] for i,j in links.select("*",j) for t in months)
        value_sum = value.getValue() + value_sum
    sw_capture.append(value_sum)

for y in years:
    value_sum = 0
    for i in recycled_nodes:
        for t in months:
            value = quicksum(flow[i,j,y,t] for i,j in links.select(i,'*') for t in months)
        value_sum = value.getValue() + value_sum
    recycled.append(value_sum)

for y in years:
    value_sum = 0
    for i in recycled_nodes:
        for t in months:
            value = quicksum(flow[i,j,y,t] for i,j in purple_pipes.select(i,'*') for t in months)
        value_sum = value.getValue() + value_sum
    reuse.append(value_sum)

for y in years:
    for i in nodes:
        if i == 'INF_CSB':
            for j in gw_nodes:
                for t in months:
                    value = quicksum(flow[i,j,y,t] for i,j in links.select(i,'*') for t in months)
            barrier_injection.append(value.getValue())

for y in years:
    for i,j in msg_import_links:
        for t in months:
            value = quicksum(flow[i,j,y,t] for i,j in msg_import_links.select('*','*') for t in months)
    msg_import_recharge.append(value.getValue())

for y in years:
    for t in months:
        value = quicksum(flow[i,j,y,t] for i,j in surface_supply_links.select('*','*') for t in months)
    surface_supplies.append(value.getValue())

for i in nodes:
    for j in nodes:
        if all([i == 'WRP_HYP', j == 'WRP_LIT']):
            for y in years:
                for t in months:
                    value = quicksum(flow[i,j,y,t] for i,j in links.select(i,j) for t in months)
                hyperion_recycled.append(value.getValue())

for y in years:
    for j in nodes:
        if j == 'MWD_MET':
            for t in months:
                value = quicksum(flow[i,j,y,t] for i,j in links.select('*',j) for t in months)
    imported_supply.append(value.getValue())

for y in years:
    for i in nodes:
        if i == 'MWD_MET':
            for t in months:
                value = quicksum(flow[i,j,y,t] for i,j in links.select(i,'*') for t in months)
    imported_use.append(value.getValue())

for i in nodes:
    for j in nodes:
        if all([i == 'INF_SWP', j == 'CTY_LAX']):
            for y in years:
                for t in months:
                    value = quicksum(flow[i,j,y,t] for i,j in links.select(i,j) for t in months)
                swp_to_lacity.append(value.getValue())

for y in years:
    for j in nodes:
        if j == 'SUR_PAC':
            for t in months:
                value = quicksum(flow[i,j,y,t] for i,j in links.select('*',j) for t in months)
    ocean_inflows.append(value.getValue())

for y in years:
    for t in months:
        value = quicksum(pool_supplies[j,y,t] for j in storage_pumpers for t in months)
    gw_pools_exchange.append(value.getValue())

## Monthly Summed Values ##
for y in years:
    for t in months:
        value_sum = 0
        for i in gw_nodes:
            value = quicksum(flow[i,j,y,t] for i,j in links.select(i,"*"))
            value_sum = value.getValue() + value_sum
        gw_pumping_month.append(value_sum)

for y in years:
    for t in months:
        value_sum = 0
        for j in gw_nodes:
            value = quicksum(flow[i,j,y,t] for i,j in links.select("*",j))
            value_sum = value.getValue() + value_sum
        gw_recharge_month.append(value_sum)

for y in years:
    for t in months:
        value_sum = 0
        for j in spreading_nodes:
            value = quicksum(flow[i,j,y,t] for i,j in links.select("*",j))
            value_sum = value.getValue() + value_sum
        sw_capture_month.append(value_sum)

for y in years:
    for t in months:
        value_sum = 0
        for i in recycled_nodes:
            value = quicksum(flow[i,j,y,t] for i,j in links.select(i,'*'))
            value_sum = value.getValue() + value_sum
        recycled_month.append(value_sum)

for y in years:
    for t in months:
        value_sum = 0
        for i in recycled_nodes:
            value = quicksum(flow[i,j,y,t] for i,j in purple_pipes.select(i,'*'))
            value_sum = value.getValue() + value_sum
        reuse_month.append(value_sum)

for y in years:
    for t in months:
        value_sum = 0
        for i in nodes:
            if i == 'MWD_MET':
                    value = quicksum(flow[i,j,y,t] for i,j in links.select(i,'*'))
        imported_supply_month.append(value.getValue())

for y in years:
    for t in months:
        value_sum = 0
        for j in nodes:
            if j == 'MWD_MET':
                    value = quicksum(flow[i,j,y,t] for i,j in links.select('*',j))
        imported_use_month.append(value.getValue())
        
for y in years:
    for t in months:
        value_sum = 0
        for j in nodes:
            if j == 'SUR_PAC':
                    value = quicksum(flow[i,j,y,t] for i,j in links.select('*',j))
        ocean_inflows_month.append(value.getValue())

for y in years:
    for t in months:
        value = quicksum(pool_supplies[j,y,t] for j in storage_pumpers)
        gw_pools_exchange_month.append(value.getValue())

## Print Summary Outputs ##
print >> f11, "parameter", (" ".join(years))
print >> f11, "gw_pumping", (" ".join( repr(e) for e in gw_pumping))
print >> f11, "gw_recharge", (" ".join( repr(e) for e in gw_recharge))
print >> f11, "sw_capture", (" ".join( repr(e) for e in sw_capture))
print >> f11, "recycled", (" ".join( repr(e) for e in recycled))
print >> f11, "reuse", (" ".join( repr(e) for e in reuse))
print >> f11, "barrier_injection", (" ".join( repr(e) for e in barrier_injection))
print >> f11, "msg_import_recharge", (" ".join( repr(e) for e in msg_import_recharge))
print >> f11, "hyperion_recycled", (" ".join( repr(e) for e in hyperion_recycled))
print >> f11, "imported_supply", (" ".join( repr(e) for e in imported_supply))
print >> f11, "imported_use", (" ".join( repr(e) for e in imported_use))
print >> f11, "ocean_inflows", (" ".join( repr(e) for e in ocean_inflows))
print >> f11, "shortages", (" ".join( repr(e) for e in shortages_file))
print >> f11, "surface_supplies", (" ".join( repr(e) for e in surface_supplies))
print >> f11, "swp_to_lacity", (" ".join( repr(e) for e in swp_to_lacity))
print >> f11, "gw_pools_exchange", (" ".join( repr(e) for e in gw_pools_exchange))

print >> f12, "gw_pumping", (" ".join( repr(e) for e in gw_pumping_month))
print >> f12, "gw_recharge", (" ".join( repr(e) for e in gw_recharge_month))
print >> f12, "sw_capture", (" ".join( repr(e) for e in sw_capture_month))
print >> f12, "recycled", (" ".join( repr(e) for e in recycled_month))
print >> f12, "reuse", (" ".join( repr(e) for e in reuse_month))
print >> f12, "imported_supply", (" ".join( repr(e) for e in imported_supply_month))
print >> f12, "imported_use", (" ".join( repr(e) for e in imported_use_month))
print >> f12, "ocean_inflows", (" ".join( repr(e) for e in ocean_inflows_month))
print >> f12, "gw_pools_exchange", (" ".join( repr(e) for e in gw_pools_exchange_month))

#### Use tablib to write out Excel file with constraints, shadows, and IIS includes
shadows.headers = ['Constraint','Shadow Value','Included in IIS?']
with open(fname_out4, 'wb') as f:
   f.write(shadows.xlsx)

###### TROUBLESHOOTING #######

# for j in storage_pumpers:
#    for y in years:
#        for t in months:
#            print j,y,t,direct_supply[j,y,t],pools_supply[j,y,t]

# print 'break'
#
# for i,j in links:
#     for y in years:
#         for t in months:
#             if j == 'MWD_THV':
#                print y,t,(flow[i,j,y,t])
#             if i == 'MWD_THV':
#                print y,t,(flow[i,j,y,t])
#
# print 'break'
#

###### END TROUBLESHOOTING #######
#('MWD_SGV','SUR_SDM'),('MWD_SGV','SUR_BDM'),('MWD_USG','SUR_SGU'),('MWD_THV','SPG_LIT')
