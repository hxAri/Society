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
from json import dumps as encoder
from typing import Any, final, List

from society.typing.readonly import Readonly


@final
class Filter( Readonly ):
	
	""" Search Filter Typing Implementation """
	
	def __init__( self, name:Str, args:Any=None ) -> None:
		
		"""
		Construct method of class Filter
		
		:params Str name
			The search tab filter name
		:params Any args
			The search tab filter arguments
		
		:return None
		"""
		
		self.name = name
		self.args = args if args is not None else ""
	
	def serialize( self ) -> Str:
		
		""" Return serialized of class Filter """
		
		return encoder({ "name": self.name, "args": encoder( self.args ) if not isinstance( self.args, str ) else self.args })
	
	...

@final
class Tab( Readonly ):
	
	""" Search Tab Typing Implementation """
	
	ANY:Str = "GLOBAL_SEARCH"
	GROUP:Str = "GROUPS_TAB"
	PAGE:Str = "PAGES_TAB"
	POST:Str = "POSTS_TAB"
	
	def __init__( self, name:Str, filters:List[Filter]=None ) -> None:
		
		"""
		Construct method of class Tab
		
		:params Str name
			The search tab name
		:params List<Filter> filters
			The search tab filters
		
		:return None
		:raises TypeError
			When the value of parameter is invalid value type
		"""
		
		self.name = name
		self.filters = filters if isinstance( filters, List ) else []
		if not all( isinstance( filter, Filter ) for filter in self.filters ):
			raise TypeError( "Invalid filters parameter, value must be List<Filter>" )
		...
	
	def append( self, filter:Filter ) -> None:

		"""
		Append search filter
		
		:params Filter filter
			The search tab filter
		
		:return None
		"""
		
		self.__filters__.append( filter )
	
	@property
	def items( self ) -> List[Str]:
		
		""" Return filters as list of string """
		
		return list( item.serialize() for item in self.filters )
	
	...
