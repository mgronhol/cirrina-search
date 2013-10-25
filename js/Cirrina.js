var Cirrina = function( text ){
	this.corpus = {};
	
	this.process = (function(self){ return function(text){
		
		var lines = text.split( "\n" );
		
		var current_word_count = 0;
		for( var i = 0 ; i < lines.length ; i += 1 ){
			var cleaned_line = lines[i]
						.replace("\.", " ")
						.replace("\,", " ")
						.replace("-", " ")
						.replace("(", " ")
						.replace(")", " ")
						.replace("!", " ");
			console.log( cleaned_line );
						
			var words = cleaned_line.split( " " );
				
			for( var j = 0 ; j < words.length ; j += 1 ){
				
				var word = words[j].toLowerCase();
				var entry = {
					line: i,
					word: j,
					total: current_word_count
					};
				
				if( word.length < 1 ){ continue; }
				
				if( (word in self.corpus) ){
					self.corpus[word].push( entry );
					} 
				else {
					self.corpus[word] = [entry];
					}
				
				
				current_word_count += 1;
				}
			
			}
		
		
		console.log( self.corpus );
		}; })(this);
	
	
	this.find_matches = (function(self){ return function(word){
		var out = [];
		for( var entry in self.corpus ){
			if( (entry.indexOf(word) >= 0) || (word.indexOf(entry) >=0 ) ){
				
				out.push( entry );
				
				}
			}
		return out;
		}; })(this);
	
	this.generate_sets = (function(self){ return function(start, rest){
		var out = [];
		if( rest.length < 1 ){
			return [start];
			}
		
		for( var i = 0 ; i < rest[0].length ; i += 1 ){
			var new_start = start.concat( [rest[0][i]] );
			out = out.concat( self.generate_sets( new_start, rest.slice(1) ) );
			}
		
		return out;
		};})(this);
	
	this.search = (function(self){ return function(terms, lines){
		
		var matches = [];
		
		for( var i = 0 ; i < terms.length ; i += 1 ){
			matches.push( self.find_matches( terms[i] ) );
			}
		
		var searchsets = self.generate_sets( [], matches );
		
		var results = [];
		
		for( var i = 0 ; i < searchsets.length ; i += 1 ){
			var entries = [];
			
			for( var j = 0 ; j < searchsets[i].length ; j += 1 ){
				entries.push( self.corpus[ searchsets[i][j]] );
				}
			
			var areas = self.generate_sets( [], entries );
			
			var spans = [];
			
			for( var j = 0 ; j < areas.length ; j += 1 ){
				var wps = [];
				for( var k = 0 ; k < areas[j].length ; k += 1 ){
					//wps.push( areas[j][k] );
					//console.log( areas[j][k] );
					wps.push( areas[j][k].total );
					}
				spans.push( [areas[j], Math.max.apply(null, wps) - Math.min.apply(null, wps)] );
				
				}
				
			spans.sort(function(a,b){
				return a[1] - b[1];
				});
			
			results.push( [searchsets[i], spans[0]] );
			
			}
		
		results.sort( function(a,b){
			return a[1][1] - b[1][1];
			});
		
		var result = results[0];
		
		var linespan = [];
		
		for( var i = 0 ; i < result[1][0].length ; i += 1 ){
			linespan.push( result[1][0][i].line );
			}
		
		if( typeof lines == "undefined" ){
			return {start: Math.min.apply( null, linespan ), stop: Math.max.apply( null, linespan ) };
			}
		else {
			var out = [];
			for( var i = Math.min.apply( null, linespan ); i <= Math.max.apply( null, linespan ) ; i += 1 ){
				out.push( lines[i] );
				}
			return out;
			}
		
		}; })(this);
	
	}
