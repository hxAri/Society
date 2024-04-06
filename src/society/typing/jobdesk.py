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

from builtins import bool as Bool, int as Int, str as Str, type as Type
from re import compile, Pattern
from typing import Any, Callable, Dict, final, List, Literal, TypeVar, Union

from society.typing.readonly import Readonly


Args = TypeVar( "Args" )
""" Argument values """

Kwargs = TypeVar( "Kwargs" )
""" Argument keywords """

Thread = TypeVar( "Thread" )
""" Just for typing """


@final
class Jobdesk( Readonly ):
	
	""" A Jobdesk class implementation """
	
	@final
	class Message( Readonly ):
		
		""" A Jobdesk Message class implementation """
		
		def __init__( self, name:Str=None, loading:Str=None, success:Str=None ) -> None:
			
			"""
			Construct method of class Message
			
			:params Str name
			:params Str loading
			:params Str success
			
			:return None
			"""
			
			self.name:Str = name
			self.loading:Str = loading
			self.success:Str = success
		
		...
	
	@final
	class Require( Readonly ):
		
		""" A Jobdesk Parameter Requirement class implementation """
		
		def __init__( self, name:Str, keyset:Str ) -> None:
			
			"""
			Construct method of class Require
			
			:params Str keyset
			:params Str name
			
			:return None
			"""
			
			self.keyset:Str = keyset
			self.name:Str = name
		
		...
	
	def __init__( self, name:Str, thread:Thread, execute:Callable[[Args,Kwargs,Int],Any], keysets:Dict[Str,Union[Callable,List[Union[Callable,Type]],Type]], pattern:Union[Pattern[Str],Str], syntax:Str, message:Message, dataset:Str=None, allowed:Bool=None, escapes:List[Str]=None, requires:List[Require]=None ) -> None:
		
		"""
		Construct method of class Jobdesk
		
		:params Str name
		:params Thread thread
		:params Callable<<Args,Kwargs,Int>,Any> execute
		:params Dict<Str,Callable|List<Callable|Type>Type> keysets
		:params Pattern<Str>|Str pattern
		:parans Str syntax
		:params Jobdesk.Message message
		:params Str dataset
		:params Bool allowed
		:params List<Str> escapes
		:params List<Jobdesk.Require> requires
		
		:return None
		"""
		
		if isinstance( pattern, Str ):
			pattern = compile( pattern )
		self.name:Str = name
		self.thread:Thread = thread
		self.execute:Callable[[Args,Kwargs,Int],Any] = execute
		self.keysets:Dict[Str,Union[Callable,List[Union[Callable,Type]],Type]] = keysets
		self.pattern:Union[Pattern[Str],Str] = pattern
		self.syntax:Str = syntax
		self.message:Jobdesk.Message = message
		self.dataset:Str = dataset
		self.allowed:Bool = allowed
		self.escapes:List[Str] = escapes
		self.requires:List[Jobdesk.Require] = requires
	
	...
