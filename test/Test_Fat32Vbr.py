import unittest
import FatVbr

class TestFAT16HeaderParser(unittest.TestCase):
    
    def testSectorSize(self):
        myFat = FatVbr.FatVbr(open("FAT32.dd", "rb"),0)
        self.assertEqual(myFat.sectorSize,512)

    def testClusterSize(self):
        myFat = FatVbr.FatVbr(open("FAT32.dd", "rb"),0)
        self.assertEqual(myFat.sectorsPerCluster,1)

    def testSectorCount(self):
        myFat = FatVbr.FatVbr(open("FAT32.dd", "rb"),0)
        self.assertEqual(myFat.sectorCount,67584)

    def testFatCount(self):
        myFat = FatVbr.FatVbr(open("FAT32.dd", "rb"),0)
        self.assertEqual(myFat.fatCount,2)

    def testReservedSectors(self):
        myFat = FatVbr.FatVbr(open("FAT32.dd", "rb"),0)
        self.assertEqual(myFat.reservedSectors,32)

    def testPositions(self):
        myFat = FatVbr.FatVbr(open("FAT32.dd", "rb"),0)
        self.assertEqual(myFat.posFirstSector,0)
        self.assertEqual(myFat.posFirstReservedSector,0)
        self.assertEqual(myFat.posLastReservedSector,31)
        self.assertEqual(myFat.posFirstFatSector,32)
        self.assertEqual(myFat.posLastFatSector,1071)
        self.assertEqual(myFat.posFirstDataSector,1072)
        self.assertEqual(myFat.posFirstRootDirSector,1072)
##TODO not yet implemented       self.assertEqual(myFat.posLastRootDirSector,4066)
        self.assertEqual(myFat.posLastDataSector,67583)
        self.assertEqual(myFat.posLastSector,67583)
        
    def testVolumeID(self):
        myFat = FatVbr.FatVbr(open("FAT32.dd", "rb"),0)
        self.assertEqual(myFat.volumeID, 0xa5f701f8)

    def testVolumeLabel(self):
        myFat = FatVbr.FatVbr(open("FAT32.dd", "rb"),0)
        self.assertEqual(myFat.volumeLabel, "NO NAME    ")

    def testRootDirEntries(self):
        myFat = FatVbr.FatVbr(open("FAT32.dd", "rb"),0)
        ##TODO self.assertEquals(myFat.rootDirEntries,512)

    def testOEMName(self):
        myFat = FatVbr.FatVbr(open("FAT32.dd", "rb"),0)
        self.assertEqual(myFat.oemName,"mkfs.fat")

    def testFileSystemIdentifier(self):
        myFat = FatVbr.FatVbr(open("FAT32.dd", "rb"),0)
        self.assertEqual(myFat.fileSystemIdentifier,"FAT32   ")

    def testExtendedBootSignature(self):
        myFat = FatVbr.FatVbr(open("FAT32.dd", "rb"),0)
        self.assertEqual(myFat.extendedBootSignature,0x29)

if __name__ == '__main__':
    unittest.main()

