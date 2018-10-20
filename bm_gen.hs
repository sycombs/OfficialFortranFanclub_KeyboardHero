import System.IO
import Data.WAVE
import Data.List
import Data.String
import System.Posix.Temp

main = do
   h <- openFile "song.wav" ReadMode
   wav <- getWAVEFile "song.wav"
   return (waveSamples wav)

-- Print Impulses to a file
--pImps

splitChan cs = [samp | samp <- map (\x -> head x) cs]

part [] = []
part xs = [d'] ++ part (drop 1470 xs)
  where d' = (x - y) `div` 5000
        x = foldl' (+) 0 (take 735 xs)
        y = foldl' (+) 0 (take 735 (drop 735 xs))

-- Get Impulses
gImps xs = map (\x -> x * 1470) (findIndices (> 350000) (map abs xs))
