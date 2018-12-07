{-|
Module      : Main
-}


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

-- | main makes all the necessary function calls to generate a beatmap using
-- and can be called via the console with the following command
-- !!! Note: Almost all of these functions have been deprecated as of the
-- demo_branch's creation. Don't judge my abilities based on this !!!
--
-- >>> ghc bm_gen.hs -e "main" > "outputfilename.txt"
--
main = do
  wav <- getWAVEFile "song.wav"
  let imps = abs.head <$> waveSamples wav :: [WAVESample]
  encodeFile "beatmap.json" (findImpulse 1 imps)

-- | boundsCheck ensures that an object is within the given ranges
--
-- > boundsCheck coordinateValue dimensionMinimum dimensionMaximum
--
boundsCheck :: (Integer, Integer, Integer) -> Integer
boundsCheck (dimVal, dMin, dMax)
  | dimVal < dMin = dMin
  | dimVal > dMax = dMax
  | otherwise     = dimVal


-- | findImpulse processes the audio data all while keeping track of successful
-- impulses
-- This is recursively by taking a chunk of 1470 samples to analyze and then
-- recursing through the rest of the list
--
-- > findImpulse frameCounter sampleList
--
findImpulse :: Integral a => Double -> [a] -> [Impulse]
findImpulse _ []  = []
findImpulse i xs  = (differenceFinder actFrame p1) ++ (findImpulse (i + 1) p2)
  where p1        = take 1470 xs
        p2        = drop 1470 xs
        actFrame  = (i * 1470) + 1

-- | differenceFinder goes through the given list and returns an impulse when
-- the difference between the amplitude of two partitions of size 735 is detected
--
-- impulse is then called in order to process the impulse and generate the RB and
-- Osu buttons
--
differenceFinder :: Integral a => Double -> [a] -> [Impulse]
differenceFinder frame ss
  | difference > 39000 = [impulse]
  | otherwise  = []
  where partition_1 = foldl' (+) 0 $ take 735 ss
        partition_2 = foldl' (+) 0 $ drop 735 ss
        difference  = (abs $ partition_1 - partition_2) `div` 50000
        impulse     = processImpulse $ frame :+ (fromIntegral difference)

-- | processImpulse calls genCircle in order to generate an Osu button
-- !!! Note: Because of time constraints and issues with the generation
-- algorithm, we always return an RB with 'A' as a placeholder
--
-- This issue has been resolved and this function deprecated as of the demo_branch's
-- creation
--
processImpulse :: Complex Double -> Impulse
processImpulse compDoub = Impulse actFrame rb osu
  where actFrame        = toInteger $ ceiling $ realPart compDoub
        rb              = RB $ 'A'
        osu             = genCircle compDoub

{- Button Generation Functions -}

-- !!! genButton has been deprecated as of the demo_build commit !!!

-- genButton :: Integer -> Char
-- genButton d
--   | s >= 1250 = 'U'
--   | s >= 900  = 'D'
--   | s >= 500  = 'L'
--   | otherwise = 'R'
--   where s = d `div` 5000


-- | genCircle generates an Osu button by taking the mod value of the x and y
-- window. Note that here is a +/- 50 for either extreme in order to keep
-- the button fully constrained within the expected radius
--
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

-- | Impulse is the main data type used in order to encapsulate the activation
-- frame and both the RB and Osu style buttons
--
-- !!! Note: I think adding documentation to Show and Generic would involve adding
-- code so those won't be documented. They simply allow Impulse, RB, and Osu to
-- be used as arbitrary classes and be displayed
--
data Impulse = Impulse {
  act_frame :: Integer,
  rb        :: RB,
  osu       :: Osu
  } deriving (Generic, Show)

-- | RB is a single value data type that contains the character that holds the
-- output Char. It's useless in this version and only left in because of time
-- constraints
--
-- !!! Note: See data Impulse for more information regarding Generic RB and
-- Show RB
--
newtype RB = RB {
  button :: Char
  } deriving (Generic, Show)

-- | Osu contains the (x,y) coordinates used to represent the location of an
-- Osu style button
-- !!! Note: See data Impulse for more information regarding Generic Osu and
-- Show Osu
--
data Osu = Osu {
  x         :: Integer,
  y         :: Integer
  } deriving (Generic, Show)

-- | ToJSON Replace is default generic instance of ToJSON for the Impulse type
instance ToJSON Impulse where
  toEncoding = genericToEncoding defaultOptions

-- | FromJSON Impulse is default generic instance of FromJSON for the Impulse
instance FromJSON Impulse

-- | ToJSON RB is default generic instance of ToJSON for the RB type
instance ToJSON RB where
  toEncoding = genericToEncoding defaultOptions

-- | FromJSON RB is default generic instance of FromJSON for the RB type
instance FromJSON RB

-- | ToJSON Osu is default generic instance of ToJSON for the Osu type
instance ToJSON Osu where
  toEncoding = genericToEncoding defaultOptions

-- | FromJSON Osu is default generic instance of FromJSON for the Osu type
instance FromJSON Osu

