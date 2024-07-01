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

from brotli import decompress as BrotliDecompress, error as BrotliError
from builtins import bool as Bool, int as Int, str as Str
from gzip import BadGzipFile, decompress as GzipDecompress
from hashlib import md5
from pyzstd import decompress as ZstdDecompress, ZstdError
from re import match
from requests import Response, Session
from requests.auth import HTTPBasicAuth, HTTPDigestAuth, HTTPProxyAuth
from requests.exceptions import (
	ConnectionError as RequestConnectionError, 
	ConnectTimeout as RequestConnectionTimeout, 
	RequestException as RequestError
)
from time import sleep
from traceback import format_exception
from typing import Any, MutableMapping, Tuple, Union
from urllib3.exceptions import (
	ConnectionError as UrllibConnectionError,
	ConnectTimeoutError as UrllibConnectTimeoutError,
	RequestError as UrllibRequestError,
	NewConnectionError as UrllibNewConnectionError
)

from society.common import typeof
from society.logging import Logging
from society.storage import Storage


def download( source:Str, mediaType:Str, directory:Str=None, proxies:MutableMapping[Str,Str]=None, stream:Bool=False, thread:Int=0 ) -> Str:

	"""
	Download media content e.g image, video

	:params Str source
		The media url source
	:params Str mediaType
		The file media type, e.g image, video
	:params Str directory
		The media directory save
	:params MutableMapping<Str,Str> proxies
		The Http request proxies
	:params Bool stream
		Allow request stream
	:params Int thread
		Current thread position number
	
	:return Str
	"""
	
	Logging.info( "Downloading media mime={}", mediaType, thread=thread, start="\x0d" )
	try:
		response = request( "GET", url=source, proxies=proxies, stream=stream, thread=thread )
		if response.status_code == 200:
			extename = extension( response, mediaType, "jpg" if mediaType == "image" else "mp4" if mediaType == "video" else "", thread=thread )
			pathname = directory if directory is not None else "history/contents"
			filename = md5( source.encode( "utf-8" ) ).hexdigest()
			fullname = f"{pathname}/{filename}.{extename}"
			try:
				Storage.mkdir( pathname )
				Storage.touch( fullname, response.content, fmode="wb" )
				Logging( "Downloaded mime={} saved={}", mediaType, fullname, thread=thread, start="\x0d" )
				return fullname
			except OSError as e:
				Logging.error( "Uncaught OSError: {}", e.strerror, thread=thread, start="\x0d" )
				Logging.error( "Failed download media mime={}", mediaType, thread=thread, start="\x0d" )
	except( ExceptionGroup, TypeError ) as e:
		if isinstance( e, ExceptionGroup ):
			Logging.error( "Uncaught ExceptionGroup: {}", e.message, thread=thread, start="\x0d" )
			for group in list( e.exceptions ):
				Logging.error( "Uncaught ExceptionGroup<{}>: {}", typeof( group ), "\x0a".join( format_exception( group ) ), thread=thread, start="\x0d" )
		else:
			Logging.error( "Uncaught TypeError: {}", e.args, thread=thread, start="\x0d" )
		Logging.error( "Failed download media mime={}", mediaType, thread=thread, start="\x0d" )
	return None

def extension( response:Response, type:Str="image", default:Str="jpg", thread:Int=0 ) -> Str:

	"""
	Return file extension name by request response.

	:params Response response
	:params Str type
		The file media type, e.g image, video
	:params Str default
		The default file extension name when the response is unknown Content-Type
	:params Int thread
		Current thread position number
	
	:return Str
	"""
	
	contentType = response.headers['Content-Type']
	matched = match( r"^(?:(?P<image>image)\/(?P<image_extension>jpg|jpeg|png|webp)|(?P<video>video\/(?P<video_extension>mp4|webm)))$", contentType )
	if matched is not None:
		groups = matched.groupdict()
		group = f"{type}_extension"
		if group in groups and groups[group]:
			return groups[group]
		return default
	raise ValueError( f"Unsupported media type for Content-Type {contentType}", ( "thread", thread ) )

def request( method:Str, url:Str, auth:Union[HTTPBasicAuth,HTTPDigestAuth,HTTPProxyAuth,Tuple[Str,Str]]=None, data:MutableMapping[Str,Any]=None, cookies:MutableMapping[Str,Str]=None, headers:MutableMapping[Str,Str]=None, params:MutableMapping[Str,Str]=None, payload:MutableMapping[Str,Any]=None, proxies:MutableMapping[Str,Str]=None, stream:Bool=False, timeout:Int=None, tries:Int=10, thread:Int=0 ) -> Response:
	
	"""
	Send HTTP Request
	
	:params Str method
		Http request method
	:params Str url
		Http request url target
	:params HTTPBasicAuth|HTTPDigestAuth|HTTPProxyAuth|Tuple<Str,Str> auth
		Http request authentication
	:params MutableMapping<Str, Any> data
		Http request multipart form data
	:params MutableMapping<Str, Str> cookies
		Http request cookies
	:params MutableMapping<Str, Str> headers
		Http request headers
	:params MutableMapping<Str, Str> params
		Http request parameters
	:params MutableMapping<Str, Any> payload
		Http request json payload data
	:params MutableMapping<Str, Any> proxies
		Http request proxies
	:params Bool stream
		Allow request stream
	:params Int timeout
		Http request timeout
	:params Int tries
		Http request timeout tries
	:params Int thread
		Current thread position number
	
	:return Response
	:raises ExceptionGroup
		Raised when the request has tried as many times as possible
		to send the request but the exception is still thrown from
		the requests module or urllib
	:raises TypeError
		Raised when the caught exception is not among the
		exceptions that can be resumed
	:example
        .. code-block:: python
        try:
			response = request( "GET", "https://www.google.com" )
			print( response )
		except ExceptionGroup as e:
			...
		except TypeError as e:
			...
	"""
	
	counter = 0
	session = Session()
	throwned = []
	throwable = [
		RequestConnectionError, 
		RequestConnectionTimeout, 
		RequestError,
		UrllibConnectionError,
		UrllibConnectTimeoutError,
		UrllibRequestError,
		UrllibNewConnectionError
	]
	continueable = ( 
		RequestConnectionError, 
		RequestConnectionTimeout, 
		UrllibConnectionError,
		UrllibConnectTimeoutError,
		UrllibNewConnectionError
	)
	if tries <= 0:
		tries = 10
	while counter <= 10:
		Logging.info( "Trying {} Request url=\"{}\"", method, url, thread=thread, start="\x0d" )
		try:
			response = session.request( 
				url=url, 
				data=data, 
				auth=auth,
				json=payload, 
				stream=stream,
				method=method, 
				cookies=cookies, 
				headers=headers, 
				timeout=timeout,
				proxies=proxies,
				params=params 
			)
			try:
				encoding = response.headers['Content-Encoding'] \
					if "Content-Encoding" in response.headers \
					else None
				if encoding is not None:
					content = response._content
					match encoding:
						case "br":
							content = BrotliDecompress( response.content )
						case "gzip":
							content = GzipDecompress( response.content )
						case "zstd":
							content = ZstdDecompress( response.content )
						case _:
							raise UnicodeEncodeError( f"Unsupported encoding {encoding}" )
					response._content = content
				...
			except BadGzipFile:
				...
			except BrotliError:
				...
			except ZstdError:
				...
			return response
		except BaseException as e:
			instance = type( e )
			throwable.append( e )
			if instance in throwable:
				Logging.error( "{}<{}>: {}", typeof( e ), counter, e, thread=thread )
				if isinstance( e, continueable ):
					counter += 1
					sleep( 2 )
					continue
			if throwned:
				raise ExceptionGroup( f"An error occurred while sending a {method} request to url=\"{url}\"", throwned ) from e
			raise TypeError( ( "prev", e ), ( "thread", thread ) ) from e
	return None
