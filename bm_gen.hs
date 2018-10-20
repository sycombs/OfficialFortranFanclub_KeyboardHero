import System.IO
import Data.WAVE
import Data.List

main = do
   h <- openFile "song.wav" ReadMode
   wav <- getWAVEFile "song.wav"
   return (waveSamples wav)

splitChan cs = [samp | samp <- map (\x -> head x) cs]

part [] = []
part xs = [d'] ++ part (drop 1470 xs)
  where d' = ( (foldl' (+) 0 x) - (foldl' (+) 0 y) ) `div` 5000
        x = take 735 xs
        y = take 735 (drop 735 xs)

lImps xs = map (\x -> x * 1470) (findIndices (> 350000) (map abs xs))
