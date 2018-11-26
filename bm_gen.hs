
{-# LANGUAGE DeriveGeneric     #-}

module BM_Gen where

-- ghc bm_gen.hs -e "main"

import Data.Aeson
import Data.List
import Data.Int
import Data.WAVE
import GHC.Generics
import Data.Complex
import System.IO

main = do
  wav <- getWAVEFile "song.wav"
  let imps = abs.head <$> waveSamples wav :: [WAVESample]
  encodeFile "beatmap.json" (findImpulse 1 imps)

boundsCheck :: (Integer, Integer, Integer) -> Integer
boundsCheck (dimVal, dMin, dMax)
  | dimVal < dMin = dMin
  | dimVal > dMax = dMax
  | otherwise     = dimVal

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
        rb              = RB $ 'A'
        osu             = genCircle compDoub

{- Button Generation Functions -}

-- genButton :: Integer -> Char
-- genButton d
--   | s >= 1250 = 'U'
--   | s >= 900  = 'D'
--   | s >= 500  = 'L'
--   | otherwise = 'R'
--   where s = d `div` 5000

genCircle :: Complex Double -> Osu
genCircle d = Osu xPos yPos -- Drag and not drag data?
  where width  = 725 -- w = Width - 75 (Width and height from game board file)
        height = 525 -- h = Height - 75
        radius = ceiling $ magnitude d
        xTrans = (toInteger radius) `mod` width
        yTrans = (toInteger radius) `mod` height
        xPos   = boundsCheck (xTrans, 50, width) -- We use 50 as a min because of
        yPos   = boundsCheck (yTrans, 50, height) -- the circle button's radii

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

instance ToJSON Impulse where
  toEncoding = genericToEncoding defaultOptions
instance FromJSON Impulse

instance ToJSON RB where
  toEncoding = genericToEncoding defaultOptions
instance FromJSON RB

instance ToJSON Osu where
  toEncoding = genericToEncoding defaultOptions
instance FromJSON Osu
