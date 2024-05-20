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

from builtins import bool as Bool, int as Int, str as Str
from json import dumps as encoder
from typing import Any, Dict, final, List, MutableMapping, Tuple, Union

from society.common import serializeable, typeof
from society.typing.builtins import Key, Val, Self
from society.typing.immutable import Immutable


class Map( MutableMapping[Key,Val] ):
	
	""" A python Map utility to transform any dictionary structure into Map """
	
	def __init__( self, collection:Union[Self,MutableMapping[Key,Val]]=None ) -> None:

		"""
		Construct method of class Map.

		:params Dict<Key, Value>|Map data
		:params Any parent

		:return None
		"""

		if isinstance( self, Immutable ):
			self.__dict__['__excepts__'] = [
				"__index__"
			]
		self.__dict__['__index__'] = 0
		self.__dict__['__values__'] = []
		self.__dict__['__keysets__'] = []
		self.update( collection if isinstance( collection, ( dict, Map ) ) else {} )
	
	@final
	def __contains__( self, name:Key ) -> Bool:
		
		""" Return whether the Map has or contains attribute|item name """
		
		return name in self.__keysets__

	@final
	def __delattr__( self, key:Key ) -> None:
		
		""" Delete attribute|item from Map """
		
		if key in self.__dict__:
			if key not in [ "__keysets__", "__index__", "__values__" ]:
				del self.__dict__[key]
		elif key in self.__dict__['__keysets__']:
			del self.__dict__['__keysets__'][key]
	
	@final
	def __delitem__( self, index:Key ) -> None:
		
		""" Delete item|attribute from Map """
		
		if index in self.__dict__['__keysets__']:
			del self.__dict__['__keysets__'][index]
		elif index in self.__dict__:
			if index not in [ "__keysets__", "__index__", "__parent__" ]:
				del self.__dict__[index]
	
	@final
	def __getattr__( self, name:Key ) -> Val:
		
		""" Return attribute|item value """
		
		if name in self.__dict__:
			return self.__dict__[name]
		if name in self.__dict__['__keysets__']:
			return self.__dict__['__values__'][self.__dict__['__keysets__'].index( name )]
		raise AttributeError( "\"{}\" Map object has no attribute \"{}\"".format( typeof( self ), name ) )
	
	@final
	def __getitem__( self, key:Key ) -> Val:
		
		""" Return item|attribute value """
		
		if key in self.__dict__['__keysets__']:
			return self.__dict__['__values__'][self.__dict__['__keysets__'].index( key )]
		if key in self.__dict__:
			return self.__dict__[key]
		raise KeyError( "\"{}\" Map object has no item \"{}\"".format( typeof( self ), key ) )

	@final
	@property
	def __index__( self ) -> Int:
		
		""" Return current index iteration """
		
		return self.__dict__['__index__']
	
	@final
	def __iter__( self ) -> Self:
		
		""" Return current instance """
		
		return self

	@final
	def __serialize__( self, *args:Any, **kwargs:Any ) -> Str:
		
		""" Serialize map instance into Json String """
		
		def iterator( values:Union[Dict[Key,Val],List[Val]] ) -> Dict[Key,Val]:
			if isinstance( values, dict ):
				for keyset in values:
					value = values[keyset]
					if isinstance( value, ( dict, list ) ):
						values[keyset] = iterator( values[keyset] )
					elif not serializeable( value ):
						values[keyset] = str( value )
			elif isinstance( value, list ):
				for index, value in enumerate( values ):
					if isinstance( value, ( dict, list ) ):
						values[index] = iterator( value )
					elif not serializeable( value ):
						values[index] = str( value )
			return values
		return encoder( iterator( self.__props__() ), *args, **kwargs )
	
	@final
	def __len__( self ) -> Int:
		
		""" Return length of map """
		
		return len( self.__dict__['__keysets__'] )

	@final
	def __next__( self ) -> Tuple[Key,Val]:
		
		""" Return next item by index """
		
		index = self.__dict__['__index__']
		values = self.__dict__['__values__']
		keysets = self.__dict__['__keysets__']
		length = self.length
		try:
			if index < length:
				self.__index__ += 1
				keyset = keysets[index]
				value = values[index]
				return tuple( (keyset, value) )
		except IndexError:
			pass
		raise StopIteration
	
	@final
	def __props__( self ) -> Dict[Key,Val]:

		"""
		Return Dictionary of Map

		:return Dict<Key, Value>
		"""

		result = {}
		values = self.__dict__['__values__']
		for index, keyset in enumerate( self.__dict__['__keysets__'] ):
			if isinstance( values[index], Map ):
				result[keyset] = values[index].__props__()
			elif isinstance( values[index], list ):
				result[keyset] = []
				for item in values[index]:
					if isinstance( item, Map ):
						result[keyset].append( item.__props__() )
					else:
						result[keyset].append( item )
			else:
				result[keyset] = values[index]
		return result
	
	@final
	def __set__( self, keyset:Key, values:Union[Self,Union[Key,Val]] ) -> None:
		if isinstance( values, ( dict, Map ) ):
			define = typeof( self )
			if isinstance( values, Map ) and define not in [ "Map", "MapBuilder" ]:
				values = builder( self, values )
			else:
				values = Map( values )
		if isinstance( values, list ):
			for i, value in enumerate( values ):
				if isinstance( value, ( dict, Map ) ):
					if isinstance( value, Map ) and define not in [ "Map", "MapBuilder" ]:
						value[i] = builder( self, value )
					else:
						value[i] = Map( value )
		excepts = [ "__index__" ]
		if isinstance( self, Immutable ):
			excepts = [ *excepts, *self.__dict__['__excepts__'] ]
		else:
			excepts = [ *excepts, *self.__dict__['__keysets__'] ]
		for eliminate in [ "__excepts__", "__keysets__", "__values__" ]:
			if eliminate in excepts:
				del excepts[excepts.index( eliminate )]
		if keyset in self.__dict__:
			if keyset == "__excepts__":
				if isinstance( values, list ):
					for value in values:
						if not isinstance( value, str ):
							if keyset in self.__dict__:
								raise TypeError( f"Cannot override attribute \"{keyset}\", cannot override attribute that has been set in a class that extends the Immutable class" )
							self.__dict__['__excepts__'] = excepts
							break
						self.__dict__['__excepts__'].append( value )
					...
				...
			if keyset not in excepts:
				raise TypeError( f"Cannot override attribute \"{keyset}\", cannot override attribute that has been set in a class that extends the Immutable class" )
			self.__dict__[keyset] = values
		elif keyset in self.__dict__['__keysets__']:
			if keyset not in excepts:
				raise TypeError( f"Cannot override item \"{keyset}\", cannot override item that has been set in a class that extends the Immutable class" )
			position = self.__dict__['__keysets__'].index( keyset )
			original = self.__dict__['__values__'][position]
			if isinstance( original, Map ) and isinstance( values, ( dict, Map ) ):
				originalNamedType = typeof( original )
				differentNamedType = typeof( values )
				if originalNamedType not in [ "Map", "MapBuilder", differentNamedType ]:
					self.__dict__['__values__'][position] = values
				else:
					for key in values:
						original[key] = values[key]
			elif isinstance( original, list ) and isinstance( values, list ):
				for item in values:
					if item not in original:
						original.append( item )
			else:
				self.__dict__['__values__'][position] = values
		else:
			self.__dict__['__keysets__'].append( keyset )
			self.__dict__['__values__'].append( values )
		...
	
	@final
	def __setattr__( self, name:Key, value:Val ) -> None:
		self.__set__( name, value )

	@final
	def __setitem__( self, key:Key, value:Val ) -> None:
		self.__set__( key, value )
	
	@final
	def __str__( self ) -> Str:
		return self.__serialize__()

	@final
	def keys( self ) -> List[Key]:
		return self.__dict__['__keysets__']
	
	@final
	@property
	def length( self ) -> Int:
		return self.__len__()
	
	def update( self, collection:Union[Self,MutableMapping[Key,Val]] ) -> None:
		if not isinstance( collection, MutableMapping ):
			raise TypeError( "Invalid \"collection\" parameter, value must be type <Self|MutableMapping<Key,Val>, {} passed".format( typeof( collection ) ) )
		if isinstance( collection, Map ):
			for generic in collection:
				self.__set__( generic[0], generic[1] )
		else:
			for keyset in collection:
				self.__set__( keyset, collection[keyset] )
		...
	
	...


def builder( parent:Map[Key,Val], collection:Union[Map[Key,Val],MutableMapping[Key,Val]] ) -> Map[Key,Val]:
	
	"""
	Map builder for child, 
	
	:params Map parent
	:params Dict<Key, Value> data
	
	:return Map
	"""
	
	if not isinstance( parent, Map ):
		raise TypeError()
	if not isinstance( parent, type ):
		parent = type( parent )
	
	@final
	class MapBuilder( parent ):
		
		"""
		Children Map builder for avoid unhandled argument 
		when create new Map for children value
		"""
		
		def __init__( self, collection:Union[Self,MutableMapping[Key,Val]] ) -> None:
			Map.__init__( self, collection )
		
		...
		
	...

	return MapBuilder( collection )
