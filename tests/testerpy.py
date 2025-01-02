
import sys
from c_wrpcc import *

from math import  fabs
import os

cb1count, cb1count2, cb2count, cb3count = 0, 0, 0, 0
cb1f, cb1f2, cb2f, cb3f, cb4f, cb5f = 0, 0, 0, 0, 0, 0
myerrcnt = 0
tptr, tptr2 = new_wrpHandle_tp(), new_wrpHandle_tp()

# intp, charp
def wrperror(rc, s):
    intp_assign(rc, intp_value(rc) + 1)
    print(s)

#int, charp 
def msg1Callback(mode, msgBuf):
    print("in msg1CB")
    global cb1count
    global cb1f
    cb1count = cb1count + 1
    if mode == 0:
        if msgBuf != "Hello G":
            cb1f = cb1f + 1
    elif mode == 1:
        if msgBuf != "Hello A":
            cb1f = cb1f + 1
    elif mode == 2:
        if msgBuf != "Hello M":
            cb1f = cb1f + 1
    elif mode == 3:
        if msgBuf != "Hello S":
            cb1f = cb1f + 1
            
#int, charp 
def msg1Callback2(mode, msgBuf):
    print("in msg1CB2")
    global cb1count2
    global cb1f2
    cb1count2 = cb1count2 + 1
    if mode == 0:
        if msgBuf != "Hello G":
            cb1f2 = cb1f2 + 1     
    elif mode == 1:
        if msgBuf != "Hello A":
            cb1f2 = cb1f2 + 1
    elif mode == 2:
        if msgBuf != "Hello M":
            cb1f2 = cb1f2 + 1
    elif mode == 3:
        if msgBuf != "Hello S":
            cb1f2 = cb1f2 + 1

#ToDo----------------------------------------------------
def msg2Callback(mode, msgBuf):
    global cb2count
    global cb2f
    
#ToDo
def allTypes(pntr, ntgr, cptrda, cptria, cptrc, csst, dbl, b, chr):
    print("in allTypes")
    global cbf4
    msg = "string"
    # strncpy(msg,csst+1,csst[0]); msg[csst[0]]='\0';
    
    #if((int) pntr%1 != 0)             cb4f++;
    if ntgr != 1:
        cb4f += 1
    if cptrc != "GAMS":
        cb4f += 1
    if msg != "GAMS":
        cb4f += 1
    if fabs(dbl - 3.14159265) > 1e-6:
        cb4f += 1
    if not b:
        cb4f += 1
    if chr != 'G':
        cb4f += 1
    for i in range(3):
        if fabs(cptrda[i] - (i+1) * 3.14159265) > 1e-6:
            cb4f += 1
    for i in range(3):
        if cptria[i] != (i+1) * 123:
            cb4f += 1

#ToDo
def gdxTypes():
    pass


def myerrorcb(errcnt, msgBuf):
    #intp_assign(errcnt, intp_value(errcnt) + 1)
    global myerrcnt
    myerrcnt += 1
    #print(msgBuf)
    return 0


if __name__ == "__main__":
    rcall = new_intp()
    intp_assign(rcall, 0)

    pda = doubleArray(3)
    pia = intArray(3)

    cp = "string"
    uel = intArray(GMS_MAX_INDEX_DIM)
    val = doubleArray(GMS_VAL_MAX)
    vrvval = doubleArray(GMS_VAL_MAX)
    sv = doubleArray(GMS_SVIDX_MAX)
    p = None
   

    print("Start of testerpy.py")
    
    print("LibLoad Test")
    ret, sst = wrpCreateL(tptr,"xyzdclib",GMS_SSSIZE)
    if ret:
        wrperror(rcall,"*** LibLoad Test Failed: Create should return 0")
    #if (None != tptr):
    #    wrperror(rcall,"*** LibLoad Test Failed: Pointer should be None")
    if (sst == ""):
        wrperror(rcall,"*** LibLoad Test Failed: Msg should not be empty");

    ret, sst = wrpCreate(tptr,GMS_SSSIZE)
    if ret == 0:
        print("Could not create wrapper object:" + sst)
        os._exit(1)

    #ToDo
    #print("PTRPROP Test")
    #wrperror(rcall,"*** PTRPROP Test failed!");
    #
    #p = wrpptrP(tptr)

    #ToDo
    #print("PTR Test")
    #if wrpptr2(tptr,p):
    #    wrperror(rcall,"*** PTR2 Test failed!")
    #if wrpptr1(tptr,p):
    #    wrperror(rcall,"*** PTR1 Test failed!")
    
    print("INT1 Test")
    if wrpint1(tptr,123):
        wrperror(rcall,"*** INT1 Test failed!");

    print("INT2 Test")
    ret, x = wrpint2(tptr, 321)
    if ret:
        wrperror(rcall,"*** INT2 Test failed (passing data to library)!")
    if wrpint1(tptr, x):
        wrperror(rcall,"*** INT2 Test failed (getting data from library)!")

    print("INT64 Test")
    xx = 987654321*987654321
    if wrpint64(tptr,xx):
        wrperror(rcall,"*** INT64 Test failed!");

    print("VINT64 Test")
    xx = 123456789*123456789
    ret, x = wrpvint64(tptr, xx)
    if ret:
        wrperror(rcall,"*** VINT64 Test failed (passing data to library)!")
    if wrpint64(tptr, x):
        wrperror(rcall,"*** VINT64 Test failed (getting data from library)!")

    print("OINT64 Test")
    xx = 0
    ret, x = wrpoint64(tptr, xx)
    if ret:
        wrperror(rcall,"*** OINT64 Test failed (getting data from library)!")
    if wrpint64(tptr, x):
        wrperror(rcall,"*** OINT64 Test failed (getting data from library)!")

    print("PDA1 Test")
    for i in range(3):
        pda[i] = (i+1)*3.14159265
    if wrppda1(tptr,pda):
        wrperror(rcall,"*** PDA1 Test failed!");

    print("PDA2 Test")
    if wrppda2(tptr,pda):
        wrperror(rcall,"*** PDA2 Test failed (passing data to library)!")
    x = 0
    for i in range(3):
        x += wrpdbl1(tptr,pda[i])
    if x:
        wrperror(rcall,"*** PDA2 Test failed (getting data from library)!");

    print("PIA1 Test")
    for i in range(3):
        pia[i] = (i+1)*123
    if wrppia1(tptr,pia) > 0:
        wrperror(rcall,"*** PIA1 Test failed!")

    print("PIA2 Test")
    if wrppia2(tptr,pia):
        wrperror(rcall,"*** PIA2 Test failed (passing data to library)!")
    x = 0
    for i in range(3):
        x += wrpint1(tptr,pia[i])
    if x:
        wrperror(rcall,"*** PIA2 Test failed (getting data from library)!")
    
    print("PC1 Test")
    if wrppc1(tptr,"GAMS"):
        wrperror(rcall,"*** PC1 Test failed!")

    print("PC2 Test")
    ret, cp = wrppc2(tptr,"XXXX")
    if ret:
        wrperror(rcall,"*** PC2 Test failed (passing data to library)!")
    if cp != "GAMS":
        wrperror(rcall,"*** PC2 Test failed (getting data from library)!");

    print("CHAR1  Test")
    if wrpC1(tptr,'G'):
        wrperror(rcall,"*** CHAR1 Test failed!")

    print("CHAR2  Test")
    ret, d = wrpC2(tptr, "X")
    if ret:
        wrperror(rcall,"*** CHAR2 Test failed (passing data to library)!")
    if wrpC1(tptr,d):
        wrperror(rcall,"*** CHAR2 Test failed (getting data from library)!")

    print("SST1 Test")
    if wrpsst1(tptr,"Hello GAMS"):
        wrperror(rcall,"*** SST1 Test failed!")

    print("SST2 Test")
    ret, sst = wrpsst2(tptr)
    if wrpsst1(tptr,sst) or sst != "Hello GAMS":
        wrperror(rcall,"*** SST2 Test failed!")
    
    print("SST3 Test")
    ret, sst = wrpsst3(tptr,GMS_SSSIZE)
    if wrpsst1(tptr,sst):
        wrperror(rcall,"*** SST3 Test failed!")
    
    print("DBL1 Test")
    if wrpdbl1(tptr,3.14159265):
        wrperror(rcall,"*** DBL1 Test failed!")

    print("DBL2 Test")
    y2 = 3.14159265*3.14159265
    ret, y = wrpdbl2(tptr,y2)
    if ret:
        wrperror(rcall,"*** DBL2 Test failed (passing data to library)!")
    if wrpdbl1(tptr,y):
        wrperror(rcall,"*** DBL2 Test failed (getting data from library)!")

    print("UELI1 Test")
    for i in range(GMS_MAX_INDEX_DIM):
        uel[i] = (i+1)*123;
    if wrpueli1(tptr,uel) > 0:
        wrperror(rcall, "*** UELI1 Test failed!");

    # Fail running clib but not dlib so far
    print("UELI2 Test")
    ret, uel = wrpueli2(tptr)
    x = 0
    for i in range(GMS_MAX_INDEX_DIM):
        x += wrpint1(tptr,uel[i])
    if x:
        wrperror(rcall,"*** UELI2 Test failed!")

    '''
    print("vII Test")
    for i in range(GMS_MAX_INDEX_DIM):
        uel[i] = (i+1)*123;
    ret, uel = wrpvII(tptr)
    print("  py1 ret=", ret)
    for i in range(GMS_MAX_INDEX_DIM):
        x += wrpint1(tptr, uel[i])
        print("   ", i, "x=", x, " uel[i]=",uel[i]," wrpint1(tptr,uel[i])=",wrpint1(tptr,uel[i]))
    if x:
        wrperror(rcall,"*** vII Test failed (passing integer array in and out of library)! ")

    print("vRV Test")
    for i in range(GMS_VAL_MAX):
        vrvval[i] = (i+1)*3.14159265;
    ret, vrvval = wrpvII(tptr)
    print("  py1 ret=", ret)
    for i in range(GMS_VAL_MAX):
        x += wrpdbl1(tptr,vrvval[i])
        print("   ", i, "x=", x, " val[i]=",vrvval[i]," wrpdbl1(tptr,dbl[i])=",wrpdbl1(tptr,vrvval[i]))
    if x:
        wrperror(rcall,"*** vRV Test failed (passing double array in and out of library)! ")
    '''

    print("VALS1 Test")
    for i in range(GMS_VAL_MAX):
        val[i] = (i+1)*3.14159265
    if wrpvals1(tptr,val) > 0:
        wrperror(rcall,"*** VALS1 Test failed!")

    print("VALS2 Test")
    ret, val = wrpvals2(tptr)
    x = 0
    for i in range(GMS_VAL_MAX):#
        x += wrpdbl1(tptr,val[i])
    if x:
        wrperror(rcall,"*** VALS2 Test failed! ")
    
    print("STRI1 Test")
    pdim = []
    for i in range(GMS_MAX_INDEX_DIM):
        pdim.append("dim" + str(i+1))
    if wrpstri1(tptr, pdim) > 0:
        wrperror(rcall,"*** STRI1 Test failed!")

    print("STRI2 Test")
    ret, pdim = wrpstri2(tptr)
    for i in range(GMS_MAX_INDEX_DIM):
        sst = "j" + str(i+1)
        if sst != pdim[i]:
            wrperror(rcall,"*** STRI2 Test failed!")
            break;
    
    print("SVALS1 Test")
    for i in range(GMS_SVIDX_MAX):
        sv[i] = (i+1)*3.14159265
    if wrpsvals1(tptr,sv) > 0:
        wrperror(rcall,"*** SVALS1 Test failed!")

    print("SVALS2 Test")
    if wrpsvals2(tptr,sv):
        wrperror(rcall,"*** SVALS2 Test failed (passing data to library)!")
    x = 0
    for i in range(GMS_SVIDX_MAX):
        x += wrpdbl1(tptr,sv[i])
    if x:
        wrperror(rcall,"*** SVALS2 Test failed (getting data from library)!")
    
    print("BOOL Test")
    if wrpbool1(tptr, True):
        wrperror(rcall,"*** BOOL Test failed (passing data to library)!")
    
    print("BOOL2 Test")
    x = new_intp()
    intp_assign(x, 0)
    if wrpbool2(tptr,x):
        wrperror(rcall,"*** BOOL2 Test failed (passing data to library)!")
    if wrpbool1(tptr,intp_value(x)):
        wrperror(rcall,"*** BOOL2 Test failed (getting data from library)!")

    print("MAXARG Test")
    if wrpMaxArg(tptr,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20) != 21*20/2:
        wrperror(rcall,"*** MAXARG Test failed!")
    
    #ToDo
    #print("ALLARGCB Test")
    #wrperror(rcall,"*** ALLARGCB Test failed!")

    #ToDo
    #print("GDXARGCB Test")
    #wrperror(rcall,"*** GDXARGCB Test failed!")

    #ToDo--------------------------------------------------------------------------
    #print("MCB Test")
    #ret, sst = wrpCreate(tptr2,GMS_SSSIZE)
    #if not ret:
    #    print("Could not create wrapper object: "+sst)
    

    #PYwrpsetmcb1(tptr, msg1Callback)
    #
    #print("-----callback-start----------------------")
    #wrpinitmcb(tptr);
    #print("-----callback-end----------------------")

    #PYwrpsetmcb1(tptr,msg1Callback)
    #PYwrpsetmcb1(tptr2,msg1Callback2)
    #PYwrpsetmcb2(tptr,msg2Callback)
    #wrpinitmcb(tptr)
    #wrpinitmcb(tptr2)
    
    
    #if cb1f or cb1count != 4:
    #    wrperror(rcall,"*** MCB1 Test failed!")
    #if cb1f2 or cb1count2 != 4:
    #    wrperror(rcall,"*** MCB1 Test failed! (Problem with 2nd object)")
    #if cb2f or cb2count != 4:
    #    wrperror(rcall,"*** MCB2 Test failed!")
    #-------------------------------------------------------------------------------
            
    #ToDo
    #print("FUNCPTR Test")
    #wrperror(rcall,"*** FUNCPTR Test failed!")
    
    print("INTPROP Test")
    wrpintPSet(tptr, 123)
    if wrpintP(tptr) != 2*123:
        wrperror(rcall, "*** INTPROP Test failed!")
    
    print("INT64PROP Test")
    xx = 987654321*987654321
    wrpint64PSet(tptr, xx)
    if wrpint64P(tptr) != xx*2:
        wrperror(rcall, "*** INT64PROP Test failed!")
    
    print("PCPROP Test")
    wrpPCPSet(tptr,"GAMS");
    if wrpPCP(tptr) != "GUMS":
        wrperror(rcall, "*** PCPROP Test failed!")
    
#    if not clibuse:
#       print("SSTPROP Test")
#       wrpSSPSet(tptr,"SMAG")
#       cp = wrpSSP(tptr)
#       if cp != "SMUG":
#           wrperror(rcall, "*** SSTPROP Test failed!")
    
    print("CHARPROP Test")
    wrpCPSet(tptr, 'G')
    if wrpC1(tptr, wrpCP(tptr)) > 0:
        wrperror(rcall, "*** CHARPROP Test failed!")
    
    print("DBLPROP Test")
    wrpDPSet(tptr, 3.14159265*3.14159265)
    if wrpdbl1(tptr, wrpDP(tptr)):
        wrperror(rcall, "*** DBLPROP Test failed!")
    
    print("BOOLPROPa Test")
    wrpboolPSet(tptr, True)
    if wrpboolP(tptr):
        wrperror(rcall, "*** BOOLPROPa Test failed!")
         
    print("BOOLPROPb Test")
    wrpboolPSet(tptr, False);
    if not wrpboolP(tptr):
        wrperror(rcall, "*** BOOLPROPb Test failed!")
    
    print("PTRRET Test")
    if wrpptr1(tptr, wrpptrR(tptr)):
        wrperror(rcall, "*** PTRRET Test failed!")
    
    print("INTRET Test")
    if wrpint1(tptr, wrpintR(tptr)):
        wrperror(rcall, "*** INTRET Test failed!")
      
    print("INT64RET Test")
    if wrpint64(tptr, wrpint64R(tptr)):
        wrperror(rcall, "*** INT64RET Test failed!")
      
    print("PCRET Test")
    if wrppc1(tptr, wrpPCR(tptr, "GAMS")) != 0:
        wrperror(rcall, "*** PCRET Test failed!")
    
#    if not clibuse:
#       print("SSTRET Test")
#       cp = wrpSSTR(tptr)
#       if cp != "Return GAMS":
#           wrperror(rcall, "*** SSTRET Test failed!")
    
    print("DBLRET Test")
    if wrpdbl1(tptr, wrpDR(tptr)):
        wrperror(rcall, "*** DBLRET Test failed!")
    
    print("BOOLRET Test")
    if not wrpboolR(tptr):
        wrperror(rcall, "*** BOOLRET Test failed!")
    
    #ToDo
    #print("FPTRRET Test")
    #wrperror(rcall, "*** FPTRRET Test failed!")
    
    print("CHARRET Test")
    if wrpC1(tptr, wrpCR(tptr)):
        wrperror(rcall,"*** CHARRET Test failed!")
    
    '''ToDo----------------------------------------------------------
     
    wrpSetScreenIndicator(0)
    wrpSetExitIndicator(0)
    
    #ToDo
    #wrpSetErrorCallback(myerrorcb)

    #ToDo
    print("DIFFARG1 Test")
    wrpdiffargs1(tptr, intp_value(x));
    if wrpGetAPIErrorCount() != 1 or myerrcnt != 1:
        wrperror(rcall, "*** DIFFARG1 Test failed!")
    
    #ToDo
    print("DIFFARG2 Test")
    wrpdiffargs2(tptr, intp_value(x))
    if wrpGetAPIErrorCount() != 2 or myerrcnt != 2:
        wrperror(rcall, "*** DIFFARG2 Test failed!")
    

    #ToDo
    print("NOENTRY Test")
    wrpisnotthere(tptr)
    if wrpGetAPIErrorCount() != 3 or myerrcnt != 3:
        wrperror(rcall, "*** NOENTRY Test failed!")


    #ToDo
    print("DIFFARGPROP Test")
    wrpdiffargsPSet(tptr,y)
    if wrpGetAPIErrorCount() != 4 or myerrcnt != 4:
        wrperror(rcall, "*** DIFFARGPROP Test failed!")

    #ToDo
    print("NOENTRYPROP Test")
    wrpnotthereP(tptr);
    if wrpGetAPIErrorCount() != 5 or myerrcnt != 5:
        wrperror(rcall, "*** NOENTRYPROP Test failed!")
    
    --------------------------------------------------------------------'''

    print("Constants Test")
    intVar = wrpIntValue
    if intVar != 64:
        wrperror(rcall,"*** Integer Constant Type Test failed!")

    intVar = wrpInt_A
    if intVar != 0:
        wrperror(rcall,"*** Integer Constant Type A Test failed!")
    intVar = wrpInt_B
    if intVar != 1:
        wrperror(rcall,"*** Integer Constant Type B Test failed!")
    intVar = wrpInt_C
    if intVar != 2:
        wrperror(rcall,"*** Integer Constant Type C Test failed!")

    floatValue = wrpFloatValue
    if abs(floatValue + 0.148759) > 0.0001 :
        wrperror(rcall,"*** Float Constant Test failed!")
    
    strValue = wrpStringValue
    if strValue != 'StringValue' :
        wrperror(rcall, "*** String Constant Test failed!")

    strValue = wrpString_Option1 
    if strValue != 'First Option' :
        wrperror(rcall, "*** String Option1 Constant Test failed!")

    strValue = wrpString_Option2
    if strValue != 'Second Option' : 
        wrperror(rcall, "*** String Option2 Constant Test failed!")

    strValue = wrpString_Option3
    if strValue != 'Third Option' :
        wrperror(rcall, "*** String Option3 Constant Test failed!")

    wrpFree(tptr)
    print("End of testerpy.py, "+ str(intp_value(rcall))+" failure(s)")
    
    exit(intp_value(rcall))
