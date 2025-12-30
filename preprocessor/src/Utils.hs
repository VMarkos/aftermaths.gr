{-# LANGUAGE OverloadedStrings #-}

module Utils where

import Data.Text
import Text.HTML.Scalpel

-- Data types

data MathContent
    = InlineMath String
    | DisplayMath String

-- Utilities

scraper :: [Char] -> IO (Maybe Text)
scraper url = scrapeURL url mainContent
    where
        mainContent :: Scraper Text Text
        mainContent =  ("div" @: [hasClass "entry-content"]) mathContents

        mathContents :: Scraper Text MathContent
        mathContents = chroots () inlineMath <|> displayMath

        mathContent :: Scraper Text
        
        inlineMath :: Scraper Text InlineMath
        inlineMath = do
            src     <- 

        displayMath :: Scraper Text DisplayMath
