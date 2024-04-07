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
from typing import Any, final, Generic
from society.typing.builtins import Key, Val


@final
class Result( Generic[Key,Val] ):
	
	"""
	A Base class for Execution Results
	"""

	def __init__( self, operation:Str, values:Any ) -> None:
		
		"""
		Construct method of class Result
		
		:params Str operation
		:params Any values
		
		:return None
		"""
		
		self.__operation__ = operation
		self.__values__ = values
	
	@property
	def operation( self ) -> Str:
		
		"""
		Return the operation name
		
		:return Str
		"""
		
		return self.__operation__
	
	@property
	def values( self ) -> Any:
		
		"""
		Return the result of operation
		
		:return Any
		"""
		
		return self.__values__
	
	...
