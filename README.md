# SGY2TXT
A Python script to translate SEG-Y seismic record file into txt files. 
If there's any bug, please contact me at: YC_Lee@WHU.edu.cn

This script helps to translate SEG-Y file into two txt files. 
One of the files, named 'outputparfilename' in the script, stores some important (or may not be so important) parameters of the SGY file including its 3200-bytes textual file header, some parameters in binary file header and trace headers.
Another file, named 'outputdatafilename' in the script, stores seismic data of the SGY file using numpy.savetxt()

The script uses numpy and binascii. While numpy only serves to save the data, binascii uses to translate binary into hexadecimal bytes.

Hope it can help.(～￣▽￣)～
