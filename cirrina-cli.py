#!/usr/bin/env python
#
# The MIT License (MIT)
# 
# Copyright (c) 2013 Markus Gronholm
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys, Cirrina

def wraplines( txt ):
	lines = txt.splitlines()
	out = ""
	current = ""
	for line in lines:
		words = line.split()
		for word in words:
			current += word+ " "
			if len( current ) > 76:
				out += current + "\n"
				current = ""
		out += current + "\n"
		current = ""
	if len( current ) > 0:
		out += current + "\n"
	return out




txt = ""

with open( sys.argv[1], 'rU' ) as handle:
	txt = handle.read()

txt = wraplines(txt)

text_lines = txt.splitlines()


search = Cirrina.Cirrina( txt )

try:
	while True:
		entry = raw_input( "> " ).strip()
		parts = [entry]
		if " " in entry:
			parts = [part.strip() for part in entry.split()]
		
		linespan = search( parts )
		print linespan
		print ""
		for row in range( linespan[0]-1, linespan[1] + 2 ):
			print text_lines[row]
		print ""
except KeyboardInterrupt:
	pass
