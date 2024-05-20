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

from builtins import bool as Bool, str as Str
from datetime import datetime, timedelta
from json import loads as decoder
from pytz import timezone
from typing import final

from society.typing.authorization import Authorization
from society.typing.browser import Browser
from society.typing.builtins import Self
from society.typing.properties import Properties
from society.typing.readonly import Readonly


@final
class Account( Readonly ):
	
	""" Account Typing Implementation """
	
	def __init__( self, authorization:Authorization, browser:Browser, usermail:Str=None, username:Str=None, password:Str=None ) -> None:
		
		"""
		Construct method of class Account
		
		:params Authorization authorization
			The account authorization credentials
		:params Browser browser
			The browser information
		:params Str usermail
			The user email address
		:params Str username
			The user username
		:params Str password
			The user password
		
		return None
		"""
		
		self.authorization:Authorization = authorization \
			if authorization is not None else \
				Authorization(
					username=username \
						if username is not None else \
						   usermail, 
					password=password 
				)
		self.browser:Browser = browser
		self.usermail:Str = usermail
		self.username:Str = username
		self.password:Str = password
	
	@property
	def isAnonymous( self ) -> Bool:
		
		"""
		Return whether the Account instance is Anonymous Identity
		
		:return Bool
		"""
		
		return self.usermail is None and \
			   self.username is None and \
			   self.password is None
	
	@property
	def refresh( self ) -> Bool:
		
		"""
		Return whether account is require refresh browser.
		
		:return Bool
		"""
		
		for cookie in self.browser.cookies:
			if cookie['name'] == "presence":
				values = cookie['value']
				if not values:
					return True
				content = values[values.index( "\x7b" ):]
				decoded = decoder( content )
				signout = timedelta( days=3 )
				currzone = timezone( Properties.TimeZone )
				currtime = datetime.now( currzone )
				try:
					presence = datetime.fromtimestamp( decoded['utc3'], currzone )
				except ValueError:
					presence = datetime.fromtimestamp( int( decoded['utc3'] / 1000 ), currzone )
				presence = presence + signout
				return presence <= currtime
		return not self.isAnonymous
	
	def withAuthorization( self, authorization:Authorization ) -> Self:
		
		"""
		Return new Account Instance with Specific Authorization
		
		:params Authorization authorization
		
		:return Account
		"""
		
		return Account( authorization, self.browser, self.usermail, self.username, self.password )
	
	def withBrowser( self, browser:Browser ) -> Self:
		
		"""
		Return new Account Instance with Specific Browser
		
		:params Browser browser
		
		:return Account
		"""
		
		return Account( self.authorization, browser, self.usermail, self.username, self.password )
	
	...

