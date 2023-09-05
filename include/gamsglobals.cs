// Copyright (c) 2016-2023 GAMS Software GmbH <support@gams.com>
// Copyright (c) 2016-2023 GAMS Development Corp. <support@gams.com>
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

/// <summary>
/// Collection of global constants
/// </summary>
public class gamsglobals
{
    /// <summary>
    /// Maximum GAMS symobl dimension
    /// </summary>
    public const int maxdim = 20;
    /// <summary>
    /// ShortString length
    /// </summary>
    public const int str_len = 256;

    /// <summary>
    /// Level
    /// </summary>
    public const int val_level = 0;
    /// <summary>
    /// Marginal
    /// </summary>
    public const int val_marginal = 1;
    /// <summary>
    /// Lower Bound
    /// </summary>
    public const int val_lower = 2;
    /// <summary>
    /// Upper Bound
    /// </summary>
    public const int val_upper = 3;
    /// <summary>
    /// Scale
    /// </summary>
    public const int val_scale = 4;
    /// <summary>
    /// Val Max
    /// </summary>
    public const int val_max = 5;

    /// <summary>
    /// Undefined
    /// </summary>
    public const int sv_und = 0;
    /// <summary>
    /// Not Applicable
    /// </summary>
    public const int sv_na = 1;
    /// <summary>
    /// Plus Infinity
    /// </summary>
    public const int sv_pin = 2;
    /// <summary>
    /// Minus Infinity
    /// </summary>
    public const int sv_min = 3;
    /// <summary>
    /// Epsilon
    /// </summary>
    public const int sv_eps = 4;
    /// <summary>
    /// Normal
    /// </summary>
    public const int sv_normal = 5;
    /// <summary>
    /// Acronym
    /// </summary>
    public const int sv_acronym = 6;
    /// <summary>
    /// SV Max
    /// </summary>
    public const int sv_max = 7;

    /// <summary>
    /// Set
    /// </summary>
    public const int dt_set = 0;
    /// <summary>
    /// Parameter
    /// </summary>
    public const int dt_par = 1;
    /// <summary>
    /// Variable
    /// </summary>
    public const int dt_var = 2;
    /// <summary>
    /// Equation
    /// </summary>
    public const int dt_equ = 3;
    /// <summary>
    /// Alias
    /// </summary>
    public const int dt_alias = 4;
    /// <summary>
    /// DT Max
    /// </summary>
    public const int dt_max = 5;

    /// <summary>
    /// Default value of Undefined
    /// </summary>
    public const double sv_valund = 1.0E300;   // undefined
    /// <summary>
    /// Default value of Not Applicable
    /// </summary>
    public const double sv_valna = 2.0E300;   // not available/applicable
    /// <summary>
    /// Default value of Plus Infinity
    /// </summary>
    public const double sv_valpin = 3.0E300;   // plus infinity
    /// <summary>
    /// Default value of Minus Infinity
    /// </summary>
    public const double sv_valmin = 4.0E300;   // minus infinity
    /// <summary>
    /// Default value of Epsilon
    /// </summary>
    public const double sv_valeps = 5.0E300;   // epsilon
    /// <summary>
    /// Default value of Acronym
    /// </summary>
    public const double sv_valacronym = 10.0E300;   // potential/real acronym
}