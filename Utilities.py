#
# Fractals - Utilities
#
# Jonatan H Sundqvist
# August 26 2014
#


# TODO | - 
#		 - 

# SPEC | - 
#		 - 


from math import sin, cos, sqrt, asin, copysign, pi as π
from cmath import rect, polar, pi as π # sin, cos, 


#==============================================================================
# Math
#==============================================================================
def RAD(deg):
	return deg*π/180.0


def DEG(rad):
	return rad*180.0/π


def sign(value):
	return value if value == 0 else copysign(1, value)


def clamp(mini, maxi, value):
	return sorted((mini, maxi, value))[1]