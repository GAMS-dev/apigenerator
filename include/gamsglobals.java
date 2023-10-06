/* Copyright (c) 2016-2023 GAMS Software GmbH <support@gams.com>
 * Copyright (c) 2016-2023 GAMS Development Corp. <support@gams.com>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

package com.gams.api;

public class gamsglobals {
    public static final int maxdim = 20;
    public static final int str_len = 256;
   
    public static final int val_level    = 0;
    public static final int val_marginal = 1;
    public static final int val_lower    = 2;
    public static final int val_upper    = 3;
    public static final int val_scale    = 4;
    public static final int val_max      = 5;

    public static final int sv_und     = 0;
    public static final int sv_na      = 1;
    public static final int sv_pin     = 2;
    public static final int sv_min     = 3;
    public static final int sv_eps     = 4;
    public static final int sv_normal  = 5;
    public static final int sv_acronym = 6;
    public static final int sv_max     = 7;

    public static final int dt_set   = 0;
    public static final int dt_par   = 1;
    public static final int dt_var   = 2;
    public static final int dt_equ   = 3;
    public static final int dt_alias = 4;
    public static final int dt_max   = 5;
    
    public static final double sv_valund     =  1.0E300;   // undefined
    public static final double sv_valna      =  2.0E300;   // not available/applicable
    public static final double sv_valpin     =  3.0E300;   // plus infinity
    public static final double sv_valmin     =  4.0E300;   // minus infinity
    public static final double sv_valeps     =  5.0E300;   // epsilon
    public static final double sv_valacronym = 10.0E300;   // potential/real acronym
}
