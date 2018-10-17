--a = [[1, 2], [1, 2], [1, 2], [1, 2]]

import System.IO
import Data.WAVE
import Data.List
import Data.Int

import System.Process
import Control.Parallel
import System.Exit

-- 7791616
-- ^ Current song length
-- Filter the results!

main = do
   h <- openFile "song.wav" ReadMode
   wav <- getWAVEFile "song.wav"
   let samples = waveSamples wav
   let song_length = (length samples)

   let halfLength = (song_length `div` 2)
   let firstHalf  = take halfLength samples
   let secondHalf = drop halfLength samples

   let quartLength = halfLength `div` 2 -- Or is song_length / 4 better?
 
   --let q1 = take quartLength firstHalf
--   let q2 = drop quartLength firstHalf
--   let q3 = take quartLength secondHalf
--   let q4 = drop quartLength secondHalf

--   leftChannel only ATM

--   let imp1 = (listImpulses (firstHalf `div` 2)) `par` (listImpulses ( `div` 2))
   let imp1 = (listImpulses (take quartLength firstHalf)) `par` (listImpulses (drop quartLength firstHalf))
   let imp2 = (listImpulses (take quartLength secondHalf)) `par` (listImpulses (drop quartLength secondHalf))

   print (length imp1)


--listImpulses :: [WAVESample] -> [WAVESample]

listImpulses [] = []
listImpulses xs = [((h' - t') `div` 5000)] ++ (listImpulses (drop 1470 xs))
   where h' = foldl' (+) 0 [h | h <- map (\a -> head a) (take 735 xs)]
         t' = foldl' (+) 0 [t | t <- map (\b -> last b) (take 735 (drop 735 xs))]
