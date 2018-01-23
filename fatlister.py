#!/usr/bin/python3.5
import argparse
from FAT import FatVbr
from FAT import FatTable
import os

class Main():
    
    def printString(self, entry):
        """Prints a directory-entry to file/standard output"""
        if entry.isDeleted():
            allocated = "deleted"
        else:
            allocated = "allocated"
        accessedDateTime = entry.getAccessedDateTime()
        modifiedDateTime = entry.getModifiedDateTime()
        createdDateTime = entry.getCreationDateTime()
        if accessedDateTime != "": 
            accessedDateTime = accessedDateTime.strftime('%d.%m.%Y')
        if modifiedDateTime != "": 
            modifiedDateTime = modifiedDateTime.strftime('%d.%m.%Y %H:%M:%S') 
        if createdDateTime != "": 
            createdDateTime = createdDateTime.strftime('%d.%m.%Y %H:%M:%S:%f')
        if self.arguments.filenameOutput:
            self.outputFile.write(str(entry.getId()) + "," + entry.getPath() + "," + entry.getFullShortname() + "," + entry.getLongFilename() + "," + allocated + "," + str(entry.getFileSize()) + "," + accessedDateTime + "," + modifiedDateTime + "," + createdDateTime + "," + str(entry.getFirstCluster()) + ";\n")
        else:
            print(self.printFormatString.format(entry.getId(),entry.getPath() + entry.getFileName(),allocated,str(entry.getFileSize())+"b", accessedDateTime,modifiedDateTime,createdDateTime,entry.getFirstCluster()))
    
    def writeDirToFile(self,directory, fat):#file, clusterList, fatVbr, path, fat):
        """Recursively writes directory-entries to file/standard output"""
        for entry in directory.getAllEntries():
            if not entry.isDirectory():
                self.printString(entry)
            if entry.isDirectory() and entry.getShortFilename() != "." and entry.getShortFilename() != "..":
                if self.showDirectories:
                    self.printString(entry)
                if not entry.isDeleted():    
                    self.writeDirToFile(fat.getDirectory(entry), fat)    
    
    def run(self):
        """Prints the files from a FAT16 filesystem to a file or standard output. -h for help."""
        self.printFormatHeader = "{:^10}{:^75}{:^10}{:^12}{:^14}{:^22}{:^27}{:^16}"
        self.printFormatString = "{:^10}{:<75}{:^10}{:>12}{:^14}{:^22}{:^27}{:^16}"
        ## Read command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("filenameImage", help="The imagefile to read filelist from (dd-image)")
        parser.add_argument("-o", "--offset", help="The offset in bytes where the FAT header(VBR) is located", type=int)
        parser.add_argument("-f", "--filenameOutput", help="The file where to output the result", type=argparse.FileType('w'))
        parser.add_argument("-d", "--showDirectories", help="choose if directories should show in the output", action="store_true")
        
        self.arguments = parser.parse_args()
        
        input_filename = self.arguments.filenameImage
        
        if not os.path.exists(input_filename):
            print ("Input file: " + input_filename + " does not exist.")
            exit()
        
        if not os.access(input_filename, os.R_OK):
            print ("You do not have access to read input file: " + input_filename + ".")
            exit()
        
        # Initialize offset
        offset = 0;
        if self.arguments.offset:
            offset = self.arguments.offset
        
        self.showDirectories = False
        if self.arguments.showDirectories:
            self.showDirectories=True
    
        if self.arguments.filenameOutput:
            self.outputFile=self.arguments.filenameOutput
            
        #Prepare the FAT Volume Boot Record
        fatVbr = FatVbr.FatVbr(open(input_filename, "rb"),offset)

        #Check that the VBR does not contain errors/warnings
        if (fatVbr.getFatType()!="FAT16"):
            fatVbr.printHeader()
            print("This FAT(" + fatVbr.getFatType() + "?) is not supported. Only FAT16 systems are supported.")
            exit()
        if (fatVbr.hasWarnings() or fatVbr.isInvalid()):
            print(fatVbr.getWarningsAsString())
            print(fatVbr)
            confirm = input("There is something wrong with the Vbr. Do you wish to continue (y/n)?")
            if confirm.upper()!="Y":
                exit()

        #Prepare the Fat File Allocation Table
        fat = FatTable.FatTable(open(input_filename, "rb"),offset, fatVbr)
    
        if self.arguments.filenameOutput:
            self.outputFile.write("Id,Path,Name,LFN,Allocated,Size,Accessed,Modified,Created,Starting Cluster;\n")
        else:
            print(self.printFormatHeader.format("Id","File","Allocated","Size","Accessed","Modified","Created","Starting Cluster"))
        
        rootDir = fat.getRootDirectory()
        if self.showDirectories:
            if self.arguments.filenameOutput:
                self.outputFile.write("0,[root directory],,,allocated,0,,,," + str(rootDir.clusterlist[0]) + ";\n")
            else:
                print(self.printFormatString.format(0,"[root directory]","allocated","0b", "", "", "",rootDir.clusterlist[0]))
        #recursively write everything under root to File
        self.writeDirToFile(rootDir, fat)

        
if __name__ == "__main__":
    main = Main()
    main.run()
