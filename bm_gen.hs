import System.IO
import Data.WAVE
import Data.List
import Data.Int

main = do
   h <- openFile "song.wav" ReadMode
   wav <- getWAVEFile "song.wav"
   let samples = waveSamples wav
   let lChanData = splitChan samples
   let lImps = impulse 1 lChanData
   let p = putStr (pOut 1 lImps)
   p


splitChan :: WAVESamples -> [WAVESample]
splitChan cs = [samp | samp <- map (\x -> head x) cs]

-- Impulse is a function that adds a frame f' to a list of frames
-- where the predicate is that the difference
--        abs (sum [f_1 .. f_736] - sum [f_737 .. f_1471])
-- exceeds some minimum threshold, and f' is equal to f_736

impulse f [] = []
impulse f xs =
   if (d > t) then [(f * 1470 + 1, d)] ++ i'
   else [] ++ i'
   where d = (abs (a - b)) `div` 5000
         a = foldl' (+) 0 (take 735 xs)
         b = foldl' (+) 0 (take 735 (drop 735 xs))
         i' = impulse (f + 1) (drop 1470 xs)
         t = 350000


pOut :: Int -> [(Int, WAVESample)] -> String
pOut n [] = []
pOut n (f:fs) = (line1 ++ line2) ++ (pOut (n + 1) fs)
   where line1 = "Note #" ++ (show n) ++ " - Activation Frame: " ++ show (fst f) ++ "\n"
         line2 = "{'Up': " ++ u ++ ", 'Down': " ++ d ++ ", 'Left': " ++ l ++ ", 'Right': " ++ r ++ "}\n"
         r = if ((350000 <= x) && (x < 375000)) then "1" else "0"
         l = if ((375000 <= x) && (x < 400000)) then "1" else "0"
         d = if ((400000 <= x) && (x < 425000)) then "1" else "0"
         u = if (x >= 425000) then "1" else "0"
         x = snd f
