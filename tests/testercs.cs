using System;
using System.Runtime.InteropServices;
using System.Collections.Generic;
using System.Text;

namespace testercs
{
    class testercs
    {
        static int rc = 0;
        static int cb1count = 0;
        static int cb1count2 = 0;
        static int cb2count = 0;
        //static int cbpcount = 0;
        static int x = 0;
        static int x2 = 0;
        //static int w = 0;
        static int v = 0;
        static int z = 0;

        static void wrperror(string err)
        {
            rc++;
            Console.WriteLine(err);
        }


        static void msg1Callback(int mode, string msgBuf)
        {
            cb1count++;
            switch (mode)
            {
                case 0:
                    if (msgBuf != "Hello G") x = x + 1;
                    return;
                case 1:
                    if (msgBuf != "Hello A") x = x + 1;
                    return;
                case 2:
                    if (msgBuf != "Hello M") x = x + 1;
                    return;
                case 3:
                    if (msgBuf != "Hello S") x = x + 1;
                    return;
            }
        }

        static void msg1Callback2(int mode, string msgBuf)
        {
            cb1count2++;
            switch (mode)
            {
                case 0:
                    if (msgBuf != "Hello G") x2 = x2 + 1;
                    return;
                case 1:
                    if (msgBuf != "Hello A") x2 = x2 + 1;
                    return;
                case 2:
                    if (msgBuf != "Hello M") x2 = x2 + 1;
                    return;
                case 3:
                    if (msgBuf != "Hello S") x2 = x2 + 1;
                    return;
            }
        }

        //static void PropCallback(int mode, string msgBuf) //pchar
        //{
        //    cbpcount++;
        //    switch (mode)
        //    {
        //        case 0:
        //            if (msgBuf != "Prop G") w = w + 1;
        //            return;
        //        case 1:
        //            if (msgBuf != "Prop A") w = w + 1;
        //            return;
        //        case 2:
        //            if (msgBuf != "Prop M") w = w + 1;
        //            return;
        //        case 3:
        //            if (msgBuf != "Prop S") w = w + 1;
        //            return;
        //    }
        //}

        static void msg2Callback(int mode, string msgBufX)
        {
            string msgBuf;
            msgBuf = msgBufX.Substring(1, (int)msgBufX[0]);
            cb2count++;
            switch (mode)
            {
                case 0:
                    if (msgBuf != "Hello G") z = z + 1;
                    return;
                case 1:
                    if (msgBuf != "Hello A") z = z + 1;
                    return;
                case 2:
                    if (msgBuf != "Hello M") z = z + 1;
                    return;
                case 3:
                    if (msgBuf != "Hello S") z = z + 1;
                    return;
            }
        }

        static void allTypes(IntPtr pntr, int ntgr, IntPtr cptrdaX, IntPtr cptriaX, string cptrc, string csst, double dbl, int b, char chr)
        {
            int i;
            string msg;
            double[] cptrda = new double[3];
            int[] cptria = new int[3];
            Marshal.Copy(cptrdaX, cptrda, 0, 3);
            Marshal.Copy(cptriaX, cptria, 0, 3);
            msg = csst.Substring(1, (int)csst[0]);
            if(pntr == IntPtr.Zero)               v++;
            if(ntgr != 1)                         v++;
            if(cptrc != "GAMS")                   v++;
            if(msg != "GAMS")                     v++;
            if(Math.Abs(dbl - 3.14159265) > 1e-6) v++;
            if(b != 1)                            v++;
            if(chr != 'G')                        v++;
            for(i=0;i<3;i++) if(Math.Abs(cptrda[i]-(i+1)*3.14159265) > 1e-6) v++;
            for(i=0;i<3;i++) if(cptria[i] != (i+1) * 123)                    v++;
        } /* alltypes */

        static void gdxTypes(IntPtr ntgriX, IntPtr recvX, IntPtr sstiX, IntPtr svalX)
        {
            int i;
            int[] ntgri = new int[gamsglobals.maxdim];
            double[] recv = new double[gamsglobals.val_max];
            string[] ssti = new string[gamsglobals.maxdim];
            double[] sval = new double[gamsglobals.sv_max];

            Marshal.Copy(ntgriX, ntgri, 0, gamsglobals.maxdim);
            Marshal.Copy(recvX, recv, 0, gamsglobals.val_max);
            //Marshal.Copy(sstiX, ssti, 0, gamsglobals.maxdim);
            Marshal.Copy(svalX, sval, 0, gamsglobals.sv_max);

            for (i = 0; i < gamsglobals.maxdim; i++) if (ntgri[i] != (i + 1) * 123) v++;
            for (i = 0; i < gamsglobals.val_max; i++) if (Math.Abs(recv[i] - i * 3.14159265) > 1e-6) v++;
            //for (i = 0; i < gamsglobals.maxdim; i++)
            //{
            //    strncpy(tmp2,ssti + i*256 + 1,(int) *(ssti + i*256));
            //    tmp2[(int) *(ssti + i*256)] = '\0';
            //    sprintf(tmp, "j%d", i+1);
            //    if(strcmp(tmp2,tmp)) v++;
            //}
            for (i = 0; i < gamsglobals.sv_max; i++) if (Math.Abs(sval[i] - i * 3.14159265) > 1e-6) v++;
        } /* gdxtypes */

        static int Main(string[] args)
        {
            IntPtr pntr = IntPtr.Zero;
            IntPtr pntr2 = IntPtr.Zero;
            int i, b, c;
            long xx;
            bool e;
            double y;
            double[] pda = new double[3];
            int[] pia = new int[3];
            byte[] pc = new byte[256];
            string sst;
            int[] ntgri = new int[gamsglobals.maxdim];
            double[] recv = new double[gamsglobals.val_max];
            string[] ssti = new string[gamsglobals.maxdim];
            double[] sval = new double[gamsglobals.sv_max];
            string Msg="";
            c_wrpcs.TMsgCallback0 AdMCB0;

            Console.WriteLine("Start of Testercs");

            c_wrpcs wrp = new c_wrpcs(ref Msg);
            if (Msg != String.Empty)
            {
                Console.WriteLine("*** Error during initialization: " + Msg);
                Environment.Exit(-1);
            }

            Console.WriteLine("PTR    Test");
            wrp.wrpptr2(ref pntr);
            if (wrp.wrpptr1(pntr) > 0)
                wrperror("*** PTR Test failed!");

            Console.WriteLine("INT1   Test");
            if (wrp.wrpint1(123) > 0)
                Console.WriteLine("*** INT1 Test failed!");

            Console.WriteLine("INT2   Test");
            x = 321;
            if (wrp.wrpint2(ref x) > 0)
                wrperror("*** INT2 Test failed (passing data to library)!");
            if (wrp.wrpint1(x) > 0)
                wrperror("*** INT2 Test failed (getting data from library)!");

            Console.WriteLine("INT64 Test");
            if (wrp.wrpint64((long)987654321*987654321) > 0)
                Console.WriteLine("*** INT64 Test failed!");

            Console.WriteLine("VINT64 Test");
            xx = (long)123456789*123456789;
            if (wrp.wrpvint64(ref xx) > 0)
                wrperror("*** VINT64 Test failed (passing data to library)!");
            if (wrp.wrpint64(xx) > 0)
                wrperror("*** VINT64 Test failed (getting data from library)!");

            Console.WriteLine("OINT64 Test");
            xx = (long)0;
            if (wrp.wrpoint64(ref xx) > 0)
                wrperror("*** OINT64 Test failed (getting data from library)!");
            if (wrp.wrpint64(xx) > 0)
                wrperror("*** OINT64 Test failed (getting data from library)!");

            Console.WriteLine("PDA1   Test");
            for (i = 0; i < 3; i++)
                pda[i] = (i + 1) * 3.14159265;

            if (wrp.wrppda1(pda) > 0)
                wrperror("*** PDA1 Test failed!");

            Console.WriteLine("PDA2   Test");
            x = 0;
            wrp.wrppda2(ref pda);
            for (i = 0; i < 3; i++)
                x = x + wrp.wrpdbl1(pda[i]);

            if (x > 0)
                wrperror("*** PDA2 Test failed!");

            Console.WriteLine("PIA1   Test");
            for (i = 0; i < 3;i++)
                pia[i] = (i + 1) * 123;

            if (wrp.wrppia1(pia) > 0)
                wrperror("*** PIA1 Test failed!");

            Console.WriteLine("PIA2   Test");
            x = 0;
            wrp.wrppia2(ref pia);
            for (i = 0;i < 3;i++)
                x = x + wrp.wrpint1(pia[i]);

            if (x > 0)
                wrperror("*** PIA2 Test failed!");

            Console.WriteLine("PC1    Test");
            sst = "GAMS";
            for (i = 0;i < sst.Length;i++)
                pc[i] = (byte)sst[i];

            if (wrp.wrppc1(pc) > 0)
                wrperror("*** PC1 Test failed!");

            Console.WriteLine("PC2    Test");
            wrp.wrppc2(ref pc);
            if (wrp.wrppc1(pc) > 0)
                wrperror("*** PC2 Test failed!");

            Console.WriteLine("SST1   Test");
            if (wrp.wrpsst1("Hello GAMS") > 0)
                wrperror("*** SST1 Test failed!");

            Console.WriteLine("SST2   Test");
            wrp.wrpsst2(ref sst);
            if (wrp.wrpsst1(sst) > 0)
                wrperror("*** SST2 Test failed!");

            Console.WriteLine("SST3   Test");
            wrp.wrpsst3(ref sst);
            if (wrp.wrpsst1(sst) > 0)
                wrperror("*** SST3 Test failed!");

            Console.WriteLine("DBL1   Test");
            if (wrp.wrpdbl1(3.14159265) > 0)
                wrperror("*** DBL1 Test failed!");

            Console.WriteLine("DBL2   Test");
            y = 3.14159265 * 3.14159265;
            wrp.wrpdbl2(ref y);
            if (wrp.wrpdbl1(y) > 0)
                wrperror("*** DBL2 Test failed!");

            Console.WriteLine("UELI1  Test");
            for (i = 0; i < gamsglobals.maxdim; i++)
                ntgri[i] = (i + 1) * 123;

            if (wrp.wrpueli1(ntgri) > 0)
                wrperror("*** UELI1 Test failed!");

            Console.WriteLine("UELI2  Test");
            x = 0;
            wrp.wrpueli2(ref ntgri);
            for (i = 0; i < gamsglobals.maxdim; i++)
                x = x + wrp.wrpint1(ntgri[i]);

            if (x > 0)
                wrperror("*** UELI2 Test failed!");

            Console.WriteLine("VALS1  Test");
            for (b = 0; b < gamsglobals.val_max; b++)
                recv[b] = (b + 1) * 3.14159265;

            if (wrp.wrpvals1(recv) > 0)
                wrperror("*** VALS1 Test failed!");

            Console.WriteLine("VALS2  Test");
            x = 0;
            wrp.wrpvals2(ref recv);
            for (b = 0; b < gamsglobals.val_max; b++)
                x = x + wrp.wrpdbl1(recv[b]);

            if (x > 0)
                wrperror("*** VALS2 Test failed!");

            Console.WriteLine("STRI1  Test");
            for (i = 0; i < gamsglobals.maxdim; i++)
                ssti[i] = "dim" + (i + 1);

            if (wrp.wrpstri1(ssti) > 0)
                wrperror("*** STRI1 Test failed!");

            Console.WriteLine("STRI2  Test");
            wrp.wrpstri2(ref ssti);

            for (i = 0; i < gamsglobals.maxdim; i++)
            {
                if (ssti[i] != "j" + (i + 1))
                {
                    wrperror("*** STRI2 Test failed!");
                    break;
                }
            }

            Console.WriteLine("SVALS1 Test");
            for (c = 0; c < gamsglobals.sv_max; c++)
                sval[c] = (c + 1) * 3.14159265;

            if (wrp.wrpsvals1(sval) > 0)
                wrperror("*** SVALS1 Test failed!");

            Console.WriteLine("SVALS2 Test");
            x = 0;
            wrp.wrpsvals2(ref sval);
            for (c = 0; c < gamsglobals.sv_max; c++)
                x = x + wrp.wrpdbl1(sval[c]);
            if (x > 0)
                wrperror("*** SVALS2 Test failed!");

            Console.WriteLine("BOOL   Test");
            if (wrp.wrpbool1(true) > 0)
                wrperror("*** BOOL Test failed (passing data to library)!");

            Console.WriteLine("BOOL2  Test");
            e = false;
            if (wrp.wrpbool2(ref e) > 0)
                wrperror("*** BOOL2 Test failed (passing data to library)!");
            if (wrp.wrpbool1(e) > 0)
                wrperror("*** BOOL2 Test failed (getting data from library)!");

            Console.WriteLine("MAXARG Test");
            if (wrp.wrpMaxArg(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20) != 21 * 20 / 2) wrperror("*** MAXARG Test failed!");

            v = 0;
            Console.WriteLine("ALLARGCB Test");
            if ((wrp.wrpFPAllTy(allTypes) > 0) || (v > 0)) wrperror("*** ALLARGCB Test failed!");

            v = 0;
            Console.WriteLine("GDXARGCB Test");
            if ((wrp.wrpFPgdxTy(gdxTypes) > 0) || (v > 0)) wrperror("*** GDXARGCB Test failed!");

            Console.WriteLine("SETMCB Test");
            //w = 0;
            x = 0;
            x2 = 0;
            z = 0;
            cb1count = 0;
            cb1count2 = 0;
            cb2count = 0;
            c_wrpcs wrp2 = new c_wrpcs(ref Msg);
            if (Msg != String.Empty)
            {
                Console.WriteLine("*** Error during initialization: " + Msg);
                Environment.Exit(-1);
            }
            wrp.wrpsetmcb1(msg1Callback);
            wrp2.wrpsetmcb1(msg1Callback2);
            //wrp.wrpmcb0pset(PropCallback);
            wrp.wrpsetmcb2(msg2Callback);
            wrp.wrpinitmcb();
            wrp2.wrpinitmcb();

            if ((x > 0) || (cb1count != 4))
                wrperror("*** SETMCB1 Test failed!");

            if ((x2 > 0) || (cb1count2 != 4))
                wrperror("*** SETMCB1 Test failed! (Problem with second object)");

            //if ((w > 0) || (cbpcount != 4))
            //    wrperror("*** MCB1SET Test failed! (property)");

            if ((z > 0) || (cb2count != 4))
                wrperror("*** SETMCB2 Test failed!");

            Console.WriteLine("GETMCB Test");
            AdMCB0 = msg1Callback;
            if (AdMCB0 != wrp.wrpgetmcb1())
                wrperror("*** GETMCB1 Test failed!");

            //AdMCB0 = PropCallback;
            //if (AdMCB0 != wrp.wrpmcb0p())
            //    wrperror("*** MCB1 Test failed! (property)");

            Console.WriteLine("PTRPROP Test");
            wrp.wrpptrPSet(pntr2);
            pntr = wrp.wrpptrP();
            if (pntr2 != pntr)
                wrperror("*** PTRPROP Test failed!");

            Console.WriteLine("INTPROP Test");
            wrp.wrpintPSet(123);
            i = wrp.wrpintP();
            if (i != 2 * 123)
                wrperror("*** INTPROP Test failed!");

            Console.WriteLine("INT64PROP Test");
            wrp.wrpint64PSet((long)987654321*987654321);
            xx = wrp.wrpint64P();
            if (xx != (long)2 * 987654321 * 987654321)
                wrperror("*** INTPROP Test failed!");

            //Console.WriteLine("PCPROP  Test");
            //sst = "GAMS";
            //for (i = 0; i < sst.Length; i++)
            //    pc[i] = (byte)sst[i];
            //wrp.wrpPCPSet(pc);
            //sst = wrp.wrpPCP();
            ////sst = "";
            ////for (i = 0; i < 4; i++)
            ////    sst = sst + (char)(pc[i]);
            //if (sst != "GUMS")
            //    wrperror("*** PCPROP Test failed!");

            //Console.WriteLine("SSTPROP Test");
            //wrp.wrpSSPSet("SMAG");
            //if (wrp.wrpSSP() != "SMUG")
            //    wrperror("*** SSTPROP Test failed!");

            Console.WriteLine("DBLPROP Test");
            wrp.wrpDPSet(3.14159265);
            y = wrp.wrpDP();
            if (Math.Abs(y * y - 3.14159265) > 0.000001)
                wrperror("*** DBLPROP Test failed!");

            Console.WriteLine("BOOLPROPa Test");
            wrp.wrpboolPSet(true);
            if (wrp.wrpboolP())
                wrperror("*** BOOLPROPa Test failed!");

            Console.WriteLine("BOOLPROPb Test");
            wrp.wrpboolPSet(false);
            if (!wrp.wrpboolP())
                wrperror("*** BOOLPROPb Test failed!");

            Console.WriteLine("PTRRET   Test");
            pntr = wrp.wrpptrR();
            if (wrp.wrpptr1(pntr) > 0)
                wrperror("*** PTRRET Test failed!");

            Console.WriteLine("INTRET   Test");
            x = wrp.wrpintR();
            if (wrp.wrpint1(x) > 0)
                wrperror("*** INTRET Test failed!");
            sst = "";

            Console.WriteLine("INT64RET Test");
            xx = wrp.wrpint64R();
            if (wrp.wrpint64(xx) > 0)
                wrperror("*** INT64RET Test failed!");
            sst = "";

            //Console.WriteLine("PCRET    Test");
            //sst = wrp.wrppcr(pc);
            //for (i = 0; i < sst.Length; i++)
            //    pc[i] = (byte)sst[i];

            //if (wrp.wrppc1(pc) > 0)
            //    wrperror("*** PCRET Test failed!");

            //Console.WriteLine("SSTRET Test");
            //if (wrp.wrpSSTR() != "Return GAMS")
            //    wrperror("*** SSTRET Test failed!");

            Console.WriteLine("DBLRET   Test");
            y = wrp.wrpDR();
            if (wrp.wrpdbl1(y) > 0)
                wrperror("*** DBLRET Test failed!");

            Console.WriteLine("BOOLRET  Test");
            if (!wrp.wrpboolR())
                wrperror("*** BOOLRET Test failed!");

            Console.WriteLine("FPTRRET  Test");
            AdMCB0 = msg1Callback;
            if (AdMCB0 != wrp.wrpFuncPtrR())
                wrperror("*** FPTRRET Test failed!");

            Console.WriteLine();
            Console.WriteLine("End of testercs: " + rc + " Failures");
            wrp.wrpFree();
            
            return rc;
        }
    }
}
