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




def generate_corpus( txt ):
	corpus = {}

	lines = txt.splitlines()

	total_word_id = 0

	for line_id in range( len( lines ) ):
		line = lines[ line_id ]
		words = line.split()
		
		for word_id in range( len( words ) ):
			word = words[word_id].lower()
			
			word = word.replace( ".", "" )
			word = word.replace( ",", "" )
			
			
			if word not in corpus:
				corpus[word] = []
			
			corpus[word].append( (total_word_id, word_id, line_id ) )
			
			total_word_id += 1
	
	return corpus

	

def find_matches( corpus, word ):

	out = []
	for entry in corpus.keys():
		if (word is entry) or (word in entry):
			out.append( entry )

	sorted_out = sorted( out, key = lambda w: w.index( word ) )
	
	return sorted_out
			
def generate_sets( start, rest ):
	if len( rest ) < 1:
		return [start]
	out = []
	
	for entry in rest[0]:
		#print entry
		new_start = start + [entry]
		out.extend( generate_sets( new_start, rest[1:] ) )

	return out



class Cirrina( object ):
	def __init__( self, text = None ):
		self.corpus = {}
		if text:
			self.process(text)
	
	def process( self, text ):
		self.corpus = generate_corpus( text )
	
	def __call__( self, words, result_type = "lines" ):
		matches = {}
		
		for word in words:
			matches[word] = find_matches( self.corpus, word ) 
		
		forest = []
		for word in words:
			forest.append( matches[word] )
		
		searchsets = [ tuple(s) for s in generate_sets( [], forest ) ]
		results = []
		
		for searchset in searchsets:
			entries = [ self.corpus[word] for word in searchset ]
			
			areas = generate_sets( [], entries )
			
			spans = []
			for area in areas:
				wps = [ w[0] for w in area ]
				spans.append( (area, max(wps) - min(wps) ) )
			
			sorted_spans = sorted( spans, key = lambda x:x[1] )
			results.append( (searchset,  sorted_spans[0]) )

		sorted_results = sorted( results, key = lambda x:x[1][1] )
		
		if len( sorted_results ) < 1:
			return []
		
		smallest_result = sorted_results[0]
		
		if result_type == "words":
			wordspan = [r[1] for r in smallest_result[1][0] ]
			#return tuple(wordspan)
			return (min(wordspan), max(wordspan))
		
		linespan = [r[2] for r in smallest_result[1][0] ]
		return (min(linespan), max(linespan))
	
			
