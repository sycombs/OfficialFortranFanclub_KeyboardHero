import System.IO
import Data.WAVE
import Data.List
import Data.Int

main = do
   h <- openFile "song.wav" ReadMode
   wav <- getWAVEFile "song.wav"
   let lImps = (putStr . pOut 1) (impulse 1 $ splitChan $ waveSamples wav)
   return lImps

splitChan :: WAVESamples -> [WAVESample]
splitChan cs = [samp | samp <- map (\x -> head x) cs]

impulse f [] = []
impulse f xs =
   if (d > 35000) then [(f * 1470 + 1, d)] ++ i'
   else [] ++ i'
   where d = (abs $ a - b) `div` 5000
         a = foldl' (+) 0 (take 735 xs)
         b = foldl' (+) 0 (take 735 $ drop 735 xs)
         i' = impulse (f + 1) (drop 1470 xs)

pOut :: Int -> [(Int, WAVESample)] -> String
pOut n [] = []
pOut n (f:fs) = (line1 ++ line2) ++ pOut (n + 1) fs
   where line1 = "Note #" ++ (show n) ++ " - Activation Frame: " ++ show (fst f) ++ "\n"
         line2 = "{'Up': " ++ u ++ ", 'Down': " ++ d ++ ", 'Left': " ++ l ++ ", 'Right': " ++ r ++ "}\n"
         u = if ((350000 <= x) && (x < 375000)) then "1" else "0"
         d = if ((375000 <= x) && (x < 400000)) then "1" else "0"
         l = if ((400000 <= x) && (x < 425000)) then "1" else "0"
         r = if (x >= 425000) then "1" else "0"
         x = snd f
