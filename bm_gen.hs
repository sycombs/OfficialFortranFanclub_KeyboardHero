import System.IO
import Data.WAVE
import Data.List
import Data.String

import System.Posix.Temp

import System.Process -- I took out parallel processing, put it back in
import Control.Parallel

-- TODO
-- 1) Filter the results so that we have a minimum threshold
-- 2) Get results from the right (?) channel as well, we only get them from the left channel ATM


main = do
   h <- openFile "song.wav" ReadMode
   wav <- getWAVEFile "song.wav"
   let samples = waveSamples wav

   let l  = lChan samples
   let r  = rChan samples

   let lImps = listImp (s' l)
   let rImps = listImp (s' r)

   return lImps

lChan :: [[WAVESample]] -> [WAVESample]
lChan cs = [l | l <- map (\x -> head x) cs]

rChan :: [[WAVESample]] -> [WAVESample]
rChan cs = [r | r <- map (\x -> last x) cs]

--s' :: [WAVESample] -> [Integer]
s' [] = []
s' xs = [d'] ++ s' (drop 1470 xs)
  where d' = (diff x - diff y) `div` 5000
        p = take 1470 xs
        x = take 735 p
        y = drop 735 p
        --x = take 735 xs
        --y = take 735 (drop 735 xs)
--s' a = [sum (take 2 a)] ++ (s' (drop 2 a))

--diff :: [Integer] -> Integer
diff [] = 0
diff xs = foldl' (+) 0 xs

listImp xs = map (\x -> x * 1470) (findIndices (> 300000) (map abs xs))
--findIndices (> 300000) (map abs xs)



-- My list is all the differences along with where they happen
--listFImp xs = [(f, d) | >


--[d'] ++ (listImpulses (drop 1470 xs))
--listImpulses xs = [((h' - t') `div` 5000), link] ++ (listImpulses (drop 1470 xs))

--listImpulses :: [[WAVESample]] -> [WAVESample]
