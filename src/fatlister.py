#!/usr/bin/python3.5
import argparse
import FatVbr
import Fat

class Main():
    
    def printString(self,id,path,name,longFilename,deleted,size, accessedDateTime,modifiedDateTime,createdDateTime,startingCluster):
        """Prints a directory-entry to file/standard output"""
        if deleted:
            allocated = "deleted"
        else:
            allocated = "allocated"
        if accessedDateTime != "": 
            accessedDateTime = accessedDateTime.strftime('%d.%m.%Y')
        if modifiedDateTime != "": 
            modifiedDateTime = modifiedDateTime.strftime('%d.%m.%Y %H:%M:%S') 
        if createdDateTime != "": 
            createdDateTime = createdDateTime.strftime('%d.%m.%Y %H:%M:%S:%f')
        if self.arguments.filenameOutput:
            self.outputFile.print(str(id) + "," + path + "," + name + "," + longFilename + "," + allocated + "," + str(size) + "," + accessedDateTime + "," + modifiedDateTime + "," + createdDateTime + "," + str(startingCluster) + ";")
        else:
            print(self.printFormatString.format(id,path + longFilename,allocated,str(size)+"b", accessedDateTime,modifiedDateTime,createdDateTime,startingCluster))
    
    def writeDirToFile(self,directory, fat):#file, clusterList, fatVbr, path, fat):
        """Recursively writes directory-entries to file/standard output"""
        for entry in directory.getAllEntries():
            if not entry.isDirectory():
                self.printString(entry.getId(), entry.getPath(), entry.getShortFilename(), entry.getLongFilename(), entry.isDeleted(), entry.getFileSize(), entry.getAccessedDateTime(), entry.getModifiedDateTime(), entry.getCreationDateTime(), entry.getFirstCluster())
            if entry.isDirectory() and entry.getShortFilename().strip() != "." and entry.getShortFilename().strip() != "..":
                if self.showDirectories:
                    self.printString(entry.getId(), entry.getPath(), entry.getShortFilename(), entry.getLongFilename(), entry.isDeleted(), entry.getFileSize(), entry.getAccessedDateTime(), entry.getModifiedDateTime(), entry.getCreationDateTime(), entry.getFirstCluster())
                if not entry.isDeleted():    
                    self.writeDirToFile(fat.getDirectory(entry), fat)    
    
    def run(self):
        """Prints the files from a FAT16 filesystem to a file or standard output. -h for help."""
        self.printFormatHeader = "{:^10}{:^40}{:^10}{:^12}{:^14}{:^22}{:^27}{:^16}"
        self.printFormatString = "{:^10}{:<40}{:^10}{:>12}{:^14}{:^22}{:^27}{:^16}"
        ## Read command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("filenameImage", help="The imagefile to read filelist from (dd-image)")
        parser.add_argument("-o", "--offset", help="The offset in bytes where the FAT header(VBR) is located", type=int)
        parser.add_argument("-f", "--filenameOutput", help="The file where to output the result", type=argparse.FileType('w'))
        parser.add_argument("-d", "--showDirectories", help="choose if directories should show in the output", action="store_true")
        
        self.arguments = parser.parse_args()
        
        input_filename = self.arguments.filenameImage
        
        # Initialize offset
        offset = 0;
        if self.arguments.offset:
            offset = self.arguments.offset
        
        self.showDirectories = False
        if self.arguments.showDirectories:
            self.showDirectories=True
    
        if self.arguments.filenameOutput:
            self.outputFile=open(self.arguments.filenameOutput,"w")
            
        #Prepare the FAT Volume Boot Record
        fatVbr = FatVbr.FatVbr(open(input_filename, "rb"),offset)
        
        #Prepare the Fat File Allocation Table
        fat = Fat.Fat(open(input_filename, "rb"),offset, fatVbr)
    
        if self.arguments.filenameOutput:
            self.outputFile.print("Id,Path,Name,LFN,Allocated,Size,Accessed,Modified,Created,Starting Cluster;")
        else:
            print(self.printFormatHeader.format("Id","File","Allocated","Size","Accessed","Modified","Created","Starting Cluster"))
        
        rootDir = fat.getRootDirectory()
        if self.showDirectories:
            self.printString(0, "", "/", "/", False, 0, "", "", "", rootDir.clusterlist[0])
        #recursively write everything under root to File
        self.writeDirToFile(rootDir, fat)

        
if __name__ == "__main__":
    main = Main()
    main.run()
    
    