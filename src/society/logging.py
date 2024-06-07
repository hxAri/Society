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
from inspect import getframeinfo, stack
from os import get_terminal_size as gts
from random import randint
from threading import current_thread as CurrentThread, main_thread as MainThread
from typing import Any, Final, MutableMapping, Union

from society.common import puts, strftime, timestamp
from society.constants import BASEPATH, BASEVENV
from society.storage import Storage
from society.typing.properties import Properties


class Logging:
	
	""" Simple Logging utility """
	
	Counter:Int = 1
	""" Logging counter """
	
	Critical:Final[Int] = randint( 10, 99 )
	""" Logging Critical Level """
	
	Debug:Final[Int] = randint( 20, 99 )
	""" Logging Debug Level """
	
	Error:Final[Int] = randint( 30, 99 )
	""" Logging Error Level """
	
	Fatal:Final[Int] = randint( 40, 99 )
	""" Logging Fatal Level """
	
	Info:Final[Int] = randint( 50, 99 )
	""" Logging Info Level """
	
	Warning:Final[Int] = randint( 60, 99 )
	""" Logging Warning Level """
	
	Levels:MutableMapping[Int,Str] = {}
	""" Logging level aliases """
	
	Levels[Critical] = "C"
	Levels[Debug] = "D"
	Levels[Error] = "E"
	Levels[Fatal] = "F"
	Levels[Info] = "I"
	Levels[Warning] = "W"
	
	DateTimeFormat:Str = "%Y-%m-%d %H:%M:%S"
	""" Logging datetime format """
	
	PreviousLength:Int = -1
	""" Previous logging length """
	
	MessageFormatComplex:Str = "-- [{level}] -- {datetime} {file}:{func}:{line} {message}"
	MessageFormatThreadComplex:Str = "-- [{level}] -- {datetime} {file}:{func}:{line}:{thread} {message}"
	MessageFormat:Str = "-- [{level}] -- {datetime} {message}"
	MessageFormatThread:Str = "-- [{level}] -- {datetime} {thread} {message}"
	""" Logging message formatter """
	
	Store:Bool = False
	""" Allow logging store messages log """
	
	@staticmethod
	def critical( message:Str, *args:Any, start:Str="", end:Str="\x0a", thread:Union[Int,Str]=0, close:Union[Bool,Int]=False, **kwargs:Any ) -> None:
		
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
		:params Int|Str thread
			Current thread position number
		:params Int close
			Close the program with exit code
		:params Any **kwargs
			The logging message ke values
		
		:return None
		"""
		
		Logging.write( Logging.Critical, message, *args, start=start, end=end, thread=thread, close=close, **kwargs )
	
	@staticmethod
	def debug( message:Str, *args:Any, start:Str="", end:Str="\x0a", thread:Union[Int,Str]=0, close:Union[Bool,Int]=False, **kwargs:Any ) -> None:
		
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
		:params Int|Str thread
			Current thread position number
		:params Int close
			Close the program with exit code
		:params Any **kwargs
			The logging message ke values
		
		:return None
		"""
		
		if Properties.Environment == "development":
			Logging.write( Logging.Debug, message, *args, start=start, end=end, thread=thread, close=close, **kwargs )
		...
	
	@staticmethod
	def error( message:Str, *args:Any, start:Str="", end:Str="\x0a", thread:Union[Int,Str]=0, close:Union[Bool,Int]=False, **kwargs:Any ) -> None:
		
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
		:params Int|Str thread
			Current thread position number
		:params Int close
			Close the program with exit code
		:params Any **kwargs
			The logging message ke values
		
		:return None
		"""
		
		Logging.write( Logging.Error, message, *args, start=start, end=end, thread=thread, close=close, **kwargs )
	
	@staticmethod
	def fatal( message:Str, *args:Any, start:Str="", end:Str="\x0a", thread:Union[Int,Str]=0, close:Union[Bool,Int]=False, **kwargs:Any ) -> None:
		
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
		:params Int|Str thread
			Current thread position number
		:params Int close
			Close the program with exit code
		:params Any **kwargs
			The logging message ke values
		
		:return None
		"""
		
		Logging.write( Logging.Fatal, message, *args, start=start, end=end, thread=thread, close=close, **kwargs )
	
	@staticmethod
	def info( message:Str, *args:Any, start:Str="", end:Str="\x0a", thread:Union[Int,Str]=0, close:Union[Bool,Int]=False, **kwargs:Any ) -> None:
		
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
		:params Int|Str thread
			Current thread position number
		:params Int close
			Close the program with exit code
		:params Any **kwargs
			The logging message ke values
		
		:return None
		"""
		
		Logging.write( Logging.Info, message, *args, start=start, end=end, thread=thread, close=close, **kwargs )
	
	@staticmethod
	def warning( message:Str, *args, start:Str="", end:Str="\x0a", thread:Union[Int,Str]=0, close:Union[Bool,Int]=False, **kwargs:Any ) -> None:
		
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
		:params Int|Str thread
			Current thread position number
		:params Int close
			Close the program with exit code
		:params Any **kwargs
			The logging message ke values
		
		:return None
		"""
		
		Logging.write( Logging.Warning, message, *args, start=start, end=end, thread=thread, close=close, **kwargs )
	
	@staticmethod
	def write( level:Int, message:Str, *args:Any, start:Str="", end:Str="\x0a", thread:Union[Int,Str]=0, close:Union[Bool,Int]=False, **kwargs:Any ) -> None:
		
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
		:params Int|Str thread
			Current thread position number
		:params Int close
			Close the program with exit code
		:params Any **kwargs
			The logging message ke values
		
		:return None
		"""
		
		color = ""
		status = "U"
		stacks = stack()
		currtime = strftime( Logging.DateTimeFormat, timestamp() )
		threading = CurrentThread() is not MainThread()
		if level in Logging.Levels:
			status = Logging.Levels[level]
			match level:
				case Logging.Critical: ...
				case Logging.Debug: ...
				case Logging.Error:
					color = "\x1b[1;31m"
				case Logging.Fatal: ...
				case Logging.Info: ...
				case Logging.Warning: ...
				case _:
					...
			...
		position = 0
		if isinstance( thread, Int ) and thread >= 1 or \
		   isinstance( thread, Str ) and thread:
			position = 3 if len( stacks )>= 4 else 2
			# position = 2 if len( stacks ) >= 3 else 1
			if threading is True:
				position = 2 if len( stacks )>= 4 else 1
			formatter = Logging.MessageFormatThread \
				if Properties.Environment is not None and \
				   Properties.Environment == "production" else \
				Logging.MessageFormatThreadComplex
			if isinstance( thread, Str ):
				status = "T"
			...
		else:
			position = 2 if len( stacks ) >= 3 else 1
			formatter = Logging.MessageFormat \
				if Properties.Environment is not None and \
				   Properties.Environment == "production" else \
				Logging.MessageFormatComplex
		tiframe = getframeinfo( stacks[position][0] )
		message = message if not args and not kwargs else message.format( *args, **kwargs )
		messages = message.splitlines()
		messages[0] = "".join([ color, messages[0], "\x1b[0m" ])
		outputs = formatter.format(
			message="\x0a".join( messages ),
			file=tiframe.filename.replace( f"{BASEPATH}/", "" ),
			func=tiframe.function,
			line=tiframe.lineno,
			datetime=currtime,
			thread=thread,
			color=color,
			level=status
		)
		outputs = outputs \
			.replace( BASEPATH, "{society}" ) \
			.replace( BASEVENV, "{virtual}" )
		length = len( outputs.splitlines().pop() )
		if Logging.PreviousLength > length and start == "\x0d":
			if Logging.PreviousLength <= gts().columns:
				outputs += "\x20" * ( Logging.PreviousLength - length )
			else:
				start = ""
		Logging.PreviousLength = length
		if Logging.Store is True:
			Logging.Counter += 1
			fmode = "w" if Logging.Counter >= 10000 else "+a"
			ftime = currtime.strftime( "%Y-%B-%d" )
			fname = f"history/logging/society - {ftime}.log"
			Storage.touch( fname, f"{outputs}\n", fmode )
		puts( f"{start}{outputs}", end=end, close=close )
	
	...	
