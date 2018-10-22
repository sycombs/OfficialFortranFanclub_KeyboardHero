{-|
Module      : Main
-}

module Main where

import System.IO
import Data.WAVE
import Data.List
import Data.Int

-- | Main aaaa
main = do
   h <- openFile "song.wav" ReadMode
   wav <- getWAVEFile "song.wav"
   let lImps = (putStr . pOut 1) (impulse 1 $ splitList $ waveSamples wav)
   return lImps

-- | As used in bm_gen, we have the types WAVESamples -> [WAVESample]
splitList ::
          [[s]]  -- ^ Input: List of lists of type s
          -> [s] -- ^ Return: The first element of each sublist
splitList cs = [samp | samp <- map (\x -> head x) cs]

{- |
  Impulse
  aaa
-}
impulse ::
        Int               -- ^ Input: Counts increments
        -> [Int32]        -- ^ Input: The[Int32]
        -> [(Int, Int32)] -- ^ [(Int, Int32)]

impulse f xs = if (d > 35000) then [(f * 1470 + 1, d)] ++ nImp
  else [] ++ nImp
  where d = (abs $ a - b) `div` 5000
        a = foldl' (+) 0 (take 735 xs)
        b = foldl' (+) 0 (take 735 $ drop 735 xs)
        nImp = impulse (f + 1) (drop 1470 xs)

-- | pOut
pOut ::
     Int                     -- ^ Int
     -> [(Int, WAVESample)]  -- ^ (Int, WAVESample)
     -> String               -- ^ String

pOut n [] = []
pOut n (f:fs) = (line1 ++ line2) ++ pOut (n + 1) fs
  where line1 = "Note #" ++ (show n) ++ " - Activation Frame: " ++ show (fst f) ++ "\n"
        line2 = "{'Up': " ++ u ++ ", 'Down': " ++ d ++ ", 'Left': " ++ l ++ ", 'Right': " ++ r ++ "}\n"
        r = if ((350000 <= x) && (x < 375000)) then "1" else "0"
        l = if ((375000 <= x) && (x < 400000)) then "1" else "0"
        d = if ((400000 <= x) && (x < 425000)) then "1" else "0"
        u = if (x >= 425000) then "1" else "0"
        x = snd f
