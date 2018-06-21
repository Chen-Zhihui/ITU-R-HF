import sys
import os
import operator
from glob import glob
import csv
import math
import datetime
import pdb 

#######################
# Output print function
#######################

def PrintComp(InData, outstr, filename):
	n = 0
	sum = 0
	sqrsum = 0
	for data in InData:
		n =  n + 1
		sum = sum + data
		sqrsum = sqrsum + math.pow(data, 2.0)
	if(n != 0):
		mean = sum/n
		std = math.sqrt(((sqrsum/n)-(math.pow(sum/n,2.0))))
	else:
		mean = 0.0;
		std = 0.0

	outstr = outstr + '\t{0:5d}\t{1:>4.1f}\t{2:>4.1f}'
	print(outstr.format(n, mean, std), file = filename)
	return()

def EoT(month):
	doty = [ 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334 ] 

	# At present this code only works for the 15th day of the month
	# If this changes a day field should be added to the path structure
	#and passed into this routine
	day = 15 

	# Earth's mean angular orbital velocity
	W = (360.0/365.24)*D2R # radians

	# The angle the earth has moved in it's orbit from the December solstice to date D
	# the approximate number of days between the Dec solstice and Jan 1st is 10 days
	D = doty[month-1] + day
	A = W*(D + 10) # radians

	# The angle the Earth has moved from the Dec solstice, including the correction for the Earth's orbital eccentricity, 0.0167
	# The number 12 is the number of days from the solstice to the Earth's perihelion
	B = A + (0.0167*math.sin(A - (12.0*W)))

	# The difference between the angles moved and the mean speed
	C = (A - math.atan2(math.tan(B), math.cos(23.44*D2R)))/math.pi

	# The equation of time is then
	return(4.0*math.pi*(C - (int(C + 0.5)))) # minutes
	
def PrintGroup(flag, Catagory):
	# This function prints out the catagory that the measurement matches
	if(flag == 0):
		# print(Catagory,',', ID,',',year,',', season)
		flag = 1
	
	return(flag)
	
# Constants
D2R = math.pi/180.0
R2D = 180.0/math.pi
# Earth radius
R0 = 6371.0

# The output files in .\D1\out are the output files from ITUHFProp() while
# the output files in .\D1\REC_out are the output files from REC533
# This routine processes the output file D1Comp.csv that is generated by
# either ITUHFProp_parse.py or REC_parse.py

#################################################################
############ Now Start the Comparison ###########################
#################################################################

# Open the D1 Compare file
D1Comp = open('D1Comp.csv','r')

# Open D1 Table 1
D1T1 = open('D1_Table1.csv','r')

# Open D1 Table 2
D1T2 = open('D1_Table2.csv','r')

# Open D1 Table 3
D1T3 = open('D1_Table3.csv','r')

# Frequency Group
FG1 = []
FG2 = []
FG3 = []
FG4 = []

# Distance Group
D01 = []
D02 = []
D03 = []
D04 = []
D05 = []
D06 = []
D07 = []
D08 = []
D09 = []
D10 = []
D11 = []
D12 = []

# Sunspot Number Group
SSN1 = []
SSN2 = []
SSN3 = []
SSN4 = []
SSN5 = []
SSN6 = []

# Season Group
WINTER = []
SUMMER = []
SPRING = []
AUTUMN = []

# Geomagnetic Latitude
GL1 = []
GL2 = []
GL3 = []
GL4 = []

# Mid point local time
MLT1 = []
MLT2 = []
MLT3 = []
MLT4 = []
MLT5 = []
MLT6 = []

# Origin of data
GER	= []
JPN	= []
CHN = []
IND	= []
DW = []
BBC = []
AUS = []

# All Group
AD1 = []
AD2 = []
AD3 = []

# Local time
LT1 = []
LT2 = []
LT3 = []
LT4 = []
LT5 = []
LT6 = []

PathID = []
for i in range(0,181):
	PathID.append([])
	
idflag = [0]*181

# Ignore the first line in the D1 Table 1 file
D1T1data = D1T1.readline()

# Ignore the first line in the D1 Table 2 file
D1T2data = D1T2.readline()

m = 1
for D1Compdata in D1Comp:

	# Parse the data to compare
	D1Compdata = D1Compdata.split(',')
	
	# Read the corresponding D1 Table 1 data
	D1T1data = D1T1.readline().split(',')

	ID = int(D1T1data[0])
	freq = float(D1T1data[3])
	dist = float(D1T1data[8])
	ssn = int(D1T1data[9])
	year = int(D1T1data[10])

	TXname = D1T1data[1]	
	
	# Determine where there the receiver is
	TXlat = D2R*(float(D1T1data[4].strip('NS').split('.')[0])+(float(D1T1data[4].strip('NS').split('.')[1])/60))
	NorS = D1T1data[4].strip('-0123456789.')
	TXlng = D2R*(float(D1T1data[5].strip('EW').split('.')[0])+(float(D1T1data[5].strip('EW').split('.')[1])/60))
	EorW = D1T1data[5].strip('-0123456789.')
		
	if(NorS == 'S'):
		TXlat = -TXlat
	if(EorW == 'W'):
		TXlng = -TXlng
			
	RXlat = math.radians(float(D1T1data[6].strip('NS').split('.')[0])+(float(D1T1data[6].strip('NS').split('.')[1])/60))
	NorS = D1T1data[6].strip('-0123456789.')
	RXlng = math.radians(float(D1T1data[7].strip('EW').split('.')[0])+(float(D1T1data[7].strip('EW').split('.')[1])/60))
	EorW = D1T1data[6].strip('-0123456789.')

	if(NorS == 'S'):
		RXlat = -RXlat
	if(EorW == 'W'):
		RXlng = -RXlng

	# Determine the path distance
	distance = 2.0*R0*math.asin(math.sqrt(math.pow((math.sin((TXlat-RXlat)/2.0)),2.0) + math.cos(TXlat)*math.cos(RXlat)*math.pow((math.sin((TXlng - RXlng)/2.0)),2.0)))

	ID = int(D1T1data[0])
	if(ID >= 169): # Long way round
		distance = 2.0*R0*math.pi - distance

	# Find the path mid point
	d = distance/R0
	A = math.sin(0.5*d)/math.sin(d)
	B = math.sin(0.5*d)/math.sin(d)
	x = A*math.cos(TXlat)*math.cos(TXlng) +  B*math.cos(RXlat)*math.cos(RXlng);
	y = A*math.cos(TXlat)*math.sin(TXlng) +  B*math.cos(RXlat)*math.sin(RXlng);
	z = A*math.sin(TXlat) +  B*math.sin(RXlat);
	midlat = math.atan2(z,math.sqrt(math.pow(x,2)+math.pow(y,2)));
	midlng = math.atan2(y,x);

	# Find the geomagnetic latitude
	# Geomagnetic pole 78.5 N 68.2 W
	GeoMagPolelat = 78.5*D2R; 
	GeoMagPolelng = -68.2*D2R;
	
	# there->lat =  asin(     sin(here.lat)*   sin(GeoMagNPole.lat) +     cos(here.lat)*   cos(GeoMagNPole.lat)*    cos(here.lng - GeoMagNPole.lng));
	gmmidlat = math.fabs(math.asin(math.sin(midlat)*math.sin(GeoMagPolelat) + math.cos(midlat)*math.cos(GeoMagPolelat)*math.cos(midlng - GeoMagPolelng)));
	# there->lng =  asin(     cos(here.lat)*   sin(here.lng - GeoMagNPole.lng)/  cos(there->lat));
	gmmidlng = math.asin(math.cos(midlat)*math.sin(midlng - GeoMagPolelng)/math.cos(gmmidlat));

	# Read the measurement data
	# Read the corresponding D1 Table 2 data
	D1T2data = D1T2.readline().split(',')

	# Check to see if the IDs match if not print an error and exit
	if((int(D1Compdata[0]) != int(D1T2data[0])) or (int(D1T2data[0]) != (int(D1T1data[0])))):
		print('Error: IDs #',m,' do not match. Prediction ID ', int(D1Compdata[0]),' ', int(D1Compdata[1]),' ', int(D1Compdata[2]), 'D1T2 = ', int(D1T2data[0]), 'D1T1 = ', int(D1T1data[0]))
		sys.exit()
	
	season = int(D1T2data[2])
	
	# Determine the mid path time offset from the UTC
	ltimeoffset = EoT(season)/60.0 + ((midlng)/(15.0*D2R))
	
	fflag = 0
	dflag = 0
	lsflag = 0
	gflag = 0
	ssnflag = 0
	mpflag = 0
	sflag = 0
	oflag = 0

	for hr in range(24):
		
		ltime = hr + ltimeoffset + 1
		# roll over the hour
		if(ltime > 24):
			ltime = ltime - 24
		elif(ltime <= 0):
			ltime = ltime + 24
				
		#if((int(D1T2data[hr+3]) != 99) and ((D1Compdata[hr+3]) != -307.0)):
		if((int(D1T2data[hr+3])) != 99):
			diff = float(D1Compdata[hr+3]) - float(D1T2data[hr+3])
			if(math.fabs(diff) > 50):
				print('Large error ', diff,' (', D1Compdata[hr+3],',',D1T2data[hr+3],') for ', ID,',',year,',', season, ',', hr)
			# Frequency Groups
			if(freq <= 5):
				fflag = PrintGroup(fflag, 'FG5')
				FG1.append(diff)
			elif((freq > 5 ) and (freq <= 10)):
				fflag = PrintGroup(fflag, 'FG5-10')
				FG2.append(diff)
			elif((freq > 10 ) and (freq <= 15)):
				fflag = PrintGroup(fflag, 'FG10-15')
				FG3.append(diff)
			elif((freq > 15 ) and (freq <= 30)):
				fflag = PrintGroup(fflag, 'FG15-30')
				FG4.append(diff)
				
			# Distances
			if((dist >= 0 ) and (dist <= 999)):
				dflag = PrintGroup(dflag, 'D0-999')
				D01.append(diff)
			elif((dist >= 1000 ) and (dist <= 1999)):
				dflag = PrintGroup(dflag, 'D1000-1999')
				D02.append(diff)
			elif((dist >= 2000 ) and (dist <= 2999)):
				dflag = PrintGroup(dflag, 'D2000-2999')
				D03.append(diff)
			elif((dist >= 3000 ) and (dist <= 3999)):
				dflag = PrintGroup(dflag, 'D3000-3999')
				D04.append(diff)
			elif((dist >= 4000 ) and (dist <= 4999)):
				dflag = PrintGroup(dflag, 'D4000-4999')
				D05.append(diff)
			elif((dist >= 5000 ) and (dist <= 6999)):
				dflag = PrintGroup(dflag, 'D5000-6999')
				D06.append(diff)
			elif((dist >= 7000 ) and (dist <= 8999)):
				dflag = PrintGroup(dflag, 'D7000-8999')
				D07.append(diff)
			elif((dist >= 9000 ) and (dist <= 11999)):
				dflag = PrintGroup(dflag, 'D9000-11999')
				D08.append(diff)
			elif((dist >= 12000 ) and (dist <= 14999)):
				dflag = PrintGroup(dflag, 'D12000-14999')
				D09.append(diff)
			elif((dist >= 15000 ) and (dist <= 17999)):
				dflag = PrintGroup(dflag, 'D15000-17999')
				D10.append(diff)
			elif((dist >= 18000 ) and (dist <= 21999)):
				dflag = PrintGroup(dflag, 'D18000-21999')
				D11.append(diff)
			elif((dist >= 22000 ) and (dist <= 40000)):
				dflag = PrintGroup(dflag, 'D22000-40000')
				D12.append(diff)
				
			# Long or Short distances
			if(dist > 9000 ):
				lsflag = PrintGroup(lsflag, 'LS9000')
				AD1.append(diff)
			elif(dist < 7000 ):
				lsflag = PrintGroup(lsflag, 'LS7000')
				AD2.append(diff)
			
			# All distances
			AD3.append(diff)
				
			# Sun Spot Number
			if((ssn >= 0 ) and (ssn <= 14)):
				ssnflag = PrintGroup(ssnflag, 'SSN0-14')
				SSN1.append(diff)
			elif((ssn >= 15 ) and (ssn <= 44)):
				ssnflag = PrintGroup(ssnflag, 'SSN15-44')
				SSN2.append(diff)
			elif((ssn >= 45 ) and (ssn <= 74)):
				ssnflag = PrintGroup(ssnflag, 'SSN45-74')
				SSN3.append(diff)
			elif((ssn >= 75 ) and (ssn <= 104)):
				ssnflag = PrintGroup(ssnflag, 'SSN75-104')
				SSN4.append(diff)
			elif((ssn >= 105 ) and (ssn <= 149)):
				ssnflag = PrintGroup(ssnflag, 'SSN105-149')
				SSN5.append(diff)
			elif(ssn > 149):
				ssnflag = PrintGroup(ssnflag, 'SSN149')
				SSN6.append(diff)
			
			# Midpoint hour
			if((ltime >= 0 ) and (ltime <= 4)):
				mpflag = PrintGroup(mpflag, 'MP0-4')
				MLT1.append(diff)
			elif((ltime > 4 ) and (ltime <= 8)):
				mpflag = PrintGroup(mpflag, 'MP4-8')
				MLT2.append(diff)
			elif((ltime > 8 ) and (ltime <= 12)):
				mpflag = PrintGroup(mpflag, 'MP8-12')
				MLT3.append(diff)
			elif((ltime > 12 ) and (ltime <= 16)):
				mpflag = PrintGroup(mpflag, 'MP12-16')
				MLT4.append(diff)
			elif((ltime > 16 ) and (ltime <= 20)):
				mpflag = PrintGroup(mpflag, 'MP16-20')
				MLT5.append(diff)
			elif((ltime > 20 ) and (ltime <= 24)):
				mpflag = PrintGroup(mpflag, 'mp20-24')
				MLT6.append(diff)

			# Season
			if(math.floor(midlat) >= 0): # Northern hemisphere
				if((season == 11 ) or (season == 12) or (season == 1) or (season == 2)):
					sflag = PrintGroup(sflag, 'WINTER')
					WINTER.append(diff)
				elif((season == 3 ) or (season == 4)):
					sflag = PrintGroup(sflag, 'SPRING')
					SPRING.append(diff)
				elif((season == 5 ) or (season == 6) or (season == 7) or (season == 8)):
					sflag = PrintGroup(sflag, 'SUMMER')
					SUMMER.append(diff)
				elif((season == 9 ) or (season == 10)):
					sflag = PrintGroup(sflag, 'AUTUMN')
					AUTUMN.append(diff)
			elif(math.floor(midlat) < 0):
				if((season == 11 ) or (season == 12) or (season == 1) or (season == 2)):
					sflag = PrintGroup(sflag, 'SUMMER')
					SUMMER.append(diff)
				elif((season == 3 ) or (season == 4)):
					sflag = PrintGroup(sflag, 'SPRING')
					AUTUMN.append(diff)
				elif((season == 5 ) or (season == 6) or (season == 7) or (season == 8)):
					sflag = PrintGroup(sflag, 'WINTER')
					WINTER.append(diff)
				elif((season == 9 ) or (season == 10)):
					sflag = PrintGroup(sflag, 'SPRING')
					SPRING.append(diff)
					
			# Geomagnetic Latitude
			if((gmmidlat >= 0*D2R ) and (gmmidlat <= 20*D2R)):
				gflag = PrintGroup(gflag, 'G0-20')
				GL1.append(diff)
			elif((gmmidlat > 20*D2R ) and (gmmidlat <= 40*D2R)):
				gflag = PrintGroup(gflag, 'G20-40')
				GL2.append(diff)
			elif((gmmidlat > 40*D2R ) and (gmmidlat <= 60*D2R)):
				gflag = PrintGroup(gflag, 'G40-60')
				GL3.append(diff)
			elif(gmmidlat > 60*D2R ):
				gflag = PrintGroup(gflag, 'G60')
				GL4.append(diff)
				
			# Origin of data
			# Germany
			if((ID ==  8) or (ID ==  9) or (ID == 10) or (ID == 11) or
			   (ID == 12) or (ID == 13) or (ID == 16) or (ID == 17) or
			   (ID == 18) or (ID == 19) or (ID == 20) or (ID == 21) or
			   (ID == 22) or (ID == 23) or (ID == 24) or (ID == 25) or
			   (ID == 26) or (ID == 27) or (ID == 28) or (ID == 29) or
			   (ID == 30) or (ID == 41) or (ID == 42) or (ID == 43) or
			   (ID == 44) or (ID == 50) or (ID == 72) or (ID == 75) or
			   (ID == 76) or (ID == 94) or (ID == 95) or (ID == 96) or
			   (ID == 97) or (ID == 98) or (ID == 99) or (ID == 103) or
			   (ID == 104) or (ID == 105) or (ID == 106) or (ID == 107) or
			   (ID == 111) or (ID == 112) or (ID == 113) or (ID == 114) or
			   (ID == 115) or (ID == 116) or (ID == 131) or (ID == 132) or
			   (ID == 133) or (ID == 134) or (ID == 135) or	(ID == 137) or
			   (ID == 138) or (ID == 139) or (ID == 142) or	(ID == 143) or
			   (ID == 144) or (ID == 145) or (ID == 161) or	(ID == 162) or
			   (ID == 163) or (ID == 164) or (ID == 165) or	(ID == 166) or
			   (ID == 167) or (ID == 168) or (ID == 170) or	(ID == 171) or
			   (ID == 172) or (ID == 173) or (ID == 175) or	(ID == 176) or
			   (ID == 177) or (ID == 178)):
				oflag = PrintGroup(oflag, 'ORG Germany')
				GER.append(diff)
			# Japan
			elif((ID ==  3) or (ID ==  4) or (ID ==  5) or (ID ==  6) or
				 (ID == 33) or
				 (ID == 102) or (ID == 136) or (ID == 152) or (ID == 157) or
				 (ID == 158) or (ID == 159) or (ID == 160) or	(ID == 180) or
				 (ID == 181)):
				oflag = PrintGroup(oflag, 'ORG Japan')
				JPN.append(diff)
			# China
			elif((ID == 31) or (ID == 34) or (ID == 35) or (ID == 36) or
				 (ID == 37) or (ID == 38) or (ID == 39) or (ID == 40) or
				 (ID == 45) or (ID == 46) or (ID == 47) or (ID == 62) or
				 (ID == 63) or (ID == 64) or (ID == 65) or (ID == 66) or
			     (ID == 80) or (ID == 81) or (ID == 82) or (ID == 83) or
			     (ID == 108) or (ID == 120) or (ID == 122) or (ID == 123) or
 			     (ID == 124) or (ID == 125) or (ID == 149)):
				oflag = PrintGroup(oflag, 'ORG China')
				CHN.append(diff)
			# India
			elif((ID ==  2) or (ID ==  7) or (ID == 32) or (ID == 49) or
				 (ID == 52) or (ID == 53) or (ID == 54) or (ID == 55) or
				 (ID == 58) or (ID == 59) or	(ID == 61) or (ID == 67) or	
				 (ID == 68) or (ID == 69) or	(ID == 70) or (ID == 77) or
				 (ID == 78) or (ID == 79) or
			     (ID == 117) or (ID == 118) or (ID == 128) or (ID == 150)):
				oflag = PrintGroup(oflag, 'ORG India')
				IND.append(diff)
			# Deutsche Welle
			elif((ID ==  1) or (ID == 14) or (ID == 15) or (ID == 51) or
			     (ID == 73) or (ID == 74) or (ID == 90) or (ID == 91) or
			     (ID == 92) or 
				 (ID == 129) or (ID == 130) or (ID == 148) or (ID == 174)):
				oflag = PrintGroup(oflag, 'ORG Deutsche Welle')
				DW.append(diff)
			# BBC/EBU
			elif((ID == 56) or (ID == 57) or (ID == 60) or (ID == 71) or (ID == 84) or
			     (ID == 85) or (ID == 86) or (ID == 87) or (ID == 88) or (ID == 89) or
			     (ID == 93) or	
				 (ID == 100) or (ID == 101) or (ID == 109) or (ID == 110) or (ID == 119) or
				 (ID == 121) or (ID == 126) or (ID == 127) or (ID == 140) or (ID == 141) or
			     (ID == 146) or	(ID == 147) or (ID == 151) or (ID == 153) or (ID == 154) or
				 (ID == 155) or	(ID == 156) or (ID == 169) or (ID == 179)):
				oflag = PrintGroup(oflag, 'ORG BBC/EBU')
				BBC.append(diff)
			# Austrailia
			elif(ID == 48):
				oflag = PrintGroup(oflag, 'ORG Austrailia')
				AUS.append(diff)
				
			# Now sort by ID
			for i in range(0,181):
				if(ID == i+1):
					idflag[i] = PrintGroup(idflag[i], '')
					PathID[i].append(diff)
	# Increment the line counter
	m = m + 1
	
# Close all the files
D1Comp.close()
D1T1.close()
D1T2.close()
D1T3.close()

#########################################################################
# Find the date time string
dtstr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Open the comparison file
D1Compfilename = 'D1 to '+str(sys.argv[1])+' '+dtstr.replace(':','-')+'.txt'
D1Compfp = open(D1Compfilename, 'wt')

# Inform the user that the report file has been created
print('\nWriting P.1148 report to file ',D1Compfilename);

##################################################################################
# Output the report						
print('************************************************************************', file = D1Compfp)
print('\tComparison between CCIR Data Bank D1 and %s():' % str(sys.argv[1]), file = D1Compfp)
print('\t\t    ITU Above and Below the MUF', file = D1Compfp)
print('\t\t       ', dtstr, file = D1Compfp)
print('************************************************************************', file = D1Compfp)
print()

# Frequency Group

print('\t\t\t\t\t\t\t\t\tCount\tdiff.\t\tstd', file = D1Compfp)	

PrintComp(FG1, '\nfrequency group   2 -  5\t\t', D1Compfp)
PrintComp(FG2,   'frequency group > 5 - 10\t\t', D1Compfp)
PrintComp(FG3,   'frequency group >10 - 15\t\t', D1Compfp)
PrintComp(FG4,   'frequency group >15 - 30\t\t', D1Compfp)

# Distance Group

PrintComp(D01, '\ndistance      0 -   999 km \t\t', D1Compfp)
PrintComp(D02,   'distance   1000 -  1999 km \t\t', D1Compfp)
PrintComp(D03,   'distance   2000 -  2999 km \t\t', D1Compfp)
PrintComp(D04,   'distance   3000 -  3999 km \t\t', D1Compfp)
PrintComp(D05,   'distance   4000 -  4999 km \t\t', D1Compfp)
PrintComp(D06,   'distance   5000 -  6999 km \t\t', D1Compfp)
PrintComp(D07,   'distance   7000 -  8999 km \t\t', D1Compfp)
PrintComp(D08,   'distance   9000 - 11999 km \t\t', D1Compfp)
PrintComp(D09,   'distance  12000 - 14999 km \t\t', D1Compfp)
PrintComp(D10,   'distance  15000 - 17999 km \t\t', D1Compfp)
PrintComp(D11,   'distance  18000 - 21999 km \t\t', D1Compfp)
PrintComp(D12,   'distance  22000 - 40000 km \t\t', D1Compfp)
# Geomagnetic Latitude

PrintComp(GL1, '\ngeom. lat.    0 - 20 deg. at midpt.', D1Compfp)
PrintComp(GL2,   'geom. lat. > 20 - 40 deg. at midpt.', D1Compfp)
PrintComp(GL3,   'geom. lat. > 40 - 60 deg. at midpt.', D1Compfp)
PrintComp(GL4,   'geom. lat.      > 60 deg. at midpt.', D1Compfp)

# Sunspot Number

PrintComp(SSN1, '\nsunspot number    0 -  14 \t\t', D1Compfp)
PrintComp(SSN2,   'sunspot number   15 -  44 \t\t', D1Compfp)
PrintComp(SSN3,   'sunspot number   45 -  74 \t\t', D1Compfp)
PrintComp(SSN4,   'sunspot number   75 - 104 \t\t', D1Compfp)
PrintComp(SSN5,   'sunspot number  105 - 149 \t\t', D1Compfp)
PrintComp(SSN6,   'sunspot number      > 149 \t\t', D1Compfp)

# Season

PrintComp(WINTER, '\nwinter\t\t\t\t\t\t\t', D1Compfp)
PrintComp(SPRING,   'spring\t\t\t\t\t\t\t', D1Compfp)
PrintComp(SUMMER,   'summer\t\t\t\t\t\t\t', D1Compfp)
PrintComp(AUTUMN,   'autumn\t\t\t\t\t\t\t', D1Compfp)

# Local time at mid point

PrintComp(MLT1, '\nlocal time > 00 - 04 UTC at midpt.', D1Compfp)
PrintComp(MLT2,   'local time > 04 - 08 UTC at midpt.', D1Compfp)
PrintComp(MLT3,   'local time > 08 - 12 UTC at midpt.', D1Compfp)
PrintComp(MLT4,   'local time > 12 - 16 UTC at midpt.', D1Compfp)
PrintComp(MLT5,   'local time > 16 - 20 UTC at midpt.', D1Compfp)
PrintComp(MLT6,   'local time > 20 - 24 UTC at midpt.', D1Compfp)

# Origin

PrintComp(GER, '\norigin of data: Germany\t\t\t', D1Compfp)
PrintComp(JPN,   'origin of data: Japan\t\t\t', D1Compfp)
PrintComp(CHN,   'origin of data: China\t\t\t', D1Compfp)
PrintComp(IND,   'origin of data: India\t\t\t', D1Compfp)
PrintComp(DW,    'origin of data: Deutsche Welle\t', D1Compfp)
PrintComp(BBC,   'origin of data: BBC/EBU\t\t\t', D1Compfp)
PrintComp(AUS,   'origin of data: Australia\t\t', D1Compfp)

# All Distances
PrintComp(AD2, '\nall distances < 7000 km \t\t', D1Compfp)
PrintComp(AD1,   'all distances > 9000 km \t\t', D1Compfp)

PrintComp(AD3, '\nall distances\t\t\t\t\t', D1Compfp)

print(' ', file = D1Compfp)
print('************************************************************************', file = D1Compfp)
print('\f', file = D1Compfp)
print('************************************************************************', file = D1Compfp)
print(' ', file = D1Compfp)
print(' ID Transmitter\t\tReceiver\tFrequency\tCount\tdiff.\t\tstd', file = D1Compfp)
print(' ', file = D1Compfp)
#####################################################################
# Create a report for each individual ID
# Open D1 Table 1
D1 = open('dbank_d1.txt','r')

# Read down to Table 1
for D1data in D1:
	if(D1data.count('ID. TX-NAME      RX-NAME') != 0):
		break
# Read 3 more lines
D1.readline()
D1.readline()
D1.readline()

# Read the next 181 lines
D1str = []
for i in range(0,181):
	D1data = D1.readline()
	ID = int(D1data[0:3])
	TX_Name = D1data[4:16]
	RX_Name = D1data[17:28]
	freq = float(D1data[30:34])
	# For this ID create the output string
	D1str.append('{0:3d}\t{1:s}\t{2:s}\t{3:>5.1f}\t'.format(ID,TX_Name, RX_Name,freq))

for i in range(0,180):
	PrintComp(PathID[i], D1str[i], D1Compfp)
	
print(' ', file = D1Compfp)
print('************************************************************************', file = D1Compfp)

D1Compfp.close()
D1.close()