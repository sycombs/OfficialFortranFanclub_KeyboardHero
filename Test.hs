module BMGen_Test where

import Test.Hspec
import qualified BM_Gen as BMG

main :: IO ()
main = hspec $ do
  describe "boundsCheck" $ do
    it "Forces circle within a dimension minimum" $
      BMG.boundsCheck(-1, 50, 850) `shouldBe` 50

    it "Forces circle within a dimension maximum" $
      BMG.boundsCheck(1000, -10, 50) `shouldBe` 50

    it "Does not change anything when circle within bounds" $
      BMG.boundsCheck(0, 0, 0)  `shouldBe` 0

  describe "genButton" $ do
    it "Forces the remainder to be positive" $
      BMG.genButton(-1) `shouldBe` 'D'

    -- it "Should not accept a fractional number" $
    --   BMG.genButton(1.5) `shouldBe` 'A'
