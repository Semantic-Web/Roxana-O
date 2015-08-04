# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 23:02:27 2015

@author: roxanaohriniuc
"""

# -*- coding: utf-8 -*-
"""

@author: roxana ohriniuc
@title:  Oxygen Saturation Mean and Std
*******
This is a histogram that depicts the mean Oxygen Saturation
 certain patients on a given period of time: 2004-2015

*******

"""
from xml.etree.ElementTree import parse
from pandas import DataFrame
#import numpy as np
import matplotlib.pyplot as plt
import os
import math

#Set up path where the data is being retrieved from : 
path = "/Users/roxanaohriniuc/Documents/FAUWorks/SMART/generated-data"
dirs = os.listdir(path)

# We will make an array of the mean and standard dev
#  for the Oxygen Saturation of each patient record
mean_oxy = []
std_oxy = []
count = 0

# finding the records: 
for patient in dirs:  
    doc = ''
    if os.path.splitext(patient)[-1].lower() != ".xml":
        continue
    filename = path +"/"+ patient  
    doc = parse(filename)
    
## We are creating an array that will hold the period of times that 
# the patient data has been saved:
    encounter_dates = []
    for encounter in doc.findall('.//{http://hl7.org/fhir}Encounter'):
        period = encounter.find('{http://hl7.org/fhir}period')
        start_date = period.find('{http://hl7.org/fhir}start')        
        encounter_dates.append(start_date.get('value'))            
    if not encounter_dates:
        continue
    
   # create an array that will hold the value for each patient for 
        # every time the oxygen saturation information has been encountered:
    oxy = []

    ## find every record where the oxygen saturation information has been registered: 
    for observation in doc.findall('.//{http://hl7.org/fhir}Observation'):
        text_ele = observation.find('{http://hl7.org/fhir}text')
        div = text_ele.find('{http://www.w3.org/1999/xhtml}div')
        if div.text.find('oxygen_saturation') != -1:
            value_quant = observation.find('{http://hl7.org/fhir}valueQuantity')
            value = value_quant.find('{http://hl7.org/fhir}value')
            ## add each roxygen saturation data to the array
            oxy.append(float(value.get('value')))

       
    # if there is not oxygen saturation record: skip the observation
    if (not oxy ):
        continue
    if len(oxy) != len(encounter_dates):
        continue
    #creating a dictionary which will hold the encountered date and 
        # the oxygen saturation value

    enc_dict = {}
    enc_dict['encounter_dates'] = encounter_dates
    enc_dict['oxy'] = oxy
    #print enc_dict

    # create  a data frame from the dictionary
    encounters = DataFrame(enc_dict, columns=['encounter_dates', 'oxy'])
    #encounters.is_copy = False
  
    #convert data into values 
    encounters = encounters.convert_objects(convert_dates='coerce', convert_numeric=True)
    enc_period = encounters[(encounters.encounter_dates.dt.year >= 2004) & (encounters.encounter_dates.dt.year <= 2015)]
    if enc_period.empty:
        continue

    # find the mean for each patient and save it in the primary arrays
    mooxy = enc_period['oxy'].mean()
    soxy = enc_period['oxy'].std()
   # print mooxy
    mean_oxy.append(mooxy)
    if math.isnan(soxy):
        soxy = 0.0
    std_oxy.append(soxy)
    count = count +1

print 'Std:\n ', std_oxy
print 'Mean:\n ', mean_oxy
print '\nNumber of records: ', count


# Plot the mean and std for all the records in a histogram.

plt.figure();
plt.hist(mean_oxy, align = 'mid',histtype = 'bar', rwidth = 0.5,stacked=True)
plt.title("2004-2015")
plt.xlabel("Mean Oxygen Saturation")
plt.ylabel("No. of Patients")
fig = plt.gcf()

plt.figure();
plt.hist(std_oxy, align = 'mid', histtype = 'bar')
plt.title("2004-2015")
plt.xlabel("Std Oxygen Saturation")
plt.ylabel("No. of Patients")
fig = plt.gcf()
