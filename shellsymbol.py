"""
This module stores the shell symbols
"""
__author__  = "Fenglai Liu"
import sys
import os

# the shell name list is taken from libint package
SHELL_NAME_LIST = [
'S', 'P', 'D', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N',
'O', 'Q', 'R', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def getShellSymbol(i):

	global SHELL_NAME_LIST
	l = len(SHELL_NAME_LIST)
	if i>=l:
		print "Why you need to claim such high order shells, L>20?"
                print "however, we still do it, but be careful with your code"
                return "L" + str(i)
	else:
		return SHELL_NAME_LIST[i]



