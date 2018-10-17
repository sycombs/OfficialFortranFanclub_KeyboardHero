import System.IO
import Data.WAVE
import Data.List

import System.Process -- I took out parallel processing, put it back in
import Control.Parallel

-- TODO
-- 1) Filter the results so that we have a minimum threshold
-- 2) Get results from the right (?) channel as well, we only get them from the left channel ATM

main = do
   h <- openFile "song.wav" ReadMode
   wav <- getWAVEFile "song.wav"
   let samples = waveSamples wav

   let imp = listImpulses samples
   return (length imp)


listImpulses :: [[WAVESample]] -> [WAVESample]

listImpulses [] = []
listImpulses xs = [((h' - t') `div` 5000)] ++ (listImpulses (drop 1470 xs))
   where h' = foldl' (+) 0 [h | h <- map (\a -> head a) (take 735 xs)]
         t' = foldl' (+) 0 [t | t <- map (\b -> last b) (take 735 (drop 735 xs))]
