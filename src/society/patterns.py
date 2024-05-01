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

from re import IGNORECASE, MULTILINE
from re import compile, Pattern
from typing import List


Hashtag:Pattern[compile] = compile( r"\#(?P<hashtag>[a-zA-Z_](?:[a-zA-Z0-9_\.]*[a-zA-Z0-9_]?)*)", MULTILINE )
""" A Pattern for capture hashtag in the media caption """

Mention:Pattern[compile] = compile( r"\@(?P<mention>[a-zA-Z_](?:[a-zA-Z0-9_\.]*[a-zA-Z0-9_]?)*)", MULTILINE )
""" A Pattern for capture mention in the media caption """

Photos:List[Pattern[compile]] = [
	compile( r"\/(?P<media_asset>[a-zA-Z]+\.[1-9](?:[0-9]+)?)\/(?P<media_id>[1-9](?:[0-9]+)?)", IGNORECASE ),
	compile( r"\bfbid\=(?P<media_id>[1-9](?:[0-9]+)?)\&set\=(?P<media_asset>[a-zA-Z]+\.[1-9](?:[0-9]+)?)" )
]
""" A patterns for capture photo media id and media asset in the url """

Snippet:Pattern[compile] = compile( r"^(?P<access>Publi[ck])(?:\s+.\s+)(?P<member>[0-9]+(?:\s*(?:K|rb)))(?:\s+(?:anggota|members?)?\s*.\s+)(?P<post>(?:[0-9]+)(\+)?)\s+(?:posts?|postingan)\s+(?:per|tiap|setiap)(?:\s*|-)?\s*(?P<time>(?:hour|jam|day|hari|week|minggu|month|bulan|year|tahun)s?)", IGNORECASE )
""" A Pattern for capture group information in the group snippet """

Username:Pattern[compile] = compile( r"^https?://(?:(?:www|web|m|mbasic|[a-zA-Z0-9-]+)\.)?facebook\.com/(?:people/)?(?P<username>[a-zA-Z_](?:[a-zA-Z0-9_\.]*[a-zA-Z0-9_]?)*)", IGNORECASE )
""" A Pattern for capture username in the url """
