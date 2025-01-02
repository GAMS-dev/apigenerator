package com.gams.tester;

import com.gams.api.*;

public class testerjava {

static int cb1count=0, cb2count=0, cb3count=0;
static long optr1=1;
static int cb1f=0, cb2f=0, cb3f=0, cb4f=0, cb5f=0;
static int myerrcnt=0;

static void wrperror(int[] rc, String s) {
  rc[0]++;
  System.out.println(s);
}

private static void msg1Callback (int mode, String msgBuf)
{
  cb1count++;
  switch (mode) {
  case 0: if (msgBuf.compareTo("Hello G") != 0) cb1f++; break;
  case 1: if (msgBuf.compareTo("Hello A") != 0) cb1f++; break;
  case 2: if (msgBuf.compareTo("Hello M") != 0) cb1f++; break;
  case 3: if (msgBuf.compareTo("Hello S") != 0) cb1f++; break;
  }
} /* msg1Callback */

private static void msg2Callback (int mode, String msgBuf)
{
  cb2count++;
  switch (mode) {
  case 0: if (msgBuf.compareTo("Hello G") != 0) cb2f++; break;
  case 1: if (msgBuf.compareTo("Hello A") != 0) cb2f++; break;
  case 2: if (msgBuf.compareTo("Hello M") != 0) cb2f++; break;
  case 3: if (msgBuf.compareTo("Hello S") != 0) cb2f++; break;
  }
} /* msg2Callback */

private static void allTypes (long pntr, int ntgr, double[] cptrda, int[] cptria, String cptrc, String csst, double dbl, int b, char chr)
{
  int i;

  if((int) pntr%1 != 0)                 cb4f++;
  if(ntgr != 1)                         cb4f++;
  if(cptrc.compareTo("GAMS") > 0)       cb4f++;
  if(csst.compareTo("GAMS") > 0)        cb4f++;
  if(Math.abs(dbl - 3.14159265) > 1e-6) cb4f++;
  if(b != 1)                            cb4f++;
  if(chr != 'G')                        cb4f++;
  for(i=0;i<3;i++) if(Math.abs(cptrda[i] - (i+1) * 3.14159265) > 1e-6) cb4f++;
  for(i=0;i<3;i++) if(cptria[i] != (i+1) * 123)                        cb4f++;
} /* alltypes */

private static void gdxTypes (int[] ntgri, double[] recv, String[] ssti, double[] sval)
{
  int i;

  for(i=0; i<gamsglobals.maxdim; i++)   if(ntgri[i]!=(i+1)*123)                     cb5f++;
  for(i=0; i<gamsglobals.val_max; i++)  if(Math.abs(recv[i] - i*3.14159265) > 1e-6) cb5f++;
  /*for(i=0; i<gamsglobals.maxdim; i++) if(ssti[i].compareTo("j" +(i+1))>0)         cb5f++;*/
  for(i=0; i<gamsglobals.sv_max; i++)   if(Math.abs(sval[i] - i*3.14159265) > 1e-6) cb5f++;
} /* gdxtypes */

static int myerrorcb (int errcnt, String msgBuf)
{
  myerrcnt++;
  System.out.println(msgBuf);
  return 0;
}
public static void main(String[] args) {

  int i,j,x;
  int[] xx = new int[1];
  long[] yy = new long[1];
  int[] rcall = new int[1];
  double[] y = new double[1];
  long[] p = new long[1];
  double[] pda = new double[3];
  int[] pia = new int[3];
  String[] sst = new String[1];
  String[] Msg = new String[1];
  char[] d = new char[1];
  boolean[] e = new boolean[1];
  int[] uel = new int[gamsglobals.maxdim];
  double[] val = new double[gamsglobals.val_max];
  String[] pdim = new String[gamsglobals.maxdim];
  double[] sv = new double[gamsglobals.sv_max];
  int[] Tptr= new int[1];
  c_wrp wrp = new c_wrp();

  rcall[0] = 0;

  System.out.println("Start of testerjava");
  System.out.println("LibLoad Test");
  if (wrp.CreateL("xyzdclib",Msg) != 0) wrperror(rcall,"*** LibLoad Test Failed: Create should return 0");
  if (wrp.GetwrpPtr() != 0 )            wrperror(rcall,"*** LibLoad Test Failed: Pointer should be NULL");
  if (Msg[0].compareTo("") == 0)        wrperror(rcall,"*** LibLoad Test Failed: Msg should not be empty");
  wrp.Create(Msg);
  if (0==wrp.GetwrpPtr()) {
    System.out.println("Could not create wrapper object: " + Msg[0]);
    System.exit(1);
  }

  System.out.println("PTR Test");
  p[0] = 0;
  wrp.ptr2(p);
  if (wrp.ptr1(p[0]) != 0) wrperror(rcall,"*** PTR Test failed!");

  System.out.println("INT1 Test");
  if (wrp.int1(123) != 0) wrperror(rcall,"*** INT1 Test failed!");

  System.out.println("INT2 Test");
  wrp.int2(xx);
  if (wrp.int1(xx[0]) != 0) wrperror(rcall,"*** INT2 Test failed!");

  System.out.println("INT64 Test");
  if (wrp.int64((long)987654321*987654321) != 0) wrperror(rcall,"*** INT64 Test failed!");

  System.out.println("VINT64 Test");
  yy[0] = (long)123456789*123456789;
  wrp.vint64(yy);
  if (wrp.int64(yy[0]) != 0) wrperror(rcall,"*** VINT64 Test failed!");

  System.out.println("OINT64 Test");
  yy[0] = (long)0;
  wrp.oint64(yy);
  if (wrp.int64(yy[0]) != 0) wrperror(rcall,"*** OINT64 Test failed!");

  System.out.println("PDA1 Test");
  for(i=0; i<3; i++) pda[i] = (i+1)*3.14159265;
  if (wrp.pda1(pda) != 0) wrperror(rcall,"*** PDA1 Test failed!");

  System.out.println("PDA2 Test");
  wrp.pda2(pda);
  x=0; for (i=0; i<3; i++)
      x += wrp.dbl1(pda[i]);
  if (x != 0) wrperror(rcall,"*** PDA2 Test failed!");

  System.out.println("PIA1 Test");
  for(i=0; i<3; i++) pia[i] = (i+1)*123;
  if (wrp.pia1(pia)>0) wrperror(rcall,"*** PIA1 Test failed!");

  System.out.println("PIA2 Test");
  wrp.pia2(pia);
  x=0; for (i=0; i<3; i++)
      x += wrp.int1(pia[i]);
  if (x != 0) wrperror(rcall,"*** PIA2 Test failed!");

  System.out.println("PC1 Test");
  if (wrp.pc1("GAMS") !=0 ) wrperror(rcall,"*** PC1 Test failed!");

  System.out.println("PC2 Test");
  wrp.pc2(sst);
  if (sst[0].compareTo("GAMS")!=0) wrperror(rcall,"*** PC2 Test failed!");

  System.out.println("SST1 Test");
  if (wrp.sst1("Hello GAMS") != 0) wrperror(rcall,"*** SST1 Test failed!");

  System.out.println("SST2 Test");
  sst[0] = ""; wrp.sst2(sst);
  if (wrp.sst1(sst[0]) != 0) wrperror(rcall,"*** SST2 Test failed!");

  System.out.println("SST3 Test");
  sst[0] = ""; wrp.sst3(sst);
  if (wrp.sst1(sst[0]) != 0) wrperror(rcall,"*** SST3 Test failed!");

  System.out.println("DBL1 Test");
  if (wrp.dbl1(3.14159265) != 0) wrperror(rcall,"*** DBL1 Test failed!");

  System.out.println("DBL2 Test");
  y[0] = 3.14159265*3.14159265; wrp.dbl2(y);
  if (wrp.dbl1(y[0]) != 0) wrperror(rcall,"*** DBL2 Test failed!");

  System.out.println("UELI1 Test");
  for(i=0; i<gamsglobals.maxdim; i++) uel[i] = (i+1)*123;
  if (wrp.ueli1(uel)>0) wrperror(rcall,"*** UELI1 Test failed!");

  System.out.println("UELI2 Test");
  wrp.ueli2(uel); x=0; for (i=0; i<gamsglobals.maxdim; i++) { 
    x += wrp.int1(uel[i]);
  }
  if (x != 0) wrperror(rcall,"*** UELI2 Test failed!");

  System.out.println("vII Test");
  for(i=0; i<gamsglobals.maxdim; i++) uel[i] = (i+1)*123;
  wrp.vII(uel);
  for (i=0; i<gamsglobals.maxdim; i++) { 
    x += wrp.int1(uel[i]);
  }
  if (x != 0) wrperror(rcall,"*** vII Test failed!");

  System.out.println("VRV Test");
  for(i=0; i<gamsglobals.val_max; i++) val[i] = (i+1)*3.14159265;
  wrp.vRV(val); 
  x=0; for (i=0; i<gamsglobals.val_max; i++) x += wrp.dbl1(val[i]);
  if (x != 0) wrperror(rcall,"*** VRV Test failed!");
  
  System.out.println("VALS1 Test");
  for(i=0; i<gamsglobals.val_max; i++) val[i] = (i+1)*3.14159265;
  if (wrp.vals1(val)>0) wrperror(rcall,"*** VALS1 Test failed!");

  System.out.println("VALS2 Test");
  wrp.vals2(val); x=0; for (i=0; i<gamsglobals.val_max; i++) x += wrp.dbl1(val[i]);
  if (x != 0) wrperror(rcall,"*** VALS2 Test failed!");

  System.out.println("STRI1 Test");
  for(i=0; i<gamsglobals.maxdim; i++) pdim[i] = "dim" + (i+1);
  if (wrp.stri1(pdim)>0) wrperror(rcall,"*** STRI1 Test failed!");

  System.out.println("STRI2 Test");
  wrp.stri2(pdim);
  for(i=0; i<gamsglobals.maxdim; i++) {
    sst[0] = "j" + (i+1);
    if (sst[0].compareTo(pdim[i]) != 0) {
      wrperror(rcall,"*** STRI2 Test failed!");
      break;
    }
  }

  System.out.println("SVALS1 Test");
  for(i=0; i<gamsglobals.sv_max; i++) {
    sv[i] = (i+1)*3.14159265;
  }
  if (wrp.svals1(sv)>0) wrperror(rcall,"*** SVALS1 Test failed!");

  System.out.println("SVALS2 Test");
  wrp.svals2(sv); x=0; for (i=0; i<gamsglobals.sv_max; i++) x += wrp.dbl1(sv[i]);
  if (x != 0 ) wrperror(rcall,"*** SVALS2 Test failed!");

  System.out.println("BOOL Test");
  if (wrp.bool1(true) != 0) wrperror(rcall,"*** BOOL Test failed (passing data to library)!");

  System.out.println("BOOL2 Test");
  e[0] = false;
  if (wrp.bool2(e) != 0) wrperror(rcall,"*** BOOL2 Test failed (passing data to library)!");
  if (wrp.bool1(e[0]) != 0) wrperror(rcall,"*** BOOL2 Test failed (getting data from library)!");

  System.out.println("MAXARG Test");
  if (wrp.MaxArg(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20) != 21*20/2) wrperror(rcall,"*** MAXARG Test failed!");

  System.out.println("ALLARGCB Test");
  optr1 = wrp.GetwrpPtr();
  if (wrp.FPAllTy("com/gams/tester/testerjava.allTypes") > 0 || cb4f > 0) wrperror(rcall,"*** ALLARGCB Test failed!");
  System.out.println("GDXARGCB Test");
  if (wrp.FPgdxTy("com/gams/tester/testerjava.gdxTypes") > 0 || cb5f > 0) wrperror(rcall,"*** GDXARGCB Test failed!");
  System.out.println("MCB Test");
  wrp.setmcb1("com/gams/tester/testerjava.msg1Callback");
  wrp.setmcb2("com/gams/tester/testerjava.msg2Callback");
  /* wrp.mcb0PSet("com/gams/tester/testerjava.msg3Callback"); */
  wrp.initmcb();

  if (cb1f!=0 || cb1count!=4) wrperror(rcall,"*** MCB1 Test failed!");
  if (cb2f!=0 || cb2count!=4) wrperror(rcall,"*** MCB2 Test failed!");

  System.out.println("FUNCPTR Test");
  if (wrp.getmcb1().compareTo("com/gams/tester/testerjava.msg1Callback") != 0) wrperror(rcall,"*** FUNCPTR Test failed!");

  System.out.println("PTRPROP Test");
  wrp.ptrPSet( p[0]);
  if (wrp.ptrP() != p[0]) wrperror(rcall, "*** PTRPROP Test failed!");

  System.out.println("INTPROP Test");
  wrp.intPSet( 123);
  if (wrp.intP() != 2*123) wrperror(rcall, "*** INTPROP Test failed!");

  System.out.println("PCPROP Test");
  wrp.PCPSet("GAMS");
  if (wrp.PCP().compareTo("GUMS") != 0) wrperror(rcall, "*** PCPROP Test failed!");

  System.out.println("CHARPROP Test");
  wrp.CPSet( 'G');
  if (wrp.C1(wrp.CP()) != 0) wrperror(rcall, "*** CHARPROP Test failed!");

  System.out.println("DBLPROP Test");
  wrp.DPSet( 3.14159265*3.14159265);
  if (wrp.dbl1(wrp.DP()) != 0) wrperror(rcall, "*** DBLPROP Test failed!");

  System.out.println("BOOLPROPa Test");
  wrp.boolPSet(true);
  if (wrp.boolP()) wrperror(rcall, "*** BOOLPROPa Test failed!");

  System.out.println("BOOLPROPb Test");
  wrp.boolPSet(false);
  if (!wrp.boolP()) wrperror(rcall, "*** BOOLPROPb Test failed!");

  System.out.println("PTRRET Test");
  if (wrp.ptr1(wrp.ptrR()) != 0) wrperror(rcall, "*** PTRRET Test failed!");

  System.out.println("INTRET Test");
  if (wrp.int1(wrp.intR()) != 0) wrperror(rcall, "*** INTRET Test failed!");

  System.out.println("PCRET Test");
  if (wrp.pc1(wrp.PCR("GAMS")) != 0) wrperror(rcall, "*** PCRET Test failed!");


  System.out.println("DBLRET Test");
  if (wrp.dbl1(wrp.DR()) != 0) wrperror(rcall, "*** DBLRET Test failed!");

  System.out.println("BOOLRET Test");
  if (!wrp.boolR()) wrperror(rcall, "*** BOOLRET Test failed!");

  System.out.println("FPTRRET Test : "+wrp.FuncPtrR());
  if (wrp.FuncPtrR().compareTo("com/gams/tester/testerjava.msg1Callback") != 0) wrperror(rcall, "*** FPTRRET Test failed!");

  System.out.println("CHAR1 Test");
  if (wrp.C1('G') != 0) wrperror(rcall,"*** CHAR1 Test failed!");

  System.out.println("Constants Test");
  int intValue = wrp.wrpIntValue;
  if (intValue != 64) wrperror(rcall,"*** Integer Max Integer Value Test failed!");

  intValue = wrp.wrpInt_A;
  if (intValue != 0) wrperror(rcall,"*** Integer Constant Type A Test failed!");
  intValue = wrp.wrpInt_B;
  if (intValue != 1) wrperror(rcall,"*** Integer Constant Type B Test failed!");
  intValue = wrp.wrpInt_C;
  if (intValue != 2) wrperror(rcall,"*** Integer Constant Type C Test failed!");

  double floatValue = wrp.wrpFloatValue;
  if (Math.abs(floatValue + 0.148759) > 0.0001) 
      wrperror(rcall,"*** Float Constant Test failed!");

  String strValue = wrp.wrpStringValue;
  if (!strValue.equals("StringValue")) wrperror(rcall, "*** String Constant Test failed!");

  strValue = wrp.wrpString_Option1;
  if (!strValue.equals("First Option")) wrperror(rcall, "*** String Option1 Constant Test failed!");

  strValue = wrp.wrpString_Option2;
  if (!strValue.equals("Second Option")) wrperror(rcall, "*** String Option2 Constant Test failed!");

  strValue = wrp.wrpString_Option3;
  if (!strValue.equals("Third Option")) wrperror(rcall, "*** String Option3 Constant Test failed!");

  wrp.Free();
  System.out.println("End of testerjava: " + rcall[0] + " failures");
  System.out.println();

  System.exit(rcall[0]);
  } /* main */
}

