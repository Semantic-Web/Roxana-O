# -*- coding: utf-8 -*-
"""

"""
from xml.etree.ElementTree import parse
from pandas import DataFrame
import matplotlib.pyplot as plt
#import plotly.plotly as py
import os
import math 
path = "/Users/roxanaohriniuc/Documents/FAUWorks/SMART/generated-data"
dirs = os.listdir(path)
#print dirs
#patient_list = ['613876','621799','644201','665677','736230','765583','880378','897185','935270','967332']
mean_bp = []
count = 0
std_bp= []

for patient in dirs:  
    doc = ''
    if os.path.splitext(patient)[-1].lower() != ".xml":
        continue
    filename = path +"/"+ patient  
    doc = parse(filename)
    #print doc


    encounter_dates = []
    for encounter in doc.findall('.//{http://hl7.org/fhir}Encounter'):
        period = encounter.find('{http://hl7.org/fhir}period')
        start_date = period.find('{http://hl7.org/fhir}start')        
        encounter_dates.append(start_date.get('value'))
    #print patient
    #print encounter_dates                
    if not encounter_dates:
        #print "No Encounter Dates"
        continue
    
    systolic_bps = []
    diastolic_bps = []
    
    for observation in doc.findall('.//{http://hl7.org/fhir}Observation'):
        text_ele = observation.find('{http://hl7.org/fhir}text')
        div = text_ele.find('{http://www.w3.org/1999/xhtml}div')
        if div.text.find('Systolic') != -1:
            value_quant = observation.find('{http://hl7.org/fhir}valueQuantity')
            value = value_quant.find('{http://hl7.org/fhir}value')
            systolic_bps.append(value.get('value'))
        if div.text.find('Diastolic') != -1:
            value_quant = observation.find('{http://hl7.org/fhir}valueQuantity')
            value = value_quant.find('{http://hl7.org/fhir}value')
            diastolic_bps.append(value.get('value'))
    
    if (not systolic_bps) & (not diastolic_bps):
        #print "No Systolic/Diastolic BP"
        continue
    if((len(encounter_dates)!=len(systolic_bps)) | (len(systolic_bps) != len(diastolic_bps))):
        continue

    enc_dict = {}
    enc_dict['encounter_date'] = encounter_dates
    enc_dict['systolic_bp'] = systolic_bps
    enc_dict['diastolic_bp'] = diastolic_bps
    encounters = DataFrame(enc_dict, columns=['encounter_date', 'diastolic_bp', 'systolic_bp'])
    encounters = encounters.convert_objects(convert_dates='coerce', convert_numeric=True)
    #print encounters
    #encounters.is_copy = False
    enc_period = encounters[(encounters.encounter_date.dt.year >= 2004) & (encounters.encounter_date.dt.year <= 2009)]
    if enc_period.empty:
        #print "No data between given period"
        continue
   
    enc_period['mean_bp'] = enc_period['diastolic_bp']
    #+ ((enc_period['systolic_bp']-enc_period['diastolic_bp'])/3)
    mbp = enc_period['mean_bp'].mean()
    sbp = enc_period['mean_bp'].std()
    if math.isnan(sbp):
        continue
    std_bp.append(sbp)
    count = count +1

    
    mean_bp.append(mbp)
    count = count + 1
   
    

print 'Std:\n ', std_bp
print 'Mean:\n ', mean_bp
print '\nNumber of records: ', count

plt.hist(mean_bp, stacked=True)
plt.title("2004-2009")
plt.xlabel("Mean Blood Pressure")
plt.ylabel("Frequency")
fig = plt.gcf()

plt.figure();
plt.hist(std_bp, align = 'mid', histtype = 'bar')
plt.title("2004-2009")
plt.xlabel("Std Blood Pressure")
plt.ylabel("No. of Patients")
fig = plt.gcf()
#plot_url = py.plot_mpl(fig, filename='mpl-basic-histogram')
