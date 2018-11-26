
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
import Control.Exception

main = do
  -- Load JSON to read parameters
  wav <- getWAVEFile "song.wav"
  let imps = abs.head <$> waveSamples wav :: [WAVESample]
  return $ findImpulse 1 imps
  --encodeFile "beatmap.json" (findImpulse 1 imps)

newtype GameParam = GameParam {
   file_name :: String
   } deriving (Generic, Show) -- Just using show to make sure this works

instance FromJSON GameParam


data MyException = ThisException | ThatException
    deriving Show

instance Exception MyException

boundsCheck :: (Double, Double, Double) -> Double
boundsCheck (dimVal, dMin, dMax)
  | dimVal < dMin = dMin
  | dimVal > dMax = dMax
  | otherwise = dimVal

findImpulse :: Integral a => Double -> [a] -> [Impulse]
findImpulse _ []  = []
findImpulse i xs  = (differenceFinder actFrame p1) ++ (findImpulse (i + 1) p2)
  where p1        = take 1470 xs
        p2        = drop 1470 xs
        actFrame  = (i * 1470) + 1

differenceFinder :: Integral a => Double -> [a] -> [Impulse]
differenceFinder frame ss
  | difference > 39000 = [impulse]
  | otherwise  = []
  where partition_1 = foldl' (+) 0 $ take 735 ss
        partition_2 = foldl' (+) 0 $ drop 735 ss
        difference  = (abs $ partition_1 - partition_2) `div` 50000
        impulse     = processImpulse $ frame :+ (fromIntegral difference)


processImpulse :: Complex Double -> Impulse
processImpulse compDoub = Impulse actFrame rb osu
  where actFrame        = toInteger $ ceiling $ realPart compDoub
        rb              = RB $ genButton actFrame
        osu             = genCircle compDoub


{- Button Generation Functions -}

genButton :: Integer -> Char
genButton d
  | m == 0    = 'U'
  | m == 1    = 'D'
  | m == 2    = 'L'
  | otherwise = 'R'
  where m = (abs d) `mod` 4


genCircle :: Complex Double -> Osu
genCircle d = Osu xPos yPos -- Drag and not drag data?
  where width  = 725 -- w = Width - 75 (Width and height from game board file)
        height = 525 -- h = Height - 75
        xPos   = (toInteger radius) `mod` width
        yPos   = (toInteger radius) `mod` height
        radius = ceiling $ magnitude d
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
  x         :: Integer,
  y         :: Integer
  } deriving (Generic, Show)

-- data Osu = Osu {
--   x         :: Double,
--   y         :: Double
--   } deriving (Generic, Show)

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
