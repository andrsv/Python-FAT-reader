class FileEntry:
    """Dummy class which handles Directory-entries found in directories"""
    def __init__(self):
        self.longFilename = ""
        self.shortFilename = ""
        self.shortExtension = ""
        self.path = "/"
        self.readOnly = False
        self.hidden = False
        self.system = False
        self.volumeId = False
        self.directory = False
        self.archive = False
        self.entryCount = 1
        self.deleted = False

    def addToLongFilename(self,filename):
        self.longFilename += filename

    def addEntryCount(self):
        self.entryCount += 1

    def setShortFilename(self,shortFileName):
        self.shortFilename = shortFileName

    def setShortExtension(self,shortextension):
        self.shortExtension = shortextension

    def setReadOnly(self,readOnly):
        self.readOnly = readOnly

    def setHidden(self,hidden):
        self.hidden = hidden

    def setSystem(self,system):
        self.system = system

    def setVolumeId(self,volumeId):
        self.volumeId = volumeId

    def setDirectory(self,directory):
        self.directory = directory

    def setArchive(self,archive):
        self.archive = archive

    def setDeleted(self,deleted):
        self.deleted = deleted

    def getShortFilename(self):
        return self.shortFilename.strip()

    def getShortExtension(self):
        return self.shortExtension.strip()

    def getFullShortname(self):
        if len(self.getShortExtension())>0:
            return self.getShortFilename() + "." + self.getShortExtension()
        else:
            return self.getShortFilename()

    def isReadOnly(self):
        return self.readOnly

    def isHidden(self):
        return self.hidden

    def isSystem(self):
        return self.system

    def isVolumeId(self):
        return self.volumeId

    def isDirectory(self):
        return self.directory

    def isArchive(self):
        return self.archive
    
    def isDeleted(self):
        return self.deleted

    def setCreationDateTime(self, creationTime):
        self.creationTime = creationTime;

    def setAccessedDateTime(self, accessedTime):
        self.accessedTime = accessedTime;

    def setModifiedDateTime(self, modificationTime):
        self.modificationTime = modificationTime;

    def setFirstCluster(self, firstCluster):
        self.firstCluster = firstCluster;

    def setFileSize(self, fileSize):
        self.fileSize = fileSize;

    def setId(self, id):
        self.id = id

    def getCreationDateTime(self):
        return self.creationTime;

    def getAccessedDateTime(self):
        return self.accessedTime;

    def getModifiedDateTime(self):
        return self.modificationTime;

    def getFileSize(self):
        return self.fileSize;

    def getLongFilename(self):
        return self.longFilename

    def getEntryCount(self):
        return self.entryCount

    def getFirstCluster(self):
        return self.firstCluster

    def setPath(self, path):
        self.path = path

    def getPath(self):
        return self.path

    def getId(self):
        return self.id;
    
    def getFileName(self):
        if len(self.longFilename)>0:
            return self.longFilename
        else:
            return self.getFullShortname()
            
    def __str__(self):
        output = "-----------------"
        output +="\nPath: " + self.path
        output += "\nLong filename: " + self.longFilename
        output += "\nShort filename: " + self.shortFilename
        if (self.readOnly):
            output += "\n*READ ONLY*"
        if (self.hidden):
            output += "\n*HIDDEN*"
        if (self.system):
            output += "\n*SYSTEM*"
        if (self.volumeId):
            output += "\n*VOLUME ID*"
        if (self.directory):
            output += "\n*DIRECTORY*"
        if (self.archive):
            output += "\n*ARCHIVE*"
        output += "\nCreation time: " + self.creationTime.strftime('%d.%m.%Y %H:%M:%S:%f')
        output += "\nLast Accessed time: " + self.accessedTime.strftime('%d.%m.%Y')
        output += "\nModification time: " + self.modificationTime.strftime('%d.%m.%Y %H:%M:%S')
        output += "\nFirst cluster: " + str(self.firstCluster)
        output += "\nFilesize: " + str(self.entryCount)

        return output





