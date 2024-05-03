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

from builtins import bool as Bool, int as Int, str as Str
from datetime import datetime
from inspect import getframeinfo, stack
from os import get_terminal_size as gts
from pytz import timezone
from random import randint
from typing import Any, Dict, Union

from society.common import puts
from society.storage import BASEPATH, BASEVENV
from society.typing.properties import Properties


CRITICAL:Int = randint( 10, 99 )
DEBUG:Int = randint( 20, 99 )
ERROR:Int = randint( 30, 99 )
FATAL:Int = randint( 40, 99 )
INFO:Int = randint( 50, 99 )
WARNING:Int = randint( 60, 99 )


class Logging:
	
	""" Simple Logging utility """

	COUNTER:Int = 1
	""" Logging counter """
	
	CRITICAL:Int = CRITICAL
	DEBUG:Int = DEBUG
	ERROR:Int = ERROR
	FATAL:Int = FATAL
	INFO:Int = INFO
	WARNING:Int = WARNING

	LEVELS:Dict[Int,Str] = {
		CRITICAL: "C",
		DEBUG: "D",
		ERROR: "E",
		FATAL: "F",
		INFO: "I",
		WARNING: "W"
	}
	""" Logging level aliases """

	DATETIME_FORMAT:Str = "%Y-%m-%d %H:%M:%S"
	""" Logging datetime format """

	PREVIOUS_LENGTH:Int = -1
	""" Previous logging length """

	MESSAGE_FORMAT_COMPLEX:Str = "-- [{level}] -- {datetime} {file}:{func}:{line} {message}"
	MESSAGE_FORMAT_THREAD_COMPLEX:Str = "-- [{level}] -- {datetime} {file}:{func}:{line}:{thread} {message}"
	MESSAGE_FORMAT:Str = "-- [{level}] -- {datetime} {message}"
	MESSAGE_FORMAT_THREAD:Str = "-- [{level}] -- {datetime} {thread} {message}"
	""" Logging message formatter """

	SAVE:Bool = False
	""" Allow logging message save """

	@staticmethod
	def critical( message:Str, *args:Any, start:Str="", end:Str="\x0a", thread:Int=0, close:Union[Bool,Int]=False, **kwargs:Any ) -> None:
		
		"""
		Write critical log into terminal screen.
		
		:params Str message
			The logging message
		:params Any *args
			The logging message position values
		:params Str start
			The prefix of output line
		:params Str end
			The end of output line
		:params Int thread
			Current thread position number
		:params Int close
			Close the program with exit code
		:params Any **kwargs
			The logging message ke values
		
		:return None
		"""
		
		Logging.write( CRITICAL, message, *args, start=start, end=end, thread=thread, close=close, **kwargs )

	@staticmethod
	def debug( message:Str, *args:Any, start:Str="", end:Str="\x0a", thread:Int=0, close:Union[Bool,Int]=False, **kwargs:Any ) -> None:
		
		"""
		Write debug log into terminal screen.
		
		:params Str message
			The logging message
		:params Any *args
			The logging message position values
		:params Str start
			The prefix of output line
		:params Str end
			The end of output line
		:params Int thread
			Current thread position number
		:params Int close
			Close the program with exit code
		:params Any **kwargs
			The logging message ke values
		
		:return None
		"""
		
		Logging.write( DEBUG, message, *args, start=start, end=end, thread=thread, close=close, **kwargs )

	@staticmethod
	def error( message:Str, *args:Any, start:Str="", end:Str="\x0a", thread:Int=0, close:Union[Bool,Int]=False, **kwargs:Any ) -> None:
		
		"""
		Write error log into terminal screen.
		
		:params Str message
			The logging message
		:params Any *args
			The logging message position values
		:params Str start
			The prefix of output line
		:params Str end
			The end of output line
		:params Int thread
			Current thread position number
		:params Int close
			Close the program with exit code
		:params Any **kwargs
			The logging message ke values
		
		:return None
		"""
		
		Logging.write( ERROR, message, *args, start=start, end=end, thread=thread, close=close, **kwargs )

	@staticmethod
	def fatal( message:Str, *args:Any, start:Str="", end:Str="\x0a", thread:Int=0, close:Union[Bool,Int]=False, **kwargs:Any ) -> None:
		
		"""
		Write fatal log into terminal screen.
		
		:params Str message
			The logging message
		:params Any *args
			The logging message position values
		:params Str start
			The prefix of output line
		:params Str end
			The end of output line
		:params Int thread
			Current thread position number
		:params Int close
			Close the program with exit code
		:params Any **kwargs
			The logging message ke values
		
		:return None
		"""
		
		Logging.write( FATAL, message, *args, start=start, end=end, thread=thread, close=close, **kwargs )

	@staticmethod
	def info( message:Str, *args:Any, start:Str="", end:Str="\x0a", thread:Int=0, close:Union[Bool,Int]=False, **kwargs:Any ) -> None:
		
		"""
		Write info log into terminal screen.
		
		:params Str message
			The logging message
		:params Any *args
			The logging message position values
		:params Str start
			The prefix of output line
		:params Str end
			The end of output line
		:params Int thread
			Current thread position number
		:params Int close
			Close the program with exit code
		:params Any **kwargs
			The logging message ke values
		
		:return None
		"""
		
		Logging.write( INFO, message, *args, start=start, end=end, thread=thread, close=close, **kwargs )

	@staticmethod
	def warning( message:Str, *args, start:Str="", end:Str="\x0a", thread:Int=0, close:Union[Bool,Int]=False, **kwargs:Any ) -> None:
		
		"""
		Write warning log into terminal screen.
		
		:params Str message
			The logging message
		:params Any *args
			The logging message position values
		:params Str start
			The prefix of output line
		:params Str end
			The end of output line
		:params Int thread
			Current thread position number
		:params Int close
			Close the program with exit code
		:params Any **kwargs
			The logging message ke values
		
		:return None
		"""
		
		Logging.write( WARNING, message, *args, start=start, end=end, thread=thread, close=close, **kwargs )

	@staticmethod
	def write( level:Int, message:Str, *args:Any, start:Str="", end:Str="\x0a", thread:Int=0, close:Union[Bool,Int]=False, **kwargs:Any ) -> None:
		
		"""
		Write log into terminal screen.
		
		:params Int level
			The logging level
		:params Str message
			The logging message
		:params Any *args
			The logging message position values
		:params Str start
			The prefix of output line
		:params Str end
			The end of output line
		:params Int thread
			Current thread position number
		:params Int close
			Close the program with exit code
		:params Any **kwargs
			The logging message ke values
		
		:return None
		"""
		
		color = ""
		stacks = stack()
		tiframe = getframeinfo( stacks[( 1 if len( stacks )>= 3 else 1 )][0] )
		currtime = datetime.now( timezone( Properties.TimeZone ) )
		current = currtime.strftime( Logging.DATETIME_FORMAT )
		if level in Logging.LEVELS:
			status = Logging.LEVELS[level] if not isinstance( thread, str ) and thread <= 0 else thread
			match level:
				case Logging.CRITICAL: ...
				case Logging.DEBUG: ...
				case Logging.ERROR:
					color = "\x1b[1;31m"
				case Logging.FATAL: ...
				case Logging.INFO: ...
				case Logging.WARNING: ...
				case _:
					...
			...
		else:
			status = "U"
		if not isinstance( thread, str ):
			if thread <= 0:
				formatter = Logging.MESSAGE_FORMAT if Properties.Environment is not None and Properties.Environment == "production" else Logging.MESSAGE_FORMAT_COMPLEX
			else:
				formatter = Logging.MESSAGE_FORMAT_THREAD if Properties.Environment is not None and Properties.Environment == "production" else Logging.MESSAGE_FORMAT_THREAD_COMPLEX
		else:
			formatter = Logging.MESSAGE_FORMAT  if Properties.Environment is not None and Properties.Environment == "production" else Logging.MESSAGE_FORMAT_COMPLEX
			status = thread
		message = message if not args and not kwargs else message.format( *args, **kwargs )
		messages = message.splitlines()
		messages[0] = "".join([ color, messages[0], "\x1b[0m" ])
		outputs = formatter.format(
			message="\x0a".join( messages ),
			file=tiframe.filename.replace( f"{BASEPATH}/", "" ),
			func=tiframe.function,
			line=tiframe.lineno,
			datetime=current,
			thread=thread,
			color=color,
			level=status
		)
		outputs = outputs \
			.replace( BASEPATH, "{society}" ) \
			.replace( BASEVENV, "{virtual}" )
		length = len( outputs.splitlines().pop() )
		if Logging.PREVIOUS_LENGTH > length and start == "\x0d":
			if Logging.PREVIOUS_LENGTH <= gts().columns:
				outputs += "\x20" * ( Logging.PREVIOUS_LENGTH - length )
			else:
				start = ""
		Logging.PREVIOUS_LENGTH = length
		if Logging.SAVE is True:
			Logging.COUNTER += 1
			fmode = "w" if Logging.COUNTER >= 10000 else "+a"
			ftime = currtime.strftime( "%Y-%B-%d" )
			fname = f"history/logging/society - {ftime}.log"
			with open( fname, fmode ) as fopen:
				fopen.write( f"{outputs}\n" )
				fopen.close()
		puts( f"{start}{outputs}", end=end, close=close )
		if close is not False:
			exit( close )

	...	
