import unittest
import FatVbr
import os

class TestFAT16HeaderParser(unittest.TestCase):
    
    def setUp(self):
        testsPath = os.path.dirname(os.path.abspath(__file__))
        FAT32filename = testsPath+"/FAT32.dd"
        self.fatVbr = FatVbr.FatVbr(open(FAT32filename, "rb"),0)
        
    def testSectorSize(self):
        self.assertEqual(self.fatVbr.sectorSize,512)

    def testClusterSize(self):
        self.assertEqual(self.fatVbr.sectorsPerCluster,1)

    def testSectorCount(self):
        self.assertEqual(self.fatVbr.sectorCount,67584)

    def testFatCount(self):
        self.assertEqual(self.fatVbr.fatCount,2)

    def testReservedSectors(self):
        self.assertEqual(self.fatVbr.reservedSectors,32)

    def testPositions(self):
        self.assertEqual(self.fatVbr.posFirstSector,0)
        self.assertEqual(self.fatVbr.posFirstReservedSector,0)
        self.assertEqual(self.fatVbr.posLastReservedSector,31)
        self.assertEqual(self.fatVbr.posFirstFatSector,32)
        self.assertEqual(self.fatVbr.posLastFatSector,1071)
        self.assertEqual(self.fatVbr.posFirstDataSector,1072)
        self.assertEqual(self.fatVbr.posFirstRootDirSector,1072)
##TODO not yet implemented       self.assertEqual(self.fatVbr.posLastRootDirSector,4066)
        self.assertEqual(self.fatVbr.posLastDataSector,67583)
        self.assertEqual(self.fatVbr.posLastSector,67583)
        
    def testVolumeID(self):
        self.assertEqual(self.fatVbr.volumeID, 0xa5f701f8)

    def testVolumeLabel(self):
        self.assertEqual(self.fatVbr.volumeLabel, "NO NAME    ")

    def testRootDirEntries(self):
        ##TODO self.assertEquals(self.fatVbr.rootDirEntries,512)
        pass

    def testOEMName(self):
        self.assertEqual(self.fatVbr.oemName,"mkfs.fat")

    def testFileSystemIdentifier(self):
        self.assertEqual(self.fatVbr.fileSystemIdentifier,"FAT32   ")

    def testExtendedBootSignature(self):
        self.assertEqual(self.fatVbr.extendedBootSignature,0x29)

if __name__ == '__main__':
    unittest.main()

