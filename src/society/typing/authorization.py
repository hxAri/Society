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
from hashlib import md5
from typing import final, TypeVar as Var

from society.common import request
from society.typing.properties import Properties
from society.typing.readonly import Readonly


Authorization = Var( "Authorization" )
""" Authorization Type Var """


@final
class Authorization( Readonly ):
	
	""" Authorization Typing Implementation """
	
	def __init__( self, username:Str, password:Str, accessToken:Str=None, browser:Str=None, machineId:Str=None, secret:Str=None, sessionKey:Str=None, storageKey:Str=None, uid:Str=None ) -> None:
		
		"""
		Construct method of class Authorization
		
		:params Str username
		:params Str password
		:params Str accessToken
		:params Str browser
		:params Str machineId
		:params Str secret
		:params Str sessionKey
		:params Str storageKey
		:params Str uid
		
		return None
		"""
		
		self.accessToken:Str = accessToken
		self.browser:Str = browser
		self.machineId:Str = machineId
		self.secret:Str = secret
		self.sessionKey:Str = sessionKey
		self.storageKey:Str = storageKey
		self.uid:Str = uid
		self.username:Str = username
		self.password:Str = password
	
	def generate( self ) -> Authorization:
		
		"""
		Facebook generate new access token
		
		:return Authorization
		"""
		
		if not self.username:
			raise TypeError( "To generate an Access Token, a username is required" )
		if not self.password:
			raise TypeError( "To generate an Access Token, a password is required" )
		if not Properties.ApiKey:
			raise TypeError( "To generate an Access Token, a API Private Key is required" )
		if not Properties.ApiSecret:
			raise TypeError( "To generate an Access Token, a API Private Secret is required" )
		
		proxies = None
		payload = {
			"api_key": Properties.ApiKey,
			"email": self.username,
			"format": "JSON",
			"locale": "vi_vn",
			"method": "auth.login",
			"password": self.password,
			"return_ssl_resources": 0,
			"v": "1.0"
		}
		payload['sig'] = md5( "".join([ "".join( list( f"{keyset}={value}" for keyset, value in payload.items() if value ) ), Properties.ApiSecret ]).encode( "utf-8" ) ).hexdigest()
		parameters = "\x26".join( list( f"{keyset}={value}" for keyset, value in payload.items() if value ) )
		response = request( "GET", f"https://api.facebook.com/restserver.php?{parameters}",
			proxies=proxies,
			headers={
			}
		)
		if response is not None:
			decoded = response.json()
			if "access_token" in decoded and decoded['access_token']:
				keysets = {
					"access_token": "accessToken",
					"machine_id": "machineId",
					"secret": "secret",
					"session_key": "sessionKey",
					"storage_key": "storageKey",
					"uid": "uid"
				}
				results = { keyset: decoded[alias] for keyset, alias in keysets.items() if keyset in decoded }
				return Authorization( browser=self.browser, username=self.username, password=self.password, **results )
			if "error_msg" in decoded and decoded['error_msg']:
				raise RuntimeError( f"{decoded['error_code']}: {decoded['error_msg']}" )
			...
		return None
	
	...
