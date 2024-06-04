#!/usr/bin/env python3

#
# @author Ari Setiawan
# @create 12.01-2024 14:31
# @github https://github.com/hxAri/Society
#
# Society Copyright (c) 2024 - Ari Setiawan <hxari@proton.me>
# Society Licence under GNU General Public Licence v3
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# Society Program is not affiliated with or endorsed, endorsed at all by
# Facebook or any other party, if you use the main account to use this
# tool we as Coders and Developers are not responsible for anything,
# use it at your own risk, and this is Strictly not for SPAM.
#

from builtins import str as Str
from sys import path as paths
from typing import Final, MutableSequence


BASEPARTS:MutableSequence[Str] = paths[0].split( "\x2f" )
BASEPATH:Final[Str] = "\x2f".join( BASEPARTS[:BASEPARTS.index( "src" )] )
""" The Base Path of Society Application """

BASEPARTS:MutableSequence[Str] = paths[4].split( "\x2f" )
BASEVENV:Final[Str] = "\x2f".join( BASEPARTS[:BASEPARTS.index( "lib" )] )
""" The Base Path of Virtual Environment """

# Delete unused constant.
del BASEPARTS
