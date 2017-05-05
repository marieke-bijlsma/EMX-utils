#!/usr/bin/env python

'''
This script converts SPSS files to CSV files.
Produces 3 output CSV files:
	-File with categoricals
	-File with descriptions
	-File with the actual data
'''

import savReaderWriter,csv,os

filePath = '[PATH_TO_FOLDER_WITH_SPSS_FILES]'

#For each file in filePath, check if file exists and ends with the SPSS file extension.
#Store rows and columns in separate lists
for file in os.listdir(filePath):
	#New rows and columns for each file
	rowList=[]
	columnList=[]

	file = filePath + file	
	outputFile = os.path.splitext(file)[0].replace(" ", "_")
	
	if os.path.isfile(file) and file.endswith('.sav'):
		with savReaderWriter.SavReader(file) as reader:
			columns = reader.header
			
			for line in reader:
 				rowList.append(line)
 				
		#Get variable and value labels of SPSS file
		with savReaderWriter.SavHeaderReader(file) as header:
			varlabels = header.all().varLabels
			valuelabels = header.all().valueLabels
	
		
		#Replacing white spaces by underscores and 
		#check if length of each column is more than 30 characters
		for column in columns:
			column = column.replace(" ", "_")
	
			if len(column) > 30:
				print column + " has more than 30 characters!"
		
			columnList.append(column)

		#Write columns and rows to csv file, comma separated
		with open(outputFile + '.csv', 'w') as csvfile:
			columnWriter = csv.DictWriter(csvfile, fieldnames=columnList, delimiter=",")
			rowWriter = csv.writer(csvfile, delimiter=",")
			columnWriter.writeheader()

			for line in rowList:
				rowWriter.writerow(line)

		csvfile.close()

		#Write descriptions to csv file, comma separated
		with open(outputFile + '_description.csv', 'w') as csvfile:
			rowWriter = csv.writer(csvfile, delimiter=",")
			for key,value in varlabels.iteritems():
				rowWriter.writerow([key] + [value])

		csvfile.close() 

		#Write categorical values to csv file, comma separated
		with open(outputFile + '_categoricals.csv', 'w') as csvfile:
			rowWriter = csv.writer(csvfile, delimiter=",")
			for key,value in valuelabels.iteritems():
				for key2,value2 in value.iteritems():
					rowWriter.writerow([key] + [key2] + [value2])

		csvfile.close() 
		
		
