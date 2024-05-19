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
from json import loads as decoder, JSONDecodeError
from time import sleep
from traceback import format_exc, format_exception
from typing import Any, Callable, Dict, Iterable, List, Literal, Set, Tuple

from society.common import snakeCase, typeof
from society.logging import Logging
from society.typing.builtins import Val
from society.typing.jobdesk import Jobdesk
from society.typing.result import Result
from society.typing.threading import Threading


def Executor( jobdesks:List[Jobdesk], sleepy:Int=1, worker:Int=2, workerDelays:Int=10, workerTimeout:Int=120, **kwargs:Any ) -> Iterable[Result[Literal['operation'],Val]]:
	
	"""
	Automation Command Line Execution
	
	:params List<Jobdesk> jobdesks
	:params Int sleepy
	:params Int worker
	:params Int workerDelays
	:params Int workerTimeout
	:params Any **kwargs
	
	:return Iterable<Result>
	"""
	
	for jobdesk in jobdesks:
		results = None
		jobdeskName = snakeCase( jobdesk.name )
		jobdeskKeysets = jobdesk.keysets
		if jobdeskName not in kwargs or jobdeskName in kwargs and not kwargs[jobdeskName]:
			continue
		jobdeskValue = kwargs[jobdeskName]
		if isinstance( jobdeskValue, Str ) and jobdesk.pattern is not None:
			jobdeskMatched = jobdesk.pattern.search( jobdeskValue \
				if not isinstance( jobdeskValue, str ) \
				else \
					f"{jobdeskValue}" \
				if jobdeskValue is not None else \
					"" 
			)
			if jobdeskMatched is None:
				Logging.error( "Invalid option value for --\x1b[1;38;5;189m{}", jobdeskName.replace( "\x5f", "\x2d" ) )
				if jobdesk.syntax is not None:
					Logging.error( "Usage option --\x1b[1;38;5;189m{}=\x1b[1;38;5;147m{}", jobdeskName.replace( "\x5f", "\x2d" ), jobdesk.syntax, close=1 )
				exit( 1 )
			jobdeskMatches = jobdeskMatched.groupdict()
		else:
			jobdeskMatches = {}
			if jobdeskKeysets:
				jobdeskMatches[list( jobdeskKeysets.keys() )[0]] = jobdeskValue
		if isinstance( jobdesk.requires, list ) and all( isinstance( r, Jobdesk.Require ) for r in jobdesk.requires ):
			for jobdeskRequire in jobdesk.requires:
				jobdeskNameRequire = snakeCase( jobdeskRequire.name )
				jobdeskKeyset = jobdeskRequire.keyset
				if jobdeskNameRequire in kwargs and kwargs[jobdeskNameRequire]:
					jobdeskMatches[jobdeskKeyset] = kwargs[jobdeskNameRequire]
		jobdeskParams = {}
		for jobdeskKeyset in jobdeskKeysets:
			if jobdeskKeyset not in jobdeskMatches or jobdeskMatches[jobdeskKeyset] is None:
				jobdeskParams[jobdeskKeyset] = None
				continue
			try:
				jobdeskTyping = jobdeskKeysets[jobdeskKeyset]
				jobdeskParams[jobdeskKeyset] = jobdeskMatches[jobdeskKeyset]
				if jobdeskParams[jobdeskKeyset] is None:
					continue
				if isinstance( jobdesk.escapes, list ):
					for escape in jobdesk.escapes:
						if isinstance( jobdeskParams[jobdeskKeyset], Str ):
							jobdeskParams[jobdeskKeyset] = jobdeskParams[jobdeskKeyset].replace( f"\\{escape}", escape )
				if jobdeskTyping in [ dict, Dict, list, List ]:
					try:
						jobdeskParams[jobdeskKeyset] = decoder( jobdeskParams[jobdeskKeyset] )
					except JSONDecodeError as e:
						raise ValueError( jobdeskKeyset, e )
				elif isinstance( jobdeskTyping, list ):
					if bool in jobdeskKeysets[jobdeskKeyset]:
						Logging.error( "The Boolean convertion can't use in multiple convertion value", close=1 )
					for jobdeskType in jobdeskKeysets[jobdeskKeyset]:
						if jobdeskType is int:
							if jobdeskParams[jobdeskKeyset] is not None and isinstance( jobdeskParams[jobdeskKeyset], str ) and jobdeskParams[jobdeskKeyset].isnumeric():
								jobdeskParams[jobdeskKeyset] = jobdeskType( jobdeskParams[jobdeskKeyset] )
							elif jobdeskParams[jobdeskKeyset] is not None and isinstance( jobdeskParams[jobdeskKeyset], int ):
								jobdeskParams[jobdeskKeyset] = jobdeskParams[jobdeskKeyset]
				elif isinstance( jobdeskTyping, type ):
					if jobdeskTyping is bool:
						jobdeskParams[jobdeskKeyset] = jobdeskParams[jobdeskKeyset]
						if jobdeskParams[jobdeskKeyset].isnumeric():
							jobdeskParams[jobdeskKeyset] = int( jobdeskParams[jobdeskKeyset] )
						elif jobdeskParams[jobdeskKeyset].lower() == "false":
							jobdeskParams[jobdeskKeyset] = -0
						elif jobdeskParams[jobdeskKeyset].lower() == "true":
							jobdeskParams[jobdeskKeyset] = +1
						jobdeskParams[jobdeskKeyset] = bool( jobdeskParams[jobdeskKeyset] )
					elif jobdeskTyping in [ dict, Dict, list, List ]:
						jobdeskParams[jobdeskKeyset] = decoder( jobdeskParams[jobdeskKeyset] )
						if jobdeskTyping in [ list, List ] and isinstance( jobdeskParams[jobdeskKeyset], dict ):
							jobdeskParams[jobdeskKeyset] = list( jobdeskParams[jobdeskKeyset].values() )
					elif not isinstance( jobdeskParams[jobdeskKeyset], jobdeskTyping ):
						jobdeskParams[jobdeskKeyset] = jobdeskTyping( jobdeskParams[jobdeskKeyset] )
				elif callable( jobdeskTyping ) is True:
					jobdeskParams[jobdeskKeyset] = jobdeskTyping( jobdeskParams[jobdeskKeyset] )
				else:
					Logging.error( "Failed convert value keyset {} into with {}", jobdeskKeyset, jobdeskTyping, close=1 )
			except TypeError as e:
				Logging.error( "Uncaught ValueError: {}", "\x0a".join( format_exception( e ) ) )
				Logging.error( "Cannot convert value type of \"{}\" with {}", jobdeskKeyset, jobdeskTyping.__name__.title(), close=1 )
			except ValueError as e:
				Logging.error( "Uncaught ValueError: {}", "\x0a".join( format_exception( e ) ) )
				Logging.error( "Invalid \"{}\" value, value type must be type {}", jobdeskKeyset, jobdeskTyping.__name__.title(), close=1 )
		jobdeskThread = jobdesk.thread
		jobdeskExecute = jobdesk.execute
		if jobdeskThread is None:
			results = jobdeskExecute( **jobdeskParams )
		elif jobdeskThread is ThreadExecutor:
			jobdeskThreadName = "Executing {execute}"
			if not jobdesk.dataset:
				Logging.error( "Cannot executute {}, unknown target dataset", jobdeskExecute, close=1 )
			jobdeskDatasetName = jobdesk.dataset
			jobdeskDatasetValue = jobdeskParams[jobdeskDatasetName]
			if isinstance( jobdeskDatasetValue, int ):
				jobdeskDatasetValue = list( i for i in range( jobdeskDatasetValue ) )
			elif isinstance( jobdesk, str ):
				jobdeskDatasetValue = [jobdeskDatasetValue]
			if jobdeskDatasetName not in jobdeskParams or not jobdeskParams[jobdeskDatasetName] or not isinstance( jobdeskParams[jobdeskDatasetName], Iterable ):
				Logging.error( "Cannot execute {}, dataset target does not iterable", jobdeskExecute, close=1 )
			if isinstance( jobdesk.message, Jobdesk.Message ):
				if jobdesk.message.name:
					jobdeskThreadName = jobdesk.message.name
			jobdeskFormats = { "execute": jobdeskExecute, **jobdeskParams }
			del jobdeskParams[jobdeskDatasetName]
			results = ThreadExecutor(
				name=jobdeskThreadName.format( **jobdeskFormats ),
				callback=lambda value, thread: jobdeskExecute(
					value, thread=thread, **jobdeskParams
				),
				dataset=jobdeskDatasetValue,
				sleepy=sleepy,
				worker=worker,
				workerDelays=workerDelays,
				workerTimeout=workerTimeout
			)
		elif jobdeskThread is ThreadRunner:
			jobdeskLoading = "Executing {execute}"
			jobdeskSuccess = None
			if isinstance( jobdesk.message, Jobdesk.Message ):
				if jobdesk.message.loading:
					jobdeskLoading = jobdesk.message.loading
				if jobdesk.message.success:
					jobdeskSuccess = jobdesk.message.success
			jobdeskThread = ThreadRunner(
				target=lambda: jobdeskExecute( **jobdeskParams, thread=1 ),
				success=jobdeskSuccess,
				loading=jobdeskLoading.format(
					execute=jobdeskExecute,
					**jobdeskParams
				)
			)
			if jobdeskThread.exception is not None:
				exception = jobdeskThread.exception
				Logging.error( "{}: {}", typeof( exception ), "\x0d".join( format_exception( exception ) ), close=1 )
			results = jobdeskThread.returns
		else:
			Logging.error( "Unhandled executor runner {}", jobdeskThread, close=1 )
		if results is not None:
			yield Result( operation=jobdeskName, values=results )
	...

def ThreadExecutor( name:Str, callback:Callable, dataset:List[Any], sleepy:Int=1, worker:Int=2, workerDelays:Int=10, workerTimeout:Int=120, *args:Any, **kwargs:Any ) -> List[Any]:
	
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
	
	results:List[Any] = []
	with ThreadPoolExecutor( max_workers=worker ) as executor:
		futures:list[Future] = []
		Logging.info( "Building Thread Pool Executor with {} workers for {}", worker, name, start="\x0d" )
		try:
			for count, data in enumerate( dataset ):
				Logging.info( "Starting thread for {}", name, start="\x0d", thread=count+1 )
				futures.append( executor.submit( callback, data, *args, thread=count+1, **kwargs ) )
				sleep( workerDelays if ( count +1 ) % worker == 0 else sleepy )
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
							Logging.info( "{}", messages, end="\x20", start="\x0d", thread=count+1 )
							sleep( 0.1 )
					...
				...
			Logging.info( "A total of {} worker threads have been completed", len( futures ), start="\x0d" )
			Logging.info( "ThreadPoolExecutor for {} stoped", name, start="\x0d" )
			results = list( future.result() for future in futures )
		except BaseException as e:
			if isinstance( e, KeyboardInterrupt ):
				executor.shutdown()
				Logging.info( "ThreadPoolExecutor has been shuting down", start="\x0a" )
			else:
				Logging.error( "Uncaught {}: {}", typeof( e ), format_exc(), start="\x0d" )
			Logging.info( "Program has ben stopped", start="\x0a", close=1 )
		...
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
				Logging.info( "{}", messages, end="\x20", start="\x0d", thread=i )
				sleep( 0.1 )
		Logging.info( "{}", success if success is not None else loading, end="\x0a", start="\x0d" )
		return thread
	except BaseException as e:
		if isinstance( e, KeyboardInterrupt ):
			Logging.info( "Program has been stopped", start="\x0a", close=1 )
		else:
			Logging.error( "Uncaught {}: {}", type( e ).__name__, format_exc(), start="\x0d", close=1 )
	return None
	...
