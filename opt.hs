import System.IO
import Data.WAVE
import Data.List
import Data.List.Split
import Data.Int

import System.Process
import Control.Concurrent
import System.Exit


main = do
   h <- openFile "song.wav" ReadMode
   wav <- hGetWAVE h
   let samples = waveSamples wav
--   return samples
   return (take 2646000 samples) -- 60 second chunk, the program crashes otherwise

-- Currently only takes the left (?) channel data into consideration
--p :: [Int] -> [Int]
p xs = [x | x <- map (\x -> head x) xs]

diff :: [WAVESample] -> WAVESample

-- Since we're passing one partition, just take the front and back half by reversing
-- the list ('partition') we passed
diff xs = n0 - n1
   where n0 = sum (take 735 xs)
         n1 = sum (take 735 (reverse xs))


eL :: [WAVESample] -> [WAVESample] -- What did eL stand for again?
eL xs
   | length xs <= 0 = []
   | otherwise = [diff (take 1470 xs)] ++ (eL (drop 1470 xs))
