"""
get the maximum L for generating the angular part of dft basis 
"""
__author__  = "Fenglai Liu"
import sys
import os

# global data 
basisSetOrder = " "
maxL = 6  # this is default, we just generate all of codes up to I orbital

def setBasisSetOrder():
	"""
	set the basis set order
        in the future we can define other basis set order
        if you want
        just modify the shell.py
	"""
	global basisSetOrder
	basisSetOrder = "libint"

def setMaxL(choice):
	"""
	set the maxL
        in the future we can define other basis set order
        if you want
        just modify the shell.py
	"""
	global maxL
        if choice >= 0:
            maxL = choice
        else:
            print "Illegal choice provided in setMaxL, must be an integer >=0"
            sys.exit()

def getBasisSetOrder():
	global basisSetOrder
	return basisSetOrder

def getMaxL():
	global maxL
	return maxL




