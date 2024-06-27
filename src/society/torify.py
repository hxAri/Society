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
from requests.auth import HTTPProxyAuth
from socks import ProxyConnectionError
from stem.control import Controller
from stem import ControllerError, Signal, SocketError
from typing import Any, Dict, final

from society.requests import request
from society.logging import Logging
from society.typing import Properties


@final
class Torify:
	
	""" Torify Utility """
	
	@staticmethod
	def ipInfo( auth:HTTPProxyAuth=None, proxies:Dict[Str,Str]=None ) -> Dict[Str,Any]:
		
		"""
		Get current ip address.
		
		:params HTTPProxyAuth auth
		:params Dict<Str,Str> proxies
		
		:return Dict<Str,Any>
			The str of ip address
		"""
		
		hostname = "https://inet-ip.info/json"
		try:
			response = request( "GET", hostname, auth=auth, proxies=proxies )
			if response is not None:
				return response.json()
		except ProxyConnectionError as e:
			Logging.error( "Uncaught ProxyConnectionError: {}", e, start="\x0d" )
		return None
	
	@staticmethod
	def reNewTorIp( proxies:Dict[Str,Str], port:Int, password:Str ) -> Dict[Str,Any]:
		
		"""
		Re-new or change the current ip address.
		
		:params Dict<Str,Str> proxies
			The tor proxy configurations
		:params Int port
			The tor port number
		:params Str password
			The tor proxy password
		:params Bool check
			Allow check ip previous ip
		
		:return Dict<Str,Any>
		"""
		
		ipInfo = Properties.IpInfo
		if ipInfo is None:
			ipInfo = Torify.ipInfo()
		if ipInfo is None:
			Logging.error( "Failed getting IP Address info", start="\x0d" )
			return None
		previousIp = ipInfo['ipAddress']
		Logging.info( "Trying to re-new IP Address address={}", previousIp, start="\x0d" )
		try:
			with Controller.from_port( port=port ) as controller:
				controller.authenticate( password=password )
				controller.signal( getattr( Signal, "NEWNYM" ) )
		except SocketError as e:
			Logging.error( "Uncaught SocketError: {}", e, start="\x0d" )
			Logging.error( "Failed to estabilish connection from={}", previousIp, start="\x0d" )
			Logging.error( "Failed to update Ip Address from={}", previousIp, start="\x0d" )
		except ControllerError as e:
			Logging.error( "Uncaught ControllerError: {}", e, start="\x0d" )
			Logging.error( "Failed sending Signal from={}", previousIp, start="\x0d" )
			Logging.error( "Failed to update Ip Address from={}", previousIp, start="\x0d" )
		ipInfo = Torify.ipInfo( proxies=proxies )
		if ipInfo is None:
			Logging.error( "Failed getting IP Address info", start="\x0d" )
			return None
		currentIp = ipInfo['ipAddress']
		if currentIp != previousIp:
			Properties.IpInfo = ipInfo
			Logging.info( "The IP Address has been updated from={} to={}", previousIp, currentIp, start="\x0d" )
			return ipInfo
		Logging.critical( "The IP Address does not change from={}", previousIp, start="\x0d" )
		return None
	
	...
