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
from dateutil.relativedelta import relativedelta
from pytz import timezone
from random import choice
from re import IGNORECASE, MULTILINE, S
from re import compile, match, split, sub as substr
from sys import exit as systemExit
from time import sleep
from typing import Any, MutableMapping, MutableSequence, Union
from urllib.parse import urlparse, parse_qs as queryparse

from society.patterns import Username
from society.typing.properties import Properties


def colorize( string:Str, base:Str=None ) -> Str:
	
	"""
	Automatic colorize the given stringa
	
	:params Str string
	:params Str base
		The string base color ansi code
	
	:return Str
	"""
	
	result = ""
	strings = [ x for x in split( r"((?:\x1b|\033)\[[0-9\;]+m)", string ) if x != "" ]
	regexps = {
		"number": {
			"pattern": r"(?P<number>\b(?:\d+)\b)",
			"colorize": "\x1b[1;38;5;61m{}{}"
		},
		"define": {
			"handler": lambda matched: substr( r"(\.|\-){1,}", lambda m: "\x1b[1;38;5;69m{}\x1b[1;38;5;111m".format( m.group() ), matched.group( 0 ) ),
			"pattern": r"(?P<define>(?:@|\$)[a-zA-Z0-9_\-\.]+)",
			"colorize": "\x1b[1;38;5;111m{}{}"
		},
		"symbol": {
			"pattern": r"(?P<symbol>\\|\:|\*|-|\+|/|&|%|=|\;|,|\.|\?|\!|\||<|>|\~){1,}",
			"colorize": "\x1b[1;38;5;69m{}{}"
		},
		"bracket": {
			"pattern": r"(?P<bracket>\{|\}|\[|\]|\(|\)){1,}",
			"colorize": "\x1b[1;38;5;214m{}{}"
		},
		"boolean": {
			"pattern": r"(?P<boolean>\b(?:False|True|None)\b)",
			"colorize": "\x1b[1;38;5;199m{}{}"
		},
		"typedef": {
			"pattern": r"(?P<typedef>\b(?:ABCMeta|AbstractSet|Annotated|Any|AnyStr|ArithmeticError|AssertionError|AsyncContextManager|AsyncGenerator|AsyncIterable|AsyncIterator|AttributeError|Awaitable|BaseException|BinaryIO|BlockingIOError|BrokenPipeError|BufferError|ByteString|BytesWarning|Callable|ChainMap|ChildProcessError|ClassVar|Collection|Concatenate|ConnectionAbortedError|ConnectionError|ConnectionRefusedError|ConnectionResetError|Container|ContextManager|Coroutine|Counter|DefaultDict|DeprecationWarning|Deque|Dict|EOFError|Ellipsis|EncodingWarning|EnvironmentError|Exception|False|FileExistsError|FileNotFoundError|Final|FloatingPointError|ForwardRef|FrozenSet|FutureWarning|Generator|GeneratorExit|Generic|GenericAlias|Hashable|IO|IOError|ImportError|ImportWarning|IndentationError|IndexError|InterruptedError|IsADirectoryError|ItemsView|Iterable|Iterator|KT|Key|KeyError|KeyboardInterrupt|KeysView|List|Literal|LookupError|Mapping|MappingView|Match|MemoryError|MethodDescriptorType|MethodWrapperType|ModuleNotFoundError|MutableMapping|MutableSequence|MutableSet|NameError|NamedTuple|NamedTupleMeta|NewType|NoReturn|None|NotADirectoryError|NotImplemented|NotImplementedError|OSError|Optional|OrderedDict|OverflowError|ParamSpec|ParamSpecArgs|ParamSpecKwargs|Pattern|PendingDeprecationWarning|PermissionError|ProcessLookupError|Protocol|RecursionError|ReferenceError|ResourceWarning|Reversible|RuntimeError|RuntimeWarning|Sequence|Set|Sized|StopAsyncIteration|StopIteration|SupportsAbs|SupportsBytes|SupportsComplex|SupportsFloat|SupportsIndex|SupportsInt|SupportsRound|SyntaxError|SyntaxWarning|SystemError|SystemExit|T|TabError|Text|TextIO|TimeoutError|True|Tuple|Type|TypeAlias|TypeError|TypeGuard|TypeVar|TypedDict|UnboundLocalError|UnicodeDecodeError|UnicodeEncodeError|UnicodeError|UnicodeTranslateError|UnicodeWarning|Union|UserWarning|Val|alueError|ValuesView|Warning|WrapperDescriptorType|ZeroDivisionError|abs|abstractmethod|aiter|all|anext|any|ascii|bin|[bB]ool|breakpoint|bytearray|bytes|callable|cast|chr|classmethod|collections|compile|complex|contextlib|copyright|credits|delattr|dict|dir|divmod|enumerate|eval|exec|exit|filter|final|[fF]loat|format|frozenset|functools|getattr|globals|hasattr|hash|help|hex|id|input|[iI]nt|(?:[iI]o|IO)|isinstance|issubclass|iter|len|license|list|locals|map|max|memoryview|min|next|[oO]bject|oct|open|operator|ord|overload|pow|print|property|quit|range|re|repr|reversed|round|[sS]et|setattr|slice|sorted|staticmethod|[sS]tr|sum|super|sys|[tT]uple|type|types|vars|zip)\b)",
			"colorize": "\x1b[1;38;5;213m{}{}"
		},
		"linked": {
			"handler": lambda matched: substr( r"(\\|\:|\*|-|\+|/|&|%|=|\;|,|\.|\?|\!|\||<|>|\~){1,}", lambda m: "\x1b[1;38;5;69m{}\x1b[1;38;5;43m".format( m.group() ), matched.group( 0 ) ),
			"pattern": r"(?P<linked>\bhttps?://[^\s]+)",
			"colorize": "\x1b[1;38;5;43m\x1b[4m{}{}"
		},
		"version": {
			"handler": lambda matched: substr( r"([\d\.]+)", lambda m: "\x1b[1;38;5;190m{}\x1b[1;38;5;112m".format( m.group() ), matched.group( 0 ) ),
			"pattern": r"(?P<version>\b[vV][\d\.]+\b)",
			"colorize": "\x1b[1;38;5;112m{}{}"
		},
		"society": {
			"pattern": r"(?P<society>\b(?:[sS][oO][cC][iI][eE][tT][yY])\b)",
			"colorize": "\x1b[1;38;5;111m{}{}"
		},
		"comment": {
			"pattern": r"(?P<comment>\#[^\n]*)",
			"colorize": "\x1b[1;38;5;250m{}{}"
		},
		"string": {
			"handler": lambda matched: substr( r"(?<!\\)(\\\"|\\\'|\\`|\\r|\\t|\\n|\\s)", lambda m: "\x1b[1;38;5;208m{}\x1b[1;38;5;220m".format( m.group() ), matched.group( 0 ) ),
			"pattern": r"(?P<string>(?<!\\)(\".*?(?<!\\)\"|\'.*?(?<!\\)\'|`.*?(?<!\\)`))",
			"colorize": "\x1b[1;38;5;220m{}{}"
		}
	}
	if not isinstance( base, Str ):
		base = "\x1b[0m"
	try:
		last = base
		escape = None
		pattern = "(?:{})".format( "|".join( regexp['pattern'] for regexp in regexps.values() ) )
		compiles = compile( pattern, MULTILINE|S )
		skipable = []
		for idx, string in enumerate( strings ):
			if idx in skipable:
				continue
			color = match( r"^(?:\x1b|\033)\[([^m]+)m$", string )
			if color is not None:
				index = idx +1
				escape = color.group( 0 )
				last = escape
				try:
					rescape = match( r"(?:\x1b|\033)\[([^m]+)m", strings[index] )
					while rescape is not None:
						skipable.append( index )
						escape += rescape.group( 0 )
						last = rescape.group( 0 )
						index += 1
						rescape = match( r"(?:\x1b|\033)\[([^m]+)m", strings[index] )
				except IndexError:
					break
				if index +1 in skipable:
					index += 1
				skipable.append( index )
			else:
				escape = last
				index = idx
			string = strings[index]
			search = 0
			matched = compiles.search( string, search )
			while matched is not None:
				if matched.groupdict():
					group = None
					groups = matched.groupdict().keys()
					for group in groups:
						if group in regexps and \
							isinstance( regexps[group], MutableMapping ) and \
							isinstance( matched.group( group ), str ):
							colorize = regexps[group]['colorize']
							break
					chars = matched.group( 0 )
					if "rematch" in regexps[group] and isinstance( regexps[group]['rematch'], MutableMapping ):
						pass
					if "handler" in regexps[group] and callable( regexps[group]['handler'] ):
						result += escape
						result += string[search:matched.end() - len( chars )]
						result += colorize.format( regexps[group]['handler']( matched ), escape )
						search = matched.end()
						matched = compiles.search( string, search )
						continue
					result += escape
					result += string[search:matched.end() - len( chars )]
					result += colorize.format( chars, escape )
					search = matched.end()
					matched = compiles.search( string, search )
				else:
					matched = None
			result += escape
			result += string[search:]
	except Exception as e:
		raise e
	return result

def converter( readable:Str ) -> Int:
	
	"""
	Convert human readbale number into Int
	
	:params Str readable
		The human readable number format
	
	:return Int
	"""
	
	pattern = compile( r"^(?P<count>[0-9]+(?:[0-9\.]+)?)\s*(?P<multiple>(?:k|rb|ribu|M|million|jt|juta|B|billion|miliar|T|trillion|triliun))?", IGNORECASE )
	matched = pattern.match( str( readable ) )
	multiples = [
		{ "keys": [ "k", "rb", "ribu" ], "multiple": 1000 },
		{ "keys": [ "m", "ml", "million", "jt", "juta" ], "multiple": 1000000 },
		{ "keys": [ "b", "bl", "billion", "miliar" ], "multiple": 1000000000 },
		{ "keys": [ "t", "tl", "trillion", "triliun" ], "multiple": 1000000000000 }
	]
	if matched is not None:
		groups = matched.groupdict()
		if "multiple" in groups and groups['multiple']:
			try:
				readable = int( groups['count'] )
			except ValueError:
				readable = float( groups['count'] )
			for multiple in multiples:
				if groups['multiple'].lower() in multiple['keys']:
					return int( readable * multiple['multiple'] )
		else:
			readable = groups['count']
	try:
		return int( readable )
	except ValueError:
		...
	return 0

def delays() -> None:
	sleep( choice([ 1.3, 1.6, 1.9, 2, 2.2, 2.4, 2.6 ]) )

def epochmillis( datestr:Str ) -> Int:

	"""
	Convert datetime string into epoch millis

	:params Str datestr

	:return Int
		Timestamp of epoch millis
	"""

	return int( datetime.strptime( datestr, "%Y-%m-%dT%H:%M:%S%z" ).timestamp() * 1000 )

def puts( *values:Any, base:Str="\x1b[0m", end:Str="\x0a", sep:Str="\x20", close:Union[Bool,Int]=False ) -> None:
	
	"""
	Print colorize text into terminal screen
	
	:params Any *values
	:params Str base
		The string base color ansi code
	:params Str end
		The end of line outputs
	:params Str sep
		The value separator
	:params Bool|Int close
		The exit code
	"""
	
	print( *[ colorize( base=base, string=value if isinstance( value, Str ) else repr( value ) ) for value in values ], end=end, sep=sep )
	if close is not False:
		systemExit( close )
	...

def serializeable( value:Any ) -> Bool:
	
	"""
	Return whether if the value is serializable.
	
	:params Any value
	
	:return Bool
	"""
	
	return isinstance( value, ( MutableMapping, MutableSequence, tuple, str, int, float, bool ) ) or value is None

def snakeCase( keyword:Str ) -> Str:

	"""
	Convert Title Case into snake case

	:params Str keyword
	
	:return Str
	"""

	return substr( r"([a-z0-9])([A-Z])", r"\1_\2", substr( r"(.)([A-Z][a-z]+)", r"\1_\2", keyword ) ).lower()

def strftime( format:Str, instance:Union[datetime,float,Int] ) -> Str:

	"""
	Convert datetime or timestamp into formated datetime

	:params Str format
		Date string format
	:params datetime|Float|Int instance
		Datetime or Timestamp want to be convert into datetime string

	:return Str
		Formated datetime
	:raises TypeError
		When the value of parameter is invalid value type
	"""

	if isinstance( instance, ( float, int ) ):
		zone = timezone( Properties.TimeZone )
		try:
			instance = datetime.fromtimestamp( int( instance ), zone )
		except ValueError:
			instance = datetime.fromtimestamp( int( instance / 1000 ), zone )
	if not isinstance( instance, datetime ):
		raise TypeError( "Invalid \"instance\" parameter, value must be type datetime|Float|Int, {} passed".format( typeof( datetime ) ) )
	return instance.strftime( format )

def timestamp( minutes:Int=0, hours:Int=0, days=0, weeks:Int=0, months:Int=0, years:Int=0, tm:Bool=False ) -> Int:
	
	"""
	Timestamp minus generator
	
	:params Int minutes
	:params Int hours
	:params Int days
	:params Int weeks
	:params Int months
	:params Int years
	:params Bool tm
		Return timestamp with *1000
	
	:return Int
		Current timestamp or current timestamp minus time
	"""
	
	zone = timezone( Properties.TimeZone )
	currtime = datetime.now( zone )
	relative = relativedelta( minutes=minutes, hours=hours, months=months, years=years, weeks=weeks, days=days )
	try:
		current = currtime - relative
	except ValueError:
		current = currtime
	if tm is True:
		return int( current.timestamp() * 1000 )
	return int( current.timestamp() )

def typeof( instance:Any ) -> Str:
	if not isinstance( instance, type ):
		instance = type( instance )
	return instance.__name__

def urlparser( url:Str ) -> MutableMapping[Str,Any]:

	"""
	The URL parser

	:params Str url
		The URL want to be parse

	:return MutableMapping<Str, Any>
	"""

	parsed = urlparse( url )
	return {
		"host": parsed.hostname,
		"path": parsed.path[1::] if parsed.path != "" else "/",
		"params": queryparse( parsed.query, keep_blank_values=True ),
		"scheme": parsed.scheme,
		"url": parsed.geturl()
	}

def unameMatcher( url:Str ) -> Str:
	if url is not None:
		matched = Username.search( url )
		if matched is not None:
			username = matched.group( "username" )
			if username == "\x70\x72\x6f\x66\x69\x6c\x65\x2e\x70\x68\x70":
				parsed = urlparser( url )
				return parsed['params']['id'] if not isinstance( parsed['params']['id'], MutableSequence ) else parsed['params']['id'].pop()
			return username
		...
	return None
