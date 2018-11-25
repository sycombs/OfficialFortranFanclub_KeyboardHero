
{-# LANGUAGE DeriveGeneric #-}

module BM_Gen where

import Data.Aeson
import Data.List
import Data.Int
import Data.WAVE
import GHC.Generics
import Data.Complex
import System.IO

main = do
   wav <- getWAVEFile "song.wav"
   -- Add getting the song length and an error check?
   let imps = abs.head <$> waveSamples wav :: [WAVESample]
   encodeFile "beatmap.json" (fImp 1 imps)

boundsCheck :: (Double, Double, Double) -> Double
boundsCheck (dimVal, dMin, dMax)
  | dimVal   < dMin = dMin
  | dimVal > dMax = dMax
  | otherwise = dimVal

--fImp :: Int -> [WAVESample] -> [Impulse]
fImp _ []  = []
fImp i xs  = (diff f p1) ++ (fImp (i + 1) p2)
  where p1 = take 1470 xs
        p2 = drop 1470 xs
        f  = (i * 1470) + 1

diff :: Integral a => Double -> [a] -> [Impulse]
diff f ss
  | d > 39000 = [i]
  | otherwise = [ ]
  where a = foldl' (+) 0 $ take 735 ss
        b = foldl' (+) 0 $ drop 735 ss
        d = (abs $ a - b) `div` 50000
        i = pImp $ f :+ (fromIntegral d)


pImp :: Complex Double -> Impulse
pImp c = Impulse a r o
  where a = toInteger $ ceiling $ realPart c
        r = RB $ genButton a
        o = genCircle c

genButton :: Integer -> Char
genButton d -- And hold / not hold?
  | m == 0    = 'U'
  | m == 1    = 'D'
  | m == 2    = 'L'
  | otherwise = 'R'
  where m = (abs d) `mod` 4


-- !! Neither width or height actually do anything right now
genCircle :: Complex Double -> Osu
genCircle d = Osu xPos yPos -- Drag and not drag data?
  where width  = 725 -- w = Width - 75 (Width and height from game board file)
        height = 525 -- h = Height - 75
        xPos   = radius * (cos theta)
        yPos   = radius * (sin theta)
        radius = magnitude d
        theta  = phase d
        minVal = 50

-- setCoordinate :: Double -> Double -> Double -> Double
-- setCoordinate dimVal dMin dMax = b

data Impulse = Impulse {
  act_frame :: Integer,
  rb        :: RB,
  osu       :: Osu
  } deriving (Generic, Show)

newtype RB = RB {
  button :: Char
  } deriving (Generic, Show)

data Osu = Osu {
  x         :: Double,
  y         :: Double
  } deriving (Generic, Show)
--life_span :: Int,
--  pos_delta :: Double


instance ToJSON Impulse where
  toEncoding = genericToEncoding defaultOptions
instance FromJSON Impulse

instance ToJSON RB where
  toEncoding = genericToEncoding defaultOptions
instance FromJSON RB

instance ToJSON Osu where
  toEncoding = genericToEncoding defaultOptions
instance FromJSON Osu
