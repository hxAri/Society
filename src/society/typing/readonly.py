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

from typing import final

from society.typing.builtins import Key, Val
from society.typing.immutable import Immutable
from society.typing.map import Map


class Readonly( Immutable ):
	
	"""
	Class representation for handling the immutable property.
	This means the class will not or should not override any values it has set.
	But if the attribute has not been set then the attribute will be allowed to be set.
	"""
	
	@final
	def __setattr__( self, name:Key, value:Val ) -> None:
		if isinstance( self, Map ):
			Map.__setattr__( self, name, value )
		else:
			excepts = []
			if "__excepts__" in self.__dict__:
				if isinstance( self.__dict__['__excepts__'], list ):
					for keyword in self.__dict__['__excepts__']:
						if keyword in excepts:
							continue
						if not isinstance( keyword, str ):
							excepts = []
							break
						excepts.append( keyword )
			if name == "__excepts__":
				if isinstance( value, list ):
					allows = True
					for keyword in value:
						if keyword in excepts: continue
						if not isinstance( keyword, str ):
							allows = False; break
					if allows:
						self.__dict__['__excepts__'] = [ *excepts, *value ]
						return
			if name in self.__dict__:
				if name not in excepts:
					raise TypeError( f"Cannot override attribute \"{name}\", cannot override attribute that has been set in a class that extends the Readonly class" )
			self.__dict__[name] = value
		...
	
	@final
	def __setitem__( self, key:Key, value:Val ) -> None:
		if isinstance( self, Map ):
			Map.__setitem__( self, key, value )
		else:
			raise TypeError( "\"{}\" Map does not support item assignment".format( type( self ).__name__ ) )
		...

	...
