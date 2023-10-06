Module gamsglobals
' Copyright (c) 2016-2023 GAMS Software GmbH <support@gams.com>
' Copyright (c) 2016-2023 GAMS Development Corp. <support@gams.com>
'
' Permission is hereby granted, free of charge, to any person obtaining a copy
' of this software and associated documentation files (the "Software"), to deal
' in the Software without restriction, including without limitation the rights
' to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
' copies of the Software, and to permit persons to whom the Software is
' furnished to do so, subject to the following conditions:
'
' The above copyright notice and this permission notice shall be included in all
' copies or substantial portions of the Software.
'
' THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
' IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
' FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
' AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
' LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
' OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
' SOFTWARE.

    Public Const maxdim As Integer = 19
    Public Const str_len As Integer = 255

    Public Const val_level As Integer = 0
    Public Const val_marginal As Integer = 1
    Public Const val_lower As Integer = 2
    Public Const val_upper As Integer = 3
    Public Const val_scale As Integer = 4
    Public Const val_max As Integer = 4

    Public Const sv_und As Integer = 0
    Public Const sv_na As Integer = 1
    Public Const sv_pin As Integer = 2
    Public Const sv_min As Integer = 3
    Public Const sv_leps As Integer = 4
    Public Const sv_normal As Integer = 5
    Public Const sv_acronym As Integer = 6
    Public Const sv_max As Integer = 6

    Public Const dt_set As Integer = 0
    Public Const dt_par As Integer = 1
    Public Const dt_var As Integer = 2
    Public Const dt_equ As Integer = 3
    Public Const dt_alias As Integer = 4
    Public Const dt_max As Integer = 4

    Public Const sv_valund As Double = 1.0E+300       ' undefined
    Public Const sv_valna As Double = 2.0E+300        ' not available/applicable
    Public Const sv_valpin As Double = 3.0E+300       ' plus infinity
    Public Const sv_valmin As Double = 4.0E+300       ' minus infinity
    Public Const sv_valeps As Double = 5.0E+300       ' epsilon
    Public Const sv_valacronym As Double = 1.0E+301   ' potential/real acronym
End Module