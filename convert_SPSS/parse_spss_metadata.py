#!/usr/bin/env python

import savReaderWriter, csv, os

'''
This script converts SPSS metadata to EMX format.
All files are converted to one EMX attribute file
NOTE: Some columns still need to be filled in manually 
'''

filePath = '[PATH_TO_FOLDER_WITH_SPSS_FILES]'

#Create lists to store information for EMX
#Some lists need to be created as dicts first in order to keep the correct index
columnList = []
labelColumnList = []
descriptionList = {}
entityList = []
dataTypeList = {}
refEntityList = []
nillableList = []
idAttributeList = []


#Write the header of the EMX attributes file
writer = csv.writer(open('EMX_attributes.csv', 'wb'), delimiter=',')
writer.writerow(['name'] + ['label'] + ['description'] + ['entity'] + ['dataType'] + ['refEntity'] + ['nillable'] + ['idAttribute'])


#For each file in filePath, check if file exists and ends with the SPSS file extension.
for file in os.listdir(filePath):

	file = filePath + file	
	
	if os.path.isfile(file) and file.endswith('.sav'):
	
		#Read SPSS file and get header + meta data
		with savReaderWriter.SavReader(file) as reader:
			columns = reader.header
	 
		with savReaderWriter.SavHeaderReader(file) as header:   
			valueLabels = header.all().valueLabels #only categoricals
			varLabels = header.all().varLabels #description
			measureLevels = header.all().measureLevels	#all variables	

		#Store data for the first two columns of EMX attributes
		for column in columns:
			labelColumn = column.lower().replace('_', ' ')	
			column = column.replace(' ','_')

			if len(column) > 30:
				print column + " has more than 30 characters!"

			columnList.append(column)
			labelColumnList.append(labelColumn)


		#Store data for the third column of EMX attributes
		#Insert item on specific index according to index of columnList
		for key,value in varLabels.iteritems():
			idx = columnList.index(key)
			descriptionList[idx] = value


		#Store data for the fourth column of EMX attributes (leave empty for now, cannot be automated)
		for i in range(len(columnList)):
			entityList.append(" ")


		#Store data for the fifth column of EMX attributes
		#Insert item on specific index according to index of columnList
		for key,value in valueLabels.iteritems():
			idx = columnList.index(key)
			dataTypeList[idx] = 'categorical'

		#ValueLabels only contain categoricals, add the other dataTypes too
		for key,value in measureLevels.iteritems():
			idx = columnList.index(key)

			if key not in valueLabels:
				if type(value) == str:
					dataTypeList[idx] = 'string'
				elif type(value) == int:
					dataTypeList[idx] = 'int'
				elif type(value) == float:
					dataTypeList[idx] = 'float'
				else:
					print "Unknown type: " + type(value2)

			
		#Store data for the sixth column of EMX attributes (leave empty for now, cannot be automated)
		for i in range(len(columnList)):
			refEntityList.append(" ")				


		#Store data for the seventh column of EMX attributes (first == idAttribute, leave other values empty for now)
		for i in range(len(columnList)):
			if i == 0:
				nillableList.append('FALSE')
			else:
				nillableList.append(" ")		


		#Store data for eight column of EMX attributes (first == idAttribute, leave other values empty for now)
		for i in range(len(columnList)):
			if i == 0:
				idAttributeList.append('TRUE')
			else:
				idAttributeList.append(" ")		


#Write data stored in lists/dicts to the EMX attributes file
for i in zip(columnList, labelColumnList, descriptionList.values(), entityList, dataTypeList.values(), refEntityList, nillableList, idAttributeList):
	writer.writerow(i)

