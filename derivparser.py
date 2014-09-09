"""
This module is used to generate the parser for the given basis set with
respect to the given derivatives
"""
__author__  = "Fenglai Liu"
import sys
import os
import shell
import basis
import codeprint

def getDerivExpression(formula, deriv, order, final_result):
	"""
	for the given formula, as well as the derivative var(something like
	XXXX, XXYZ etc. generated in derivorder.py). We can get the derivatives 
	expression for the current formula. We note that this process continues
	in recursively way until all of the derivatives are processed. If the 
	final order is arrived, we will push the result into the final_result
	"""
	result = { }
	axis   = deriv[order]
	nunderscore = 1
	for k, bas in formula.iteritems():

		# to get rid of the "-" sign first
		k = k.replace("-","")

		# get the first term in the derivative expression
		# the first term is "(l,m,n)*chi(l,m,n - delta)"
		(l,m,n) = bas.loweringAng(axis)

                # add a comment: if the loweringAng produce new 
                # l,m,n no matter which one is smaller than 0;
                # then l,m,n are all none
                # we only need to check that whether l is none or not
                # so that to know the new basis set exist or not
		if l is not None:
			newBasis = basis.basis(l,m,n)
			com = bas.getComponent(axis)
			newkey1  = k + "_" + str(com)
			if result.has_key(newkey1):
				for i in range(nunderscore):
					newkey1 = newkey1 + "-"
				nunderscore = nunderscore + 1
				result[newkey1] = newBasis
			else:
				result[newkey1] = newBasis

		# get the second term
		# the second term is 2alpha*chi(l,m,n + delta)
		(l,m,n) = bas.raisingAng(axis)
		newBasis = basis.basis(l,m,n)
		newkey2  = k + "_" + "2alpha"
		if result.has_key(newkey2):
			for i in range(nunderscore):
				newkey2 = newkey2 + "_"
			nunderscore = nunderscore + 1
			result[newkey2] = newBasis
		else:
			result[newkey2] = newBasis

	# now let's judge whether we need to proceed it
	order = order + 1
	desire_order = len(deriv)
	if order == desire_order:
		for k, bas in result.iteritems():
			final_result[k] = bas
	else:
		getDerivExpression(result, deriv, order, final_result)


def printExpression(expression, derivOrder, basIndex, f):
	"""
	now we print out the derivative expression here for the 
	given derivative order. 
	"""
	# set up the LHS of the expression
	line = "bas[" + str(basIndex) + "] = "

	# get the length of the derivative order
	l = len(derivOrder)

	# we use count to know whether this is the first term
	count = 0

	# now let's search each order - for every order,
	# we have a rad term
	for order in range(l+1):

		# set up the list for basis and coefficients
		# they are corresponding to the same rad term
		basList = [ ] 
		coeList = [ ]

		for k, bas in expression.iteritems():

			# to get rid of the "-" sign first
			k = k.replace("-","")
			klist = k.split("_")

			# determine how many 2alpha we have in the k
			# we only pick up these who math the order
			n2alpha = 0
			for i in klist:
				if i == "2alpha":
					n2alpha = n2alpha + 1
			if n2alpha != order:
				continue

			# determine the coefficient in the k
			coe = 1
			for i in klist:
				if i.isdigit() and i != "0":
					coe = coe*int(i)

			# push back the basis and coe
			if bas in basList:
				index = basList.index(bas)
				coeList[index] = coeList[index] + coe
			else:
				basList.append(bas)
				coeList.append(coe)

		if len(basList) > 0:
			
			# give the offset for the radial array
			# we add the minus sign to this part
			if order == 0:
				rad = "rad[ip]"
			elif order == 1:
				rad = "rad[ip+ng]"
			else:
				rad = "rad[ip+" + str(order) + "*ng]"
			if order % 2 == 1:
				rad = "-" + rad 
			elif count > 0: # these term should have "+" sign
				rad = "+" + rad
		
			# set the basis set, by combining it with coefficients 
			# we will get the term corresponding to the rad term
			ang = "*"
			if len(basList) > 1:
				ang = ang + "("
			for bas in basList:
				L       = bas.getL()
				gOffSet = L*(L+1)*(L+2)/6  # counting all of lower shell index since S
				s       = shell.shell(L)
				bList   = s.getBasis()
				bind    = bList.index(bas)
				index   = bind + gOffSet
				cind    = basList.index(bas)
				if coeList[cind] != 1:
					c       = str(coeList[cind]) + "*"
				else:
					c       = ""
				ang  = ang + c
				ang  = ang + "angArray[" + str(index) + "]"  
				#ang = ang + c + bas.getName()
				if cind == len(basList) - 1:
					if ang.find("(") > 0:
						ang = ang + ")"
				else:
					ang = ang + "+"

			# now add this order 
			line = line + rad + ang

			# finally add counting
			count = count + 1

	line = line + ";"
	codeprint.printLine(line,f)

