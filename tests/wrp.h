/* wrp.h
 * Header file for C-style interface to the WRP library
 */

#if ! defined(_WRPCC_H_)
#     define  _WRPCC_H_

#include "gclgms.h"

#if defined(_WIN32)
# include <windows.h>
# define WRP_CALLCONV __stdcall
#else
# define WRP_CALLCONV
#endif

#if defined(__cplusplus)
extern "C" {
#endif

struct wrpHandle_;
typedef struct wrpHandle_ *wrpHandle_t;

struct wrptestRec;
typedef struct wrptestRec wrptestRec_t;

#include "c_wrpcb1.h"

typedef int (*wrpErrorCallback_t) (int ErrCount, const char *msg);
extern int wrpAPIErrorCount;

struct wrptestRec {
  char myString[256];
  char *s2;
  char *myBuf;
  int wrpsetmcb1_mcb0_CallByRef;
  int wrpsetmcb2_mcb255_CallByRef;
  int wrpFPAllTy_allArg_CallByRef;
  int wrpFPgdxTy_gdxArg_CallByRef;
  TMsgCallback0_t wrpsetmcb1_mcb0;
  TMsgCallback255_t wrpsetmcb2_mcb255;
  TAllTypesCB_t wrpFPAllTy_allArg;
  TgdxTypesCB_t wrpFPgdxTy_gdxArg;
};

#if defined(WRP_MAIN)    /* we must define some things only once */
# define WRP_FUNCPTR(NAME)  NAME##_t NAME = NULL
#else
# define WRP_FUNCPTR(NAME)  extern NAME##_t NAME
#endif

/* function typedefs and pointer definitions */
void wrpCreate (wrptestRec_t **p, char *msgBuf, int msgBufLen);
void wrpFree (wrptestRec_t **p);
int wrpptr1 (wrptestRec_t *p, void *pntr);
int wrpptr2 (wrptestRec_t *p, void **pntr);
int wrpint1 (wrptestRec_t *p, int ntgr);
int wrpint2 (wrptestRec_t *p, int *ntgr);
int wrpint64  (wrptestRec_t *p, INT64 ntgr);
int wrpvint64 (wrptestRec_t *p, INT64 *ntgr);
int wrpoint64 (wrptestRec_t *p, INT64 *ntgr);
int wrppda1 (wrptestRec_t *p, const double *ptrda);
int wrppda2 (wrptestRec_t *p, double *ptrda);
int wrppia1 (wrptestRec_t *p, const int *ptria);
int wrppia2 (wrptestRec_t *p, int *ptria);
int wrppc1 (wrptestRec_t *p, const char *ptrc);
int wrppc2 (wrptestRec_t *p, char *ptrc);
int wrpC1 (wrptestRec_t *p, char chr);
int wrpC2 (wrptestRec_t *p, char *chr);
int wrpsst1 (wrptestRec_t *p, const char *sst);
int wrpsst2 (wrptestRec_t *p, char *sst);
int wrpsst3 (wrptestRec_t *p, char *sst, int sst_i);
int wrpdbl1 (wrptestRec_t *p, double dbl);
int wrpdbl2 (wrptestRec_t *p, double *dbl);
int wrpueli1 (wrptestRec_t *p, const int *ntgri);
int wrpueli2 (wrptestRec_t *p, int *ntgri);
int wrpvII (wrptestRec_t *p, int *pvii);
int wrpvRV (wrptestRec_t *p, double *pvrv);
int wrpvals1 (wrptestRec_t *p, const double *recv);
int wrpvals2 (wrptestRec_t *p, double *recv);
int wrpstri1 (wrptestRec_t *p, const char **ssti);
int wrpstri2 (wrptestRec_t *p, char **ssti);
int wrpsvals1 (wrptestRec_t *p, const double *sval);
int wrpsvals2 (wrptestRec_t *p, double *sval);
int wrpbool1 (wrptestRec_t *p, int b);
int wrpbool2 (wrptestRec_t *p, int *b);
int wrpMaxArg (wrptestRec_t *p, int int1, int int2, int int3, int int4, int int5, int int6, int int7, int int8, int int9, int int10, int int11, int int12, int int13, int int14, int int15, int int16, int int17, int int18, int int19, int int20);
int wrpFPAllTy (wrptestRec_t *p, TAllTypesCB_t allArg);
int wrpFPgdxTy (wrptestRec_t *p, TgdxTypesCB_t gdxArg);
int wrpsetmcb1 (wrptestRec_t *p, TMsgCallback0_t mcb0);
TMsgCallback0_t wrpgetmcb1 (wrptestRec_t *p);
int wrpsetmcb2 (wrptestRec_t *p, TMsgCallback255_t mcb255);
void wrpinitmcb (wrptestRec_t *p);
void * wrpptrR (wrptestRec_t *p);
int wrpintR (wrptestRec_t *p);
INT64 wrpint64R (wrptestRec_t *p);
char * wrpPCR (wrptestRec_t *p, const char *ptrc);
char wrpCR (wrptestRec_t *p);
double wrpDR (wrptestRec_t *p);
int wrpboolR (wrptestRec_t *p);
TMsgCallback0_t wrpFuncPtrR (wrptestRec_t *p);
void wrpdiffargs1 (wrptestRec_t *p);
void wrpdiffargs2 (wrptestRec_t *p, double dummy);
void * wrpptrP (wrptestRec_t *p);
void wrpptrPSet (wrptestRec_t *p, void *x);
int wrpintP (wrptestRec_t *p);
void wrpintPSet (wrptestRec_t *p, int x);
INT64 wrpint64P (wrptestRec_t *p);
void wrpint64PSet (wrptestRec_t *p, INT64 x);
char * wrpPCP (wrptestRec_t *p);
void wrpPCPSet (wrptestRec_t *p, char *x);
char wrpCP (wrptestRec_t *p);
void wrpCPSet (wrptestRec_t *p, char x);
double wrpDP (wrptestRec_t *p);
void wrpDPSet (wrptestRec_t *p, double x);
int  wrpboolP (wrptestRec_t *p);
void wrpboolPSet (wrptestRec_t *p, int x);
/* TMsgCallback0_t wrpmcb0P (wrptestRec_t *p);
void wrpmcb0PSet (wrptestRec_t *p, TMsgCallback0_t x); */
void wrpdiffargsPSet (wrptestRec_t *p, int x);
#if defined(__cplusplus)
}
#endif
#endif /* #if ! defined(_WRPCC_H_) */
