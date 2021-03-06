#!/usr/bin/python
# coding: utf-8

import struct
from FAT import FileEntry
import datetime
import sys

def getDateTimeFromDosTime(dosDate, dosTime,dosTenthOfSecond):
    """ reads a dos/fat time and returns a datetime.datetime object."""
    creationYear = readBitsFromByte(dosDate, 16, 7) + 1980
    creationMonth = readBitsFromByte(dosDate, 9, 4)
    creationDay = readBitsFromByte(dosDate, 5, 5)
    creationHour = readBitsFromByte(dosTime, 16, 5)
    creationMinute = readBitsFromByte(dosTime, 11, 6)
    creationSecond = int(readBitsFromByte(dosTime, 5, 5)*2 + dosTenthOfSecond / 100)
    creationMicroSecond = (dosTenthOfSecond % 100) * 10000
    return datetime.datetime(creationYear, creationMonth, creationDay, creationHour, creationMinute, creationSecond, creationMicroSecond)

def readBitsFromByte(value, startIndex, bitCount):
    """ Reads bitCount number of bits from value, starting at bit number *startIndex* (from right)"""    
    return (value & (2**startIndex -1)) >> (startIndex - bitCount)

def getNthBit(num, n):
    """ Returns the n'th bit in num"""   
    return (num>>n)&1   
    
def getStringFromLongFilename(firstChars, secondChars, thirdChars):
    """ Converts a DOS long filename to String"""  
    #TODO: This is not 100% correct... .
    filename = ""
    for i in range(0, len(firstChars)-1,2):
        if firstChars[i] != 0xff and firstChars[i] != 0x00:
            filename += chr(firstChars[i])
    for i in range(0, len(secondChars)-1,2):
        if secondChars[i] != 0xff and secondChars[i] != 0x00:
            filename += chr(secondChars[i])
    for i in range(0, len(thirdChars)-1,2):
        if thirdChars[i] != 0xff and thirdChars[i] != 0x00:
            filename += chr(thirdChars[i])
    return filename

class Directory:
    """Handles content of a directory"""    
    def __init__(self, file, clusterlist, fatVbr, path):
        self.inputFile = file
        self.clusterlist = clusterlist
        self.dataOffset = fatVbr.getDataOffsetInBytes() + (fatVbr.getRootDirSectorCount()- 2 * fatVbr.getSectorsPerCluster()) * fatVbr.getSectorSize()
        self.fatVbr = fatVbr
        self.entries = []
        self.path = path
        self.readAllEntries()

    #TODO: I should put a getNextClusterdata() in FatTable class. Then I would not need this code here.
    def isEmpty(self):
        """Checks if the directory is of size 0"""
        return self.clusterlist[0]==0 #It seems like first cluster is set to 0 when fileSize is 0.

    def readAllEntries(self):
        """Prepares the Directoryclass by reading and storing the data of all directory entries. This method is called during initialization of the class."""
        index = 0;
        while (self.isDirEntry(index) and index*32<len(self.clusterlist)*self.fatVbr.getClusterSize() and not self.isEmpty()):
            fileEntry = self.getEntry(index)
            self.entries.append(fileEntry)
            index+=fileEntry.getEntryCount()

    def getEntry(self, index):
        """Returns the entry at index. Should only be called internally, in case og long filenames present, this function should only be called with the index of the last long filename entry as it will recursively read all relevant entries."""
        if (self.isLongFileNameEntry(index)):
            self.inputFile.seek(self.getOffset(index))
            (entryOrder, firstChars, attributes, longEntryType, checksum, secondChars, alwaysZero, thirdChars) = struct.unpack_from("<B10sBBB12sH4s",self.inputFile.read(32))
            if longEntryType==0: # longEntryType always has longEntryType==0.
                #TODO: Should check checksum and verify... 
                if sys.version_info.major<3:
                    firstChars = bytearray(firstChars)
                    secondChars = bytearray(secondChars)
                    thirdChars = bytearray(thirdChars)
                fileEntry = self.getEntry(index+1)
                fileEntry.addToLongFilename(getStringFromLongFilename(firstChars,secondChars, thirdChars))
                fileEntry.addEntryCount()
            return fileEntry    
        else:
            fileEntry = FileEntry.FileEntry()
            self.inputFile.seek(self.getOffset(index))
            (shortFilenameTemp,shortExtensionTemp,attributes,reserved,creationTenthOfSeconds,creationTime,creationDate, lastAccessedDate, notUsedForFat16, lastModificationTime, lastModificationDate, firstClusterNumber, fileSize) = struct.unpack_from("<8s3sBBBHHHHHHHL",self.inputFile.read(32))
            fileEntry.setDeleted(self.isDeletedEntry(index))
            if self.isDeletedEntry(index):
                fileEntry.setShortFilename("?" + shortFilenameTemp[1:].decode("utf-8"))
            else:
                fileEntry.setShortFilename(shortFilenameTemp.decode("utf-8"))
            fileEntry.setShortExtension(shortExtensionTemp.decode("utf-8"))
            fileEntry.setReadOnly(getNthBit(attributes, 0))
            fileEntry.setHidden(getNthBit(attributes, 1))
            fileEntry.setSystem(getNthBit(attributes, 2))
            fileEntry.setVolumeId(getNthBit(attributes, 3))
            fileEntry.setDirectory(getNthBit(attributes, 4))
            fileEntry.setArchive(getNthBit(attributes, 5)) 
            fileEntry.setCreationDateTime(getDateTimeFromDosTime(creationDate, creationTime, creationTenthOfSeconds))
            fileEntry.setAccessedDateTime(getDateTimeFromDosTime(lastAccessedDate, 0, 0))
            fileEntry.setModifiedDateTime(getDateTimeFromDosTime(lastModificationDate, lastModificationTime, 0))
            fileEntry.setFirstCluster(firstClusterNumber)
            fileEntry.setFileSize(fileSize)
            fileEntry.setPath(self.path)
            fileEntry.setId(self.getOffset(index))
            return fileEntry

    def hasDirectory(self, directoryname):
        """Checks if a directory with longfilename directoryname exists."""
        for fileEntry in self.entries:
            if (fileEntry.isDirectory() and fileEntry.getLongFilename() == directoryname):
                return True
        return False;

    def getDirectoryEntry(self, directoryname):
        """Returns a fileEntry to a directory with name directoryname""" 
        for fileEntry in self.entries:
            if (fileEntry.isDirectory() and fileEntry.getLongFilename() == directoryname):
                return fileEntry
        raise ValueError("Can't find directory + " + self.path + directoryname)

    def getFileEntry(self, filename):
        """Returns a fileEntry to a directory with name directoryname""" 
        for fileEntry in self.entries:
            if (not fileEntry.isDirectory() and fileEntry.getLongFilename() == filename):
                return fileEntry
        raise ValueError("Can't find directory + " + self.path + filename)

    def hasFile(self, filename):
        """ Checks if the filename is present within this directory"""
        for fileEntry in self.entries:
            if (not fileEntry.isDirectory() and fileEntry.getLongFilename() == filename):
                return True
        return False;

    def isDirEntry(self, index):
        """ When all directory entries have been read, the next one will start with 0x00 which is not an entry. This code checks if first byte of the entry is 0x00."""
        return self.getFirstByte(index)!=0

    def isLongFileNameEntry(self, index):
        """ In long filename entries, the Attribute-byte will be 0x0F. This functions checks if the attribute byte is 0x0F""" 
        return self.getAttributeByte(index)==0x0F

    def isDeletedEntry(self, index):
        """ When records are deleted, the first byte will be 0xE5. This code checks if the first byte is 0xE5"""
        return self.getFirstByte(index)==0xE5

    def getFirstByte(self, index):
        """ Returns the first byte of the directory-entry at a specified index of the directory. The function Multiplies index by 32 to get the file-position"""
        self.inputFile.seek(self.getOffset(index))
        return struct.unpack_from("<B",self.inputFile.read(1))[0]
    
    def getOffset(self, index):
        clusterIndex = int(index/self.fatVbr.getEntriesPerCluster())
        clusterOffset = self.clusterlist[clusterIndex]*self.fatVbr.getClusterSize()
        indexOffset = (index % self.fatVbr.getEntriesPerCluster()) * self.fatVbr.getBytesPrRootDirEntry()
        return int(round(self.dataOffset + clusterOffset + indexOffset))
        
    def getAttributeByte(self, index):
        """ Returns the attribute byte of the directory-entry at a specified index of the directory. The function Multiplies index by 32 to get the file-position"""
        self.inputFile.seek(self.getOffset(index)+11)
        return struct.unpack_from("<B",self.inputFile.read(1))[0]

    def getDirEntries(self):
        """ Returns all the entries for directories in current directory."""
        dirEntries = []
        for fileEntry in self.entries:
            if (fileEntry.isDirectory()):
                dirEntries.append(fileEntry)
        return dirEntries
        
    def getFileEntries(self):
        """ Returns all the entries for file in current directory."""
        fileEntries = []
        for fileEntry in self.entries:
            if not fileEntry.isDirectory():
                fileEntries.append(fileEntry)
        return fileEntries
        
    def getAllEntries(self):
        """ Returns all the entries in current directory."""
        return self.entries
    
    def getPath(self):
        """ Returns the parent-path for current directory."""
        return self.path
        