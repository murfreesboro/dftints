"""
This module is used to provide functions to print the real codes
"""
__author__  = "Fenglai Liu"
import sys
import os

# the indentLength indicates current indent length in the code
# in default, each time we increase 3
indentLength = 0

def increaseIndentation():
	"""
	increase the indent for 3
	"""
	global indentLength
	indentLength = indentLength + 3

def decreaseIndentation():
	"""
	decrease the indent for 3
	"""
	global indentLength
	indentLength = indentLength - 3
	if indentLength < 0:
		print "Illegal indentLength in printcode.py\n"
		sys.exit()

def printLine(line,f):
	"""
	print out the given line of code
	"""
	global indentLength
	if indentLength != 0:
		for i in range(indentLength):
			f.write(" ")
	f.write(line)
	f.write("\n")

def initilizeIndent():
	global indentLength
	indentLength = 0

