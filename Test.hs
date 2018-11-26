module Main where

import Data.Int
import Test.Hspec
import qualified BM_Gen as BMG

main :: IO ()
main = hspec $ do
  -- I have no idea why these have to be here, but they do
  let zeroStream = (take 1000000 $ repeat 0    ) :: [Int32]
  let dupeStream = (take 88200      $ repeat 81273) :: [Int32]
  let bigD       = 999999999999999999               :: Double
  let medD       = 99999999                         :: Double
  let smlD       = 99999                            :: Double
  let negD       = -44100                           :: Double

  describe "boundsCheck" $ do
    it "Forces circle within a dimension minimum" $
      BMG.boundsCheck(-1, 50, 850) `shouldBe` 50

    it "Forces circle within a dimension maximum" $
      BMG.boundsCheck(1000, -10, 50) `shouldBe` 50

    it "Does not change anything when circle within bounds" $
      BMG.boundsCheck(0, 0, 0)  `shouldBe` 0

  -- describe "genButton" $ do
  --   it "Doesn't crash with negative values" $
  --     BMG.genButton(-1) `shouldBe` 'R'

  describe "differenceFinder" $ do
    it "Returns [] when fed a huge stream of zeros" $
      length (BMG.differenceFinder bigD zeroStream) `shouldBe` 0

    it "Returns [] when fed a medium size stream of zeros" $
      length (BMG.differenceFinder medD zeroStream) `shouldBe` 0

    it "Returns [] when fed a huge small of zeros" $
      length (BMG.differenceFinder smlD zeroStream) `shouldBe` 0

    it "Returns [] when fed a negative frame counter" $
      length (BMG.differenceFinder negD zeroStream) `shouldBe` 0

    it "Returns [] when fed a stream of duplicates" $
      length (BMG.differenceFinder medD dupeStream) `shouldBe` 0

  describe "findImpulse" $ do
    it "Returns [] when fed a huge stream of zeros" $
      length (BMG.findImpulse bigD zeroStream) `shouldBe` 0

    it "Returns [] when fed a medium size stream of zeros" $
      length (BMG.findImpulse medD zeroStream) `shouldBe` 0

    it "Returns [] when fed a huge small of zeros" $
      length (BMG.findImpulse smlD zeroStream) `shouldBe` 0

    it "Returns [] when fed a negative frame counter" $
      length (BMG.findImpulse negD zeroStream) `shouldBe` 0

    it "Returns [] when fed a stream of duplicates" $
      length (BMG.findImpulse medD dupeStream) `shouldBe` 0

  -- describe "main" $ do
  --   it "Doesn't blow up when the song isn't there" $
  --     BMG.main `shouldReturn` ()

{-
--
  Test ideas :
    Pass a stream of all 0's
    Don't pass anything at all
    Don't allow it to write... do stuff...
-}

-- it "Should not accept a fractional number" $
--   BMG.genButton(1.5) `shouldBe` 'A'
