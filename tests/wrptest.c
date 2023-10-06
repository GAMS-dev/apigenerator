#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <ctype.h>
#include <errno.h>
#include <math.h>

#include "gclgms.h"
#include "wrp.h"
#include "c_wrpcb2.h"

#define WRPFREE(X) do { \
  if (NULL != (X)) { free(X);(X) = NULL;} \
 } while (0)
#define WRPMALLOC(PTR,TYPE,N) \
 ((PTR) = (TYPE *)malloc((N)*sizeof(TYPE)))


static char *DLLLoadPath;
static void *ptrPV;
static int intPV;
static INT64 int64PV;
static char CPV;
static double DPV;
static int boolPV;

static wrptestRec_t * wrpRecInit (void);

void wrpCreate (wrptestRec_t **wrp, char *msgBuf, int msgBufLen)
{
    msgBuf[0] = '\0';
    *wrp = wrpRecInit();
}

void wrpFree (wrptestRec_t **wrp)
{
  if (NULL == *wrp)
    return;
  WRPFREE(*wrp);
}

static wrptestRec_t *wrpRecInit (void)
{
  wrptestRec_t *wrp;
  WRPMALLOC(wrp, wrptestRec_t, 1);
  if (NULL == wrp)
    return NULL;
  strcpy(wrp->myString,"");
  wrp->s2       = (char *) NULL;
  wrp->myBuf    = (char *) NULL;
  wrp->wrpsetmcb1_mcb0   = NULL;
/*  wrp->MsgCallbackProp   = NULL; */
  wrp->wrpsetmcb2_mcb255 = NULL;
  return wrp;
}

int wrpptr1(wrptestRec_t *wrp, void *pntr)
{
  if(pntr != &DLLLoadPath)
    return 1;
  else
    return 0;
}

int wrpptr2(wrptestRec_t *wrp, void **pntr)
{
  int rc = 0;
  if(ptrPV != *pntr) rc = 1;
  *pntr = &DLLLoadPath;
  return rc;
}

int wrpint1(wrptestRec_t *wrp, int ntgr)
{
  if(123 != ntgr)
    return 1;
  else
    return 0;
}

int wrpint2(wrptestRec_t *wrp, int *ntgr)
{
  int rc = 0;
  if(*ntgr != 321) rc = 1;
  *ntgr = 123;
  return rc;
}

int wrpint64(wrptestRec_t *wrp, INT64 ntgr)
{
  if((INT64)987654321*(INT64)987654321 != ntgr)
    return 1;
  else
    return 0;
}

int wrpvint64(wrptestRec_t *wrp, INT64 *ntgr)
{
  int rc = 0;
  if(*ntgr != (INT64)123456789*(INT64)123456789) rc = 1;
  *ntgr = (INT64)987654321*(INT64)987654321;
  return rc;
}

int wrpoint64(wrptestRec_t *wrp, INT64 *ntgr)
{
  *ntgr = (INT64)987654321*(INT64)987654321;
  return 0;
}

int wrppda1(wrptestRec_t *wrp, const double *ptrda)
{
  int i;
  for(i=1;i<=3;i++)
    if(fabs(i*3.14159265 - ptrda[i-1]) > 1e-6)
      return 1;
  return 0;
}

int wrppda2(wrptestRec_t *wrp, double *ptrda)
{
  int i;
  int rc = 0;
  rc = wrppda1(wrp, ptrda);
  for(i=1;i<=3;i++)
    ptrda[i-1] = ptrda[i-1]/i;
  return rc;
}

int wrppia1(wrptestRec_t *wrp, const int *ptria)
{
  int i;
  for(i=1;i<=3;i++)
    if(ptria[i-1] != i*123)
      return 1;
  return 0;
}

int wrppia2(wrptestRec_t *wrp, int *ptria)
{
  int i;
  int rc = 0;
  rc = wrppia1(wrp, ptria);
  for(i=1;i<=3;i++)
    ptria[i-1] = ptria[i-1] / i;
  return rc;
}

int wrppc1(wrptestRec_t *wrp, const char *ptrc)
{
  if(strcmp(ptrc,"GAMS"))
    return 1;
  return 0;
}

int wrppc2(wrptestRec_t *wrp, char *ptrc)
{
  int rc = 0;
  if(strcmp(ptrc,"XXXX"))
    rc = 1;
  strcpy(ptrc,"GAMS");
  return rc;
}

int wrpC1(wrptestRec_t *wrp, char chr)
{
  if('G' != chr)
    return 1;
  return 0;
}

int wrpC2(wrptestRec_t *wrp, char *chr)
{
  int rc = 0;
  if('X' != *chr) rc = 1;
  *chr = 'G';
  return rc;
}

int wrpsst1(wrptestRec_t *wrp, const char *sst)
{
  if(strcmp(sst,"Hello GAMS"))
    return 1;
  return 0;
}

int wrpsst2(wrptestRec_t *wrp, char *sst)
{
  strcpy(sst,"Hello GAMS");
  return 0;
}

int wrpsst3(wrptestRec_t *wrp, char *sst, int sst_i)
{
  strcpy(sst,"Hello GAMS");
  return 0;
}

int wrpdbl1(wrptestRec_t *wrp, double dbl)
{
  if(fabs(3.14159265 - dbl) > 1e-6)
    return 1;
  return 0;
}

int wrpdbl2(wrptestRec_t *wrp, double *dbl)
{
  int rc = 0;
  rc = wrpdbl1(wrp, sqrt(*dbl));
  *dbl = sqrt(*dbl);
  return rc;
}

int wrpueli1(wrptestRec_t *wrp, const int *ntgri)
{
  int i;
  for(i=0;i<GMS_MAX_INDEX_DIM;i++)
    if(ntgri[i] != (i+1)*123)
      return 1;
  return 0;
}

int wrpueli2(wrptestRec_t *wrp, int *ntgri)
{
  int i;
  int rc = 0;
  rc = wrpueli1(wrp, ntgri);
  for(i=0;i<GMS_MAX_INDEX_DIM;i++) {
    ntgri[i] = 123;
  }
  return rc;
}

int wrpvII(wrptestRec_t *wrp, int *pvii)
{
  int i;
  printf("  c1 wrpvII: pvii=[");
  for(i=0;i<GMS_MAX_INDEX_DIM;i++)
     printf("%d ", pvii[i]);
  printf("]\n");
  for(i=0;i<GMS_MAX_INDEX_DIM;i++) {
    pvii[i] = pvii[i] / (i+1);
  }
  printf("  c2 wrpvII: pvii=[");
  for(i=0;i<GMS_MAX_INDEX_DIM;i++)
     printf("%d ", pvii[i]);
  printf("]\n");
  return 0;
}

int wrpvRV(wrptestRec_t *wrp, double *pvrv)
{
  int i;
  printf("  c1 wrpvRV: pvrv=[");
  for(i=0;i<GMS_VAL_MAX;i++)
     printf("%.6f ", pvrv[i]);
  printf("]\n");
  for(i=0;i<GMS_VAL_MAX;i++)
    pvrv[i] = pvrv[i]/(i+1);
  printf("  c2 wrpvRV: pvrv=[");
  for(i=0;i<GMS_VAL_MAX;i++)
     printf("%.6f ", pvrv[i]);
  printf("]\n");
  return 0;
}

int wrpvals1(wrptestRec_t *wrp, const double *recv)
{
  int i;
  for(i=0;i<GMS_VAL_MAX;i++) {
  if(fabs((i+1)*3.14159265 - recv[i]) > 1e-6)
    return 1;                 }
  return 0;
}

int wrpvals2(wrptestRec_t *wrp, double *recv)
{
  int i;
  int rc = 0;
  rc = wrpvals1(wrp, recv);
  for(i=0;i<GMS_VAL_MAX;i++)
    recv[i] = 3.14159265; //recv[i]/(i+1);
  return rc;
}

int wrpstri1(wrptestRec_t *wrp, const char **ssti)
{
  int  i;
  char tmp[256];
  for(i=0;i<GMS_MAX_INDEX_DIM;i++)
  {
    sprintf(tmp,"dim%d",i+1);
    if(strcmp(ssti[i],tmp))
      return 1;
  }
  return 0;
}

int wrpstri2(wrptestRec_t *wrp, char **ssti)
{
  int i;
  for(i=0;i<GMS_MAX_INDEX_DIM;i++)
    sprintf(ssti[i],"j%d",i+1);
  return 0;
}


int wrpsvals1(wrptestRec_t *wrp, const double *sval)
{
  int i;
  for(i=0;i<GMS_SVIDX_MAX;i++)
    if(fabs((i+1)*3.14159265 - sval[i]) > 1e-6)
      return 1;
  return 0;
}

int wrpsvals2(wrptestRec_t *wrp, double *sval)
{
  int i;
  int rc = 0;
  rc = wrpsvals1(wrp, sval);
  for(i=0;i<GMS_SVIDX_MAX;i++)
    sval[i] = sval[i]/(i+1);
  return rc;
}

int wrpbool1(wrptestRec_t *wrp, int b)
{
  printf("  c1 wrpbool1: b=%d\n",b);
  if(b == 0) return 1;
  b = 0;
  printf("  c2 wrpbool1: b=%d\n",b);
  return 0;
}

int wrpbool2 (wrptestRec_t *wrp, int *b)
{
  printf("  c1 wrpbool2: b=%d\n", *b);
  int rc = 0;
  if(*b != 0) rc = 1;
  *b = 1;
  printf("  c2 wrpbool2: b=%d\n", *b);
  printf("  c3 wrpbool2: rc=%d\n",rc);
  return rc;
}

int wrpMaxArg (wrptestRec_t *wrp, int int1,  int int2,  int int3,  int int4,  int int5,
                                  int int6,  int int7,  int int8,  int int9,  int int10,
                                  int int11, int int12, int int13, int int14, int int15,
                                  int int16, int int17, int int18, int int19, int int20)
{
  return int1  + int2  + int3  + int4  + int5  +
         int6  + int7  + int8  + int9  + int10 +
         int11 + int12 + int13 + int14 + int15 +
         int16 + int17 + int18 + int19 + int20;
}

int wrpFPAllTy (wrptestRec_t *wrp, TAllTypesCB_t allArg)
{
  int     i;
  char    s[256],charBuf[255];
  double  cptrda[3];
  int     cptria[3];
  char   *cptrc;

  for(i=0; i<3; i++) cptrda[i] = (i+1)*3.14159265;
  for(i=0; i<3; i++) cptria[i] = (i+1)*123;
  cptrc = s; strcpy(s,"GAMS");
  sprintf(charBuf,"%cGAMS",4);
  wrp->wrpFPAllTy_allArg = allArg;
  wrpFPAllTy_allArg_FC(wrp,&DLLLoadPath,1,cptrda,cptria,cptrc,charBuf,3.14159265,1,'G');
  return 0;
}

int wrpFPgdxTy (wrptestRec_t *wrp, TgdxTypesCB_t gdxArg)
{
  int i,j = 2;
  gdxUelIndex_t ntgri;
  gdxValues_t recv;
  gdxStrIndex_t ssti;
  gdxSVals_t sval;

  for(i=0; i<GMS_MAX_INDEX_DIM; i++) ntgri[i] = (i+1)*123;
  for(i=0; i<GMS_VAL_MAX; i++) recv[i] = i*3.14159265;
  for(i=0; i<GMS_MAX_INDEX_DIM; i++) { if(i==9) j++; sprintf(ssti[i], "%cj%d",j,i+1); }
  for(i=0; i<GMS_SVIDX_MAX; i++) sval[i] = i*3.14159265;
  wrp->wrpFPgdxTy_gdxArg = gdxArg;
  wrpFPgdxTy_gdxArg_FC(wrp,ntgri,recv,(const char **)ssti,sval);
  return 0;
}

int wrpsetmcb1(wrptestRec_t *wrp, TMsgCallback0_t mcb0)
{
  wrp->wrpsetmcb1_mcb0 = mcb0;
  return 0;
}

TMsgCallback0_t wrpgetmcb1(wrptestRec_t *wrp)
{
  return wrp->wrpsetmcb1_mcb0;
}

int wrpsetmcb2(wrptestRec_t *wrp, TMsgCallback255_t mcb255)
{
  wrp->wrpsetmcb2_mcb255 = mcb255;
  return 0;
}

void wrpinitmcb(wrptestRec_t *wrp)
{
  char charBuf[255];
  if((wrp->wrpsetmcb1_mcb0) != NULL)
  {
    wrpsetmcb1_mcb0_FC(wrp, 0, "Hello G");
    wrpsetmcb1_mcb0_FC(wrp, 1, "Hello A");
    wrpsetmcb1_mcb0_FC(wrp, 2, "Hello M");
    wrpsetmcb1_mcb0_FC(wrp, 3, "Hello S");
  }
/*  if(&(wrp->MsgCallbackProp) != NULL)
  {
    wrp->MsgCallbackProp(0, "Prop G");
    wrp->MsgCallbackProp(1, "Prop A");
    wrp->MsgCallbackProp(2, "Prop M");
    wrp->MsgCallbackProp(3, "Prop S");
  } */
  if((wrp->wrpsetmcb2_mcb255) != NULL)
  {
    sprintf(charBuf,"%cHello G",7);
    wrpsetmcb2_mcb255_FC(wrp, 0, charBuf);
    sprintf(charBuf,"%cHello A",7);
    wrpsetmcb2_mcb255_FC(wrp, 1, charBuf);
    sprintf(charBuf,"%cHello M",7);
    wrpsetmcb2_mcb255_FC(wrp, 2, charBuf);
    sprintf(charBuf,"%cHello S",7);
    wrpsetmcb2_mcb255_FC(wrp, 3, charBuf);
  }
}

void * wrpptrP (wrptestRec_t *wrp)
{
  return ptrPV;
}

void wrpptrPSet (wrptestRec_t *wrp, void *x)
{
  ptrPV = x;
}

int wrpintP (wrptestRec_t *wrp)
{
  return intPV * 2;
}

void wrpintPSet (wrptestRec_t *wrp, int x)
{
  intPV = x;
}

INT64 wrpint64P (wrptestRec_t *wrp)
{
  return int64PV * 2;
}

void wrpint64PSet (wrptestRec_t *wrp, INT64 x)
{
  int64PV = x;
}

char * wrpPCP (wrptestRec_t *wrp)
{
  if(strlen(wrp->myString) < 2)
    strcpy(wrp->myString,"1U");
  else
    wrp->myString[1] = 'U';
  return wrp->myString;
}

void wrpPCPSet (wrptestRec_t *wrp, char *x)
{
  strcpy(wrp->myString,x);
}

char wrpCP (wrptestRec_t *wrp)
{
  return CPV;
}

void wrpCPSet (wrptestRec_t *wrp, char x)
{
  CPV = x;
}

double wrpDP (wrptestRec_t *wrp)
{
  return sqrt(DPV);
}

void wrpDPSet (wrptestRec_t *wrp, double x)
{
  DPV = x;
}

int  wrpboolP (wrptestRec_t *wrp)
{
  boolPV = -1 * (boolPV-1);
  if(boolPV)
    return 1;
  else
    return 0;
}

void wrpboolPSet (wrptestRec_t *wrp, int x)
{
  boolPV = x != 0;
}

/* TMsgCallback0_t wrpmcb0P (wrptestRec_t *wrp)
{
  return wrp->MsgCallbackProp;
}

void wrpmcb0PSet (wrptestRec_t *wrp, TMsgCallback0_t x)
{
  wrp->MsgCallbackProp = x;
} */

void * wrpptrR (wrptestRec_t *wrp)
{
  return &DLLLoadPath;
}

int wrpintR (wrptestRec_t *wrp)
{
  return 123;
}

INT64 wrpint64R (wrptestRec_t *wrp)
{
  return (INT64)987654321*(INT64)987654321;
}

char * wrpPCR (wrptestRec_t *wrp, const char *ptrc)
{
  wrp->s2 = (char *) ptrc;
  return wrp->s2;
}

char wrpCR (wrptestRec_t *wrp)
{
  return 'G';
}

double wrpDR (wrptestRec_t *wrp)
{
  return 3.14159265;
}

int wrpboolR (wrptestRec_t *wrp)
{
  return 1;
}

TMsgCallback0_t wrpFuncPtrR (wrptestRec_t *wrp)
{
  return wrp->wrpsetmcb1_mcb0;
}

void wrpdiffargs1 (wrptestRec_t *wrp)
{
}

void wrpdiffargs2 (wrptestRec_t *wrp, double dummy)
{
}

void wrpdiffargsPSet (wrptestRec_t *wrp, int x)
{
}
