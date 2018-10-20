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

   let leftChan = lChan samples
   --let imps = (s' leftChan)
   return leftChan
   --let imp = --filter (>350000) (map abs (listImpulses samples))
   --let imp = listImpulses samples
   --return imp



lChan :: [[WAVESample]] -> [WAVESample]
lChan cs = [l | l <- map (\x -> head x) cs]

--rChan :: [a] -> a
--rChan cs = [r | r <- map (\x -> last x) cs]

--s' :: [WAVESample] -> [Integer]
s' [] = []
s' xs = [d'] ++ s' (drop 1470 xs)
  where d' = diff x - diff y
        x = take 735 xs
        y = take 735 (drop 735 xs)
--s' a = [sum (take 2 a)] ++ (s' (drop 2 a))

--diff :: [Integer] -> Integer
diff [] = 0
diff xs = foldl' (+) 0 xs-- ++ (diff (drop 2 xs))
  --where d' = (take 1 xs) - (take 1 (drop 1 xs))

listImp xs = findIndices (> 350000) xs


-- My list is all the differences along with where they happen
--listFImp xs = [(f, d) | >


--[d'] ++ (listImpulses (drop 1470 xs))
--listImpulses xs = [((h' - t') `div` 5000), link] ++ (listImpulses (drop 1470 xs))

--listImpulses :: [[WAVESample]] -> [WAVESample]
