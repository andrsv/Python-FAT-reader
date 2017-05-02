#!/usr/bin/python3.5
import argparse
import FatVbr
import os
import hashlib



def Main():
    ## Read command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="The file to read FAT header from")
    parser.add_argument("-o", "--offset", help="The offset in bytes where the FAT header(VBR) is located", type=int)
    
    arguments = parser.parse_args()
    
    filename = arguments.filename
    
    # Initialize offset
    offset = 0;
    if arguments.offset:
        offset = arguments.offset
    
    # Evaluate the file, and find it's md5 hashsum
    statinfo = os.stat(filename)
    file = open(filename,"rb")
    md5=0
    if (statinfo.st_size<=1000000000):
        data = file.read()    
        md5 = hashlib.md5(data).hexdigest()
    
    # Print information about the file
    printFormatString = "{:<23}{:<}"
    print("File Information")
    print(printFormatString.format("-- Name: ", str(filename)))        
    print(printFormatString.format("-- File Size: ", str(statinfo.st_size) + " bytes."))
    if (md5==0):
        print("-- WARNING: md5 is not supported for files larger than 1GB. (1.000.000.000 bytes")
    else:        
        print(printFormatString.format("-- MD5: ", str(md5)))        
    
    
    #Read and print info from the VBR    
    myFat = FatVbr.FatVbr(open(filename, "rb"),offset)
    myFat.printHeader()
    
    
if __name__ == "__main__":
    Main()