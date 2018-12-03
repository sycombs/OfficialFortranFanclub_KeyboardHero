module Main where

-- ghc Tester.hs -e "main" > testResults.txt

import Data.Int
import Test.Hspec
import qualified BM_Gen as BMG

main :: IO ()
main = hspec $ do
  -- I have no idea why these have to be here, but they do
  let zIntStream = take 1000000 $ repeat 0
  let dupeStream = take 88200 $ repeat 81273
  let bigD       = 999999999999999999
  let smlD       = 99999
  let negD       = -44100

  describe "Bounds Checker : boundsCheck" $ do
    it "Forces circle within a dimension minimum" $
      BMG.boundsCheck(-1, 50, 850) `shouldBe` 50

    it "Forces circle within a dimension maximum" $
      BMG.boundsCheck(1000, -10, 50) `shouldBe` 50

    it "Does not change anything when circle within bounds" $
      BMG.boundsCheck(0, 0, 0)  `shouldBe` 0

  describe "Generate Button : genButton" $ do
    it "Returns a valid out when fed a negative value" $
      BMG.genButton(-1) `shouldBe` Just 'U'

    it "Returns Nothing when fed a multiple of 5" $
      BMG.genButton(5 * 5) `shouldBe` Nothing

  describe "Percent Difference : pctDiff" $ do
    it "Returns Nothing when fed inputs of 0" $
     (BMG.pctDiff 0 0) `shouldBe` Nothing

    it "Returns Nothing when fed identical inputs" $
     (BMG.pctDiff (-15) (-15)) `shouldBe` Nothing

    it "Returns Nothing when fed additive inverse inputs" $
     (BMG.pctDiff 1000 (-1000)) `shouldBe` Nothing

  describe "findImpulse" $ do
    it "Returns a list of length 0 when fed a huge stream of zeros" $
      length(BMG.findImpulse bigD zIntStream)  `shouldBe` 0

    it "Returns a list of length 0 when fed a stream of duplicates" $
      length(BMG.findImpulse smlD dupeStream)  `shouldBe` 0

    it "Functions normally even when given a negative starting frame" $
      length (BMG.findImpulse negD zIntStream) `shouldBe` 0
