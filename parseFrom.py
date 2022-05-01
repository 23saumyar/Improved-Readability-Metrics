import csv

rtotal = [] #taskNo, caption, fc, c, s, o, type

data = []
r1_50 = []
r51_100 = []
r101_150 = []
r151_200 = []
with open('r3_results_1-50.csv', 'r') as f:
	csvreader = csv.reader(f)
	fields = next(csvreader)
	
	for row in csvreader:
		r1_50.append(row)

with open('r3_results_51-100.csv', 'r') as f:
	csvreader = csv.reader(f)
	fields = next(csvreader)
	
	for row in csvreader:
		r51_100.append(row)

with open('r3_results_101-150.csv', 'r') as f:
	csvreader = csv.reader(f)
	fields = next(csvreader)
	
	for row in csvreader:
		r101_150.append(row)

with open('r3_results_151-200.csv', 'r') as f:
	csvreader = csv.reader(f)
	fields = next(csvreader)
	
	for row in csvreader:
		r151_200.append(row)


with open('final_200_data.csv', 'r') as f:
	csvreader = csv.reader(f)
	fields = next(csvreader)

	for row in csvreader:
		data.append(row)
currTask = 0
dataInd = 0
def parse(pResults, dataInd, currTask):
	print(dataInd)
	for row in pResults:
		caption = row[0]
		if ("Rating Task" in caption):
			currTask += 1
			dataInd += 1
		elif (caption =="" or caption=="Dicom Viewer Link:" or  caption=="Caption"):
			continue
		else:
			if (row[1]== ""):
				fc = ""
				c = ""
				s = ""
				o = ""
			else: 
				fc = row[1][0]
				c = row[2][0]
				s = row[3][0]
				o = row[4][0]		
			cType = data[dataInd][2]
			dicomId = data[dataInd][0]
			rtotal.append([currTask, caption, fc, c, s, o, cType, dicomId])
			dataInd += 1
	return dataInd, currTask
dataInd, currTask = parse(r1_50, dataInd, currTask)
dataInd, currTask = parse(r51_100, dataInd+1, currTask+1)
dataInd, currTask = parse(r101_150, dataInd+1, currTask+1)
dataInd, currTask = parse(r151_200, dataInd+1, currTask+1)

with open("r3_results_parsed.csv", "w") as f:
	w = csv.writer(f)
	w.writerows(rtotal)
