{-|
Module      : Main
-}

module Main where

import System.IO
import Data.WAVE
import Data.List
import Data.Int

-- | main makes all the necessary function calls to generate a beatmap using
-- (currently) a single audio channel and when called with the proper commands
-- via the console (listed below)
--
-- >>> ghc bm_gen.hs -e "main" > "outputfilename.txt"
--
main = do
   h <- openFile "song.wav" ReadMode
   wav <- getWAVEFile "song.wav"
   let lImps = (putStr . pOut 1) (impulse 1 $ splitList $ waveSamples wav)
   return lImps

-- | splitList
-- Returns the first element in a list of lists
--
-- WAVESamples -> [WAVESample]
--
-- >>> splitList audioSamples
--
splitList :: [[s]] -> [s]
splitList cs = [samp | samp <- map (\x -> head x) cs]

-- |
-- Returns a list 'impulses'
--
-- Two adjacent 735 subsamples are compared and if
-- the difference between them passes an (currently arbitrarily chosen by me)
-- threshold it adds the the frame in which it occurs and the magnitude of the
-- difference
--
-- >>> impulse counter [DATA.WAVESample] -> [(Int, WAVESample)]
--
impulse :: Int -> [Int32] -> [(Int, Int32)]

impulse f xs = if (d > 35000) then [(f * 1470 + 1, d)] ++ nImp
  else [] ++ nImp
  where d = (abs $ a - b) `div` 5000
        a = foldl' (+) 0 (take 735 xs)
        b = foldl' (+) 0 (take 735 $ drop 735 xs)
        nImp = impulse (f + 1) (drop 1470 xs)

-- |
-- Formats data in a such a way as to be useable by OFF Keyboard Hero's game_logic.py.
-- Our current format is:
--
-- > Note #n - Activation Frame: f
-- > {'Up': u, 'Down': d, 'Left': l, 'Right': r}
--
--

pOut :: Int -> [(Int, WAVESample)] -> String

pOut n [] = []
pOut n (f:fs) = (line1 ++ line2) ++ pOut (n + 1) fs
  where line1 = "Note #" ++ (show n) ++ " - Activation Frame: " ++ show (fst f) ++ "\n"
        line2 = "{'Up': " ++ u ++ ", 'Down': " ++ d ++ ", 'Left': " ++ l ++ ", 'Right': " ++ r ++ "}\n"
        r = if ((350000 <= x) && (x < 375000)) then "1" else "0"
        l = if ((375000 <= x) && (x < 400000)) then "1" else "0"
        d = if ((400000 <= x) && (x < 425000)) then "1" else "0"
        u = if (x >= 425000) then "1" else "0"
        x = snd f
