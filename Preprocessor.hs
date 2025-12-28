module Preprocessor where

-- Get the contents of <div class="entry-content"></div> element from a WP Post
extractEntryContent :: [Char] -> [Char]
extractEntryContent text = entryContentHelper text False

-- Helper function to get the contents of <div class="entry-content"></div>
	entryContentHelper [Char] Bool -> [Char]
	entryContentHelper [] _			= []
	entryContentHelper (_:xs) False = entryContentHelper xs False
