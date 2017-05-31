import unittest
import FatVbr
import os

class TestFAT16HeaderParser(unittest.TestCase):
    
    def setUp(self):
        testsPath = os.path.dirname(os.path.abspath(__file__))
        FAT16filename = testsPath+"/FAT16.dd"
        self.fatVbr = FatVbr.FatVbr(open(FAT16filename, "rb"),0)
    
    def testSectorSize(self):
        self.assertEqual(self.fatVbr.sectorSize,512)

    def testClusterSize(self):
        self.assertEqual(self.fatVbr.sectorsPerCluster,4)

    def testSectorCount(self):
        self.assertEqual(self.fatVbr.sectorCount,34816)

    def testFatCount(self):
        self.assertEqual(self.fatVbr.fatCount,2)

    def testReservedSectors(self):
        self.assertEqual(self.fatVbr.reservedSectors,4)

    def testPositions(self):
        self.assertEqual(self.fatVbr.posFirstSector,0)
        self.assertEqual(self.fatVbr.posFirstReservedSector,0)
        self.assertEqual(self.fatVbr.posLastReservedSector,3)
        self.assertEqual(self.fatVbr.posFirstFatSector,4)
        self.assertEqual(self.fatVbr.posLastFatSector,75)
        self.assertEqual(self.fatVbr.posFirstDataSector,76)
        self.assertEqual(self.fatVbr.posFirstRootDirSector,76)
        self.assertEqual(self.fatVbr.posLastRootDirSector,107)
        self.assertEqual(self.fatVbr.posLastDataSector,34815)
        self.assertEqual(self.fatVbr.posLastSector,34815)
        
    def testVolumeID(self):
        self.assertEqual(self.fatVbr.volumeID, 0x8822b991)

    def testVolumeLabel(self):
        self.assertEqual(self.fatVbr.volumeLabel, "NO NAME    ")

    def testRootDirEntries(self):
        self.assertEqual(self.fatVbr.rootDirEntries,512)

    def testOEMName(self):
        self.assertEqual(self.fatVbr.oemName,"mkfs.fat")

    def testFileSystemIdentifier(self):
        self.assertEqual(self.fatVbr.fileSystemIdentifier,"FAT16   ")

    def testExtendedBootSignature(self):
        self.assertEqual(self.fatVbr.extendedBootSignature,0x29)
