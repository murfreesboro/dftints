"""
This module is used describe the class related to the "basis set functions". 
Originally, each basis set function is a combination of Gaussian primitive
functions:
psi = sum_{mu}d_{mu}chi_{mu}
psi is the basis set function, and chi_{mu} is the primitive functions.
All of chi are on the same center as psi, and d_{mu} is some fixed 
coefficients. All of Gaussian primitive functions share the same angular
momentum with the basis set.

For each Gaussian primitive function, it has the form that:
chi = x^{l}y^{m}z^{n}e^{-alpha*r^{2}}
x^{l}y^{m}z^{n} is its angular momentum part, which is characterized by
three number of l, m, and n. The e^{-alpha*r^{2}} is its radial part,
so l,m,n combined with alpha and its prefactor of d_{mu}, then we know
all of information to get psi.
"""
__author__  = "Fenglai Liu"
import sys
import os
import shellsymbol

class basis:

	def __init__(self,l0,m0,n0):
		"""
		Basis class is characterized by three numbers
		They are corresponding to the angular momentum numbers
		"""
		self.l = l0
		self.m = m0
		self.n = n0

		# test the angular momentum number
		if l0<0 or m0<0 or n0<0:
			print "Illegal angular momentum number in basis.py. It should not be less than zero\n"
			print l0,m0,n0
			sys.exit()


	def __eq__(self,t):
		"""
		testing whether two basis sets are equal with each other
		"""
		l0,m0,n0 = self.getlmn()
		l1,m1,n1 = t.getlmn()
		if l0 == l1 and m0 == m1 and n0 == n1:
			return True
		else:
			return False


	def __ne__(self,t):
		"""
		testing whether two basis sets are equal with each other
		"""
		l0,m0,n0 = self.getlmn()
		l1,m1,n1 = t.getlmn()
		if l0 == l1 and m0 == m1 and n0 == n1:
			return False
		else:
			return True


	def getName(self):
		"""
		depending on the l,m,n; we get the name for this basis set
		"""
		L = self.l + self.m + self.n
		name = shellsymbol.getShellSymbol(L)
		if self.l > 0:
			if self.l == 1:
				name = name + "x"
			else:
				name = name + str(self.l) + "x"
		if self.m > 0:
			if self.m == 1:
				name = name + "y"
			else:
				name = name + str(self.m) + "y"
		if self.n > 0:
			if self.n == 1:
				name = name + "z"
			else:
				name = name + str(self.n) + "z"
		return name


	def getlmn(self):
		"""
		l,m,n is given
		"""
		return (self.l, self.m, self.n)


	def getComponent(self,axis):
		"""
		for the given axis (X, Y or Z) we return the component
		"""
		if axis == "X":
				return self.l
		elif axis == "Y":
				return self.m
		elif axis == "Z":
				return self.n
		else:
			print "Wrong axis passed in the getComponent"
			sys.exit()

	def getL(self):
		"""
		return the total angular momentum number of L
		"""
		L = self.l + self.m + self.n
		return L


	def loweringAng(self,axis):
		"""
		for the given axis (X, Y or Z) we determine
		which component to lowering
		"""
		if axis == "X":
			l1 = self.l - 1
			m1 = self.m
			n1 = self.n
			if l1 < 0:
				return (None,None,None)
			else:
				return (l1,m1,n1)
		elif axis == "Y":
			l1 = self.l 
			m1 = self.m - 1
			n1 = self.n
			if m1 < 0:
				return (None,None,None)
			else:
				return (l1,m1,n1)
		elif axis == "Z":
			l1 = self.l 
			m1 = self.m
			n1 = self.n - 1
			if n1 < 0:
				return (None,None,None)
			else:
				return (l1,m1,n1)
		else:
			print "Wrong axis passed in the loweringAng"
			sys.exit()


	def raisingAng(self,axis):
		"""
		for the given axis (X, Y or Z) we determine
		which component to raising up
		"""
		if axis == "X":
			l1 = self.l + 1
			m1 = self.m
			n1 = self.n
		elif axis == "Y":
			l1 = self.l 
			m1 = self.m + 1
			n1 = self.n
		elif axis == "Z":
			l1 = self.l 
			m1 = self.m
			n1 = self.n + 1
		else:
			print "Wrong axis passed in the raisingAng"
			sys.exit()
		return (l1,m1,n1)


