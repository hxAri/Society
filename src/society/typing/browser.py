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
from selenium.webdriver.remote.webdriver import WebDriver
from seleniumwire.inspect import InspectRequestsMixin as Inspector
from seleniumwire.webdriver import (
	Chrome, ChromeOptions, 
	Firefox, FirefoxOptions
)
from typing import Any, Dict, final, List, Union
from urllib.parse import unquote as UrlDecoder

from society.typing.builtins import Val
from society.typing.readonly import Readonly


@final
class Driver( Inspector, WebDriver ): ...

@final
class Browser( Readonly ):
	
	""" Base Browser class """
	
	def __init__( self, driver:Str, cookies:Union[List[Dict[Str,Val]],Str], headers:Dict[Str,Str], options:List[Dict[Str,Any]], payload:Dict[Str,Str], session:Dict[Str,Str], storage:Dict[Str,Str] ) -> None:
		
		"""
		Construct method of class Browser
		
		:params Str driver
			The browser driver automation e.g Chrome, Firefox
		:params List<Dict<Str,Val>>|Str cookies
			The browser cookies
		:params Dict<Str,Str> headers
			The browser headers
		:params List<Dict<Str,Any>> options
			The browser driver options
		:params Dict<Str,Str> payload
			The browser graphql payload
		:params Dict<Str,Str> session
			The browser session storage
		:params Dict<Str,Str> storage
			The browser local storage
		
		:return None
		"""
		
		if cookies is None:
			if "Cookie" in headers:
				cookies = headers['Cookie']
				del headers['Cookie']
		if isinstance( cookies, Str ):
			explode = cookies.split( "; " )
			cookies = []
			for item in explode:
				parts = item.split( "=" )
				cookies.append({
					"name": parts[0],
					"value": UrlDecoder( parts[1] )
				})
		for i, cookie in enumerate( cookies ):
			if "domain" not in cookie:
				cookie['domain'] = ".facebook.com"
				cookies[i] = cookie
		self.driver:Str = driver.capitalize()
		self.cookies:List[Dict[Str,Val]] = cookies
		self.headers:Dict[Str,Str] = headers
		self.options:List[Dict[Str,Any]] = options
		self.payload:Dict[Str,Str] = payload
		self.session:Dict[Str,Str] = session if session is not None else {}
		self.storage:Dict[Str,Str] = storage if storage is not None else {}
	
	def create( self ) -> Driver:
		
		"""
		Return browser instance
		
		:return WebDriver
		"""
		
		if self.driver == "Chrome":
			options = ChromeOptions()
			driver = Chrome
		else:
			options = FirefoxOptions()
			driver = Firefox 
		for option in self.options:
			if option['type'] in [ "argument" ]:
				options.add_argument( option['value'] )
			if option['type'] in [ "add_experimental_option", "experimental" ]:
				if hasattr( options, "add_experimental_option" ):
					options.add_experimental_option( option['param'], option['value'] )
				...
			...
		...
		proxy = {} # The browser typing currently does not have access to account typing.
		parameters = {
			"options": options,
			"seleniumwire_options": {
				"disable_encoding": True,
				"mitm_http2": False,
				"proxy": proxy
			}
		}
		return driver( **parameters, keep_alive=True )
	
	...
