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
from threading import Thread
from typing import Any, Callable, final


@final
class Threading( Thread ):

	""" Thread class support data return """

	def __init__( self, group=None, target:Callable=None, name:Str=None, args:Any=None, kwargs:Any=None ) -> None:
		Thread.__init__( self, group=group, target=target, name=name, args=args if args else (), kwargs=kwargs if kwargs else {} )
		self.__return__:Any = None
		self.__exception__:Exception = None

	def run( self ) -> None:
		try:
			if callable( self._target ):
				self.__return__ = self._target( *self._args, **self._kwargs )
		except BaseException as e:
			self.__exception__ = e
	
	@property
	def exception( self ) -> Exception:
		return self.__exception__
	
	@property
	def returns( self ) -> Any:
		return self.__return__

	...

