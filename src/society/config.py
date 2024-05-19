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
from yaml import (
	safe_dump as YamlDumper, 
	safe_load as YamlLoader
)
from typing import Any, Dict, final, List, Tuple

from society.common import typeof
from society.logging import Logging
from society.storage import Storage
from society.torify import Torify
from society.typing.account import Account
from society.typing.anonym import Anonymity
from society.typing.authorization import Authorization
from society.typing.browser import Browser
from society.typing.properties import Properties


class Config:
	
	""" The Society Configurations """
	
	def __init__( self ) -> None:
		
		"""
		Construct method of class Config
		
		:return None
		:raises FileNotFoundError
			When the file configuration not found
		:raises RuntimeError
			When something is wrong at setup the anonimity (only production mode)
		:raises ValueError
			When the value of environment mode is invalid value
		"""
		
		address = None
		filename = "properties.yaml"
		contents = YamlLoader( Storage.cat( filename, stream=True ) )
		society = contents['society']
		society['environment'] = society['environment'].lower()
		envimode = society['environment']
		anonymity = Anonymity( **contents['anonymity'] )
		if envimode not in [ "development", "production" ]:
			raise ValueError( f"Invalid environment mode {envimode}" )
		try:
			if envimode == "production":
				if anonymity.torify['enabled'] is True:
					address = Torify.reNewTorIp( 
						port=anonymity.torify['port'], 
						proxies=anonymity.torify['proxies'], 
						password=anonymity.torify['password'] 
					)
				elif anonymity.proxies is not None:
					address = Torify.ipInfo( proxies=anonymity.proxies, complex=True )
				else:
					address = Torify.ipInfo( complex=True )
				if address is not None:
					Properties.IpInfo = address
					Properties.TimeZone = address['timezone']
		except Exception as e:
			Logging.error( "Uncaught {}:{}", typeof( e ), e, start="\x0d" )
			raise RuntimeError( "Failed to setup anonymity", e )
		active = 0
		accounts = []
		if "account" in contents:
			if "active" in contents['account']:
				active = contents['account']['active']
			if "saveds" in contents['account'] and isinstance( contents['account']['saveds'], list ):
				for saved in contents['account']['saveds']:
					if saved is None:
						continue
					authorization = None
					if "authorization" in saved and isinstance( saved['authorization'], dict ):
						authorization = Authorization( **saved['authorization'],
							username=saved['username'] if saved['username'] is not None else saved['usermail'], 
							password=saved['password'] 
						)
					browser = None
					if "browser" in saved and isinstance( saved['browser'], dict ):
						browser = Browser( **saved['browser'] )
					accounts.append(
						Account(
							authorization=authorization,
							browser=browser,
							usermail=saved['usermail'],
							username=saved['username'],
							password=saved['password']
						)
					)
		api = { "key": None, "secret": None }
		if "api" in contents and contents['api']:
			api = contents['api']
			Properties.ApiKey = api['key']
			Properties.ApiSecret = api['secret']
		self.__active__:Int = active
		self.__accounts__:List[Account] = accounts
		self.__api__:Dict[Str,Any] = api
		self.__anonymity__:Anonymity = anonymity
		self.__filename__:Str = filename
		self.__society__:Dict[Str,Any] = society
	
	@property
	def active( self ) -> Tuple[Int,Account]:
		return ( self.__active__, self.accounts[self.__active__-1] )
	
	def activate( self, position:Int ) -> None:
		
		"""
		Activate the account by position number
		
		:params Int position
			The position number
		
		:return None
		"""
		
		length = len( self.accounts )
		length-= 1
		if position > length and position < 0:
			raise IndexError( f"Account position {position} out of range" )
		self.__active__ = position
	
	@property
	def accounts( self ) -> List[Account]:
		return self.__accounts__
	
	@property
	def anonymity( self ) -> Anonymity:
		return self.__anonymity__
	
	@property
	def api( self ) -> Dict[Str,Str]:
		return self.__api__
	
	@property
	def environment( self ) -> Str:
		return self.__society__['environment']
	
	@property
	def filename( self ) -> Str:
		return self.__filename__
	
	@final
	def save( self ) -> None:
		
		"""
		Save society configuration as yaml
		
		:return None
		"""
		
		accounts = []
		for account in self.accounts:
			authorization = None
			if isinstance( account.authorization, Authorization ):
				authorization = {
					"accessToken": account.authorization.accessToken,
					"browser": account.authorization.browser,
					"machineId": account.authorization.machineId,
					"secret": account.authorization.secret,
					"sessionKey": account.authorization.sessionKey,
					"storageKey": account.authorization.storageKey,
					"uid": account.authorization.uid
				}
			browser = None
			if isinstance( account.browser, Browser ):
				browser = {
					"cookies": account.browser.cookies,
					"driver": account.browser.driver,
					"headers": account.browser.headers,
					"options": account.browser.options,
					"payload": account.browser.payload,
					"session": account.browser.session,
					"storage": account.browser.storage,
				}
			accounts.append({
				"authorization": authorization,
				"browser": browser,
				"usermail": account.usermail,
				"username": account.username,
				"password": account.password
			})
		anonymity = {
			"proxies": self.anonymity.proxies,
			"torify": self.anonymity.torify
		}
		comments = "\x0a\x23\x0a\x23\x20\x40\x61\x75\x74\x68\x6f\x72\x20\x41\x72\x69\x20\x53\x65\x74\x69\x61\x77\x61\x6e\x0a\x23\x20\x40\x63\x72\x65\x61\x74\x65\x20\x31\x32\x2e\x30\x31\x2d\x32\x30\x32\x34\x20\x31\x34\x3a\x33\x31\x0a\x23\x20\x40\x67\x69\x74\x68\x75\x62\x20\x68\x74\x74\x70\x73\x3a\x2f\x2f\x67\x69\x74\x68\x75\x62\x2e\x63\x6f\x6d\x2f\x68\x78\x41\x72\x69\x2f\x53\x6f\x63\x69\x65\x74\x79\x0a\x23\x0a\x23\x20\x53\x6f\x63\x69\x65\x74\x79\x20\x43\x6f\x70\x79\x72\x69\x67\x68\x74\x20\x28\x63\x29\x20\x32\x30\x32\x34\x20\x2d\x20\x41\x72\x69\x20\x53\x65\x74\x69\x61\x77\x61\x6e\x20\x3c\x68\x78\x61\x72\x69\x40\x70\x72\x6f\x74\x6f\x6e\x2e\x6d\x65\x3e\x0a\x23\x20\x53\x6f\x63\x69\x65\x74\x79\x20\x4c\x69\x63\x65\x6e\x63\x65\x20\x75\x6e\x64\x65\x72\x20\x47\x4e\x55\x20\x47\x65\x6e\x65\x72\x61\x6c\x20\x50\x75\x62\x6c\x69\x63\x20\x4c\x69\x63\x65\x6e\x63\x65\x20\x76\x33\x0a\x23\x0a\x23\x20\x54\x68\x69\x73\x20\x70\x72\x6f\x67\x72\x61\x6d\x20\x69\x73\x20\x66\x72\x65\x65\x20\x73\x6f\x66\x74\x77\x61\x72\x65\x3a\x20\x79\x6f\x75\x20\x63\x61\x6e\x20\x72\x65\x64\x69\x73\x74\x72\x69\x62\x75\x74\x65\x20\x69\x74\x20\x61\x6e\x64\x2f\x6f\x72\x20\x6d\x6f\x64\x69\x66\x79\x0a\x23\x20\x69\x74\x20\x75\x6e\x64\x65\x72\x20\x74\x68\x65\x20\x74\x65\x72\x6d\x73\x20\x6f\x66\x20\x74\x68\x65\x20\x47\x4e\x55\x20\x47\x65\x6e\x65\x72\x61\x6c\x20\x50\x75\x62\x6c\x69\x63\x20\x4c\x69\x63\x65\x6e\x73\x65\x20\x61\x73\x20\x70\x75\x62\x6c\x69\x73\x68\x65\x64\x20\x62\x79\x0a\x23\x20\x74\x68\x65\x20\x46\x72\x65\x65\x20\x53\x6f\x66\x74\x77\x61\x72\x65\x20\x46\x6f\x75\x6e\x64\x61\x74\x69\x6f\x6e\x2c\x20\x65\x69\x74\x68\x65\x72\x20\x76\x65\x72\x73\x69\x6f\x6e\x20\x33\x20\x6f\x66\x20\x74\x68\x65\x20\x4c\x69\x63\x65\x6e\x73\x65\x2c\x20\x6f\x72\x0a\x23\x20\x61\x6e\x79\x20\x6c\x61\x74\x65\x72\x20\x76\x65\x72\x73\x69\x6f\x6e\x2e\x0a\x23\x0a\x23\x20\x59\x6f\x75\x20\x73\x68\x6f\x75\x6c\x64\x20\x68\x61\x76\x65\x20\x72\x65\x63\x65\x69\x76\x65\x64\x20\x61\x20\x63\x6f\x70\x79\x20\x6f\x66\x20\x74\x68\x65\x20\x47\x4e\x55\x20\x47\x65\x6e\x65\x72\x61\x6c\x20\x50\x75\x62\x6c\x69\x63\x20\x4c\x69\x63\x65\x6e\x73\x65\x0a\x23\x20\x61\x6c\x6f\x6e\x67\x20\x77\x69\x74\x68\x20\x74\x68\x69\x73\x20\x70\x72\x6f\x67\x72\x61\x6d\x2e\x20\x49\x66\x20\x6e\x6f\x74\x2c\x20\x73\x65\x65\x20\x3c\x68\x74\x74\x70\x73\x3a\x2f\x2f\x77\x77\x77\x2e\x67\x6e\x75\x2e\x6f\x72\x67\x2f\x6c\x69\x63\x65\x6e\x73\x65\x73\x2f\x5c\x3e\x2e\x0a\x23\x0a\x23\x20\x53\x6f\x63\x69\x65\x74\x79\x20\x50\x72\x6f\x67\x72\x61\x6d\x20\x69\x73\x20\x6e\x6f\x74\x20\x61\x66\x66\x69\x6c\x69\x61\x74\x65\x64\x20\x77\x69\x74\x68\x20\x6f\x72\x20\x65\x6e\x64\x6f\x72\x73\x65\x64\x2c\x20\x65\x6e\x64\x6f\x72\x73\x65\x64\x20\x61\x74\x20\x61\x6c\x6c\x20\x62\x79\x0a\x23\x20\x46\x61\x63\x65\x62\x6f\x6f\x6b\x20\x6f\x72\x20\x61\x6e\x79\x20\x6f\x74\x68\x65\x72\x20\x70\x61\x72\x74\x79\x2c\x20\x69\x66\x20\x79\x6f\x75\x20\x75\x73\x65\x20\x74\x68\x65\x20\x6d\x61\x69\x6e\x20\x61\x63\x63\x6f\x75\x6e\x74\x20\x74\x6f\x20\x75\x73\x65\x20\x74\x68\x69\x73\x0a\x23\x20\x74\x6f\x6f\x6c\x20\x77\x65\x20\x61\x73\x20\x43\x6f\x64\x65\x72\x73\x20\x61\x6e\x64\x20\x44\x65\x76\x65\x6c\x6f\x70\x65\x72\x73\x20\x61\x72\x65\x20\x6e\x6f\x74\x20\x72\x65\x73\x70\x6f\x6e\x73\x69\x62\x6c\x65\x20\x66\x6f\x72\x20\x61\x6e\x79\x74\x68\x69\x6e\x67\x2c\x0a\x23\x20\x75\x73\x65\x20\x69\x74\x20\x61\x74\x20\x79\x6f\x75\x72\x20\x6f\x77\x6e\x20\x72\x69\x73\x6b\x2c\x20\x61\x6e\x64\x20\x74\x68\x69\x73\x20\x69\x73\x20\x53\x74\x72\x69\x63\x74\x6c\x79\xc2\xa0\x6e\x6f\x74\x20\x66\x6f\x72\x20\x53\x50\x41\x4d\x2e\x0a\x23\x0a"
		contents = "\x0a".join([
			comments,
			YamlDumper( 
				indent=4, 
				data={
					"account": {
						"active": self.active[0],
						"saveds": accounts
					},
					"anonymity": anonymity,
					"api": self.api,
					"society": self.society
				}
			),
			""
		])
		Storage.touch( self.filename, contents )
	
	@final
	@property
	def society( self ) -> Dict[Str,Any]:
		return self.__society__
	
	...
