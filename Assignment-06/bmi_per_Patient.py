# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 13:27:15 2015

@author: roxanaohriniuc

*******
This is a histogram that depicts the mean BMI of a pool of patients 
on a given period of time: 2004-2008

*******
"""

# -*- coding: utf-8 -*-
"""

"""
from xml.etree.ElementTree import parse
from pandas import DataFrame
import matplotlib.pyplot as plt
import os

#Set up path where the data is being retrieved from : 
path = "/Users/roxanaohriniuc/Documents/FAUWorks/SMART/generated-data"
dirs = os.listdir(path)

# We will make an array of the mean Bmi`s for each patient record
mean_bmi = []
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
        # every time the bmi information has been encountered:
    bmi = []
    
    ## find every record where the bmi information has been registered: 
    for observation in doc.findall('.//{http://hl7.org/fhir}Observation'):
        text_ele = observation.find('{http://hl7.org/fhir}text')
        div = text_ele.find('{http://www.w3.org/1999/xhtml}div')
        if div.text.find('bmi') != -1:
            value_quant = observation.find('{http://hl7.org/fhir}valueQuantity')
            value = value_quant.find('{http://hl7.org/fhir}value')
            ## add each bmi data to the array
            bmi.append(float(value.get('value')))
            
    # if there is not bmi record: skip the observation
    if (not bmi):
        continue
    if len(bmi) != len(encounter_dates):
        continue
    
    #creating a dictionary which will hold the encountered date and 
        # the bmi value
    enc_dict = {}
    enc_dict['encounter_date'] = encounter_dates
    enc_dict['bmi'] = bmi
    
    # create  a data frame from the dictionary
    encounters = DataFrame(enc_dict, columns=['encounter_date', 'bmi'])
    encounter.is_copy = False
    
    #convert data into values 
    encounters = encounters.convert_objects(convert_dates='coerce', convert_numeric=True)
    #encounters.loc['encounter_date', 'bmi'] = ''
    enc_period = encounters[(encounters.encounter_date.dt.year >= 2004) & (encounters.encounter_date.dt.year <= 2008)]
    if enc_period.empty:
        continue
    
    # find the mean for each patient and save it in the mean_bmi array
    mbmi = enc_period['bmi'].mean()
    mean_bmi.append(mbmi)

    count = count +1
print "Mean BMI: "
mean = float(sum(mean_bmi))/ float(len(mean_bmi))
print '%.2f' % mean
# Plot the mean BMI for all the records in a histogram.
plt.figure();
plt.hist(mean_bmi, align = 'mid',histtype = 'bar', rwidth = 0.5,color = 'red',stacked=True)
plt.title("2004-2008")
plt.xlabel("Mean BMI")
plt.ylabel("No. of Patients")
fig = plt.gcf()
