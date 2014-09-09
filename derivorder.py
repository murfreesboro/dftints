"""
This module is used to generate the derivatives sequence for the program
The derivatives sequence is like this, if we want to do 3rd order derivatives;
for example; do derivatives with respect to X, Y and Z then the derivative
var is written into "XYZ". For each order derivatives, we will set up
the sequence and then parse it later
"""
__author__  = "Fenglai Liu"
import sys
import os


def derivOrderGeneration(order):
	"""
	generating the derivatives sequence:
	XX, YY etc. for derivatives order 2
	XXX, XYY, ZZZ etc. for derivatives order 3
	"""
	axis = ( "X", "Y", "Z" )
	result = [ ]
	if order == 1:
		result = axis
	elif order == 2:
		for i in axis:
			for j in axis:
				if axis.index(j) > axis.index(i):
					continue
				var = j + i
				result.append(var)
	elif order == 3:
		for i in axis:
			for j in axis:
				for k in axis:
					if axis.index(j) > axis.index(i):
						continue
					if axis.index(k) > axis.index(j):
						continue
					var = k + j + i
					result.append(var)
	elif order == 4:
		for i in axis:
			for j in axis:
				for k in axis:
					for l in axis:
						if axis.index(j) > axis.index(i):
							continue
						if axis.index(k) > axis.index(j):
							continue
						if axis.index(l) > axis.index(k):
							continue
						var = l + k + j + i
						result.append(var)
	else:
		print "Improper order in the derivOrderGeneration\n"
		sys.exit()
	
	# return
	return result


def parseDeriv(var):
	"""
	for each given var, which is in format of XX, YY, XYZ etc.
	we need to parse it to figure out that how many X, how many
	Y and how many Z it has
	"""
	nx = 0
	ny = 0
	nz = 0
	for i in range(len(var)):
		if var[i] == "X":
			nx = nx + 1
		elif var[i] == "Y":
			ny = ny + 1
		elif var[i] == "Z":
			nz = nz + 1
		else:
			print "Illegal character got in parseDeriv. Could be only X, Y or Z"
			sys.exit()
	return (nx, ny, nz)


