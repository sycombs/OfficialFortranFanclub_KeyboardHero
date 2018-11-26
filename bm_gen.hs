
{-# LANGUAGE DeriveGeneric     #-}

module BM_Gen where

import Data.Aeson
import Data.List
import Data.Int
import Data.WAVE
import GHC.Generics
import Data.Complex
import System.IO
import System.Exit
-- import qualified Data.ByteString.Lazy as BL

main = do
  -- Load JSON to read parameters
  wav <- getWAVEFile "song.wav"
  let imps = abs.head <$> waveSamples wav :: [WAVESample]
  encodeFile "beatmap.json" (findImpulse 1 imps)

newtype GameParam = GameParam {
   file_name :: String
   } deriving (Generic, Show) -- Just using show to make sure this works

instance FromJSON GameParam


boundsCheck :: (Double, Double, Double) -> Double
boundsCheck (dimVal, dMin, dMax)
  | dimVal < dMin = dMin
  | dimVal > dMax = dMax
  | otherwise = dimVal

findImpulse :: Integral a => Double -> [a] -> [Impulse]
findImpulse _ []  = []
findImpulse i xs  = (differenceFinder f p1) ++ (findImpulse (i + 1) p2)
  where p1 = take 1470 xs
        p2 = drop 1470 xs
        f  = (i * 1470) + 1

differenceFinder :: Integral a => Double -> [a] -> [Impulse]
differenceFinder frame ss
  | d > 39000 = [i]
  | otherwise = [ ]
  where a = foldl' (+) 0 $ take 735 ss
        b = foldl' (+) 0 $ drop 735 ss
        d = (abs $ a - b) `div` 50000
        i = processImpulse $ frame :+ (fromIntegral d)


processImpulse :: Complex Double -> Impulse
processImpulse c = Impulse a r o
  where a = toInteger $ ceiling $ realPart c
        r = RB $ genButton a
        o = genCircle c


{- Button Generation Functions -}

genButton :: Integer -> Char
genButton d -- And hold / not hold?
  | m == 0    = 'U'
  | m == 1    = 'D'
  | m == 2    = 'L'
  | otherwise = 'R'
  where m = (abs d) `mod` 4


genCircle :: Complex Double -> Osu
genCircle d = Osu xPos yPos -- Drag and not drag data?
  where width  = 725 -- w = Width - 75 (Width and height from game board file)
        height = 525 -- h = Height - 75
        xPos   = boundsCheck ((radius * (cos theta)), minVal,  width)
        yPos   = boundsCheck ((radius * (sin theta)), minVal, height)
        radius = magnitude d
        theta  = phase d
        minVal = 50

{- Data Types -}

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

{- JSON Encoders / Decoders -}

instance ToJSON Impulse where
  toEncoding = genericToEncoding defaultOptions
instance FromJSON Impulse

instance ToJSON RB where
  toEncoding = genericToEncoding defaultOptions
instance FromJSON RB

instance ToJSON Osu where
  toEncoding = genericToEncoding defaultOptions
instance FromJSON Osu
