{-# LANGUAGE OverloadedStrings #-}

module Utils where

import          Data.Text
import          Text.HTML.Scalpel

scraper :: [Char] -> IO (Maybe Text)
scraper url = scrapeURL url mainContent
    where
        mainContent :: Scraper Text Text
        mainContent = text ("div" @: [hasClass "entry-content"])
