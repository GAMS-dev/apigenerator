Module testervbnet
    Dim rc As Integer = 0
    Dim cb1count As Integer = 0
    Dim cb1count2 As Integer = 0
    Dim cb2count As Integer = 0
    'Dim cbpcount As Integer = 0
    Dim v As Integer = 0
    Dim x As Integer = 0
    Dim x2 As Integer = 0
    Dim w As Integer = 0
    Dim z As Integer = 0

    Dim objptr As Integer
    Dim objptr2 As Integer

    Sub wrperror(ByVal err As String)
        rc = rc + 1
        Console.WriteLine(err)
    End Sub

    Sub msg1Callback(ByVal mode As Integer, ByVal msgBuf As String) 'pchar
        cb1count = cb1count + 1
        Select Case mode
            Case 0
                If msgBuf <> "Hello G" Then x = x + 1
            Case 1
                If msgBuf <> "Hello A" Then x = x + 1
            Case 2
                If msgBuf <> "Hello M" Then x = x + 1
            Case 3
                If msgBuf <> "Hello S" Then x = x + 1
        End Select
    End Sub

    Sub msg1Callback2(ByVal mode As Integer, ByVal msgBuf As String) 'pchar
        cb1count2 = cb1count2 + 1
        Select Case mode
            Case 0
                If msgBuf <> "Hello G" Then x2 = x2 + 1
            Case 1
                If msgBuf <> "Hello A" Then x2 = x2 + 1
            Case 2
                If msgBuf <> "Hello M" Then x2 = x2 + 1
            Case 3
                If msgBuf <> "Hello S" Then x2 = x2 + 1
        End Select
    End Sub

    'Sub PropCallback(ByVal mode As Integer, ByVal msgBuf As String) 'pchar
    '    cbpcount = cbpcount + 1
    '    Select Case mode
    '        Case 0
    '            If msgBuf <> "Prop G" Then w = w + 1
    '        Case 1
    '            If msgBuf <> "Prop A" Then w = w + 1
    '        Case 2
    '            If msgBuf <> "Prop M" Then w = w + 1
    '        Case 3
    '            If msgBuf <> "Prop S" Then w = w + 1
    '    End Select
    'End Sub

    Sub msg2Callback(ByVal mode As Integer, ByVal msgBufX As String)
        Dim msgbuf As String = ""
        msgbuf = msgBufX.Substring(1, Asc(msgBufX))
        cb2count = cb2count + 1
        Select Case mode
            Case 0
                If msgbuf <> "Hello G" Then z = z + 1
            Case 1
                If msgbuf <> "Hello A" Then z = z + 1
            Case 2
                If msgbuf <> "Hello M" Then z = z + 1
            Case 3
                If msgbuf <> "Hello S" Then z = z + 1
        End Select
    End Sub

    Sub allTypes(ByVal pntr As IntPtr, ByVal ntgr As Integer, ByVal cptrdaX As IntPtr, ByVal cptriaX As IntPtr, ByVal cptrc As String, ByVal csst As String, ByVal dbl As Double, ByVal b As Integer, ByVal chr As Char)
        Dim i As Integer
        Dim msg As String = ""
        Dim cptrda(2) As Double
        Dim cptria(2) As Integer
        msg = csst.Substring(1, Asc(csst))
        System.Runtime.InteropServices.Marshal.Copy(cptrdaX, cptrda, 0, 3)
        System.Runtime.InteropServices.Marshal.Copy(cptriaX, cptria, 0, 3)

        If pntr.ToInt64 Mod 1 <> 0 Then v = v + 1
        If ntgr <> 1 Then v = v + 1
        If cptrc <> "GAMS" Then v = v + 1
        If msg <> "GAMS" Then v = v + 1
        If Math.Abs(dbl - 3.14159265) > 0.000001 Then v = v + 1
        If b <> 1 Then v = v + 1
        If chr <> "G" Then v = v + 1
        For i = 0 To 2
            If Math.Abs(cptrda(i) - (i + 1) * 3.14159265) > 0.000001 Then v = v + 1
        Next
        For i = 0 To 2
            If cptria(i) <> (i + 1) * 123 Then v = v + 1
        Next
    End Sub

    Sub gdxTypes(ByVal ntgriX As IntPtr, ByVal recvX As IntPtr, ByVal sstiX As IntPtr, ByVal svalX As IntPtr)
        Dim i As Integer
        Dim ntgri_l(maxdim) As Integer
        Dim recv_l(val_max) As Double
        Dim ssti_l(maxdim) As IntPtr
        Dim cvcv(255) As Char
        Dim sval_l(sv_max) As Double

        System.Runtime.InteropServices.Marshal.Copy(ntgriX, ntgri_l, 0, maxdim + 1)
        System.Runtime.InteropServices.Marshal.Copy(recvX, recv_l, 0, val_max + 1)
        System.Runtime.InteropServices.Marshal.Copy(sstiX, ssti_l, 0, maxdim + 1)
        System.Runtime.InteropServices.Marshal.Copy(svalX, sval_l, 0, sv_max + 1)

        For i = 0 To maxdim
            If ntgri_l(i) <> (i + 1) * 123 Then v = v + 1
        Next
        For i = 0 To val_max
            If Math.Abs(recv_l(i) - i * 3.14159265) > 0.000001 Then v = v + 1
        Next
        'For i = 0 To maxdim
        '    If ssti_l(i) <> "j" + (i + 1).ToString Then v = v + 1
        'Next
        For i = 0 To sv_max
            If Math.Abs(sval_l(i) - i * 3.14159265) > 0.000001 Then v = v + 1
        Next
    End Sub


    Sub Main()
        Dim pntr As IntPtr = 0
        Dim i As Integer
        Dim b As Integer
        Dim c As Integer
        Dim xx As Int64
        Dim d As Char
        Dim e As Boolean
        Dim y As Double
        Dim pda(2) As Double
        Dim pia(2) As Integer
        Dim pc(255) As Byte
        Dim sst As String
        Dim ntgri(maxdim) As Integer
        Dim recv(val_max) As Double
        Dim ssti(maxdim) As String
        Dim sval(sv_max) As Double
        Dim Msg As String = String.Empty
        Dim AdMCB0 As tmsgcallback0

        Console.WriteLine("Start of testervbnet")

        If Not wrpcreate(objptr, Msg) Then
            Console.WriteLine("*** Error during initialization!")
            Exit Sub
        End If

        Console.WriteLine("PTR    Test")
        wrpptr2(objptr, pntr)
        If wrpptr1(objptr, pntr) > 0 Then
            wrperror("*** PTR Test failed!")
        End If

        Console.WriteLine("INT1   Test")
        If wrpint1(objptr, 123) > 0 Then
            wrperror("*** INT1 Test failed!")
        End If

        Console.WriteLine("INT2   Test")
        x = 321
        If wrpint2(objptr, x) > 0 Then
            wrperror("*** INT2 Test failed (passing data to library)!")
        End If
        If wrpint1(objptr, x) > 0 Then
            wrperror("*** INT2 Test failed (getting data from library)!")
        End If

        Console.WriteLine("INT64 Test")
        xx = Convert.ToInt64(987654321) * 987654321
        If wrpint64(objptr, xx) > 0 Then
            wrperror("*** INT64 Test failed!")
        End If

        Console.WriteLine("VINT64 Test")
        xx = Convert.ToInt64(123456789) * 123456789
        If wrpvint64(objptr, xx) > 0 Then
            wrperror("*** VINT64 Test failed (passing data to library)!")
        End If
        If wrpint64(objptr, xx) > 0 Then
            wrperror("*** VINT642 Test failed (getting data from library)!")
        End If

        Console.WriteLine("OINT64 Test")
        xx = Convert.ToInt64(0)
        If wrpoint64(objptr, xx) > 0 Then
            wrperror("*** OINT64 Test failed (getting data from library)!")
        End If
        If wrpint64(objptr, xx) > 0 Then
            wrperror("*** OINT642 Test failed (getting data from library)!")
        End If

        Console.WriteLine("PDA1   Test")
        For i = 1 To 3
            pda(i - 1) = i * 3.14159265
        Next
        If wrppda1(objptr, pda) > 0 Then
            wrperror("*** PDA1 Test failed!")
        End If
        Console.WriteLine("PDA2   Test")
        x = 0
        wrppda2(objptr, pda)
        For i = 0 To 2
            x = x + wrpdbl1(objptr, pda(i))
        Next
        If x > 0 Then
            wrperror("*** PDA2 Test failed!")
        End If

        Console.WriteLine("PIA1   Test")
        For i = 1 To 3
            pia(i - 1) = i * 123
        Next
        If wrppia1(objptr, pia) > 0 Then
            wrperror("*** PIA1 Test failed!")
        End If

        Console.WriteLine("PIA2   Test")
        x = 0
        wrppia2(objptr, pia)
        For i = 0 To 2
            x = x + wrpint1(objptr, pia(i))
        Next
        If x > 0 Then
            wrperror("*** PIA2 Test failed!")
        End If

        Console.WriteLine("PC1    Test")
        sst = "GAMS"
        For i = 1 To sst.Length
            pc(i - 1) = Asc(Mid(sst, i, 1))
        Next i
        If wrppc1(objptr, pc(0)) > 0 Then
            wrperror("*** PC1 Test failed!")
        End If

        Console.WriteLine("PC2    Test")
        wrppc2(objptr, pc(0))
        If wrppc1(objptr, pc(0)) > 0 Then
            wrperror("*** PC2 Test failed!")
        End If

        Console.WriteLine("SST1   Test")
        If wrpsst1(objptr, "Hello GAMS") > 0 Then
            wrperror("*** SST1 Test failed!")
        End If

        Console.WriteLine("SST2   Test")
        wrpsst2(objptr, sst)
        If wrpsst1(objptr, sst) > 0 Then
            wrperror("*** SST2 Test failed!")
        End If

        Console.WriteLine("SST3   Test")
        wrpsst3(objptr, sst)
        If wrpsst1(objptr, sst) > 0 Then
            wrperror("*** SST3 Test failed!")
        End If

        Console.WriteLine("DBL1   Test")
        If wrpdbl1(objptr, 3.14159265) > 0 Then
            wrperror("*** DBL1 Test failed!")
        End If

        Console.WriteLine("DBL2   Test")
        y = 3.14159265 * 3.14159265
        wrpdbl2(objptr, y)
        If wrpdbl1(objptr, y) > 0 Then
            wrperror("*** DBL2 Test failed!")
        End If

        Console.WriteLine("UELI1  Test")
        For i = 0 To maxdim
            ntgri(i) = (i + 1) * 123
        Next
        If wrpueli1(objptr, ntgri) > 0 Then
            wrperror("*** UELI1 Test failed!")
        End If

        Console.WriteLine("UELI2  Test")
        x = 0
        wrpueli2(objptr, ntgri)
        For i = 0 To maxdim
            x = x + wrpint1(objptr, ntgri(i))
        Next
        If x > 0 Then
            wrperror("*** UELI2 Test failed!")
        End If

        Console.WriteLine("VALS1  Test")
        For b = 0 To val_max
            recv(b) = (b + 1) * 3.14159265
        Next
        If wrpvals1(objptr, recv) > 0 Then
            wrperror("*** VALS1 Test failed!")
        End If

        Console.WriteLine("VALS2  Test")
        x = 0
        wrpvals2(objptr, recv)
        For b = 0 To val_max
            x = x + wrpdbl1(objptr, recv(b))
        Next
        If x > 0 Then
            wrperror("*** VALS2 Test failed!")
        End If

        Console.WriteLine("STRI1  Test")
        For i = 0 To maxdim
            ssti(i) = "dim" + (i + 1).ToString
        Next

        If wrpstri1(objptr, ssti) > 0 Then
            wrperror("*** STRI1 Test failed!")
        End If

        Console.WriteLine("STRI2  Test")
        wrpstri2(objptr, ssti)
        For i = 0 To maxdim
            If ssti(i) <> "j" + (i + 1).ToString Then
                wrperror("*** STRI2 Test failed!")
                Exit For
            End If
        Next

        Console.WriteLine("SVALS1 Test")
        For c = 0 To sv_max
            sval(c) = (c + 1) * 3.14159265
        Next

        If wrpsvals1(objptr, sval) > 0 Then
            wrperror("*** SVALS1 Test failed!")
        End If

        Console.WriteLine("SVALS2 Test")
        x = 0
        wrpsvals2(objptr, sval)
        For c = 0 To sv_max
            x = x + wrpdbl1(objptr, sval(c))
        Next
        If x > 0 Then
            wrperror("*** SVALS2 Test failed!")
        End If

        Console.WriteLine("BOOL   Test")
        If (wrpbool1(objptr, True) > 0) Then
            wrperror("*** BOOL Test failed (passing data to library)!")
        End If


        Console.WriteLine("BOOL2  Test")
        e = False
        If (wrpbool2(objptr, e) > 0) Then
            wrperror("*** BOOL2 Test failed (passing data to library)!")
        End If
        If (wrpbool1(objptr, e) > 0) Then
            wrperror("*** BOOL2 Test failed (getting data from library)!")
        End If

        Console.WriteLine("MAXARG Test")
        If wrpmaxarg(objptr, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20) <> 21 * 20 / 2 Then
            wrperror("*** MAXARG Test failed!")
        End If

        v = 0
        Console.WriteLine("ALLARGCB Test")
        If (wrpfpallty(objptr, AddressOf allTypes) > 0) Or (v > 0) Then
            wrperror("*** ALLARGCB Test failed!")
        End If

        v = 0
        Console.WriteLine("GDXARGCB Test")
        If (wrpfpgdxty(objptr, AddressOf gdxTypes) > 0) Or (v > 0) Then
            wrperror("*** GDXARGCB Test failed!")
        End If

        Console.WriteLine("SETMCB Test")
        w = 0
        x = 0
        z = 0
        cb1count = 0
        cb1count2 = 0
        cb2count = 0
        If Not wrpcreate(objptr2, Msg) Then
            Console.WriteLine("*** Error during initialization!")
            Exit Sub
        End If
        wrpsetmcb1(objptr, AddressOf msg1Callback)
        wrpsetmcb1(objptr2, AddressOf msg1Callback2)
        'wrpmcb0pset(objptr, AddressOf PropCallback)
        wrpsetmcb2(objptr, AddressOf msg2Callback)
        wrpinitmcb(objptr)
        wrpinitmcb(objptr2)
        If (x > 0) Or (cb1count <> 4) Then
            wrperror("*** SETMCB1 Test failed!")
        End If
        If (x2 > 0) Or (cb1count2 <> 4) Then
            wrperror("*** SETMCB1 Test failed! (Problem with second object)")
        End If
        'If (w > 0) Or (cbpcount <> 4) Then
        '    wrperror("*** MCB1SET Test failed! (property)")
        'End If
        If (z > 0) Or (cb2count <> 4) Then
            wrperror("*** SETMCB2 Test failed!")
        End If

        Console.WriteLine("GETMCB Test")
        AdMCB0 = AddressOf msg1Callback
        If AdMCB0 <> wrpgetmcb1(objptr) Then
            wrperror("*** GETMCB1 Test failed!")
        End If

        'AdMCB0 = AddressOf PropCallback
        'If AdMCB0 <> wrpmcb0p(objptr) Then
        '    wrperror("*** MCB1 Test failed! (property)")
        'End If

        Console.WriteLine("PTRPROP Test")
        wrpptrpset(objptr, x)
        pntr = wrpptrp(objptr)
        If x <> pntr Then
            wrperror("*** PTRPROP Test failed!")
        End If

        Console.WriteLine("INTPROP Test")
        wrpintpset(objptr, 123)
        i = wrpintp(objptr)
        If i <> 2 * 123 Then
            wrperror("*** INTPROP Test failed!")
        End If

        Console.WriteLine("INT64PROP Test")
        wrpint64pset(objptr, Convert.ToInt64(987654321) * 987654321)
        xx = wrpint64p(objptr)
        If xx <> Convert.ToInt64(2) * 987654321 * 987654321 Then
            wrperror("*** INT64PROP Test failed!")
        End If

        'Console.WriteLine("PCPROP  Test")
        'sst = "GAMS"
        'For i = 1 To sst.Length
        '    pc(i - 1) = Asc(Mid(sst, i, 1))
        'Next i
        'wrppcpset(objptr, pc(0))
        'sst = ""
        'sst = wrppcp(objptr)
        'If sst <> "GUMS" Then
        '    wrperror("*** PCPROP Test failed!")
        'End If

        'Console.WriteLine("SSTPROP Test")
        'wrpsspset(objptr, "SMAG")
        'If wrpssp(objptr) <> "SMUG" Then
        '    wrperror("*** SSTPROP Test failed!")
        'End If

        Console.WriteLine("DBLPROP Test")
        wrpdpset(objptr, 3.14159265)
        y = wrpdp(objptr)
        If Math.Abs(y * y - 3.14159265) > 0.000001 Then
            wrperror("*** DBLPROP Test failed!")
        End If

        Console.WriteLine("BOOLPROPa Test")
        wrpboolpset(objptr, True)
        If wrpboolp(objptr) Then
            wrperror("*** BOOLPROPa Test failed!")
        End If

        Console.WriteLine("BOOLPROPb Test")
        wrpboolpset(objptr, False)
        If Not wrpboolp(objptr) Then
            wrperror("*** BOOLPROPb Test failed!")
        End If

        Console.WriteLine("PTRRET   Test")
        pntr = wrpptrr(objptr)
        If wrpptr1(objptr, pntr) > 0 Then
            wrperror("*** PTRRET Test failed!")
        End If

        Console.WriteLine("INTRET   Test")
        x = wrpintr(objptr)
        If wrpint1(objptr, x) > 0 Then
            wrperror("*** INTRET Test failed!")
        End If

        Console.WriteLine("INT64RET Test")
        xx = wrpint64r(objptr)
        If wrpint64(objptr, xx) > 0 Then
            wrperror("*** INT64RET Test failed!")
        End If

        'sst = ""
        'Console.WriteLine("PCRET    Test")
        'sst = wrpPCR(objptr, pc(0))

        'For i = 1 To sst.Length
        '    pc(i - 1) = Asc(Mid(sst, i, 1))
        'Next i

        'If wrppc1(objptr, pc(0)) > 0 Then
        '    wrperror("*** PCRET Test failed!")
        'End If

        'Console.WriteLine("SSTRET   Test")
        'If wrpsstr(objptr) <> "Return GAMS" Then
        '    wrperror("*** SSTRET Test failed!")
        'End If

        Console.WriteLine("DBLRET   Test")
        y = wrpdr(objptr)
        If wrpdbl1(objptr, y) > 0 Then
            wrperror("*** DBLRET Test failed!")
        End If

        Console.WriteLine("BOOLRET  Test")
        If Not wrpboolr(objptr) Then
            wrperror("*** BOOLRET Test failed!")
        End If

        Console.WriteLine("FPTRRET  Test")
        AdMCB0 = AddressOf msg1Callback
        If AdMCB0 <> wrpfuncptrr(objptr) Then
            wrperror("*** FPTRRET Test failed!")
        End If

        Console.WriteLine("CHAR1  Test")
        If wrpc1(objptr, "G") > 0 Then
            wrperror("*** CHAR1 Test failed!")
        End If

        Console.WriteLine("CHAR2  Test")
        wrpc2(objptr, d)
        If wrpc1(objptr, d) > 0 Then
            wrperror("*** CHAR2 Test failed!")
        End If

        Console.WriteLine("CHARRET Test")
        If wrpc1(objptr, wrpcr(objptr)) > 0 Then
            wrperror("*** CHARRET Test failed!")
        End If

        Console.WriteLine("Constants Test")
        Dim intValue As Integer
        Dim floatValue As Double

        intValue = wrpIntValue
        If intValue <> 64 Then
            wrperror("*** Integer Max Integer Vlaue Test failed!")
        End If

        intValue = wrpInt_A
        If intValue <> 0 Then
            wrperror("*** Integer Constant Type A Test failed!")
        End If

        intValue = wrpInt_B
        If intValue <> 1 Then
            wrperror("*** Integer Constant Type B Test failed!")
        End If

        intValue = wrpInt_C
        If intValue <> 2 Then
            wrperror("*** Integer Constant Type C Test failed!")
        End If
      
        floatValue = wrpFloatValue
        If Math.Abs(floatValue + 0.148759) > 0.0001 Then
            wrperror("*** Double Constant Test failed!")
        End If

        Dim strValue As String

        strValue = wrpStringValue
        If String.Compare(strValue, "StringValue") <> 0 Then
            wrperror("*** String Constant Test failed!")
        End If

        strValue = wrpString_Option1
        If String.Compare(strValue, "First Option") <> 0 Then
            wrperror("*** String Option1 Constant Test failed!")
        End If

        strValue = wrpString_Option2
        If String.Compare(strValue, "Second Option") <> 0 Then
            wrperror("*** String Option2 Constant Test failed!")
        End If

        strValue = wrpString_Option3
        If String.Compare(strValue, "Third Option") <> 0 Then
            wrperror("*** String Option3 Constant Test failed!")
        End If

        Console.WriteLine()
        Console.WriteLine("End of testervbnet: " & rc & " Failures")
        wrpFree(objptr)

        Environment.Exit(rc)

    End Sub


End Module
