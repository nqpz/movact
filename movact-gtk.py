#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#   movact: A program that reads, runs and converts hypertext fiction files
#   Copyright (C) 2009, 2010  Niels Serup

#   This file is part of movact.
#
#   movact is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   movact is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with movact.  If not, see <http://www.gnu.org/licenses/>.

#   Maintained by Niels Serup <ns@metanohi.org>

##''''''''''' Documentation and downloads are available at '''''''''''##
################# http://metanohi.org/projects/movact/ #################

                                 ############
                                 ## movact ##
                                 ############

#############
## IMPORTS ##
#############
## Global
import sys

## Local
import movactorg.frontends.gtk as front
from movactorg.core.load import *

##############
## THE GAME ##
##############

try:
	game = Loader(args=sys.argv[1:], frontend=front, always_run=True)
except (KeyboardInterrupt, EOFError):
	print # A newline
