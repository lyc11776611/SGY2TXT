# Written by Cungu E-mail: YC_Lee@whu.edu.cn
# A Python script for reading SEG-Y format seismic data.
# Will read basic headers & data
# More about SEG-Y format please read:
# https://seg.org/Portals/0/SEG/News%20and%20Resources/Technical%20Standards/seg_y_rev2_0-mar2017.pdf
import numpy as np      # Used to save data matrix
import os               # Used to pause....
import binascii as ba   # Used to transform binary into hex.


filename = '0701-0_all.sgy' # The filename of sgy that you want to transform, could use address if it's in other path
outputparfilename = 'SGYparameters.txt'
outputdatafilename = 'SGYdata.txt'



def h2f( objstr , formatcode = 5):
    # This function translate bins data into floats, only support two kinds of float now.
    obj = str(bin(int(bytes.decode(objstr), 16)))
    res = 0
    if int(obj,2)==0:return 0.0
    if(formatcode==5):  # This is to translate binary into IEEE 32-bytes floating points
        obj = '0'*(34-len(obj))+obj[2:34]
        minus = int(obj[0],2)
        expo = int(obj[1:9],2) -127
        nn=0.5
        res = 1
        for c in obj[9:32]:
            res = res + int(c) * nn
            nn=nn/2.0
        res = (-1)** minus * res * 2**(expo)
    if (formatcode == 1): # This is to translate binary into IBM 32-bytes floating points
        obj = '0' * (34 - len(obj)) + obj[2:34]
        minus = int(obj[0], 2)
        expo = int(obj[1:8], 2) - 64
        nn = 0.5
        res = 1
        for c in obj[8:32]:
            res = res + int(c) * nn
            nn = nn / 2.0
        res = (-1) ** minus * res * 2 ** (expo)
    return res

file = open(filename, 'r', encoding="cp500")
TFheader = file.read(3200)                                  # Textual File Header encoded by EBCDIC 'cp500' x 3600
print(TFheader)
file.close()
file = open(filename, 'rb')                         # Binary File Header encoded in binary x 400 b
file.read(3200)
#check = file.read(400)
#print(check)
#os.system('pause')
print("Where not otherwise indicated, a value of zero indicates an unknown or unspecified value.")
JInum = int(ba.b2a_hex(file.read(4)),16)  # Job identification number
print("Job identification number = ", JInum)
Linenum =int(ba.b2a_hex(file.read(4)),16)  # Line number.
print("Line number = ", Linenum)
Reelnum = int(ba.b2a_hex(file.read(4)),16) # Reel number
print("Reel number = ", Reelnum)
Numof_traces_per_ensemble = int(ba.b2a_hex(file.read(2)),16)
if(Numof_traces_per_ensemble==0):Numof_traces_per_ensemble=None
print("Number of data traces per ensemble = ", Numof_traces_per_ensemble)
Numof_AUXtraces_per_ensemble = int(ba.b2a_hex(file.read(2)),16)
print("Number of auxiliary traces per ensemble = ", Numof_AUXtraces_per_ensemble)
Sampinterval= int(ba.b2a_hex(file.read(2)),16)  # Sample interval
# Microseconds (µs) for time data, Hertz (Hz) for frequency data, meters (m) or feet (ft) for depth data.
print("Sample interval = ", Sampinterval, " μs")
OFRSampinterval= int(ba.b2a_hex(file.read(2)),16)  # Sample interval
# Microseconds (µs) for time data, Hertz (Hz) for frequency data, meters (m) or feet (ft) for depth data.
print("Sample interval of original field recording = ", OFRSampinterval, " μs")
Sampnum =int(ba.b2a_hex(file.read(2)),16)  # Number of samples per data trace
print("Number of samples per data trace = ", Sampnum)
OFRSampnum = int(ba.b2a_hex(file.read(2)),16)  # Number of samples per data trace for origin field recording
print("Number of samples per data trace for origin field recording = ", OFRSampnum)
DSformatcode = int(ba.b2a_hex(file.read(2)),16)
# Data sample format code.
#1 = 4-byte IBM floating-point
#2 = 4-byte, two's complement integer
#3 = 2-byte, two's complement integer
#4 = 4-byte fixed-point with gain (obsolete)
#5 = 4-byte IEEE floating-point
#6 = 8-byte IEEE floating-point
#7 = 3-byte two’s complement integer
##9 = 8-byte, two's complement integer
#10 = 4-byte, unsigned integer
#11 = 2-byte, unsigned integer
#12 = 8-byte, unsigned integer
#15 = 3-byte, unsigned integer
#16 = 1-byte, unsigned integer
print("Data sample format code = ", DSformatcode)
print("Finished reading main parameters in file headers")
#os.system('pause')
file.seek(3600,0)
ntr = 0
totaldata=[]
X=[]
Y=[]
###########################以下为部分道头参数进行读取#################################################
rcfieldnum = [] # 野外原始记录号。强烈推荐所有类型的数据使用 9 - 12
trfieldnum = [] # 野外原始记录的道号。强烈推荐所有类型的数据使用 13 - 16
sourcenum = []  # 震源点号――当在相同有效地表位置多于一个记录时使用。 17 - 20
c2cdistance = []  # 从震源中心点到检波器组中心的距离（若与炮激发线方向相反取负） 37 - 40
sourceX = []    # 震源坐标――X	参考坐标系应通过扩展头位置数据文本段识别（见D-1节）。73 - 76
# 若坐标单位为弧度秒、小数度或度/分/秒(DMS)，X值代表经度，Y值代表纬度。
# 正值代表格林威治子午线以东或赤道以北，负值代表南或西。
sourceY = []    # 震源坐标――Y   77 - 80
phoneX = []     # 检波器坐标――X 81 - 84
phoneY = []     # 检波器坐标――Y 85 - 88
corunit = []    # 坐标单位        89 - 90
Windedlayerspeed = []   # 风化层速度（如二进制文件头3255-3256字节指明的ft/s或m/s）91 - 92
starttime = []          # 起始切除时间（毫秒）111 - 112
endtime = []            # 终止切除时间（毫秒）113 - 114
numofpoint = []         # 该道采样点数。强烈推荐所有类型的数据使用 115 - 116
pointinterval = []      # 该道采样间隔（微秒）。 117 - 118
lowestfre = []  # 低截频率（赫兹），若使用 149 - 150
highestfre = [] # 高截频率（赫兹），若使用 151 - 152
#################################################以上#################################################
while(ntr!=Numof_traces_per_ensemble):
    a = file.read(240)
    if(not a):break

    rcfieldnum.append(int(ba.b2a_hex(a[8:12]),16))
    trfieldnum.append(int(ba.b2a_hex(a[12:16]),16))
    sourcenum.append(int(ba.b2a_hex(a[16:20]),16))
    c2cdistance.append(int(ba.b2a_hex(a[36:40]),16))
# 以防出现补码（事实上还真出现了），采用突兀并令人难以忍受的判定...
    temptpar = int(ba.b2a_hex(a[72:76]),16)
    if(temptpar>2147483648):temptpar = temptpar - 4294967296
    sourceX.append(temptpar)

    temptpar = int(ba.b2a_hex(a[76:80]),16)
    if(temptpar>2147483648):temptpar = temptpar - 4294967296
    sourceY.append(temptpar)

    temptpar = int(ba.b2a_hex(a[80:84]),16)
    if(temptpar>2147483648):temptpar = temptpar - 4294967296
    phoneX.append(temptpar)

    temptpar = int(ba.b2a_hex(a[84:88]),16)
    if(temptpar>2147483648):temptpar = temptpar - 4294967296
    phoneY.append(temptpar)

    corunit.append(int(ba.b2a_hex(a[88:90]),16))
    Windedlayerspeed.append(int(ba.b2a_hex(a[90:92]),16))
    starttime.append(int(ba.b2a_hex(a[110:112]),16))
    endtime.append(int(ba.b2a_hex(a[112:114]),16))
    numofpoint.append(int(ba.b2a_hex(a[114:116]),16))
    pointinterval.append(int(ba.b2a_hex(a[116:118]),16))
    lowestfre.append(int(ba.b2a_hex(a[148:150]),16))
    highestfre.append(int(ba.b2a_hex(a[150:152]),16))

    ndata = 0
    totaldata.append([])
    X.append([])
    Y.append([])
    while(ndata<Sampnum):
        tempdata = h2f(ba.b2a_hex(file.read(4)),DSformatcode)
        print(tempdata)
#        os.system('pause')
        totaldata[ntr].append(tempdata)
        print(len(totaldata[ntr]))
        ndata = ndata +1
        X[ntr].append(ntr)
        Y[ntr].append(ndata)
    ntr = ntr + 1
print("Num of traces:",ntr)
#########################################Now it's time to save datas & parameters##################################
np.savetxt(outputdatafilename,np.array(totaldata))
with open(outputparfilename,'w+') as f:
    f.write("Below are the parameters of "+filename+':\n')
    f.write("Where not otherwise indicated, a value of zero indicates an unknown or unspecified value.\n")
    f.write("here is the 3200 bytes Textual header:\n")
    for i in range(0,40):
        f.write(TFheader[i*80:(i+1)*80]+'\n')
    f.write("\nhere are parameters in binary header:\n")
    f.write("Job identification number = "+ str(JInum)+'\n')
    f.write("Line number = "+  str(Linenum)+'\n')
    f.write("Reel number = "+  str(Reelnum)+'\n')
    f.write("Number of data traces per ensemble = "+  str(Numof_traces_per_ensemble)+'\n')
    f.write("Number of auxiliary traces per ensemble = "+  str(Numof_AUXtraces_per_ensemble)+'\n')
    f.write("Sample interval = "+  str(Sampinterval)+ " μs"+'\n')
    f.write("Sample interval of original field recording = "+  str(OFRSampinterval)+ " μs"+'\n')
    f.write("Number of samples per data trace = "+ str(Sampnum)+'\n')
    f.write("Number of samples per data trace for origin field recording = "+  str(OFRSampnum)+'\n')
    f.write("Data sample format code = "+  str(DSformatcode)+'\n')
    f.write("Upon are the information of the binary headers.\n\n")
    f.write("Below are parameters of traces:")
    f.write("Original field record number:")
    for i in range(0,ntr):
        f.write(str(rcfieldnum[i])+' ')
    f.write('\nTrace field record number:')
    for i in range(0,ntr):
        f.write(str(trfieldnum[i])+' ')
    f.write('\nSource number:')
    for i in range(0,ntr):
        f.write(str(sourcenum[i])+' ')
    f.write('\nDistance of centers(phones and sources):')
    for i in range(0,ntr):
        f.write(str(c2cdistance[i])+' ')
    f.write('\nX Coordinates of source:')
    for i in range(0,ntr):
        f.write(str(sourceX[i])+' ')
    f.write('\nY Coordinates of source:')
    for i in range(0,ntr):
        f.write(str(sourceY[i])+' ')
    f.write('\nX Coordinates of phone:')
    for i in range(0,ntr):
        f.write(str(phoneX[i])+' ')
    f.write('\nY Coordinates of phone:')
    for i in range(0,ntr):
        f.write(str(phoneY[i])+' ')
    f.write('\nUnit number of coordinate:')
    for i in range(0,ntr):
        f.write(str(corunit[i])+' ')
    f.write('\nWinded layer''s speed(Why am I writing this?!):')
    for i in range(0,ntr):
        f.write(str(Windedlayerspeed[i])+' ')
    f.write('\nStart time:')
    for i in range(0,ntr):
        f.write(str(starttime[i])+' ')
    f.write('\nEnd time:')
    for i in range(0,ntr):
        f.write(str(endtime[i])+' ')
    f.write('\nNumber of samples:')
    for i in range(0,ntr):
        f.write(str(numofpoint[i])+' ')
    f.write('\nInterval of samples:')
    for i in range(0,ntr):
        f.write(str(pointinterval[i])+' ')
    f.write('\nLowest frequency:')
    for i in range(0,ntr):
        f.write(str(lowestfre[i])+' ')
    f.write('\nHighest frequency:')
    for i in range(0,ntr):
        f.write(str(highestfre[i])+' ')
    f.write("\nUpon are the parameters in binary trace headers")

print('Done.')
