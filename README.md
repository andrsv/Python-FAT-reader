# Python-FAT-reader
----------------
- Installation -
----------------
Install Python 3.5
Copy src folder to local computer.

------------------------
- What is this program -
------------------------
There are 2 programs available:

fsstat.py
---------
This program takes a dd input file. It generates a md5 sum of the file and 
extracts and prints data from the FAT VBR. The offset of the FAT VBR must be 
specified in bytes with the -o argument. FAT 12/16 and 32 and partyl exFat are 
supported. Tested with Python 3.5.

For FAT32 partitions, size of root directory is wrongly presented as the root 
directory size is not stored in the VBR. 

If there are data in the VBR which the program does not understand, then 
warnings will be printed on the screen together with the resulting data. 

fatlister.py
------------
This program takes a dd input file. The offset of the FAT VBR must be specified 
in bytes with the -o argument. The program extracts data regarding the files in 
a FAT 16 (only FAT 16 is supported) partition. Output will by default be printed 
to screen. An outputfile could optionally be specified with the -f parameter, 
then the output will be in csv format. Tested with Python 2.7 and Python 3.5.

The sourcecode is separated into classes in these files:

FATVbr.py
---------
Reads the FAT12/16/32 Volume Boot Record

Fat.py
------
Reads the first File Allocation Table of a FAT16 partition. It also handles the 
special case of the root-folder.

Directory.py
------------
Reads a directory from disk.

FileEntry.py
------------
Dummy object which stores data for a directory-entry found in Directory.

-----------------------
- Test of the program -
-----------------------
The results of the program has been manually compared with results from 
Sleuthkit's fsstat and output from FTK-imager using 4 image files, 2 with FAT16 
and 2 with FAT32. I have also made unittests which are located in the tests 
folder.

The unit test can be run from any tool which supports running Python unittests 
(unittest.TestCase). I have used LiClipse and Jenkins to run the unit tests. In 
case you do not have such tools available, I have added code so that the 
unittests can be run as standalone scripts. Move the file from /src to /tests 
and then run the Test_*.py scripts with python3.5.

----------------------------------
- How does the fatlister.py work -
----------------------------------
First the VBR is read. For FAT16 (which is the only supported FileSystem) the 
VBR contains information regarding the root directory. The root directory is 
read, and recursively all allocated child-directories are read. The Directory 
class has a cluster-list which is populated from the Fat class. The cluster 
list contains all clusters for the specific Directory. 

---------
- Usage -
---------
usage: fsstat.py [-h] [-o OFFSET] filename

positional arguments:
  filename              The file to read FAT header from

optional arguments:
  -h, --help            show this help message and exit
  -o OFFSET, --offset OFFSET
                        The offset in bytes where the FAT header(VBR) is
                        located


usage: fatlister.py [-h] [-o OFFSET] [-f FILENAMEOUTPUT] [-d] filenameImage

positional arguments:
  filenameImage         The imagefile to read filelist from (dd-image)

optional arguments:
  -h, --help            show this help message and exit
  -o OFFSET, --offset OFFSET
                        The offset in bytes where the FAT header(VBR) is
                        located
  -f FILENAMEOUTPUT, --filenameOutput FILENAMEOUTPUT
                        The file where to output the result
  -d, --showDirectories
                        choose if directories should show in the output
                        