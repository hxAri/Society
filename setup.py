#!/usr/bin/env bash

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
from setuptools import setup


def reader( fname:Str, encoding:Str="utf-8" ) -> Str:
	fread = ""
	with open( fname, "r", encoding=encoding ) as fopen:
		fread = fopen.read()
		fopen.close()
	return fread


if __name__ == "__main__":
	setup(
		name="society",
		version="1.0.0",
		author="Ari Setiawan (hxAri)",
		author_email="hxari@proton.me",
		maintainer="Ari Setiawan (hxAri)",
		maintainer_email="hxari@proton.me",
		description="Society is an Open-Source project for doing various things related to Facebook, e.g Login, Generate Access Token, Media Downloader, etc.",
		long_description=reader( "README.md" ),
		long_description_content_type="md",
		packages=['society'],
		package_dir={ "": "src" },
		provides=filter( 
			lambda value: len( value ) >= 1, 
			reader( "requirements.txt" ).splitlines() 
		),
		url="https://github.com/hxAri/Society",
		download_url="https://github.com/hxAri/Society/archive/refs/heads/main.tar.gz",
		license="GNU General Public License v3",
		classifiers=[
			"Environment :: CLI Environment",
			"Intended Audience :: Developers",
			"Licence :: GNU",
			"Natural Language :: English",
			"Operating System :: OS Independent",
			"Topic :: Internet :: Command Line Interface",
			"Topic :: Software Development :: Libraries",
			"Programming Language :: Python",
			"Programming Language :: Python :: 3",
			"Programming Language :: Python :: 3.10",
			"Programming Language :: Python :: 3.11",
			"Programming Language :: Python :: 3.12",
			"Programming Language :: Python :: 3 :: Only"
		]
	)
