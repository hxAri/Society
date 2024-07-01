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
from concurrent.futures import CancelledError, Future, ThreadPoolExecutor, TimeoutError
from json import loads as decoder, JSONDecodeError
from time import sleep
from traceback import format_exc, format_exception
from typing import Any, Callable, Dict, Iterable, List, Literal, MutableMapping, MutableSequence, TypeVar as Var

from society.common import snakeCase, typeof
from society.logging import Logging
from society.typing.builtins import Val
from society.typing.jobdesk import Jobdesk
from society.typing.result import Result
from society.typing.threading import Threading


Args = Var( "Args" )
""" Arguments """

Kwargs = Var( "Kwargs" )
""" Key Arguments """


def Executor( jobdesks:MutableSequence[Jobdesk], sleepy:Int=1, worker:Int=2, workerDelays:Int=10, **kwargs:Any ) -> Iterable[Result[Literal['operation'],Val]]:
	
	"""
	Automation Command Line Execution
	
	:params MutableSequence<Jobdesk> jobdesks
	:params Int sleepy
	:params Int worker
	:params Int workerDelays
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
				Logging.error( "Terminated", close=1 )
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
				if jobdeskTyping in [ dict, Dict, list, List, MutableMapping, MutableSequence ]:
					try:
						jobdeskParams[jobdeskKeyset] = decoder( jobdeskParams[jobdeskKeyset] )
					except JSONDecodeError as e:
						raise ValueError( jobdeskKeyset, e ) from e
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
					elif jobdeskTyping in [ dict, Dict, list, List, MutableMapping, MutableSequence ]:
						jobdeskParams[jobdeskKeyset] = decoder( jobdeskParams[jobdeskKeyset] )
						if jobdeskTyping in [ list, List, MutableMapping, MutableSequence ] and isinstance( jobdeskParams[jobdeskKeyset], dict ):
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
			executes = ThreadExecutor(
				name=jobdeskThreadName.format( **jobdeskFormats ),
				callback=jobdeskExecute,
				dataset=jobdeskDatasetValue,
				sleepy=sleepy,
				worker=worker,
				workerDelays=workerDelays,
				**jobdeskParams
			)
			results = list( execute for execute in executes )
		elif jobdeskThread is ThreadRunner:
			jobdeskLoading = "Executing {execute}"
			jobdeskSuccess = None
			if isinstance( jobdesk.message, Jobdesk.Message ):
				if jobdesk.message.loading:
					jobdeskLoading = jobdesk.message.loading
				if jobdesk.message.success:
					jobdeskSuccess = jobdesk.message.success
			jobdeskThread = ThreadRunner(
				target=jobdeskExecute,
				success=jobdeskSuccess,
				loading=jobdeskLoading.format(
					execute=jobdeskExecute,
					**jobdeskParams
				),
				thread=1,
				**jobdeskParams
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

def ThreadExecutor( name:Str, callback:Callable[[Any,Args,Kwargs,Int],Any], dataset:Iterable[Any], sleepy:Int=1, worker:Int=2, workerDelays:Int=10, *args:Any, **kwargs:Any ) -> Iterable[Any]:
	
	"""
	Short ThreadPoolExecutor
	
	:params Str name
	:params Callable<<Any,Args,Kwargs>,Any> callback
	:params Iterable<Any> dataset
	:params Int sleepy
	:params Int worker
	:params Int workerDelays
	:params Any *args
	:params Any **kwargs
	
	:return Iterable<Any>
	"""
	
	results:MutableSequence[Any] = []
	futures:list[Future] = []
	with ThreadPoolExecutor( thread_name_prefix=name, max_workers=worker ) as executor:
		Logging.info( "Building ThreadPoolExecutor with {} workers for {}", worker, name, start="\x0d", thread="T" )
		try:
			for count, data in enumerate( dataset ):
				Logging.info( "Starting thread for {}", name, start="\x0d", thread=count+1 )
				futures.append( executor.submit( callback, data, *args, thread=count+1, **kwargs ) )
				sleep( workerDelays if ( count +1 ) % worker == 0 else sleepy )
			while futures and all( future.done() for future in [ *futures ] ) is False:
				for count, future in enumerate([ *futures ]):
					if future.running():
						loading = f"Future thread worker T<{count+1}> is running..."
						length = len( loading )
						position = -1
						for i in "\\|/-" * 16:
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
								messagePrefix = loading[:position-1]
								messageSuffix = loading[position:]
								messages = "".join([
									messagePrefix, 
									messageChar, 
									messageSuffix
								])
							Logging.info( "{}", messages, end="\x20", start="\x0d", thread=i )
							sleep( 0.1 )
						try:
							throwned = future.exception( 0.4 )
							if isinstance( throwned, BaseException ):
								Logging.error( "Future thread worker {} is raised {}: {}", count+1, typeof( throwned ), "\x0a".join( format_exception( throwned ) ), thread=count+1, start="\x0d" )
								Logging.error( "Future thread worker {} is deleted from futures", count+1, thread=count+1, start="\x0d" )
								del futures[count]
						except CancelledError:
							...
						except TimeoutError:
							...
						finally:
							...
						...
					...
				...
			...
		except BaseException as e:
			if isinstance( e, KeyboardInterrupt ):
				Logging.error( "ThreadPoolExecutor has been shuting down", start="\x0a", thread="T" )
				executor.shutdown()
			else:
				Logging.error( "{}: {}", typeof( e ), "\x0a".join( format_exception( e ) ), start="\x0d", thread="T" )
			...
		...
		Logging.warning( "ThreadPoolExecutor enumerating futures", start="\x0d", thread="T" )
		for i, future in enumerate( futures ):
			if future.cancelled() is True:
				Logging.warning( "Future thread worker T<{}> is cancelled", i+1, start="\x0d", thread=i+1 )
				continue
			try:
				yield future.result( 1 )
				results.append( future )
			except CancelledError:
				Logging.warning( "Future thread worker T<{}> is cancelled", i+1, start="\x0d", thread=i+1 )
			except TimeoutError:
				Logging.warning( "Future thread worker T<{}> is timeout", i+1, start="\x0d", thread=i+1 )
			except BaseException as e:
				Logging.error( "{}: {}", typeof( e ), "\x0a".join( format_exception( e ) ), start="\x0d", thread=i+1 )
			...
		Logging.info( "A total of {} worker threads have been completed", len( results ), start="\x0d", thread="T" )
		Logging.info( "ThreadPoolExecutor for {} stoped", name, start="\x0d", thread="T" )
	results = None
	futures = None

def ThreadRunner( loading:Str, success:Str=None, group=None, target:Callable[[Args,Kwargs],Any]=None, name=None, *args:Any, **kwargs:Any ) -> Threading:
	
	"""
	Short Threading
	
	:params Str loading
	:params Str success
	:params Any group
	:params Callable<<Args,Kwargs>,Any> target
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
			for i in "\\|/-" * 16:
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
