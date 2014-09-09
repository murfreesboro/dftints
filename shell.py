"""
This module is used describe the class related to the "Shell". 
Shell actually is a group of basis set functions in the quantum chemistry,
all of these basis set functions share the same L, namely:
L = l+m+n
For example, Shell of L=1 has theree basis set functions, namely
Px  1,0,0
Py  0,1,0
Pz  0,0,1
"""
__author__  = "Fenglai Liu"
import sys
import os
import basis
import shellsymbol
import infor

class shell:

	def __init__(self,L0):
		"""
		constructor for the shell class
		L0 is the shell's angular momentum type
		In the initilization, we also generate all of basis set functions
		"""
		self.L = L0

		# check the L, it should not be less than zero
		if L0 < 0:
			print "L can not be less than zero in shell class\n"
			sys.exit()


	def __eq__(self,t):
		if self.L == t.L:
			return True
		else:
			return False


	def __ne__(self,t):
		if self.L != t.L:
			return True
		else:
			return False


	def getL(self):
		"""
		return the L
		"""
		return self.L


	def getBasis(self):
		"""
		return the full basis set list
		"""

		# get the basis set order
		order = self.generateBasisSetOrders()

		# generate the basis set functions for this shell
		# each basis set function is characterized by three numbers
		l = len(order)/3
		basisSets = [ ]
		i = 0
		while i < l:
			basisSet = basis.basis(order[3*i],order[3*i+1],order[3*i+2])
			basisSets.append(basisSet)
			i = i + 1
		return basisSets
			

	def generateBasisSetOrders(self):
		"""
		generating the basis set's ordering
		"""
		orderList = []
		L = self.L
		i = 0
		basisSetOrder = infor.getBasisSetOrder()
		if basisSetOrder == "libint":
			while i <= L:
				nx = L - i
				j = 0
				while j<=i: 
					ny = i-j
					nz = j
					orderList.append(nx)
					orderList.append(ny)
					orderList.append(nz)
					j = j + 1
				i = i + 1
                else:
			print "Unrecognized basis set ordering to generate basis sets\n"
			sys.exit()

		return orderList


	def hasBasisSet(self,bas):
		"""
		testing that whether we have the basis set in the
		given shell
		"""
		bL = bas.getL()
		if bL == self.L:
			return True
		else:
			return False


	def getName(self):
		"""
		give the name for this shell
		"""
		name = shellsymbol.getShellSymbol(self.L)
		return name


