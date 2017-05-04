# -*- coding: utf-8 -*-
"""Reads FAT (File Allocation Table) FSs (File System) VBR (Volume Boot Record) of a partition."""
import struct
import math


class FatVbr:
    """Reads FAT (File Allocation Table) FSs (File System) VBR (Volume Boot Record) of a partition.
     
    References:
    https://phs.pingpong.net/courseId/43700/node.do?id=24830674
    http://www.tavi.co.uk/phobos/fat.html
    https://en.wikipedia.org/wiki/Design_of_the_FAT_file_system
    http://wiki.osdev.org/FAT
    """
    def __init__(self, file, offset):
        """Read the VBR of a FAT Filesystem"""
        ## initilizing variables
        self.unhandledWarning = False
        self.unhandledWarningMessage = ""
        self.posFirstRootDirSector = 0;
        self.extendedBootSignature = 0;
        self.volumeLabel ="";
        self.fileSystemIdentifier = "";
        self.volumeID = 0;
        self.posLastRootDirSector =0;
        rootDirClusterPos = 0;
        self.fatType= ""
        self.offset = offset
        self.inputFile = file

        ## Read data: 
        ## 8 bytes, OEM name
        file.seek(offset + 0x03)
        oemNameTemp = struct.unpack_from("<8s",file.read(8))[0]
        self.oemName = oemNameTemp.decode("utf-8")
        if (self.oemName == "EXFAT   "):
            self.unhandledWarning = True
            self.unhandledWarningMessage += "This module does not support EXFAT.\n"
            ##TODO: read exfat BPB 0x40 - 0x77
        elif (self.oemName == "NTFS    "):
            self.unhandledWarning = True
            self.unhandledWarningMessage += "This module does not support NTFS.\n"
            ##TODO: NTFS: read 0x0b 25bytes DOS3.31 BPB NTFS BPB 0x24 - 0x50 +(DWORD)
        
        ## Read Bios Parameter Block (BPB) data for FAT versions since DOS 2.0: 
        ## 2 bytes, bytes per sector
        ## 1 byte,  sectors per cluster
        ## 2 bytes, count of reserved sectors
        ## 1 byte, number of Fats
        ## 2 bytes, max number of root directory entries 
        ## 2 bytes, Sectors in partition
        ## 1 byte, Media descriptor
        ## 2 bytes sectors per FAT
        file.seek(offset + 0x0B)
        (self.sectorSize,self.sectorsPerCluster,self.reservedSectors,self.fatCount, self.rootDirEntries, self.sectorCount, mediaDescriptor, self.fatSize) = struct.unpack_from("<HBHBHHBH",file.read(13))
         
        ##Note, I do not care for the DOS 3.0 and DOS 3.2 extensions as they seem to be incompatible with the Dos 3.31 extension 
               
        ## Read Bios Parameter Block (BPB) data for FAT versions since DOS 3.31: 
        ## 2 bytes, sectors per track (used for bootloader)
        ## 2 bytes, number of heads (used for bootloader)
        ## 4 bytes, count of hidden sectors (used for bootloader)
        ## 4 bytes, Sectors in partition (if not set in 0x13)
        file.seek(offset + 0x18)
        (sectorsPerTrack,headCount, hiddenSectors, sectorCount0x20) = struct.unpack_from("<HHII",file.read(12))
        
        if self.sectorCount == 0:
            self.sectorCount = sectorCount0x20
        

        ## Read Extended Bios Parameter Block (EBPB) data for FAT12 and FAT16 since OS/2 1.0 and DOS 4.0: 
        ## 1 bytes, physical drive number
        ## 1 bytes, Reserved, WinNT use it to indicate cHKDSK should be run
        ## 1 bytes, Extended boot signature, should be 0x29 or 0x28 for old OSes
        ## 4 bytes, VolumeID (serial number) 
        ## 11 bytes, VolumeLabel, user specified label
        ## 8 bytes, File system Type, for display purpose only, sometimes incorrectly used to identify the type of the filesystem.
        file.seek(offset + 0x26)
        if (self.getFatType() == "FAT12" or self.getFatType() == "FAT16"):
            file.seek(offset + 0x24)
            (physicalDriveNumber, reserved, self.extendedBootSignature, self.volumeID,volumeLabelTemp, fileSystemIdentifierTemp ) = struct.unpack_from("<BBBI11s8s",file.read(26))
            self.volumeLabel = volumeLabelTemp.decode("utf-8") 
            self.fileSystemIdentifier = fileSystemIdentifierTemp.decode("utf-8") 

        ##Read FAT32 Extended BIOS Parameter Block (EBPB): "Microsoft and IBM operating systems determine the type of FAT file system used on a volume solely by the number of clusters" [wikipedia]
        ## 4 bytes, sectors per file allocation table (FAT)
        ## 2 bytes, Drive description
        ## 2 bytes, version number (I don't know how to read this... :()
        ## 4 bytes, sector number of root directory start. 
        ## 2 bytes, sector position of FS Information Sector /typically 1)
        ## 2 bytes, first sector of the 3 FAT32 boot sectors
        ## 12 bytes, reserved, sometimes used for filename of "IBMBIO   COM"
        else:
            file.seek(offset + 0x42)
            extendedBootSignature = struct.unpack_from("<B",file.read(1))[0]
            if (extendedBootSignature==0x28 or extendedBootSignature==0x29):
                file.seek(offset + 0x24)
                (self.fatSize, driveDescription, version, rootDirClusterPos, posFSInformationSector, posFirstFatBootSector) = struct.unpack_from("<IHHIHHxxxxxxxxxxxx",file.read(28))
                ## The next bytes of the FAT32 EBPB are not available for exfat partitions
                ## 1 bytes, Physical drive number 
                ## 1 bytes, Reserved
                ## 1 bytes, Extended boot signature
                ## 4 bytes, Volume ID
                ## 11 bytes, VolumeLabel, user specified label
                ## 8 bytes, File system Type, for display purpose only, sometimes incorrectly used to identify the type of the filesystem.
                if (self.getFatType() == "FAT32"):
                    file.seek(offset + 0x40)
                    (physicalDriveNumber,self.extendedBootSignature, self.volumeID,volumeLabelTemp, fileSystemIdentifierTemp) = struct.unpack_from("<BxBI11s8s",file.read(26))
                    self.volumeLabel = volumeLabelTemp.decode("utf-8") 
                    self.fileSystemIdentifier = fileSystemIdentifierTemp.decode("utf-8") 

        ## Find the position of the various data.
        self.posFirstSector = 0
        self.posFirstReservedSector = self.posFirstSector
        self.posLastReservedSector = self.posFirstReservedSector + self.reservedSectors-1
        self.posFirstFatSector = self.posLastReservedSector+1
        self.posLastFatSector = self.posFirstFatSector + self.fatCount*self.fatSize-1
        self.posFirstDataSector = self.posLastFatSector + 1
        if rootDirClusterPos>0: ##If set in the FAT32 EBPB
            self.posFirstRootDirSector = (rootDirClusterPos -2) * self.sectorsPerCluster + self.posFirstDataSector
            self.posLastRootDirSector = self.posFirstRootDirSector
        else:
            self.posFirstRootDirSector = self.posFirstDataSector;
            if (self.sectorSize>0):
                self.posLastRootDirSector = self.posFirstRootDirSector + self.getRootDirSectorCount()-1
        self.posLastDataSector = self.posFirstSector + self.sectorCount-1
        self.posLastSector = self.posFirstSector + self.sectorCount-1
    
        file.close()

        ## Setup warnings for unhandled data/data with errors.
        if self.sectorSize<32:
            self.unhandledWarning = True
            self.unhandledWarningMessage += "sector size is less than 32. This is not valid for any known FS ("+str(self.sectorSize)+").\n"
        if self.reservedSectors<1:
            self.unhandledWarning = True
            self.unhandledWarningMessage += "There are no reserved sectors. This is not valid for any known FS ("+str(self.reservedSectors)+").\n"
        if self.fatCount==0:
            self.unhandledWarning = True
            self.unhandledWarningMessage += "No FATs. This is not valid for any known FS.\n"
        if self.fatCount!=2:
            self.unhandledWarning = True
            self.unhandledWarningMessage += "Not 2 FATs. This might mean that this is a TFAT volume which is not supported ("+str(self.fatCount)+").\n"
        if self.rootDirEntries==0:
            self.unhandledWarning = True
            self.unhandledWarningMessage += "No root dir entries, this is probably not a FAT16 VBR. The size of Root Dir is not supported\n"
        if hiddenSectors != 0:
            self.unhandledWarning = True
            self.unhandledWarningMessage += "hiddenSectors is set ("+str(hiddenSectors)+").\n"
        if self.extendedBootSignature != 0x28 and self.extendedBootSignature != 0x29:
            self.unhandledWarning = True
            self.unhandledWarningMessage += "this is not an extendedBoot signature.\n"
            
        self.fatType = self.getFatType();

    ## Pseudocode from http://wiki.osdev.org/FAT
    ## Determine the FAT version based on cluster(logical sector) width.
   
    def getFatType(self):
        """Find out which type of FAT Filesystem is used"""
        if self.sectorCount == 0:
            return "FAT32" ##Not sure if this is correct way to handle it... But I guess it is better than returning FAT12.
        dataSectors = self.sectorCount - (self.fatCount * self.fatSize) - self.reservedSectors
        clusterCount = dataSectors / self.sectorsPerCluster
        if (clusterCount <4085): ## Max clusters: 2^12 -12 = 4084 
            return "FAT12"
        elif (clusterCount < 65525): ## Max clusters: 2^16 -12 = 65524
            return "FAT16"
        elif (clusterCount < 268435445): ## Max clusters: 2^28 -12 = 268435444
            return "FAT32"
        else:
            return "exFAT"
        ## Why -12 ?? Because the following are reserved:
        ## The entry for cluster 0 must be identical to the media descriptor byte found in BPB
        ## The entry for cluster 0x01 reflects the entry for end-of-chain value used by the formatter for cluster chains, eg. 0xFFF
        ## 0xFF6 is reserved for future standardization
        ## 0xFF7 means thecluster is marked as "bad
        ## 0xFF8 - 0xFFF means end of cluster chain.

    def getSectorSize(self):
        """Returns the size of a sector, typically 512"""
        return self.sectorSize    

    def getClusterSize(self):
        """Returns the size of a cluster"""
        return self.sectorSize * self.sectorsPerCluster 

    def getInputFile(self):
        """Returns the image file opened as readable"""
        return self.inputFile

    def getDataOffsetInBytes(self):
        """ Returns the byte-offset of the first data sector relative to the start of the file."""
        return self.posFirstDataSector * self.getSectorSize() + self.offset

    def getSectorsPerCluster(self):
        """ Returns number of sectors per cluster"""
        return self.sectorsPerCluster

    def getBytesPrRootDirEntry(self):
        """ Returns the size in bytes of a directory entry."""
        return 32 ## Each entry in the Root folder is 32 bytes.
    
    def getEntriesPerCluster(self):
        """ Returns the number of possible directory-entries per cluster """
        return self.getClusterSize() / self.getBytesPrRootDirEntry()
    
    def getRootDirSectorCount(self):
        """ returns the number of sectors used by the root directory"""
        return math.ceil((self.getBytesPrRootDirEntry() * self.rootDirEntries)/self.sectorSize)
   
    def printHeader(self):
        """Print details from the FATs VBR"""
        if (self.unhandledWarning):
            print("\n*** WARNING ***");
            print("There are settings enabled which this parser does not support")
            print(self.unhandledWarningMessage)
            print("*** WARNING ***\n");
        printFormatString = "{:<23}{:<}"
        print("FS Information")
        print(printFormatString.format("-- Volume Label: ", str(self.volumeLabel)))        
        print(printFormatString.format("-- OEM Name: ", str(self.oemName)))        
        print(printFormatString.format("-- File System: ", str(self.fileSystemIdentifier)))        
        print(printFormatString.format("-- Volume ID: ", hex(self.volumeID).upper())) ##TODO: Does this support leading zeros?    
        print(printFormatString.format("-- Sector size:", str(self.sectorSize)))        
        print(printFormatString.format("-- Cluster size:", str(self.sectorsPerCluster*self.sectorSize) + " bytes (" + str(self.sectorsPerCluster) + " Sectors)"))        
        print(printFormatString.format("-- Number of Sectors:", str(self.sectorCount)))        
        print(printFormatString.format("-- Number of FATs:", str(self.fatCount)))        
        print(printFormatString.format("-- Total Range:", str(self.posFirstSector) + " - " + str(self.posLastSector) + " (" + str(self.sectorCount) + " Sectors)"))        
        print("FS Layout")
        print(printFormatString.format("-- Reserved:", str(self.posFirstReservedSector) + " - " + str(self.posLastReservedSector) + " (" + str(self.posLastReservedSector +1 - self.posFirstReservedSector) + " Sectors)"))        
        print(printFormatString.format("---- VBR:", "0 - 0 (1 Sector)"))
        for n in range(self.fatCount):
            start = self.posFirstFatSector + n* self.fatSize;
            end = self.posFirstFatSector + (n+1)* self.fatSize - 1;
            print(printFormatString.format("-- FAT " + str(n) + ":", str(start) + " - " + str(end) + " (" + str(self.fatSize) + " Sectors)"))        

        print(printFormatString.format("-- Data Area:", str(self.posFirstDataSector) + " - " + str(self.posLastDataSector) + " (" + str(self.posLastDataSector +1 - self.posFirstDataSector) + " Sectors)"))        
        print(printFormatString.format("---- Root Dir:", str(self.posFirstRootDirSector) + " - " + str(self.posLastRootDirSector) + " (" + str(self.posLastRootDirSector +1 - self.posFirstRootDirSector) + " Sectors)"))        
        
