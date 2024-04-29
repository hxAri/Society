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
from typing import Any, Dict, TypeGuard as Guard, Union

from society.typing.readonly import Readonly


class Anonymity( Readonly ):
	
	def __init__( self, proxies:Guard[Union[Dict[Str,Str],None]], torify:Guard[Dict[Str,Any]] ) -> None:
		self.proxies:Dict[Str,Str] = proxies
		self.torify:Dict[Str,Any] = torify
	
	...
