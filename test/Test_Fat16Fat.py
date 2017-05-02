import unittest
import Fat
import FatVbr

class TestFAT16FileAllocationTable(unittest.TestCase):
    
    def testGetFatValue(self):
        myFatVbr = FatVbr.FatVbr(open("FAT16.dd", "rb"),0)
        myFat = Fat.Fat(open("FAT16.dd", "rb"),0, myFatVbr)
        self.assertEqual(myFat.getNextSector(3),0xffff)

if __name__ == '__main__':
    unittest.main()
