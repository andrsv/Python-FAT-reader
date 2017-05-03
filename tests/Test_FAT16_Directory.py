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
        
    def testGetStringFromLongFilename(self):
        testString = Directory.getStringFromLongFilename([0x74,0x00,0x65,0x00,0x73,0x00,0x74,0x00,0x00,0x00],[0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff],[0xff,0xff,0xff,0xff])
        self.assertEqual("test", testString)

    def testDirectoriesInRoot(self):
        rootDir = self.fat.getRootDirectory()
        self.assertTrue(rootDir.hasDirectory("test1"))
        self.assertFalse(rootDir.hasDirectory("test5"))

    def testFilesInRoot(self):
        rootDir = self.fat.getRootDirectory()
        self.assertFalse(rootDir.hasFile("NoSuchFile.txt"))

    def testNonRootDir(self):
        rootDir = self.fat.getRootDirectory()
        testDirEntry = rootDir.getDirectoryEntry("test2")
        testDir = self.fat.getDirectory(testDirEntry)
        
        self.assertFalse(testDir.hasFile("NoSuchFile"))
        self.assertTrue(testDir.hasDirectory("test2.1"))
        
        test2DirEntry = testDir.getDirectoryEntry("test2.1")
        test2Dir = self.fat.getDirectory(test2DirEntry)
        self.assertTrue(test2Dir.hasFile("bigTextFileWithGarbageData.txt"))
        
                    
    def testSubSubDir(self):
        rootDir = self.fat.getRootDirectory()
        testDirEntry = rootDir.getDirectoryEntry("test2")
        testDir = self.fat.getDirectory(testDirEntry)

        test2DirEntry = testDir.getDirectoryEntry("test2.1")
        test2Dir = self.fat.getDirectory(test2DirEntry)
        
        self.assertFalse(testDir.hasFile("NoSuchFile"))
                    

if __name__ == '__main__':
    unittest.main()
