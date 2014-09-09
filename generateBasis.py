"""
This module is used to generate the DFT basis set value etc.
up to the fourth derivatives
"""
__author__  = "Fenglai Liu"
import sys
import os
import infor
import shell
import basis
import codeprint
import shellsymbol
import derivorder
import derivparser

def generateCode(order):
	"""
	print out the code 
	"""

	# get the file name
	if order == 1:
		funName = "dftbasisderiv1"
	elif order == 2:
		funName = "dftbasisderiv2"
	elif order == 3:
		funName = "dftbasisderiv3"
	elif order == 4:
		funName = "dftbasisderiv4"
	else:
		print "Improper order in the generateCode of generateBasis.py"
		sys.exit()
	inf = funName + ".cpp"


	# now we open the file	
	f = open(inf, "w")
	codeprint.initilizeIndent()

	# the comment part for the file
	f.write("/**\n")
	line = " * This function is used to generate "+str(order)+" derivatives for basis set " 
	codeprint.printLine(line,f)
	line = " * The basis set derivatives are evaluated for the given shell which " 
	codeprint.printLine(line,f)
	line = " * is characterized by the L(no composite shell!). Generally, by given the "
	codeprint.printLine(line,f)
	line = " * derivative order (for exmaple, X, Y Z or XX, YY or XYY etc.)"
	codeprint.printLine(line,f)
	line = " * for an arbitrary shell we could combine the radial part and "
	codeprint.printLine(line,f)
	line = " * the angular part together so to form the result." 
	codeprint.printLine(line,f)
	line = " * The result is arranged as: (nBas, ng, nDerivOrder)"
	codeprint.printLine(line,f)
	line = " * nBas is the number of Cartesian type basis set for shell with L"
	codeprint.printLine(line,f)
	line = " * \\param ng         number of grid points " 
	codeprint.printLine(line,f)
	line = " * \\param L          angular momentum of the shell " 
	codeprint.printLine(line,f)
	line = " * \\param nTolCarBas number of Cartesian basis set in the ang array " 
	codeprint.printLine(line,f)
	line = " * \\param ang        angular part of the basis set values(nTolCarBas,ng) "
	codeprint.printLine(line,f)
	line = " * \\param rad        radial part of the basis set values "
	codeprint.printLine(line,f)
	line = " * \\return basis     derivatives of basis set values for the given order"
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
	f.write("\n")

	# print out the function name
	line = "void " + "BatchBasis::" + funName + '''(const UInt& ng, const UInt& L, const UInt& nTolCarBas, const Double* ang, const Double* rad, Double* basis) const '''
	codeprint.printLine(line,f)

	# here we enter in real code
	line = "{"
	codeprint.printLine(line,f)
	codeprint.increaseIndentation()
	f.write("\n")

        # set up the nBas
	line  = "// now we set up the nBas for the computation"
	codeprint.printLine(line,f)
        line  = "UInt nBas = (L+1)*(L+2)/2;"
	codeprint.printLine(line,f)
	f.write("\n")

	# now we create the derivatives order
	orderList = derivorder.derivOrderGeneration(order)
	for derivOrder in orderList:

		# comment 
		line  = "// now we do derivatives for the given basis set to " + derivOrder
		codeprint.printLine(line,f)
		indexDerivOrder = orderList.index(derivOrder)
		if indexDerivOrder > 0 :
			line  = "basis = basis + " + "ng*nBas; "
			codeprint.printLine(line,f)
			f.write("\n")

		# within the loop, actually we choose doing code from S to I
		maxL = infor.getMaxL()
		for L in range(maxL+1):

			# print out the block
			if L == 0:
				line = "if(L == " + str(L) + ") {"  
			else:
				line = "} else if(L == " + str(L) + ") {"  
			codeprint.printLine(line,f)
			codeprint.increaseIndentation()
			f.write("\n")

			# now it's the real work module
			line = "for(UInt ip = 0; ip<ng; ip++) {" 
			codeprint.printLine(line,f)
			codeprint.increaseIndentation()
			line = "Double* bas = &basis[ip*nBas];" 
			codeprint.printLine(line,f)
			line = "const Double* angArray = &ang[ip*nTolCarBas];" 
			codeprint.printLine(line,f)
			s = shell.shell(L)
			basList = s.getBasis()
			for bas in basList:
				formula = {"0":bas}
				result = { }
				derivparser.getDerivExpression(formula, derivOrder, 0, result)
				ind = basList.index(bas)
				derivparser.printExpression(result,derivOrder,ind,f)
			
			# block end for ip
			codeprint.decreaseIndentation()  
			line = "}" 
			codeprint.printLine(line,f)
			codeprint.decreaseIndentation()  
			f.write("\n")

		# block end with the L
		line = "}" 
		codeprint.printLine(line,f)
		f.write("\n\n")

	# end of function block
	codeprint.decreaseIndentation()
	line = "}"  
	codeprint.printLine(line,f)
	f.write("\n\n")

	# end of whole file
	f.close()

