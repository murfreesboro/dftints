"""
This module is used to generate the angular part of codes for DFT basis set 
module
"""
__author__  = "Fenglai Liu"
import sys
import os
import infor
import shell
import basis
import codeprint
import shellsymbol

def generateCode():
	"""
	print out the code for angular part
	"""
	f = open("angdftbasis.cpp", "w")
	maxL = infor.getMaxL() + 4 # we consider the fourth derivatives of basis set

	# the comment part for the file
	f.write("/**\n")
	line = " * This function is used to generating the angular part for the " 
	codeprint.printLine(line,f)
	line = " * Cartesian type of basis set functions on a given atom. The " 
	codeprint.printLine(line,f)
	line = " * basis set functions are evaluated for the given shell which " 
	codeprint.printLine(line,f)
	line = " * is characterized by the lmax value." 
	codeprint.printLine(line,f)
	line = " * \\param  ng  number of grid points " 
	codeprint.printLine(line,f)
	line = " * \\param  pts grid point coordinates(3*ng) " 
	codeprint.printLine(line,f)
	line = " * \\param  c   basis set center coordinates(3) " 
	codeprint.printLine(line,f)
	line = " * \\param lmax maximum L value of all shells on this atom " 
	codeprint.printLine(line,f)
	line = " * \\return ang angular part of the basis set values(nCarBas,ng) "
	codeprint.printLine(line,f)
	line = " * \\author Fenglai Liu and Jing Kong " 
	codeprint.printLine(line,f)
	f.write(" */\n")

	# including head files
	line = "#include\"libgen.h\"" 
	codeprint.printLine(line,f)
	line = "#include\"batchbasis.h\"" 
	codeprint.printLine(line,f)
	line = "using namespace batchbasis;" 
	codeprint.printLine(line,f)
	f.write("\n\n")

	# print out the function name
	line = "void BatchBasis::angDFTBasis(const UInt& ng, const UInt& lmax, const Double* pts, const Double* c, Double* ang)" 
	codeprint.printLine(line,f)

	# here we enter in real code
	line = "{"
	codeprint.printLine(line,f)
	codeprint.increaseIndentation()
	f.write("\n")

	# now begin the loop over grids
	# for each grid point, we calculate all the
	# possible angular basis sets
	line = "for(UInt i=0; i<ng; i++) {" 
	codeprint.printLine(line,f)
	codeprint.increaseIndentation()
	f.write("\n")
	line = "Double GCX = pts[i*3  ]  - c[0];  // X"  # x
	codeprint.printLine(line,f)
	line = "Double GCY = pts[i*3+1]  - c[1];  // Y"  # y
	codeprint.printLine(line,f)
	line = "Double GCZ = pts[i*3+2]  - c[2];  // Z"  # z
	codeprint.printLine(line,f)

        # set the total basis set number
	f.write("\n")
        line = "// this is to evaluate total number of basis sets, L from 0 to lmax"
	codeprint.printLine(line,f)
	line = "UInt nTolBas = (lmax+1)*(lmax+2)*(lmax+3)/6; " 
	codeprint.printLine(line,f)

	# loop over the angular momentums
	f.write("\n")
	line = "for(UInt L=0; L<= lmax; L++) {"
	codeprint.printLine(line,f)
	codeprint.increaseIndentation()

	# loop over all possible angular momentums
	for L in range(maxL+1):
		    symbol = shellsymbol.getShellSymbol(L)
		    if L == 0:
	    		line = "if(L == " + str(L) + ") {"  
    		    else:		
                        line = "} else if(L == " + str(L) + ") {"  
		    codeprint.printLine(line,f)
		    codeprint.increaseIndentation()
		    s = shell.shell(L)
		    printCodeForShell(s,f)
		    codeprint.decreaseIndentation()

	line = "}"   # matching the if 
	codeprint.printLine(line,f)

	# end block of l = lmin to lmax
	codeprint.decreaseIndentation()  
	line = "}"   # matching the for loop on L
	codeprint.printLine(line,f)

	codeprint.decreaseIndentation()
	line = "}"   # matching the loop over grids
	codeprint.printLine(line,f)

	# end of function block
	codeprint.decreaseIndentation()
	line = "}"   # matching the main body function
	codeprint.printLine(line,f)
	f.write("\n\n")

	# end of whole file
	f.close()


def printCodeForShell(s,f):
	"""
	print out the code of shell section
	"""
        # consider S shell
	L  = s.getL()       
        if L == 0:
                code = "ang[0+i*nTolBas]" + " = ONE;" 
        	codeprint.printLine(code,f)
                return

	# real work
	basisList = s.getBasis()
	offset = L*(L+1)*(L+2)/6 # calculate the position of this shell 
	pos = 0
	for bas in basisList:
		l,m,n = bas.getlmn()
		position = pos + offset
		code = "ang[" + str(position) + "+i*nTolBas" + "]" + " = " # LHS

		# get RHS
		if l > 0:
			codex  = getXYZMultiplication("GCX",l)
		else:
			codex = ""
		if m > 0:
			codey  = getXYZMultiplication("GCY",m)
		else:
			codey = ""
		if n > 0:
			codez  = getXYZMultiplication("GCZ",n)
		else:
			codez = ""

		# real expression
		if m > 0 or n > 0:
			if l > 0:
				codex += "*"
		if n > 0:
			if m > 0:
				codey += "*"
		code += codex + codey + codez + ";"
		codeprint.printLine(code,f)
		pos = pos + 1


def getXYZMultiplication(v,order):
	"""
	here for each GCX, GCY or GCZ we multiply it up to order
	and return the string
	"""
	result = ""
	if order == 1:
		result = v
	elif order > 1:
		result = v
		for i in range(order-1):
			result = result + "*" + v
	else:
		print "Inproper order in getXYZMultiplication"
		sys.exit()
	return result

