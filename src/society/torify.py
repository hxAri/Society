
from builtins import bool as Bool, int as Int, str as Str
from socks import ProxyConnectionError
from stem.control import Controller
from stem import ControllerError, Signal, SocketError
from typing import Any, Dict, final

from society.common import request
from society.logging import Logging


@final
class Torify:
	
	@staticmethod
	def ipInfo( proxies:Dict[Str,Str]=None, complex:Bool=False ) -> Dict[Str,Any]:
		
		"""
		Get current ip address.
		
		:params Dict<Str,Str> proxies
		:params Bool complex
			When the complex is allowed we wel send 2x 
			request for get ip address information
		
		:return Dict<Str,Any>
			The str of ip address
		"""
		
		try:
			response = request( "GET", "https://api.ipify.org/?format=json", proxies=proxies )
			if response is not None:
				# Logging.info( "{}", response.text )
				if complex is True:
					address = response.json()['ip']
					
					"""
					Deliberately doing two requests, because every time I try to 
					get the IP address information, the Tor proxy is often hit or 
					detected and cannot get the IP address information.
					"""
					response = request( "GET", f"https://ipapi.co/{address}/json" )
					if response is None:
						return None
					# Logging.info( "{}", response.text, start="\x0d" )
				contents = response.json()
				if "error" not in contents:
					return contents
				Logging.error( "{}:{}", contents['reason'], contents['message'], start="\x0d" )
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
		
		ipInfo = Torify.ipInfo()
		if ipInfo is None:
			Logging.error( "Failed getting IP Address info", start="\x0d" )
			return None
		previousIp = ipInfo['ip']
		Logging.info( "Trying to re-new IP Address address={}", previousIp, start="\x0d" )
		try:
			with Controller.from_port( port=port ) as controller:
				controller.authenticate( password=password )
				controller.signal( Signal.NEWNYM )
		except SocketError as e:
			Logging.error( "Uncaught SocketError: {}", e, start="\x0d" )
			Logging.error( "Failed to estabilish connection from={}", previousIp, start="\x0d" )
			Logging.error( "Failed to update Ip Address from={}", previousIp, start="\x0d" )
		except ControllerError as e:
			Logging.error( "Uncaught ControllerError: {}", e, start="\x0d" )
			Logging.error( "Failed sending Signal from={}", previousIp, start="\x0d" )
			Logging.error( "Failed to update Ip Address from={}", previousIp, start="\x0d" )
		ipInfo = Torify.ipInfo( proxies=proxies, complex=True )
		if ipInfo is None:
			Logging.error( "Failed getting IP Address info", start="\x0d" )
			return None
		currentIp = ipInfo['ip']
		if currentIp != previousIp:
			Logging.info( "The IP Address has been updated from={} to={}", previousIp, currentIp, start="\x0d" )
			return ipInfo
		Logging.critical( "The IP Address does not change from={}", previousIp, start="\x0d" )
		return None
	
	...
