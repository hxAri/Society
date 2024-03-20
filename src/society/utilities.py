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
from concurrent.futures import Future, ThreadPoolExecutor
from json import loads as decoder
from re import search
from time import sleep
from traceback import format_exc
from typing import Any, Callable, Dict, Iterable, List, Literal

from society.common import snakeCase, typeof
from society.logging import Logging
from society.typing.builtins import Val
from society.typing.result import Result
from society.typing.threading import Threading

def Executor( jobdesks:List[Dict[Str,Any]], sleepy:Int=1, worker:Int=2, workerDelays:Int=10, workerTimeout:Int=120, **kwargs:Any ) -> Iterable[Result[Literal['operation'],Val]]:

	"""
	Automation Command Line Execution

	:params List<Dict<Str, Any>> jobdesks
	:params Int sleepy
	:params Int worker
	:params Int workerDelays
	:params Int workerTimeout
	:params Any **kwargs

	:return Iterable<Result>
	"""
	
	for jobdesk in jobdesks:
		results = None
		tokenName = snakeCase( jobdesk['name'] )
		tokenKeysets = jobdesk['keysets']
		if tokenName not in kwargs or tokenName in kwargs and not kwargs[tokenName]:
			continue
		tokenValue = kwargs[tokenName]
		if isinstance( tokenValue, Str ):
			tokenMatched = search( jobdesk['pattern'], tokenValue if not isinstance( tokenValue, str ) else f"{tokenValue}" if tokenValue is not None else "" )
			if tokenMatched is None:
				Logging.error( "Invalid option value for --{}", tokenName.replace( "_", "-" ), close=1 )
			tokenMatches = tokenMatched.groupdict()
		else:
			tokenMatches = {}
			if tokenKeysets:
				tokenMatches[list( tokenKeysets.keys() )[0]] = tokenValue
		if "requires" in jobdesk and isinstance( jobdesk['requires'], list ):
			for tokenRequire in jobdesk['requires']:
				tokenNameRequire = snakeCase( tokenRequire['name'] )
				tokenKeyset = tokenRequire['keyset']
				if tokenNameRequire in kwargs and kwargs[tokenNameRequire]:
					tokenMatches[tokenKeyset] = kwargs[tokenNameRequire]
		tokenParams = {}
		for tokenKeyset in tokenKeysets:
			if tokenKeyset not in tokenMatches or tokenMatches[tokenKeyset] is None:
				tokenParams[tokenKeyset] = None
				continue
			try:
				tokenTyping = tokenKeysets[tokenKeyset]
				tokenParams[tokenKeyset] = tokenMatches[tokenKeyset]
				if "escapes" in jobdesk and isinstance( jobdesk['escapes'], list ):
					for escape in jobdesk['escapes']:
						tokenParams[tokenKeyset] = tokenParams[tokenKeyset].replace( f"\\{escape}", escape )
				if isinstance( tokenTyping, list ):
					if bool in tokenKeysets[tokenKeyset]:
						Logging.error( "The Boolean convertion can't use in multiple convertion value", close=1 )
					for tokenType in tokenKeysets[tokenKeyset]:
						if tokenType is int:
							if tokenParams[tokenKeyset] is not None and isinstance( tokenParams[tokenKeyset], str ) and tokenParams[tokenKeyset].isnumeric():
								tokenParams[tokenKeyset] = tokenType( tokenParams[tokenKeyset] )
							elif tokenParams[tokenKeyset] is not None and isinstance( tokenParams[tokenKeyset], int ):
								tokenParams[tokenKeyset] = tokenParams[tokenKeyset]
				elif isinstance( tokenTyping, type ) or callable( tokenTyping ):
					if tokenParams[tokenKeyset] is not None:
						if tokenTyping is bool:
							tokenParams[tokenKeyset] = tokenParams[tokenKeyset]
							if tokenParams[tokenKeyset].isnumeric():
								tokenParams[tokenKeyset] = int( tokenParams[tokenKeyset] )
							elif tokenParams[tokenKeyset].lower() == "false":
								tokenParams[tokenKeyset] = -0
							elif tokenParams[tokenKeyset].lower() == "true":
								tokenParams[tokenKeyset] = +1
							tokenParams[tokenKeyset] = bool( tokenParams[tokenKeyset] )
						elif tokenTyping is dict or tokenTyping is list:
							tokenParams[tokenKeyset] = decoder( tokenParams[tokenKeyset] )
							if tokenTyping is list and isinstance( tokenParams[tokenKeyset], dict ):
								tokenParams[tokenKeyset] = list( tokenParams[tokenKeyset].values() )
						else:
							tokenParams[tokenKeyset] = tokenTyping( tokenParams[tokenKeyset] )
				else:
					Logging.error( "Failed convert value keyset {} into with {}", tokenKeyset, tokenTyping, close=1 )
			except TypeError as e:
				Logging.error( "Uncaught ValueError: {}", e )
				Logging.error( "Cannot convert value type of \"{}\" with {}", tokenKeyset, tokenTyping.__name__.title(), close=1 )
			except ValueError as e:
				Logging.error( "Uncaught ValueError: {}", e )
				Logging.error( "Invalid \"{}\" value, value type must be type {}", tokenKeyset, tokenTyping.__name__.title(), close=1 )
		tokenThread = jobdesk['thread']
		tokenExecute = jobdesk['execute']
		if tokenThread is None:
			results = tokenExecute( **tokenParams )
		elif tokenThread is ThreadExecutor:
			tokenThreadName = "Executing {execute}"
			if "dataset" not in jobdesk or not jobdesk['dataset']:
				Logging.error( "Cannot executute {}, unknown target dataset", tokenExecute, close=1 )
			tokenDatasetName = jobdesk['dataset']
			tokenDatasetValue = tokenParams[tokenDatasetName]
			if isinstance( tokenDatasetValue, int ):
				tokenDatasetValue = list( i for i in range( tokenDatasetValue ) )
			elif isinstance( jobdesk, str ):
				tokenDatasetValue = [tokenDatasetValue]
			if tokenDatasetName not in tokenParams or not tokenParams[tokenDatasetName] or not isinstance( tokenParams[tokenDatasetName], Iterable ):
				Logging.error( "Cannot execute {}, dataset target does not iterable", tokenExecute, close=1 )
			if "message" in jobdesk and isinstance( jobdesk['message'], dict ):
				if "name" in jobdesk['message'] and jobdesk['message']['name']:
					tokenThreadName = jobdesk['message']['name']
			tokenFormats = { "execute": tokenExecute, **tokenParams }
			del tokenParams[tokenDatasetName]
			results = ThreadExecutor(
				name=tokenThreadName.format( **tokenFormats ),
				callback=lambda value, thread: tokenExecute(
					value, thread=thread, **tokenParams
				),
				dataset=tokenDatasetValue,
				sleepy=sleepy,
				worker=worker,
				workerDelays=workerDelays,
				workerTimeout=workerTimeout
			)
		elif tokenThread is ThreadRunner:
			tokenLoading = "Executing {execute}"
			tokenSuccess = None
			if "message" in jobdesk and isinstance( jobdesk['message'], dict ):
				if "loading" in jobdesk['message'] and jobdesk['message']['loading']:
					tokenLoading = jobdesk['message']['loading']
				if "success" in jobdesk['message'] and jobdesk['message']['success']:
					tokenSuccess = jobdesk['message']['success']
			tokenThread = ThreadRunner(
				target=lambda: tokenExecute( **tokenParams, thread=1 ),
				success=tokenSuccess,
				loading=tokenLoading.format(
					execute=tokenExecute,
					**tokenParams
				)
			)
			if tokenThread.exception is not None:
				exception = tokenThread.exception
				Logging.error( "{}: {}", typeof( exception ), exception, close=1 )
			results = tokenThread.returns
		else:
			Logging.error( "Unhandled executor runner {}", tokenThread, close=1 )
		if results is not None and results:
			yield Result( operation=tokenName, values=results )
	...

def ThreadExecutor( name:Str, callback:Callable, dataset:List[Any], sleepy:Int=1, workers:Int=2, workerDelays:Int=10, workerTimeout:Int=120, *args:Any, **kwargs:Any ) -> List[Any]:

	"""
	Short ThreadPoolExecutor

	:params Str name
	:params Callable callback
	:params List<Any> dataset
	:params Int sleepy
	:params Int worker
	:params Int workerDelays
	:params Int workerTimeout
	:params Any *args
	:params Any **kwargs

	:return List<Any>
	"""

	results:list[Any] = []
	
	with ThreadPoolExecutor( max_workers=workers ) as executor:
		futures:list[Future] = []
		Logging.info( "Building Thread Pool Executor with {} workers for {}", workers, name, start="\r" )
		try:
			for count, data in enumerate( dataset ):
				Logging.info( "Starting thread for {}", name, start="\r", thread=count+1 )
				futures.append( executor.submit( callback, data, *args, thread=count+1, **kwargs ) )
				sleep( workerDelays if ( count +1 ) % workers == 0 else sleepy )
			while all( future.done() for future in futures ) is False:
				for count, future in enumerate( futures ):
					if future.running() is True:
						loading = f"Future thread worker {count+1} is running..."
						length = len( loading )
						position = -1
						for i in loading:
							if position >= length:
								position = -1
							position += 1
							messages = loading
							if position >= 1:
								messageChar = loading[position-1:position]
								messageChar = messageChar.lower() \
									if messageChar.isupper() \
									else messageChar.upper()
								messagePrefix = loading[0:position-1]
								messageSuffix = loading[position:]
								messages = "".join([
									messagePrefix, 
									messageChar, 
									messageSuffix
								])
							Logging.info( "{}", messages, end="\x20", start="\r", thread=count+1 )
							sleep( 0.1 )
					...
				...
			Logging.info( "A total of {} worker threads have been completed", len( futures ), start="\r" )
			results = list( future.result() for future in futures )
		except BaseException as e:
			if isinstance( e, KeyboardInterrupt ):
				Logging.info( "Program has been stopped", start="\x0a", close=1 )
			else:
				Logging.error( "Uncaught {}: {}", typeof( e ), format_exc(), start="\r", close=1 )
	Logging.info( "Thread Pool for {} stoped", name, start="\r" )
	return results

def ThreadRunner( loading:Str, success:Str=None, group=None, target:Callable=None, name=None, args=None, kwargs=None ) -> Threading:

	"""
	Short Threading

	:params Str loading
	:params Str success
	:params Any group
	:params Callable target
	:params Str name
	:params Any args
	:params Any kwargs

	:return Threading
	"""

	try:
		thread = Threading( group=group, target=target, name=name, args=args, kwargs=kwargs )
		thread.start()
		while thread.is_alive():
			length = len( loading )
			position = -1
			for i in "\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-\|/-":
				if position >= length:
					position = -1
				position += 1
				messages = loading
				if position >= 1:
					messageChar = loading[position-1:position]
					messageChar = messageChar.lower() \
						if messageChar.isupper() \
						else messageChar.upper()
					messagePrefix = loading[0:position-1]
					messageSuffix = loading[position:]
					messages = "".join([
						messagePrefix, 
						messageChar, 
						messageSuffix
					])
				Logging.info( "{}", messages, end="\x20", start="\r", thread=i )
				sleep( 0.1 )
		Logging.info( "{}", success if success is not None else loading, end="\x0a", start="\r" )
		return thread
	except BaseException as e:
		if isinstance( e, KeyboardInterrupt ):
			Logging.info( "Program has been stopped", start="\x0a", close=1 )
		else:
			Logging.error( "Uncaught {}: {}", type( e ).__name__, format_exc(), start="\r", close=1 )
	return None
	...
