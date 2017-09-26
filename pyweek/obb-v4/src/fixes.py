# This file taken from:

# Wobleigh Towers
# ------------------------------------------------------
# An entry in the PyWeek 10 Game Programming Competition
# by Gregory Ewing
# greg.ewing@canterbury.ac.nz

# http://www.pyweek.org/e/greg_pw10/



#-----------------------------------------------------------------------------
#
#   PyWeek 10 - Fixed versions of pygame 1.9.1 routines
#
#-----------------------------------------------------------------------------

import numpy, pygame

def pixels_alpha (surface):

	if surface.get_bytesize () != 4:
		raise ValueError("unsupported bit depth for alpha reference array")
	
	lilendian = pygame.get_sdl_byteorder() == pygame.LIL_ENDIAN
	alpha_shift = surface.get_shifts()[3]
	
	if alpha_shift & 7 <> 0:
		raise ValueError("unsupported colormasks for alpha reference array")

	start = alpha_shift >> 3
	if not lilendian:
		start = 3 - start

	array = numpy.ndarray \
			(shape=(surface.get_width (), surface.get_height ()),
			 dtype=numpy.uint8, buffer=surface.get_buffer (),
			 offset=start, strides=(4, surface.get_pitch ()))
	return array
