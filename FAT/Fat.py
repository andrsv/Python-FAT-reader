import struct
from FAT import Directory

class Fat():
    """This class handles the File Allocation Table for FAT16 File Systems."""
    def __init__(self, file, offset, fatVbr):
        self.fatVbr = fatVbr
        self.fatStartOffset = offset + fatVbr.posFirstFatSector * fatVbr.sectorSize
        self.file = file
        self.FatVbr = fatVbr
        
        
    def getNextSector(self, index):
        """ Returns the offset of the next sector from the FAT table.""" 
        if (self.fatVbr.fatType == "FAT16"):
            indexOffset = index * 2; # *2 as it is FAT16 (16 bits = 2 bytes) 
            self.file.seek(self.fatStartOffset + indexOffset)
            nextSector = struct.unpack_from("<H",self.file.read(2))[0]
            return nextSector

    def getDirectory(self,directoryEntry):
        """ Returns a Directory instance from a FileEntry."""
        currentCluster = directoryEntry.getFirstCluster()
        clusterList = [currentCluster]
        while(self.getNextSector(currentCluster)<0xfff8):
            if self.getNextSector(currentCluster)==0xfff7:
                raise Exception("Tried to read a cluster marked as bad, cluster: " + currentCluster)
            currentCluster=self.getNextSector(currentCluster)
            clusterList.append(currentCluster)
        return Directory.Directory(self.file, clusterList, self.fatVbr, directoryEntry.getPath() + directoryEntry.getFileName() + "/")

    def getRootDirectory(self):
        """ Returns the root directory"""
        clusterList = [] #which clusters contains the Directory-data?
        clustersCount = self.fatVbr.getRootDirSectorCount() / self.fatVbr.getSectorsPerCluster()
        for x in range(int(-clustersCount)+2, 2): # +2 as two first values of FAT is reserved
            clusterList.append(x)
        return Directory.Directory(self.file, clusterList, self.fatVbr, "/")
