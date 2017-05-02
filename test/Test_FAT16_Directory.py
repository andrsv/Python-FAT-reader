import unittest
import Directory
import FatVbr
import Fat

class TestFAT16RootDirectory(unittest.TestCase):

    def testGetStringFromLongFilename(self):
        testString = Directory.getStringFromLongFilename([0x74,0x00,0x65,0x00,0x73,0x00,0x74,0x00,0x00,0x00],[0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff],[0xff,0xff,0xff,0xff])
        self.assertEqual("test", testString)

    def testDirectoriesInRoot(self):
        fatVbr = FatVbr.FatVbr(open("FAT16.dd", "rb"),0)
        fat = Fat.Fat(open("FAT16.dd", "rb"),0, fatVbr)
        rootDir = fat.getRootDirectory()
        self.assertTrue(rootDir.hasDirectory("test1"))
        self.assertFalse(rootDir.hasDirectory("test5"))

    def testFilesInRoot(self):
        fatVbr = FatVbr.FatVbr(open("FAT16.dd", "rb"),0)
        fat = Fat.Fat(open("FAT16.dd", "rb"),0, fatVbr)
        rootDir = fat.getRootDirectory()
        self.assertFalse(rootDir.hasFile("NoSuchFile.txt"))

    def testNonRootDir(self):
        fatVbr = FatVbr.FatVbr(open("FAT16.dd", "rb"),0)
        fat = Fat.Fat(open("FAT16.dd", "rb"),0, fatVbr)
        rootDir = fat.getRootDirectory()
        testDirEntry = rootDir.getDirectoryEntry("test2")
        testDir = fat.getDirectory(testDirEntry)
        
        self.assertFalse(testDir.hasFile("NoSuchFile"))
        self.assertTrue(testDir.hasDirectory("test2.1"))
        
        test2DirEntry = testDir.getDirectoryEntry("test2.1")
        test2Dir = fat.getDirectory(test2DirEntry)
        self.assertTrue(test2Dir.hasFile("bigTextFileWithGarbageData.txt"))
        
                    
    def testSubSubDir(self):
        fatVbr = FatVbr.FatVbr(open("FAT16.dd", "rb"),0)
        fat = Fat.Fat(open("FAT16.dd", "rb"),0, fatVbr)
        rootDir = fat.getRootDirectory()
        testDirEntry = rootDir.getDirectoryEntry("test2")
        testDir = fat.getDirectory(testDirEntry)
        for entry in testDir.getAllEntries():
            print (entry)
        test2DirEntry = testDir.getDirectoryEntry("test2.1")
        test2Dir = fat.getDirectory(test2DirEntry)
        for entry in test2Dir.getAllEntries():
            print (entry)
        
        self.assertFalse(testDir.hasFile("NoSuchFile"))
                    

if __name__ == '__main__':
    unittest.main()
