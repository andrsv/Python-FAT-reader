import unittest
import Directory
import FatVbr
import Fat
import os

class TestFAT16RootDirectory(unittest.TestCase):

    def setUp(self):
        testsPath = os.path.dirname(os.path.abspath(__file__))
        FAT16filename = testsPath+"/FAT16.dd"
        self.fatVbr = FatVbr.FatVbr(open(FAT16filename, "rb"),0)
        self.fat = Fat.Fat(open(FAT16filename, "rb"),0, self.fatVbr)


    def testNonRootDir(self):
        rootDir = self.fat.getRootDirectory()
        testDirEntry = rootDir.getDirectoryEntry("test2")
        testDir = self.fat.getDirectory(testDirEntry)
        
        self.assertFalse(testDir.hasFile("NoSuchFile"))
        self.assertTrue(testDir.hasDirectory("test2.1"))
        
        test2DirEntry = testDir.getDirectoryEntry("test2.1")
        test2Dir = self.fat.getDirectory(test2DirEntry)
        self.assertTrue(test2Dir.hasFile("bigTextFileWithGarbageData.txt"))

        bigTextFile = test2Dir.getFileEntry("bigTextFileWithGarbageData.txt")
        self.assertEqual(bigTextFile.getModifiedDateTime().strftime('%d.%m.%Y %H:%M:%S') ,"02.05.2017 12:21:50")
      