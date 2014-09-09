"""
main module for dft basis sets
"""
__author__  = "Fenglai Liu"
import sys
import os
import infor
import generateAngBasis
import generateBasis
import derivorder

# setting the basis set order 
maxLChoice = 6
if len(sys.argv) == 2:
	maxLChoice = int(sys.argv[1])
elif len(sys.argv) > 2:
	print "Wrong argv list! We only support zero/one arguments! Please check it!\n"
	sys.exit()
infor.setBasisSetOrder()
infor.setMaxL(maxLChoice)

# print out the angular part of code
generateAngBasis.generateCode()

# print out the basis set code
for i in range(4):
	i = i + 1
	generateBasis.generateCode(i)

# finally, we try to print out the derivatives information
# used in the program
count = 1
for i in range(4):
	i = i + 1
	dlist = derivorder.derivOrderGeneration(i)
	for var in dlist:
		v = "DERIV_" + var
		line = "UInt " + v + " = " + str(count) + ";"
		print line
		count = count + 1


