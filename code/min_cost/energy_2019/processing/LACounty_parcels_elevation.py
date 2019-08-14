##################################################################################
#
# Artes: Modeling Water Management in Los Angeles for Local Water Supplies
#
# This algorithm calculates average energy intensity for pumping water within a
# municipal conveyance system based on assumptions for operating parameters and the
# difference in elevation between the central point of a Water Distribution Network
# all all properties (end-users) in the network).
#
# Copyright: Erik Porse
# California Center for Sustainability Communities at UCLA
# December 2018
#
# http://waterhub.ucla.edu
#
# Permission and use permitted with attribution.
# Creative Commons Attribution 4.0 International License
#
# Please cite the reference below when using or adapting code:
#
# Porse, Erik C., Kathryn B. Mika, Elizabeth Litvak, Kim Manago, Kartiki Naik,
#  Madelyn Glickfeld, Terri Hogue, Mark Gold, Diane Pataki, and Stephanie Pincetl. (2017)
#  Systems Analysis and Optimization of Local Water Supplies in Los Angeles.
#  Journal of Water Resources Planning and Management. 143(9)
#
# This code calculates the elevation and distance differences between water management
# features in LA County for estimating energy intensity for distribution. The estimates
# include the difference between municipal system centroids and each demand parcel, as
# well as the difference between a municipal groundwater pumping site and the system centroid.
# It then calculates the average energy intensity based on difference in height and distance
# between points.
#
##################################################################################

import csv
import numpy as np
from numpy import genfromtxt
import os

######### ENGINEERING CALCULATIONS FOR ENERGY-FOR-PUMPING #########

## Constants and calculations ##
pipe_diameter = 0.8                                         # pipe diameter, in m
q_pump_hr = 2500                                            # pump flow, in m3/hr
q_pump = q_pump_hr/3600.0                                   # pump flow, in m3/sec
h_d = (q_pump/(3.14*(pipe_diameter*0.25)**2))/(2*9.81)      # dynamic head
pump_eff = 0.85                                             # pump efficiency
g = 9.81                                                    # acceleration from gravity
dens_h2o = 1000                                             # density of water, in kg/m3
hour_vol_pumped = q_pump_hr/1233.0                          # one-hour volume of water pumped, based on Flow Rate Q
velocity = q_pump/((3.14*(pipe_diameter**2))*0.25)          # velocity of pipe flow, in m/s
roughness_coef = 100                                        # pipe roughness coefficient, C

# Head for pressurizing water supply pipes, assuming 70 psi
h_p = 70 * 2.31 * 0.305                                        # 1 psi = 2.31 ft. head, converted to meters

####################### IMPORT FILES AND CRUNCH DATA #######################

parcels_file_in = <enter file destination>
#parcels_file_in = <enter file destination>
retailers_file_in = <enter file destination>
gwpump_file_in = <enter file destination>
path = <enter file destination>

# retailers
retailers = np.genfromtxt(fname = retailers_file_in,  delimiter=",",dtype=("|S10"), usecols=(0))
retailers_xcoor = np.genfromtxt(fname = retailers_file_in,  delimiter=",",dtype=(int), usecols=(1))
retailers_ycoor = np.genfromtxt(fname = retailers_file_in,  delimiter=",",dtype=(int), usecols=(2))
retailers_elev = np.genfromtxt(fname = retailers_file_in,  delimiter=",",dtype=(int), usecols=(3))

### Calculations for parcels ###

# text files for printing
#os.remove(path + 'energy_retailers')
f1 = open(path + 'energy_convey_retailers2.txt', 'w')
print >> f1, ' '.join(map(str, ["node", "average_head", "average_energy_intensity", '\r']))

# f = open(path + 'retailers_numparcels.txt', 'w')
# print >> f, ' '.join(map(str, ["node", "number_parcels", '\r']))

# parcels
parcels_elev = np.genfromtxt(fname = parcels_file_in,  delimiter=",",dtype=(int), usecols=(0))
parcels_xcoor = np.genfromtxt(fname = parcels_file_in,  delimiter=",",dtype=(int), usecols=(1))
parcels_ycoor= np.genfromtxt(fname = parcels_file_in,  delimiter=",",dtype=(int), usecols=(2))
parcels_retailer = np.genfromtxt(fname = parcels_file_in,  delimiter=",",dtype=("|S10"), usecols=(4),invalid_raise=False,missing_values='',usemask=False,filling_values=0.0)

print "parcel arrays created"

for x in np.nditer(retailers):
    print x
    index = np.where(retailers == x)
    matches = np.where(parcels_retailer == x)

    parcels_elev_match = np.take(parcels_elev,matches[0])
    parcels_xcoor_match = np.take(parcels_xcoor,matches[0])
    parcels_ycoor_match = np.take(parcels_ycoor,matches[0])

    ## Calculate elevation and distances from retailer centroid to parcel
    h_s = (retailers_elev[index[0]] - parcels_elev_match)*0.305   # static head, convert to meters
    distance =  np.sqrt(((retailers_xcoor[index[0]] - parcels_xcoor_match)*0.305)**2+((retailers_ycoor[index[0]] - parcels_ycoor_match)*0.305)**2)  # in meters
    h_f = 10.67*(((q_pump**1.852)*distance)/((roughness_coef**1.852)*(pipe_diameter**4.8704)))
    h_t_avg = str(np.average(h_s + h_d + h_p + h_f))                    # add static and dynamic head, along with head to pressurize pipes

    ## Calculate energy intensity of pumping  ##
    time = distance / velocity
    power = (q_pump*(h_s + h_d + h_p + h_f)*g*dens_h2o)/(pump_eff*1000)         # in kW
    volume = (q_pump*time)/1233                                     # convert to ac-ft
    energy_intensity = (power*time*0.000278)/volume                 # convert seconds to hours, in kWh/ac-ft
    avg_energy_intensity = np.average(energy_intensity)
    print avg_energy_intensity

    aei = str(avg_energy_intensity)

    print >> f1, ' '.join(map(str, [x, h_t_avg, aei,'\r']))

    # num_parcels = np.count_nonzero(matches)
    # print >> f, ' '.join(map(str, [x, num_parcels, '\r']))

### Calculations for groundwater wells ###

# Readin text files with data
# f2 = open(path + 'energy_convey_gw_pumping.txt', 'w')
# print >> f2, ' '.join(map(str, ["node", "average_head", "average_energy_intensity", '\r']))
#
# # groundwater pumps
# gw_pumps = np.genfromtxt(fname = gwpump_file_in,  delimiter=",",dtype=("|S10"), usecols=(0))
# gw_pumps_xcoor = np.genfromtxt(fname = gwpump_file_in,  delimiter=",",dtype=(int), usecols=(9))
# gw_pumps_ycoor = np.genfromtxt(fname = gwpump_file_in,  delimiter=",",dtype=(int), usecols=(10))
# gw_pumps_elev = np.genfromtxt(fname = gwpump_file_in,  delimiter=",",dtype=(int), usecols=(6))
# gw_pumps_retailer = np.genfromtxt(fname = gwpump_file_in,  delimiter=",",dtype=("|S10"), usecols=(8))
#
# print "groundwater pumping arrays created"
#
# for x in np.nditer(retailers):
#     print x
#     index = np.where(retailers == x)
#     matches = np.where(gw_pumps_retailer == x)
#
#     gw_pumps_elev_match = np.take(gw_pumps_elev, matches[0])
#     gw_pumps_xcoor_match = np.take(gw_pumps_xcoor, matches[0])
#     gw_pumps_ycoor_match = np.take(gw_pumps_ycoor, matches[0])
#
#     ## Calculate elevation and distances from retailer centroid to parcel
#     h_s = (gw_pumps_elev_match - retailers_elev[index[0]]) * 0.305  # static head, convert to meters
#     distance = np.sqrt(((gw_pumps_xcoor_match - retailers_xcoor[index[0]]) * 0.305) ** 2 + (
#                 (gw_pumps_ycoor_match - retailers_ycoor[index[0]]) * 0.305) ** 2)  # in meters
#     h_t_avg = str(np.average(h_s + h_d + h_p))                          # add static and dynamic head, along with head to pressurize pipes
#
#     ## Calculate energy intensity of pumping  ##
#     time = distance / velocity
#     power = (q_pump * (h_s + h_d + h_p) * g * dens_h2o) / (pump_eff * 1000)  # in kW
#     volume = (q_pump * time) / 1233  # convert to ac-ft
#     energy_intensity = (power * time * 0.000278) / volume  # convert seconds to hours, in kWh/ac-ft
#     avg_energy_intensity = np.average(energy_intensity)
#
#     aei = str(avg_energy_intensity)
#
#     print >> f2, ' '.join(map(str, [x, h_t_avg, aei, '\r']))

print "done"
