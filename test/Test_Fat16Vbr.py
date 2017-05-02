import unittest
import FatVbr

class TestFAT16HeaderParser(unittest.TestCase):
    
    def testSectorSize(self):
        myFat = FatVbr.FatVbr(open("FAT16.dd", "rb"),0)
        self.assertEqual(myFat.sectorSize,512)

    def testClusterSize(self):
        myFat = FatVbr.FatVbr(open("FAT16.dd", "rb"),0)
        self.assertEqual(myFat.sectorsPerCluster,4)

    def testSectorCount(self):
        myFat = FatVbr.FatVbr(open("FAT16.dd", "rb"),0)
        self.assertEqual(myFat.sectorCount,262144)

    def testFatCount(self):
        myFat = FatVbr.FatVbr(open("FAT16.dd", "rb"),0)
        self.assertEqual(myFat.fatCount,2)

    def testReservedSectors(self):
        myFat = FatVbr.FatVbr(open("FAT16.dd", "rb"),0)
        self.assertEqual(myFat.reservedSectors,4)

    def testPositions(self):
        myFat = FatVbr.FatVbr(open("FAT16.dd", "rb"),0)
        self.assertEqual(myFat.posFirstSector,0)
        self.assertEqual(myFat.posFirstReservedSector,0)
        self.assertEqual(myFat.posLastReservedSector,3)
        self.assertEqual(myFat.posFirstFatSector,4)
        self.assertEqual(myFat.posLastFatSector,515)
        self.assertEqual(myFat.posFirstDataSector,516)
        self.assertEqual(myFat.posFirstRootDirSector,516)
        self.assertEqual(myFat.posLastRootDirSector,547)
        self.assertEqual(myFat.posLastDataSector,262143)
        self.assertEqual(myFat.posLastSector,262143)
        
    def testVolumeID(self):
        myFat = FatVbr.FatVbr(open("FAT16.dd", "rb"),0)
        self.assertEqual(myFat.volumeID, 0x91f81caf)

    def testVolumeLabel(self):
        myFat = FatVbr.FatVbr(open("FAT16.dd", "rb"),0)
        self.assertEqual(myFat.volumeLabel, "NO NAME    ")

    def testRootDirEntries(self):
        myFat = FatVbr.FatVbr(open("FAT16.dd", "rb"),0)
        self.assertEqual(myFat.rootDirEntries,512)

    def testOEMName(self):
        myFat = FatVbr.FatVbr(open("FAT16.dd", "rb"),0)
        self.assertEqual(myFat.oemName,"mkfs.fat")

    def testFileSystemIdentifier(self):
        myFat = FatVbr.FatVbr(open("FAT16.dd", "rb"),0)
        self.assertEqual(myFat.fileSystemIdentifier,"FAT16   ")

    def testExtendedBootSignature(self):
        myFat = FatVbr.FatVbr(open("FAT16.dd", "rb"),0)
        self.assertEqual(myFat.extendedBootSignature,0x29)

if __name__ == '__main__':
    unittest.main()
