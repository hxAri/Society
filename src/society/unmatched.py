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

from builtins import int as Int, str as Str
from inspect import getframeinfo, stack
from json import dumps as encoder
from typing import Any, Dict, final, List, Union

from society.common import strftime, timestamp
from society.logging import Logging
from society.storage import Storage


@final
class Unmatched:
	
	""" An Unmatched Class Implementation for dumping every unmatched graphql contents """
	
	@staticmethod
	def dumping( metadata:Dict[Str,Any], contents:Union[Dict[Str,Any],List[Dict[Str,Any]],Str], thread:Int=0 ) -> None:
		
		"""
		Dumping unmatched contents
		
		:params Dict<Str,Any> metadata
			:keyset Str message
				:value Str
			Metadata unmatched graphql contents
		:params Dict<Str,Any>|List<Dict<Str,Any>>|Str contents
			Unmatched graphql contents
		:params Int thread
			Current thread position number
		
		:return None
		"""
		
		currtime = timestamp()
		pathname = strftime( "%d.%m-%Y %H:%M", currtime )
		traceback = getframeinfo( stack()[2][0] )
		filename = traceback.filename
		function = traceback.function
		inlineno = traceback.lineno
		metadata = {
			**metadata,
			**{
				"filename": filename,
				"function": function,
				"inlineno": inlineno,
				"position": {
					"column": {
						"start": traceback.positions.col_offset,
						"end": traceback.positions.end_col_offset
					},
					"lineno": {
						"start": traceback.positions.lineno,
						"end": traceback.positions.end_lineno
					}
				}
			}
		}
		counter = 1
		realname = f"resources/unparsed/{currtime}"
		directory = realname
		while Storage.d( directory ) is True:
			directory = f"{realname}/{counter}"
			counter += 1
		Logging.warning( "Found unmatched contents on {}:{}", filename, inlineno, thread=thread, start="\x0d" )
		Storage.mkdir( directory )
		if isinstance( contents, ( dict, list ) ):
			Storage.touch( f"{directory}/unmatched-contents-{pathname}.json", encoder( contents, indent=4 ) )
		else:
			Storage.touch( f"{directory}/unmatched-contents-{pathname}.html", encoder( contents, indent=4 ) )
		Storage.touch( f"{directory}/unmatched-metadata-{pathname}.json", encoder( metadata, indent=4 ) )
	
	...
