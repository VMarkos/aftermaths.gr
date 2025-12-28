{-# LANGUAGE OverloadedStrings #-}

module Main where

import Data.Text.IO as TIO
import Utils (scraper)

main :: IO ()
main = do
    result <- scraper "https://aftermathsgr.wordpress.com/2024/08/04/%cf%84%ce%b1-%ce%bf%ce%bb%cf%85%ce%bc%cf%80%ce%b9%ce%b1%ce%ba%ce%ac-%cf%85%ce%b4%cf%81%ce%bf%ce%b8%ce%b5%cf%81%ce%bc%ce%b9%ce%ba%ce%ad%cf%82-%cf%83%cf%85%ce%bd%ce%b1%cf%81%cf%84%ce%ae%cf%83%ce%b5/"
    case result of
        Just x  -> TIO.writeFile "preprocessed_test.html" x
        Nothing -> print "Did not find any match"

-- URL = "https://aftermathsgr.wordpress.com/2024/08/04/%cf%84%ce%b1-%ce%bf%ce%bb%cf%85%ce%bc%cf%80%ce%b9%ce%b1%ce%ba%ce%ac-%cf%85%ce%b4%cf%81%ce%bf%ce%b8%ce%b5%cf%81%ce%bc%ce%b9%ce%ba%ce%ad%cf%82-%cf%83%cf%85%ce%bd%ce%b1%cf%81%cf%84%ce%ae%cf%83%ce%b5/"
