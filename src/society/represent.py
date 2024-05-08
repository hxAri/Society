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


@final
class Represent:

	@staticmethod
	def normalize( string:str ) -> str:
		return string \
			.replace( "\"", "\\\"" ) \
			.replace( "\n", "\\n" ) \
			.replace( "\t", "\\t" )

	@staticmethod
	def typeof( instance:object ) -> str:
		return type( instance ).__name__

	@staticmethod
	def wrapper( data:dict|list|object, indent:int=4 ) -> str:
		values = []
		length = len( data )
		spaces = "\x20" * indent
		if isinstance( data, dict ):
			define = "\"{}\""
			indexs = data.keys()
		else:
			define = "[{}]"
			indexs = list( idx for idx in range( length ) )
		for index in indexs:
			key = define.format( index )
			value = data[index]
			if isinstance( value, dict ):
				if len( value ) >= 1:
					values.append( "{}: {}".format( key, Represent.convert( value, indent +4 ) ) )
				else:
					values.append( "{}: {}(\n{})".format( key, Represent.typeof( value ), spaces ) )
			elif isinstance( value, list ):
				length = len( value )
				lspace = indent + 4
				lspace = "\x20" * lspace
				if length >= 1:
					array = []
					for i in range( length ):
						if isinstance( value[i], ( dict, list ) ):
							array.append( "[{}]: {}".format( i, Represent.convert( value[i], indent +8 ) ) )
						else:
							if isinstance( value[i], str ):
								value[i] = f"\"{Represent.normalize(value[i])}\""
							array.append( "[{}]: {}({})".format( i, Represent.typeof( value[i] ), value[i] ) )
					values.append( "{0}: {1}(\n{2}{4}\n{3})".format( key, Represent.typeof( value ), lspace, spaces, f",\n{lspace}".join( array ) ) )
				else:
					values.append( "{0}: {1}(\n{2})".format( key, Represent.typeof( value ), spaces ) )
			else:
				if isinstance( value, str ):
					value = f"\"{Represent.normalize(value)}\""
				values.append( "{}: {}({})".format( key, Represent.typeof( value ), value ) )
		return f",\n{spaces}".join( values )

	@staticmethod
	def convert( data:dict|list|object, indent:int=4 ) -> str:
		if len( data ) >= 1:
			return "{}(\n{}{}\n{})".format( Represent.typeof( data ), "\x20" * indent, Represent.wrapper( data, indent=indent ), "\x20" * ( 0 if indent == 4 else indent -4 ) )
		return "{}(\n{})".format( Represent.typeof( data ), "\x20" * ( 0 if indent == 4 else indent -4 ) )

	...
