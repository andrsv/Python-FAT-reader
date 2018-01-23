import unittest, os
from context import FAT
from FAT import Fat, FatVbr

class testFAT16FileAllocationTable(unittest.TestCase):
    
    def testGetFatTableValue(self):
        testsPath = os.path.dirname(os.path.abspath(__file__))
        FAT16filename = testsPath+"/FAT16.dd"
        myFatVbr = FatVbr.FatVbr(open(FAT16filename, "rb"),0)
        myFat = Fat.Fat(open(FAT16filename, "rb"),0, myFatVbr)
        self.assertEqual(myFat.getNextSector(3),20)
