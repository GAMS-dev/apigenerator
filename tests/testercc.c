#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include "gclgms.h"
#include "c_wrpcc.h"

static int cb1count=0, cb1count2=0, cb2count=0;
static int cb1f=0, cb1f2=0, cb2f=0, cb4f=0, cb5f=0;
// static int cb3count=0, cb3f=0;
static int myerrcnt=0;
static wrpHandle_t Tptr,Tptr2=NULL;


static void wrperror(int *rc, const char *s) {
  (*rc)++;
  printf("%s",s);
} /* wrperror */

static void WRP_CALLCONV
msg1Callback (int mode, const char *msgBuf)
{
  cb1count++;
  switch (mode) {
  case 0: if (strcmp(msgBuf,"Hello G")) cb1f++; break;
  case 1: if (strcmp(msgBuf,"Hello A")) cb1f++; break;
  case 2: if (strcmp(msgBuf,"Hello M")) cb1f++; break;
  case 3: if (strcmp(msgBuf,"Hello S")) cb1f++; break;
  }
} /* msg1Callback */

static void WRP_CALLCONV
msg1Callback2 (int mode, const char *msgBuf)
{
  cb1count2++;
  switch (mode) {
  case 0: if (strcmp(msgBuf,"Hello G")) cb1f2++; break;
  case 1: if (strcmp(msgBuf,"Hello A")) cb1f2++; break;
  case 2: if (strcmp(msgBuf,"Hello M")) cb1f2++; break;
  case 3: if (strcmp(msgBuf,"Hello S")) cb1f2++; break;
  }
} /* msg1Callback2 */

static void WRP_CALLCONV
msg2Callback (int mode, const char *msgBuf)
{ char msg[256];
  cb2count++; strncpy(msg,msgBuf+1,msgBuf[0]); msg[(unsigned char)msgBuf[0]]='\0';
  switch (mode) {
  case 0: if (strcmp(msg,"Hello G")) cb2f++; break;
  case 1: if (strcmp(msg,"Hello A")) cb2f++; break;
  case 2: if (strcmp(msg,"Hello M")) cb2f++; break;
  case 3: if (strcmp(msg,"Hello S")) cb2f++; break;
  }
} /* msg2Callback */

/* static void WRP_CALLCONV
msg3Callback (int mode, const char *msgBuf)
{
  cb3count++;
  switch (mode) {
  case 0: if (strcmp(msgBuf,"Prop G")) cb3f++; break;
  case 1: if (strcmp(msgBuf,"Prop A")) cb3f++; break;
  case 2: if (strcmp(msgBuf,"Prop M")) cb3f++; break;
  case 3: if (strcmp(msgBuf,"Prop S")) cb3f++; break;
  }
}*/ /* msg3Callback */

static void WRP_CALLCONV
allTypes (void *pntr, int ntgr, const double *cptrda, const int *cptria, const char *cptrc, const char *csst, double dbl, int b, char chr)
{
  int i;
  char msg[256];
  strncpy(msg,csst+1,csst[0]); msg[(unsigned char)csst[0]]='\0';

  if((size_t) pntr%1 != 0)          cb4f++;
  if(ntgr != 1)                     cb4f++;
  if(strcmp(cptrc,"GAMS"))          cb4f++;
  if(strcmp(msg,"GAMS"))            cb4f++;
  if(fabs(dbl - 3.14159265) > 1e-6) cb4f++;
  if(!b)                            cb4f++;
  if(chr != 'G')                    cb4f++;
  for(i=0;i<3;i++) if(fabs(cptrda[i] - (i+1) * 3.14159265) > 1e-6) cb4f++;
  for(i=0;i<3;i++) if(cptria[i] != (i+1) * 123)                   cb4f++;
} /* alltypes */

static void WRP_CALLCONV
gdxTypes (const int *ntgri, const double *recv, const char *ssti, const double *sval)
{
  int i;
  char tmp[256];
  char tmp2[256];

  for(i=0; i<GMS_MAX_INDEX_DIM; i++)   if(ntgri[i]!=(i+1)*123)                 cb5f++;
  for(i=0; i<GMS_VAL_MAX; i++)         if(fabs(recv[i] - i*3.14159265) > 1e-6) cb5f++;
  for(i=0;i<GMS_MAX_INDEX_DIM;i++)
  {
    strncpy(tmp2,ssti + i*256 + 1,(int) *(ssti + i*256));
    tmp2[(int) *(ssti + i*256)] = '\0';
    sprintf(tmp, "j%d", i+1);
    if(strcmp(tmp2,tmp)) cb5f++;
  }
  for(i=0; i<GMS_SVIDX_MAX; i++)       if(fabs(sval[i] - i*3.14159265) > 1e-6) cb5f++;
} /* gdxtypes */

static int
myerrorcb (int errcnt, const char *msgBuf)
{
  myerrcnt++;
  /* printf("%s\n",msgBuf); */
  return 0;
}

int main (int argc, char *argv[]) {

  int x,i,rcall=0;
  INT64 xx;
  double y;
  void *p=NULL;
  double pda[3];
  int pia[3];
  char sst[256];
  char *cp, d;
  gdxUelIndex_t uel;
  gdxValues_t val;
  gdxStrIndex_t dim;
  gdxStrIndexPtrs_t pdim;
  gdxSVals_t sv;

  printf("Start of test %s on C library.\n", argv[0]);

  wrpCreate(&Tptr,sst,256);
  if (NULL==Tptr) {
    printf("Could not create wrapper object: %s\n", sst);
    exit(1);
  }

  printf("PTRPROP Test\n");
  wrpptrPSet(Tptr, (void *)&wrperror); p = wrpptrP(Tptr);
  if (p != (void *)&wrperror) wrperror(&rcall, "*** PTRPROP Test failed!\n");

  printf("PTR Test\n");
  if (wrpptr2(Tptr,&p)) wrperror(&rcall,"*** PTR2 Test failed!\n");
  if (wrpptr1(Tptr,p))  wrperror(&rcall,"*** PTR1 Test failed!\n");

  printf("INT1 Test\n");
  if (wrpint1(Tptr,123)) wrperror(&rcall,"*** INT1 Test failed!\n");

  printf("INT2 Test\n");
  x = 321; if (wrpint2(Tptr,&x)) wrperror(&rcall,"*** INT2 Test failed (passing data to library)!\n");
  if (wrpint1(Tptr,x)) wrperror(&rcall,"*** INT2 Test failed (getting data from library)!\n");

  printf("INT64 Test\n");
  if (wrpint64(Tptr,(INT64)987654321*987654321)!=0) wrperror(&rcall,"*** INT64 Test failed!\n");

  printf("INT642 Test\n");
  xx = (INT64)123456789*123456789; if (wrpvint64(Tptr,&xx)!=0) wrperror(&rcall,"*** VINT64 Test failed (passing data to library)!\n");
  if (wrpint64(Tptr,xx)!=0) wrperror(&rcall,"*** VINT64 Test failed (getting data from library)!\n");

  printf("OINT64 Test\n");
  xx = (INT64)0; if (wrpoint64(Tptr,&xx)!=0) wrperror(&rcall,"*** OINT64 Test failed (getting data from library)!\n");
  if (wrpint64(Tptr,xx)!=0) wrperror(&rcall,"*** OINT64 Test failed (getting data from library)!\n");

  printf("PDA1 Test\n");
  for(i=0; i<3; i++) pda[i] = (i+1)*3.14159265;
  if (wrppda1(Tptr,pda)) wrperror(&rcall,"*** PDA1 Test failed!\n");

  printf("PDA2 Test\n");
  if (wrppda2(Tptr,pda)) wrperror(&rcall,"*** PDA2 Test failed (passing data to library)!\n");
  x=0; for (i=0; i<3; i++) x += wrpdbl1(Tptr,pda[i]);
  if (x) wrperror(&rcall,"*** PDA2 Test failed (getting data from library)!\n");

  printf("PIA1 Test\n");
  for(i=0; i<3; i++) pia[i] = (i+1)*123;
  if (wrppia1(Tptr,pia)>0) wrperror(&rcall,"*** PIA1 Test failed!\n");

  printf("PIA2 Test\n");
  if (wrppia2(Tptr,pia)) wrperror(&rcall,"*** PIA2 Test failed (passing data to library)!\n");
  x=0; for (i=0; i<3; i++) x += wrpint1(Tptr,pia[i]);
  if (x) wrperror(&rcall,"*** PIA2 Test failed (getting data from library)!\n");

  printf("PC1 Test\n");
  if (wrppc1(Tptr,"GAMS")) wrperror(&rcall,"*** PC1 Test failed!\n");

  printf("PC2 Test\n");
  cp = sst; strcpy(sst,"XXXX"); if (wrppc2(Tptr,cp)) wrperror(&rcall,"*** PC2 Test failed (passing data to library)!\n");
  if (strcmp("GAMS",cp)) wrperror(&rcall,"*** PC2 Test failed (getting data from library)!\n");

  printf("CHAR1  Test\n");
  if (wrpC1(Tptr,'G')) wrperror(&rcall,"*** CHAR1 Test failed!\n");

  printf("CHAR2  Test\n");
  d = 'X'; if (wrpC2(Tptr,&d)) wrperror(&rcall,"*** CHAR2 Test failed (passing data to library)!\n");
  if (wrpC1(Tptr,d)) wrperror(&rcall,"*** CHAR2 Test failed (getting data from library)!\n");

  printf("SST1 Test\n");
  if (wrpsst1(Tptr,"Hello GAMS")) wrperror(&rcall,"*** SST1 Test failed!\n");

  printf("SST2 Test\n");
  strcpy(sst,""); wrpsst2(Tptr,sst);
  if (wrpsst1(Tptr,sst)) wrperror(&rcall,"*** SST2 Test failed!\n");

  printf("SST3 Test\n");
  strcpy(sst,""); wrpsst3(Tptr,sst,sizeof(sst));
  if (wrpsst1(Tptr,sst)) wrperror(&rcall,"*** SST3 Test failed!\n");

  printf("DBL1 Test\n");
  if (wrpdbl1(Tptr,3.14159265)) wrperror(&rcall,"*** DBL1 Test failed!\n");

  printf("DBL2 Test\n");
  y = 3.14159265*3.14159265; if (wrpdbl2(Tptr,&y)) wrperror(&rcall,"*** DBL2 Test failed (passing data to library)!\n");
  if (wrpdbl1(Tptr,y)) wrperror(&rcall,"*** DBL2 Test failed (getting data from library)!\n");

  printf("UELI1 Test\n");
  for(i=0; i<GMS_MAX_INDEX_DIM; i++) uel[i] = (i+1)*123;
  if (wrpueli1(Tptr,uel)>0) wrperror(&rcall,"*** UELI1 Test failed!\n");

  printf("UELI2 Test\n");
  if (wrpueli2(Tptr,uel)) wrperror(&rcall,"*** UELI2 Test failed (passing data to library)!\n");
  x=0; for (i=0; i<GMS_MAX_INDEX_DIM; i++) x += wrpint1(Tptr,uel[i]);
  if (x) wrperror(&rcall,"*** UELI2 Test failed (getting data from library)!\n");

  printf("VII Test\n");
  for(i=0; i<GMS_MAX_INDEX_DIM; i++) uel[i] = (i+1)*123;
  if (wrpvII(Tptr,uel)) wrperror(&rcall,"*** VII Test failed (passing integer array in and out of library)!\n");
  x=0; for (i=0; i<GMS_MAX_INDEX_DIM; i++) x += wrpint1(Tptr,uel[i]);
  if (x) wrperror(&rcall,"*** VII Test failed (passing integer array in and out of library)!\n");

  printf("VRV Test\n");
  for(i=0; i<GMS_VAL_MAX; i++) val[i] = (i+1)*3.14159265;
  if (wrpvRV(Tptr,val)) wrperror(&rcall,"*** VRV Test failed (passing double array in and out of library)!\n");
  x=0; for (i=0; i<GMS_VAL_MAX; i++) x += wrpdbl1(Tptr,val[i]);
  if (x) wrperror(&rcall,"*** VRV Test failed (passing double array in and out of library)!\n");

  printf("VALS1 Test\n");
  for(i=0; i<GMS_VAL_MAX; i++) val[i] = (i+1)*3.14159265;
  if (wrpvals1(Tptr,val)>0) wrperror(&rcall,"*** VALS1 Test failed!\n");

  printf("VALS2 Test\n");
  if (wrpvals2(Tptr,val)) wrperror(&rcall,"*** VALS2 Test failed (passing data to library)!\n");
  x=0; for (i=0; i<GMS_VAL_MAX; i++) x += wrpdbl1(Tptr,val[i]);
  if (x) wrperror(&rcall,"*** VALS2 Test failed (getting data from library)!\n");

  GDXSTRINDEXPTRS_INIT(dim,pdim); /* assign pdim */

  printf("STRI1 Test\n");
  for(i=0; i<GMS_MAX_INDEX_DIM; i++) sprintf(pdim[i], "dim%d", i+1);
  if (wrpstri1(Tptr,(const char**)pdim)>0) wrperror(&rcall,"*** STRI1 Test failed!\n");

  printf("STRI2 Test\n");
  wrpstri2(Tptr,pdim);
  for(i=0; i<GMS_MAX_INDEX_DIM; i++) {
    sprintf(sst, "j%d", i+1);
    if (strcmp(sst,pdim[i])) {
      wrperror(&rcall,"*** STRI2 Test failed!\n");
      break;
    }
  }

  printf("SVALS1 Test\n");
  for(i=0; i<GMS_SVIDX_MAX; i++) {
    sv[i] = (i+1)*3.14159265;
  }
  if (wrpsvals1(Tptr,sv)>0) wrperror(&rcall,"*** SVALS1 Test failed!\n");

  printf("SVALS2 Test\n");
  if (wrpsvals2(Tptr,sv)) wrperror(&rcall,"*** SVALS2 Test failed (passing data to library)!\n");
  x=0; for (i=0; i<GMS_SVIDX_MAX; i++) x += wrpdbl1(Tptr,sv[i]);
  if (x) wrperror(&rcall,"*** SVALS2 Test failed (getting data from library)!\n");

  printf("BOOL Test\n");
  if (wrpbool1(Tptr,1)) wrperror(&rcall,"*** BOOL Test failed (passing data to library)!\n");

  printf("BOOL2 Test\n");
  x = 0;
  if (wrpbool2(Tptr,&x)) wrperror(&rcall,"*** BOOL2 Test failed (passing data to library)!\n");
  if (wrpbool1(Tptr,x)) wrperror(&rcall,"*** BOOL2 Test failed (getting data from library)!\n");

  printf("MAXARG Test\n");
  if (wrpMaxArg(Tptr,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20) != 21*20/2) wrperror(&rcall,"*** MAXARG Test failed!\n");

  printf("ALLARGCB Test\n");
  if (wrpFPAllTy(Tptr,allTypes) || cb4f) wrperror(&rcall,"*** ALLARGCB Test failed!\n");

  printf("GDXARGCB Test\n");
  if (wrpFPgdxTy(Tptr,gdxTypes) || cb5f) wrperror(&rcall,"*** GDXARGCB Test failed!\n");

  printf("MCB Test\n");
  wrpCreate(&Tptr2,sst,256);
  if (NULL==Tptr2) {
    printf("Could not create wrapper object: %s\n", sst);
    exit(1);
  }
  wrpsetmcb1(Tptr,msg1Callback);
  wrpsetmcb1(Tptr2,msg1Callback2);
  wrpsetmcb2(Tptr,msg2Callback);
/*  wrpmcb0PSet(Tptr,msg3Callback); */
  wrpinitmcb(Tptr);
  wrpinitmcb(Tptr2);

  if (cb1f || cb1count !=4) wrperror(&rcall,"*** MCB1 Test failed!\n");
  if (cb1f2|| cb1count2!=4) wrperror(&rcall,"*** MCB1 Test failed! (Problem with 2nd object)\n");
  if (cb2f || cb2count !=4) wrperror(&rcall,"*** MCB2 Test failed!\n");
/*  if (cb3f || cb3count !=4) wrperror(&rcall,"*** MCB3 Test failed!\n"); */

  printf("FUNCPTR Test\n");
  if (wrpgetmcb1(Tptr) != &msg1Callback) wrperror(&rcall,"*** FUNCPTR Test failed!\n");

/*  printf("FUNCPTRPROP Test\n");
  if (wrpmcb0P(Tptr) != &msg3Callback) wrperror(&rcall,"*** FUNCPTRPROP Test failed!\n"); */

  printf("INTPROP Test\n");
  wrpintPSet(Tptr, 123);
  if (wrpintP(Tptr) != 2*123) wrperror(&rcall, "*** INTPROP Test failed!\n");

  printf("INT64PROP Test\n");
  wrpint64PSet(Tptr, (INT64)987654321*987654321);
  if (wrpint64P(Tptr) != (INT64)2*987654321*987654321) wrperror(&rcall, "*** INT64PROP Test failed!\n");

  printf("PCPROP Test\n");
  cp = sst; strcpy(sst,"GAMS"); wrpPCPSet(Tptr,cp);
  if (strcmp("GUMS",wrpPCP(Tptr))) wrperror(&rcall, "*** PCPROP Test failed!\n");

  printf("CHARPROP Test\n");
  wrpCPSet(Tptr, 'G');
  if (wrpC1(Tptr,wrpCP(Tptr)) > 0) wrperror(&rcall, "*** CHARPROP Test failed!\n");

  printf("DBLPROP Test\n");
  wrpDPSet(Tptr, 3.14159265*3.14159265);
  if (wrpdbl1(Tptr,wrpDP(Tptr))) wrperror(&rcall, "*** DBLPROP Test failed!\n");

  printf("BOOLPROPa Test\n");
  wrpboolPSet(Tptr, 1);
  if (wrpboolP(Tptr)) wrperror(&rcall, "*** BOOLPROPa Test failed!\n");

  printf("BOOLPROPb Test\n");
  wrpboolPSet(Tptr, 0);
  if (!wrpboolP(Tptr)) wrperror(&rcall, "*** BOOLPROPb Test failed!\n");

  printf("PTRRET Test\n");
  if (wrpptr1(Tptr,wrpptrR(Tptr))) wrperror(&rcall, "*** PTRRET Test failed!\n");

  printf("INTRET Test\n");
  if (wrpint1(Tptr,wrpintR(Tptr))) wrperror(&rcall, "*** INTRET Test failed!\n");

  printf("INT64RET Test\n");
  if (wrpint64(Tptr,wrpint64R(Tptr))) wrperror(&rcall, "*** INT64RET Test failed!\n");

  printf("PCRET Test\n");
  cp = sst; strcpy(sst,"GAMS"); if (wrppc1(Tptr,wrpPCR(Tptr,cp))) wrperror(&rcall, "*** PCRET Test failed!\n");

  printf("DBLRET Test\n");
  if (wrpdbl1(Tptr,wrpDR(Tptr))) wrperror(&rcall, "*** DBLRET Test failed!\n");

  printf("BOOLRET Test\n");
  if (!wrpboolR(Tptr)) wrperror(&rcall, "*** BOOLRET Test failed!\n");

  printf("FPTRRET Test\n");
  if (wrpFuncPtrR(Tptr) != &msg1Callback) wrperror(&rcall, "*** FPTRRET Test failed!\n");

  printf("CHARRET Test\n");
  if (wrpC1(Tptr,wrpCR(Tptr))) wrperror(&rcall,"*** CHARRET Test failed!\n");

  printf("Constants Test\n");
  int intValue = wrpIntValue;
  if (intValue != 64) wrperror(&rcall,"*** Integer Max Integer Value Test failed!\n");

  enum wrpIntConstType intVar = wrpInt_A;
  if (intVar != 0) wrperror(&rcall,"*** Integer Constant Type A Test failed!\n");
  intVar = wrpInt_B;
  if (intVar != 1) wrperror(&rcall,"*** Integer Constant Type B Test failed!\n");
  intVar = wrpInt_C;
  if (intVar != 2) wrperror(&rcall,"*** Integer Constant Type C Test failed!\n");

  float floatValue = wrpFloatValue;
  if (fabs(floatValue + 0.148759) > 0.0001) 
      wrperror(&rcall,"*** Float Constant Test failed!\n");

  char *strValue = sst; 
  strcpy(strValue, wrpStringValue);
  if (strcmp("StringValue", strValue) != 0) wrperror(&rcall, "*** String Constant Test failed!\n");

  strcpy(strValue, wrpString_Option1);
  if (strcmp("First Option", strValue) != 0) wrperror(&rcall, "*** String Option1 Constant Test failed!\n");

  strcpy(strValue, wrpString_Option2);
  if (strcmp("Second Option", strValue) != 0) wrperror(&rcall, "*** String Option2 Constant Test failed!\n");

  strcpy(strValue, wrpString_Option3);
  if (strcmp("Third Option", strValue) != 0) wrperror(&rcall, "*** String Option3 Constant Test failed!\n");

  wrpFree(&Tptr);
  printf("End of test %s on C library: %d failures\n\n", argv[0], rcall);

  return rcall;
} /* main */
