{-# LANGUAGE DeriveGeneric #-}
module BM_Gen where

-- ghc BM_Gen.hs -e "main"

import Data.Aeson
import Data.Complex
import System.IO
import Data.WAVE
import Data.List
import Data.Int
import GHC.Generics

main = do
  wav <- getWAVEFile "song.wav"
  let subSamp = waveSamples wav
  let ss = map fromIntegral $ head <$> subSamp
  let i = findImpulse 1 ss
  encodeFile "beatmap.json" (findImpulse 1 ss)

genButton q
  | r ==    4 = Just 'U'
  | r ==    3 = Just 'D'
  | r ==    2 = Just 'L'
  | r ==    1 = Just 'R'
  | otherwise = Nothing
  where r = (ceiling q) `mod` 5

genCircle x y  = Osu xPos yPos -- Drag and not drag data?
  where width  = 725 -- w = Width - 75 (Width and height from game board file)
        height = 525 -- h = Height - 75
        xPos   = boundsCheck ((x `mod` width), 60, width)
        yPos   = boundsCheck ((y `mod` height), 60, height)

-- boundsCheck :: (Integer, Integer, Integer) -> Integer
boundsCheck (dimVal, dMin, dMax)
  | dimVal < dMin = dMin
  | dimVal > dMax = dMax
  | otherwise     = dimVal

findImpulse _ [] = []
findImpulse i xs = do
  let res = checkPartition frame (fst part)
  case res of
    Nothing -> next
    Just r' -> [r'] ++ next
  where part  = splitAt 1470 xs
        next  = findImpulse (i + 1) (snd part)
        frame = (1470 * i) + 1

checkPartition f ps =
  Impulse <$> (pure f) <*> rock <*> (pure osu)
  where part = splitAt 735 ps
        subA = fCat $ fst part
        subB = fCat $ snd part
        diff = pctDiff (fromIntegral subA) (fromIntegral subB)
        rock = diff >>= genButton
        osu  = genCircle subA subB

-- pctDiff :: Double -> Double -> Maybe Double
pctDiff a b
  | dif == 0  = Nothing
  | avg == 0  = Nothing
  | pct < 150  = Nothing
  | otherwise = Just pct
  where avg = (a + b) / 2
        dif = (a - b)
        pct = (*100) $ abs (avg / dif)

fCat :: (Foldable t, Num b) => t b -> b
fCat = foldl' (+) 0

data Impulse = Impulse {
  act_frame :: Integer,
  rb        :: Char,
  osu       :: Osu
  } deriving (Generic, Show)

data Osu = Osu {
  x         :: Int,
  y         :: Int
  } deriving (Generic, Show)

instance ToJSON Impulse where
  toEncoding = genericToEncoding defaultOptions
instance FromJSON Impulse

instance ToJSON Osu where
  toEncoding = genericToEncoding defaultOptions
instance FromJSON Osu
