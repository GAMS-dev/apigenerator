#!/usr/bin/env python3
import sys
import argparse
import os
import datetime
import yaml
import pandas as pd
import pathlib
import subprocess
from jinja2 import Environment, FileSystemLoader
from datavalidator import DataValidator
from yamlloader import Loader

class Definition:
    @staticmethod
    def data_definition():
        datadef = dict()
        datadef['ta'] = {  # Basic Argument types: not language specific
                    'columns'  : ['name', 'text'],
                    'elements' : DataValidator.type_arguments() }
        datadef['tass'] = { # String type arguments
                                 'columns'  : ['ta'],
                                 'elements' : DataValidator.string_type_arguments() }
        datadef['tapc'] = { # PChar type arguments
                                 'columns'  : ['ta' ],
                                 'elements' : DataValidator.pchar_type_arguments()  }
        datadef['taar'] = { # Array type arguments
                                 'columns'  : ['ta'],
                                 'elements' : DataValidator.array_type_arguments()  }
        datadef['tp'] = { # argument position
                              'columns'  : [ 'tp' ],
                              'elements' : [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', 'p' ]
        }
        datadef['tpp'] = { 'columns'  : [ 'tp' ],
                                'elements' : [ '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20' ]
        }
        datadef['pactions'] = {
            'columns'  : ['name', 'text'],
            'elements' : DataValidator.pactions()  }
        datadef['gmsta'] = {  # GAMS Data types
            'columns'  : ['ta', 'text'],
            'elements' : [ ['cII', ''],
                           ['vII', ''],
                           ['cRV', ''],
                           ['vRV', ''],
                           ['cSI', ''],
                           ['oSI', ''],
                           ['cSVA', ''],
                           ['vSVA', ''] ]        }
        datadef['taind'] = { # Index of argument type
            'columns'  : ['type', 'value'],
            'elements' : [ ['void', 0],
                           ['ptr', 1],
                           ['Vptr', 2],
                           ['int', 3],
                           ['Oint', 4],
                           ['Vint', 21],
                           ['int64', 23],
                           ['Vint64', 24],
                           ['Oint64', 25],
                           ['CPDA', 5],
                           ['PDA', 6],
                           ['CPLIA', 7],
                           ['PLIA', 8],
                           ['CPC', 9],
                           ['PC', 10],
                           ['cSS', 11],
                           ['oSS', 12],
                           ['xSS', 17],
                           ['D', 13],
                           ['OD', 14],
                           ['VD', 22],
                           ['bool', 15],
                           ['Vbool', 20],
                           ['cII', 51],
                           ['vII', 52],
                           ['cRV', 53],
                           ['vRV', 54],
                           ['cSI', 55],
                           ['oSI', 56],
                           ['cSVA', 57],
                           ['vSVA', 58],
                           ['FuncPtr', 59],
                           ['C', 18],
                           ['vC', 19] ]        }

        datadef['noType'] = { 'columns'  : ['ta', 'text'],
                                   'elements' : [ ]        }
        datadef['Spectamap'] = { 'bool'  :  'int' ,
                                      'Vbool' :  'Vint',
                                      'cII'   : 'CPLIA',
                                      'vII'   : 'PLIA' ,
                                      'cRV'   : 'CPDA' ,
                                      'vRV'   : 'PDA'  ,
                                      'cSVA'  : 'CPDA' ,
                                      'vSVA'  :  'PDA'  }
        datadef['CType'] = {
            'columns'  : ['ta', 'text'],
            'elements' : [ ['ptr', 'void'],     ['Vptr', 'void'],
                           ['int', 'int'],      ['Oint', 'int'],      ['Vint', 'int'],
                           ['int64', 'INT64'],  ['Oint64', 'INT64'],  ['Vint64', 'INT64'],
                           ['CPDA', 'double'],  ['PDA', 'double'],
                           ['CPLIA', 'int'],    ['PLIA', 'int'],
                           ['CPC', 'char'],     ['PC', 'char'],       ['cSS', 'char'],
                           ['oSS', 'char'],     ['xSS', 'char'],
                           ['D', 'double'],     ['OD', 'double'],     ['VD', 'double'],
                           ['bool', 'int'],     ['Vbool', 'int'],     ['cII', 'int'],    ['vII', 'int'],
                           ['cRV', 'double'],   ['vRV', 'double'],    ['cSI', 'char'],
                           ['oSI', 'char'],
                           ['cSVA', 'double'],    ['vSVA', 'double'],
                           ['void', 'void'],
                           ['C', 'char'],         ['vC', 'char'] ]        }
        datadef['CCall'] = {
            'columns'  : ['ta', 'text'],
            'elements' : [ ['ptr', '*'],
                           ['Vptr', '**'],
                           ['int', ''],     ['Oint', '*'],   ['Vint', '*'],
                           ['int64', ''],   ['Oint64', '*'], ['Vint64', '*'],
                           ['CPDA', ''],    ['PDA', ''],     ['CPLIA', ''],     ['PLIA', ''],
                           ['CPC', '*'],    ['PC', '*'],     ['cSS', '*'],      ['oSS', '*'],
                           ['xSS', '*'],
                           ['D', ''],
                           ['OD', '*'],     ['VD', '*'],
                           ['bool', ''],
                           ['Vbool', '*'],
                           ['cII', ''],     ['vII', ''],     ['cRV', ''],       ['vRV', ''],
                           ['cSI', '*'],    ['oSI', '*'],
                           ['cSVA', ''],    ['vSVA', ''],    ['FuncPtr', ''],   ['void', ''],
                           ['C', ''],
                           ['vC', '*'] ]        }
        datadef['CCall2'] = { # fix needed for sgi fortran compilers
            'columns'  : ['ta', 'text'],
            'elements' : [ ['ptr', ''],      ['Vptr', ''],
                           ['int', ''],      ['Oint', ''],     ['Vint', ''],
                           ['int64', ''],    ['Oint64', ''],   ['Vint64', ''],
                           ['CPDA', ''],     ['PDA', ''],        ['CPLIA', ''],        ['PLIA', ''],
                           ['CPC', '*'],     ['PC', '*'],
                           ['cSS', '*'],     ['oSS', '*'],       ['xSS', '*'],
                           ['D', ''],        ['OD', ''],         ['VD', ''],
                           ['bool', ''],     ['Vbool', ''],      ['cII', ''],           ['vII', ''],
                           ['cRV', ''],      ['vRV', ''],        ['cSI', ''],           ['oSI', ''],
                           ['cSVA', ''],     ['vSVA', ''],
                           ['FuncPtr', ''],  ['C', ''],
                           ['vC', '*'] ]        }
        datadef['CTMod'] = {
            'columns'  : ['ta', 'text'],
            'elements' : [ ['ptr', ''],           ['Vptr', ''],
                           ['int', ''],           ['Oint', ''],          ['Vint', ''],
                           ['int64', ''],         ['Oint64', ''],        ['Vint64', ''],
                           ['CPDA', 'const '],
                           ['PDA', ''],
                           ['CPLIA', 'const '],
                           ['PLIA', ''],
                           ['CPC', 'const '],
                           ['PC', ''],
                           ['cSS', 'const '],
                           ['oSS', ''],           ['xSS', ''],
                           ['D', ''],             ['OD', ''],       ['VD', ''],
                           ['bool', ''],          ['Vbool', ''],
                           ['cII', 'const '],
                           ['vII', ''],
                           ['cRV', 'const '],
                           ['vRV', ''],
                           ['cSI', 'const '],
                           ['oSI', ''],
                           ['cSVA', 'const '],
                           ['vSVA', ''],
                           ['FuncPtr', ''],
                           ['void', ''],
                           ['C', 'const '],
                           ['vC', ''] ]        }
        datadef['CDefVal'] = { # Default Return Values
            'columns'  : ['ta', 'text'],
            'elements' : [ ['ptr', 'NULL'],
                           ['int', '0'],
                           ['int64', '0'],
                           ['PDA', 'NULL'],
                           ['PLIA', 'NULL'],
                           ['PC', 'NULL'],
                           ['oSS', 'NULL'],
                           ['D', '0.0'],
                           ['bool', '0'],
                           ['FuncPtr', 'NULL'],
                           ['void', ''],
                           ['C', "'\\0'"] ]        }
        datadef['CArraySuf'] = {
            'columns'  : ['ta', 'text'],
            'elements' : [ ['ptr', ''],       ['Vptr', ''],
                           ['int', ''],       ['Oint', ''],      ['Vint', ''],
                           ['int64', ''],     ['Oint64', ''],    ['Vint64', ''],
                           ['CPDA', '[]'],    ['PDA', '[]'],    ['CPLIA', '[]'],   ['PLIA', '[]'],
                           ['CPC', ''],       ['PC', ''],
                           ['cSS', ''],       ['oSS', ''],      ['xSS', ''],
                           ['D', ''],         ['OD', ''],       ['VD', ''],
                           ['bool', ''],      ['Vbool', ''],
                           ['cII', '[]'],     ['vII', '[]'],    ['cRV', '[]'],     ['vRV', '[]'],
                           ['cSI', '[]'],     ['oSI', '[]'],    ['cSVA', '[]'],    ['vSVA', '[]'],
                           ['FuncPtr', ''],   ['void', ''],
                           ['C', ''],         ['vC', ''] ]        }
        datadef['CCType'] = {
            'columns'  : ['ta', 'text'],
            'elements' : [ ['ptr', 'void'],         ['Vptr', 'void'],
                           ['int', 'int'],          ['Oint', 'int'],         ['Vint', 'int'],
                           ['int64', 'INT64'],      ['Oint64', 'INT64'],     ['Vint64', 'INT64'],
                           ['CPDA', 'double'],      ['PDA', 'double'],
                           ['CPLIA', 'int'],        ['PLIA', 'int'],
                           ['CPC', 'char'],         ['PC', 'char'],
                           ['cSS', 'std::string'],  ['oSS', 'std::string'],  ['xSS', 'std::string'],
                           ['D', 'double'],         ['OD', 'double'],        ['VD', 'double'],
                           ['bool', 'bool'],        ['Vbool', 'bool'],
                           ['cII', 'int'],          ['vII', 'int'],
                           ['cRV', 'double'],       ['vRV', 'double'],
                           ['cSI', 'std::string'],  ['oSI', 'std::string'],
                           ['cSVA', 'double'],      ['vSVA', 'double'],
                           ['void', 'void'],
                           ['C', 'char'],           ['vC', 'char'] ]        }
        datadef['CCCall'] = {
            'columns'  : ['ta', 'text'],
            'elements' : [ ['ptr', '*'],
                           ['Vptr', '**'],
                           ['int', ''],      ['Oint', '&'],    ['Vint', '&'],
                           ['int64', ''],    ['Oint64', '&'],  ['Vint64', '&'],
                           ['CPDA', ''],     ['PDA', ''],
                           ['CPLIA', ''],    ['PLIA', ''],
                           ['CPC', '*'],     ['PC', '*'],
                           ['cSS', '&'],     ['oSS', '&'],    ['xSS', '&'],
                           ['D', ''],
                           ['OD', '&'],      ['VD', '&'],
                           ['bool', ''],
                           ['Vbool', '&'],
                           ['cII', ''],      ['vII', ''],     ['cRV', ''],      ['vRV', ''],
                           ['cSI', ''],      ['oSI', ''],     ['cSVA', ''],     ['vSVA', ''],
                           ['FuncPtr', ''],
                           ['C', ''],
                           ['vC', '&'] ]        }
        datadef['CCCall2'] = { # fix needed for sgi fortran compilers
            'columns'  : ['ta', 'text'],
            'elements' : [ ['ptr', ''],      ['Vptr', ''],
                           ['int', ''],      ['Oint', ''],     ['Vint', ''],
                           ['int64', ''],    ['Oint64', ''],   ['Vint64', ''],
                           ['CPDA', ''],     ['PDA', ''],    ['CPLIA', ''],    ['PLIA', ''],
                           ['CPC', '*'],     ['PC', '*'],
                           ['cSS', '*'],     ['oSS', '*'],   ['xSS', '*'],
                           ['D', ''],        ['OD', ''],     ['VD', ''],
                           ['bool', ''],     ['Vbool', ''],
                           ['cSI', '*'],     ['oSI', '*'],
                           ['FuncPtr', ''],
                           ['C', ''],
                           ['vC', '*'] ]        }
        datadef['CCTMod'] = {
            'columns'  : ['ta', 'text'],
            'elements' : [ ['ptr', ''],          ['Vptr', ''],
                           ['int', ''],          ['Oint', ''],         ['Vint', ''],
                           ['int64', ''],        ['Oint64', ''],       ['Vint64', ''],
                           ['CPDA', 'const '],
                           ['PDA', ''],
                           ['CPLIA', 'const '],
                           ['PLIA', ''],
                           ['CPC', 'const '],
                           ['PC', ''],
                           ['cSS', 'const '],
                           ['oSS', ''],          ['xSS', ''],
                           ['D', ''],            ['OD', ''],      ['VD', ''],
                           ['bool', ''],         ['Vbool', ''],
                           ['cII', 'const '],
                           ['vII', ''],
                           ['cRV', 'const '],
                           ['vRV', ''],
                           ['cSI', 'const '],
                           ['oSI', ''],
                           ['cSVA', 'const '],
                           ['vSVA', ''],
                           ['FuncPtr', ''],
                           ['C', ''],
                           ['vC', ''] ]        }
        datadef['CCTPost'] = {
            'columns'  : ['ta', 'text'],
            'elements' : [ ['ptr', ''],          ['Vptr', ''],
                           ['int', ''],          ['Oint', ''],     ['Vint', ''],
                           ['int64', ''],        ['Oint64', ''],   ['Vint64', ''],
                           ['CPDA', '[]'],       ['PDA', '[]'],    ['CPLIA', '[]'],  ['PLIA', '[]'],
                           ['CPC', ''],          ['PC', ''],
                           ['cSS', '.c_str()'],
                           ['oSS', ''],          ['xSS', ''],
                           ['D', ''],            ['OD', ''],       ['VD', ''],
                           ['bool', ''],         ['Vbool', ''],
                           ['cII', '[]'],        ['vII', '[]'],    ['cRV', '[]'],    ['vRV', '[]'],
                           ['cSI', '[]'],        ['oSI', '[]'],    ['cSVA', '[]'],   ['vSVA', '[]'],
                           ['FuncPtr', ''],
                           ['C', ''],
                           ['vC', ''] ]        }
        datadef['CCTPre'] = {
            'columns'  : ['ta', 'text'],
            'elements' : [ ['ptr', ''],       ['Vptr', ''],
                           ['int', ''],       ['Oint', '&'],     ['Vint', '&'],
                           ['int64', ''],     ['Oint64', '&'],   ['Vint64', '&'],
                           ['CPDA', ''],      ['PDA', ''],     ['CPLIA', ''],   ['PLIA', ''],
                           ['CPC', ''],       ['PC', ''],
                           ['cSS', ''],       ['oSS', ''],     ['xSS', ''],
                           ['D', ''],
                           ['OD', '&'],       ['VD', '&'],
                           ['bool', ''],
                           ['Vbool', '&'],
                           ['cII', ''],       ['vII', ''],     ['cRV', ''],     ['vRV', ''],
                           ['cSI', ''],       ['oSI', ''],     ['cSVA', ''],    ['vSVA', ''],
                           ['FuncPtr', ''],
                           ['C', ''],
                           ['vC', '&'] ]        }

        datadef['FChar'] = {
            'columns'  : ['ta', 'text'],
            'elements' : [ ['CPC', ''],  ['PC', ''],
                           ['cSS', ''],  ['oSS', ''],  ['xSS', ''],
                           ['cSI', ''],  ['oSI', ''] ]        }
        datadef['FVal'] = {
            'columns'  : ['ta', 'text'],
            'elements' : [ ['ptr', ''],
                           ['int', ''],
                           ['int64', ''],
                           ['D', ''],
                           ['bool', ''] ]        }
        datadef['FLoc'] = {
            'columns'  : ['ta', 'text'],
            'elements' : [ ['Vptr', ''],
                           ['Oint', ''],
                           ['Oint64', ''],
                           ['Vint', ''],
                           ['Vint64', ''],
                           ['CPC', ''],
                           ['PC', ''],
                           ['cSS', ''],
                           ['oSS', ''],
                           ['xSS', ''],
                           ['OD', ''],
                           ['VD', ''],
                           ['Vbool', ''],
                           ['cSI', ''],
                           ['oSI', ''],
                           ['C', ''],
                           ['vC', ''] ]        }

        for key in datadef.keys():
            if  key in ['ta', 'taind', 'gmsta', 'pactions',
                        'CCall', 'CCall2', 'CType', 'CTMod', 'CArraySuf', 'CDefVal',
                        'JCall', 'JType', 'JTMod', 'jniCall', 'jniType', 'jniTMod','jniSig',
                        'VBAType', 'VBACall', 'VBNetType', 'VBNetCall', 'VBNetDefVal',
                        'FChar','FVal', 'FLoc']:
               for e in datadef[key]['elements']:
                   e[0] = e[0].lower()
               df = pd.DataFrame(datadef[key]['elements'], columns=datadef[key]['columns'])
               datadef[key]['elements'] = df
            elif key in ['tass', 'tapc', 'taar', 'tp', 'tpp']:
               elist = [e.lower() for e in datadef[key]['elements']]
               df = pd.DataFrame(elist, columns=datadef[key]['columns'])
               datadef[key]['elements'] = df

        for key,value in datadef['Spectamap'].items():
            Definition.addSpecialTypeMap(datadef, 'CType',  datadef['CType']['elements'],  key, value)
            Definition.addSpecialTypeMap(datadef, 'CCall',  datadef['CCall']['elements'],  key, value)
            Definition.addSpecialTypeMap(datadef, 'CCall2', datadef['CCall2']['elements'], key, value)
            Definition.addSpecialTypeMap(datadef, 'CTMod',  datadef['CTMod']['elements'],  key, value)
            Definition.addSpecialTypeMap(datadef, 'CArraySuf', datadef['CArraySuf']['elements'], key, value)

        datadef['extraFuncNames']   = { # function names
            'columns' : ['name'],
            'elements': [ 'Create','CreateD','CreateDD','CreateL',
                          'GetReady','GetReadyD','GetReadyL',
                          'Exit','Free','GetAPIErrorCount',
                          'GetScreenIndicator','SetScreenIndicator','GetExitIndicator','SetExitIndicator',
                          'SetErrorCallback']  }

        datadef['definition']   = {
            'title'       : 'Title',
            'prefix'      : 'Prefix',
            'preprefix'   : 'Preprefix',
            'description' : 'Description',
            'apiversion'  : 'APIVersion',
            'compatibleversion' : 'Version',
            'output'      : 'output',
            'testmode'    : 'testmode',
            'outputpath'  : 'OutputPath',
            'extrause'    : 'ExtraUse',
            'extrausem'   : 'ExtraUse',
            'extracuse'   : 'ExtraCUse',
            'title'       : 'Title',
            'dunit'       : 'DUnit',
            'dobject'     : 'DObject',
            'dobjectint'  : 'DObjectInt',
            'usecd'       : 'UseCD',
            'generic'     : 'generic',
            'maxdimstyle' : 'MaxDimStyle',
            'clibuse'     : 'CLibUse',
            'use_xxxloadpath'   : 'ulp',
            'haveinifini'       : 'hif',
            'symboldimensions'  : 'callSymbolDim',
            'nofortrancb'       : 'NOFORTRANCB',
            'internalcs'        : 'internalCS',
            'skippy'            : 'skipPy',
            'useadim'           : 'useADim',
            'usecurrentdim'     : 'useCurrentDim',
            'usesymboldim'      : 'useSymbolDim'
        }

        datadef['MultipleConfigurationKeys'] = ['clibuse', 'apiversion','compatibleversion', 'prefix', 'preprefix', 'output','testmode']

        return datadef

    @staticmethod
    def addSpecialTypeMap(datadef, data, df, key, value):
        if key.lower() in datadef[data]['elements']['ta'].tolist():
            df = df.set_index(df['ta'])
            df.loc[df['ta'] == key.lower(), 'ta'] = value
        else:
            newvalue = df[df['ta']==value.lower()]['text'].iloc[0]
            df.loc[df.index.max()+1] = [ key.lower(), newvalue ]

    @staticmethod
    def initCSTypemapData(datadef):
        CSkeys = ['csType', 'csCall', 'csDefVal']
        datadef['csType'] = {
            'columns'  : ['ta', 'text'],
            'elements' : [ ['ptr', 'IntPtr'],      ['vptr', 'IntPtr'],
                           ['int', 'int'],         ['oint', 'int'],       ['vint', 'int'],
                           ['int64', 'Int64'],     ['Oint64', 'Int64'],   ['Vint64', 'Int64'],
                           ['bool', 'bool'],       ['Vbool', 'bool'],
                           ['CPDA', 'double[]'],   ['PDA', 'double[]'],
                           ['CPLIA', 'int[]'],     ['PLIA', 'int[]'],
                           ['CPC', 'byte[]'],      ['PC', 'byte[]'],
                           ['cSS', 'string'],      ['oSS', 'string'],     ['xSS', 'string'],
                           ['vII', 'int[]'],       ['cII', 'int[]'],
                           ['vRV', 'double[]'],    ['cRV', 'double[]'],
                           ['cSI', 'string[]'],    ['oSI', 'string[]'],
                           ['vsVA', 'double[]'],   ['csVA', 'double[]'],
                           ['D', 'double'],        ['OD', 'double'],      ['VD', 'double'],
                           ['void', 'void'], 
                           ['C', 'char'],          ['vC', 'char']  ]
        }

        datadef['csCall'] = { 'columns'  : ['ta', 'text'], 
                                   'elements' : [ ]                }
        for ta in ['ptr','int','int64','D','FuncPtr','bool','cSS','C'] :
            datadef['csCall']['elements'].append( [ ta, ''] )
        for ta in ['PC','CPC','PDA','PLIA','CPDA','CPLIA','cII','vII','cRV','vRV','cSVA','vSVA','oSI'] :
            datadef['csCall']['elements'].append( [ ta, ''] )
        for ta in ['Vptr','Oint','Oint64','Vint','Vint64','OD','VD','oSS','xSS','vC','Vbool'] :
            datadef['csCall']['elements'].append( [ ta, 'ref '] )

        datadef['csDefVal'] = {  # Default Return Values
            'columns'  : ['ta', 'text'],
            'elements' : [ ['void', ''],
                           ['PDA', 'null'],         ['PLIA', 'null'],        ['PC', 'null'], 
                           ['oSS', 'null'],         ['FuncPtr', 'null'],
                           ['ptr', 'IntPtr.Zero'],
                           ['int', '0'],            ['int64', '0'],          ['bool', '0'],
                           ['D', '0.0'],
                           ['C', "'\\0'"] ]        }

        for key in CSkeys:
            for e in datadef[key]['elements']:
                e[0] = e[0].lower()
            df = pd.DataFrame(datadef[key]['elements'], columns=datadef[key]['columns'])
            datadef[key]['elements'] = df

    @staticmethod
    def initJavaTypemapData(datadef):
        Javakeys = ['JType', 'JCall', 'JTMod', 'jniType', 'jniSig', 'jniCall', 'jniTMod']
        datadef['JType'] = {
            'columns'  : ['ta', 'text'],
            'elements' : [ ['int', 'int'],         ['oint', 'int'],       ['vint', 'int'],
                           ['int64', 'long'],      ['Oint64', 'long'],    ['Vint64', 'long'],
                           ['CPDA', 'double'],     ['PDA', 'double'],
                           ['bool', 'boolean'],    ['Vbool', 'boolean'],
                           ['CPLIA', 'int'],       ['PLIA', 'int'],
                           ['CPC', 'String'],      ['PC', 'String'],      ['cSS', 'String'],      ['oSS', 'String'],
                           ['xSS', 'String'],      ['cSI', 'String'],     ['oSI', 'String'],
                           ['C', 'char'],          ['vC', 'char'],
                           ['D', 'double'],        ['OD', 'double'],       ['VD', 'double'],
                           ['void', 'void'], 
                           ['ptr', 'long'],        ['Vptr', 'long']  ]
        }

        datadef['JCall'] = { 'columns'  : ['ta', 'text'], 
                                  'elements' : [ ]                }
        for ta in ['int','int64','bool','ptr','D','void','FuncPtr','C','CPC','cSS'] :
            datadef['JCall']['elements'].append( [ ta, ''] )
        for ta in ['VBool','Vptr','cSI','oSI'] :
            datadef['JCall']['elements'].append( [ ta, '[]'] )
        for ta in ['Oint','Oint64','Vint','Vint64','CPDA','PDA','CPLIA','PLIA','PC','OD','VD','vC','oSS','xSS'] :
            datadef['JCall']['elements'].append( [ ta, '[]'] )

        datadef['JTMod'] = { 'columns'  : ['ta', 'text'], 
                                  'elements' : [ ]                }
        for ta in ['Vptr','ptr','int','int64','Oint','Oint64','Vint','Vint64','D','PDA','PLIA','PC','oSI','oSS','xSS','OD','VD','FuncPtr','void','c','vC'] :
            datadef['JTMod']['elements'].append( [ ta, ''] )
        for ta in ['CPLIA','CPDA','CPC','cSI','cSS'] :
            datadef['JTMod']['elements'].append( [ ta, 'const'] )

        datadef['jniType'] = {
            'columns'  : ['ta', 'text'],
            'elements' : [ ['int', 'jint'],            ['oint', 'jintArray'],      ['vint', 'jintArray'],
                           ['int64', 'jlong'],         ['Oint64', 'jlongArray'],   ['Vint64', 'jlongArray'],
                           ['CPDA', 'jdoubleArray'],   ['PDA', 'jdoubleArray'],   ['OD', 'jdoubleArray'],  ['VD', 'jdoubleArray'],
                           ['CPLIA', 'jintArray'],     ['PLIA', 'jintArray'],
                           ['bool', 'jboolean'],
                           ['Vbool', 'jbooleanArray'],
                           ['CPC', 'jstring'],         ['cSS', 'jstring'],
                           ['PC', 'jobjectArray'],     ['oSS', 'jobjectArray'],   ['xSS', 'jobjectArray'], ['cSI', 'jobjectArray'], ['oSI', 'jobjectArray'],
                           ['C', 'jbyte'],
                           ['vC', 'jbyteArray'],
                           ['D', 'jdouble'],
                           ['void', 'void'],
                           ['ptr', 'jlong'],
                           ['Vptr', 'jlongArray']  ]
        }

        datadef['jniSig'] = {
            'columns'  : ['ta', 'text'],
            'elements' : [ ['int', 'I'],      ['oint', '[I'],    ['Vint', '[I'],
                           ['int64', 'J'],    ['oint64', '[J'],  ['vint64', '[J'],
                           ['cpda', '[D'],    ['pda', '[D'],  ['od', '[D'],  ['vd', '[D'], 
                           ['cplia', '[I'],   ['plia', '[I'], 
                           ['bool', 'I'],
                           ['vbool', '[I'],
                           ['cpc', 'Ljava/lang/String;'],     ['css', 'Ljava/lang/String;'], 
                           ['pc', '[Ljava/lang/String;'],      ['oss', '[Ljava/lang/String;'],
                           ['xss', '[Ljava/lang/String;'],     ['csi', '[Ljava/lang/String;'],   ['osi', '[Ljava/lang/String;'],
                           ['c', 'C'],
                           ['vc', '[C'],
                           ['d', 'D'],
                           ['void', 'V'],
                           ['ptr', 'J'],
                           ['vptr', '[J']   ]
        }

        datadef['jniCall'] = { 'columns'  : ['ta', 'text'], 
                                    'elements' : [ ]                }
        for ta in ['ptr','int','int64','bool','D','void','FuncPtr','C','cSS'] :
            datadef['jniCall']['elements'].append( [ ta, ''] )
        for ta in ['VBool','Vptr','cSI','oSI'] :
            datadef['jniCall']['elements'].append( [ ta, '*'] )
        for ta in ['Oint','Oint64','Vint','Vint64','CPDA','PDA','CPLIA','PLIA','CPC','PC','OD','VD','vC','oSS','xSS'] :
            datadef['jniCall']['elements'].append( [ ta, '*'] )

        datadef['jniTMod'] = { 'columns'  : ['ta', 'text'], 
                                    'elements' : [ ]                }
        for ta in ['Vptr','ptr','int','int64','Oint','Oint64','Vint','Vint64','Vbool','D','PDA','PLIA','PC','oSI','oSS','xSS','OD','VD','FuncPtr','void','c','vC'] :
            datadef['jniTMod']['elements'].append( [ ta, ''] )
        for ta in ['bool','CPLIA','CPDA','CPC','cSI','cSS'] :
            datadef['jniTMod']['elements'].append( [ ta, 'const'] )

        for key in Javakeys:
            for e in datadef[key]['elements']:
                e[0] = e[0].lower()
            df = pd.DataFrame(datadef[key]['elements'], columns=datadef[key]['columns'])
            datadef[key]['elements'] = df

        for key,value in datadef['Spectamap'].items():
            if key.lower() not in ['bool','vbool']:
                Definition.addSpecialTypeMap(datadef, 'JType',   datadef['JType']['elements'],   key, value)
                Definition.addSpecialTypeMap(datadef, 'JCall',   datadef['JCall']['elements'],   key, value)
                Definition.addSpecialTypeMap(datadef, 'JTMod',   datadef['JTMod']['elements'],   key, value)
                Definition.addSpecialTypeMap(datadef, 'jniType', datadef['jniType']['elements'], key, value)
                Definition.addSpecialTypeMap(datadef, 'jniSig',  datadef['jniSig']['elements'],  key, value)
                Definition.addSpecialTypeMap(datadef, 'jniTMod', datadef['jniTMod']['elements'], key, value)

    @staticmethod
    def initVBTypemapData(datadef):
        VBkeys = ['VBAType', 'VBACall', 'VBNetType', 'VBNetCall', 'VBNetDefVal']
        datadef['VBAType'] = {
            'columns'  : ['ta', 'text'],
            'elements' : [ ['ptr', 'vbaptr'],   ['Vptr', 'vbaptr'],
                           ['int', 'Long'],     ['Oint', 'Long'],     ['Vint', 'Long'],
                           ['int64', 'Int64'],  ['Oint64', 'Int64'],  ['Vint64', 'Int64'],
                           ['bool', 'Boolean'], ['Vbool', 'Boolean'],
                           ['CPDA', 'Double'],  ['PDA', 'Double'],
                           ['CPLIA', 'Long'],   ['PLIA', 'Long'],
                           ['CPC', 'Byte'],     ['PC', 'Byte'],
                           ['cSS', 'String'],   ['oSS', 'String'],    ['xSS', 'String'],
                           ['cII', 'Long'],     ['vII', 'Long'],
                           ['cRV', 'Double'],   ['vRV', 'Double'],
                           ['cSI', 'String'],   ['oSI', 'String'],
                           ['cSVA', 'Double'],  ['vSVA', 'Double'],
                           ['D', 'Double'],     ['OD', 'Double'],     ['VD', 'Double'],
                           ['C', 'Char'],       ['vC', 'Char']  ]
        }

        datadef['VBACall'] = { 'columns'  : ['ta', 'text'], 
                                    'elements' : [ ]                }
        for ta in ['ptr','int','int64','D','FuncPtr','bool','cSS','cSI','C'] :
            datadef['VBACall']['elements'].append( [ ta, 'ByVal'] )
        for ta in ['PDA','PLIA','PC','CPDA','CPLIA','CPC','Vptr','Oint','Oint64','Vint','Vint64','OD','VD',
                   'vII','vRV','oSS','xSS','oSI','vSVA','cII','cRV','cSVA','vC','Vbool'] :
            datadef['VBACall']['elements'].append( [ ta, 'ByRef'] )

        datadef['VBNetType'] = {
            'columns'  : ['ta', 'text'],
            'elements' : [ ['ptr', 'IntPtr'],      ['Vptr', 'IntPtr'],
                           ['int', 'Integer'],     ['Oint', 'Integer'],    ['Vint', 'Integer'],
                           ['int64', 'Int64'],     ['Oint64', 'Int64'],    ['Vint64', 'Int64'],
                           ['bool', 'Boolean'],    ['Vbool', 'Boolean'],
                           ['CPDA', 'Double()'],   ['PDA', 'Double()'],
                           ['CPLIA', 'Integer()'], ['PLIA', 'Integer()'],
                           ['CPC', 'Byte'],        ['PC', 'Byte'],
                           ['cSS', 'String'],      ['oSS', 'String'],      ['xSS', 'String'],
                           ['cII', 'Integer()'],   ['vII', 'Integer()'],
                           ['cRV', 'Double()'],    ['vRV', 'Double()'],
                           ['cSI', 'String()'],    ['oSI', 'String()'],
                           ['cSVA', 'Double()'],   ['vSVA', 'Double()'],
                           ['D', 'Double'],        ['OD', 'Double'],       ['VD', 'Double'],
                           ['C', 'Char'],          ['vC', 'Char']  ]
        }

        datadef['VBNetCall'] = { 'columns'  : ['ta', 'text'], 
                                      'elements' : [ ]                }
        for ta in ['ptr','int','int64','D','FuncPtr','bool','cSS','C'] :
            datadef['VBNetCall']['elements'].append( [ ta, 'ByVal'] )
        for ta in ['PC','CPC','Vptr','Oint','Oint64','Vint','Vint64','OD','VD','oSS','xSS','vC','Vbool'] :
            datadef['VBNetCall']['elements'].append( [ ta, 'ByRef'] )
        for ta in ['CPDA','PDA','CPLIA','PLIA','vII','cII','vRV','cRV','cSI','oSI','vSVA','cSVA'] :
            datadef['VBNetCall']['elements'].append( [ ta, ''] )

        datadef['VBNetDefVal'] = {  # Default Return Values
            'columns'  : ['ta', 'text'],
            'elements' : [ ['void', ''],
                           ['oSS', 'String.Empty'],
                           ['FuncPtr', 'Nothing'],
                           ['PDA', 'IntPtr.Zero'],  ['PLIA', 'IntPtr.Zero'], ['PC', 'IntPtr.Zero'], ['ptr', 'IntPtr.Zero'],
                           ['int', '0'],            ['int64', '0'],          ['bool', '0'],
                           ['D', '0.0'],
                           ['C', '"\\0"'] ]        }

        for key in VBkeys:
            for e in datadef[key]['elements']:
                e[0] = e[0].lower()
            df = pd.DataFrame(datadef[key]['elements'], columns=datadef[key]['columns'])
            datadef[key]['elements'] = df

    @staticmethod
    def api_definition():
        apidef = dict()
        apidef['output'] = []
        apidef['Prefix'],    apidef['multiprefix'], apidef['APIVersion'] = '', '', ''
        apidef['prexfix'],   apidef['premulti'],    apidef['preprefix'], apidef['prexfixl']  = '', '', '', ''
        apidef['DelphiLib'], apidef['CLib'],        apidef['CCall'],     apidef['CCB']       = '', '', '', ''
        apidef['FCall'],     apidef['F9Call'],      apidef['F9glu']      = '', '', ''
        apidef['PySetup'],   apidef['CDLink'],      apidef['CPPCall']    = '', '', ''
        apidef['flx'],       apidef['fmodule'],     apidef['fptr']       = '', '', ''
        apidef['dcx'], apidef['dox'], apidef['DelphiCall'] , apidef['DelphiObj'] = '', '', '', ''
        apidef['DelphiCon'], apidef['DelphiDec'], apidef['CCon'] = '', '', ''
        apidef['multi'], apidef['doc'], apidef['trace']                                   = False, False, False
        apidef['FCLIB'], apidef['NOFORTRANCB'], apidef['availifdefs'], apidef['testmode'] = False, False, False, False  # ToDo

        apidef['Title']         = { # API Title
                                         'columns' : ['prefix', 'text'], 'elements': pd.DataFrame() }
        apidef['Description']   = { # API Description
                                         'columns' : ['prefix', 'text'], 'elements': pd.DataFrame() }
        apidef['Version']       = { # Recent Version and compatible version',
                                       'columns' : ['prefix', 'rv', 'cv'], 'elements': pd.DataFrame() }
        apidef['RecentVersion'] = { # Recent Version'                                         
                                        'columns' : ['prefix', 'rv'], 'elements': pd.DataFrame() }
        apidef['DUnit']         = { # Delphi Unit
                                         'columns' : ['prefix', 'text'], 'elements': pd.DataFrame() }
        apidef['DObject']       = { # Delphi Object
                                         'columns' : ['prefix', 'text'], 'elements': pd.DataFrame() }
        apidef['DObjectInt']    = { # Delphi Object Int
                                         'columns' : ['prefix', 'text'], 'elements': pd.DataFrame() }
        apidef['ExtraCUse']     = { # Extra C Usage
                                         'columns' : ['prefix', 'text'], 'elements': pd.DataFrame() }
        apidef['ExtraUse']      = { # Extra  Usage
                                         'columns' : ['prefix', 'text'], 'elements': pd.DataFrame() }
        apidef['pre']           = { # prefix
                                         'columns' : ['prefix', 'text'], 'elements': pd.DataFrame() }
        apidef['prex']          = { # prefix
                                         'columns' : ['prefix', 'text'], 'elements': pd.DataFrame() }
        apidef['ulp']           = { # use_xxxloadpath
                                         'columns' : ['prefix'], 'elements': pd.DataFrame() }
        apidef['CLibUse']       = { # C Library Usage
                                         'columns' : ['prefix'], 'elements': pd.DataFrame() }
        apidef['hif']           = { # Initialization and Finalization flag
                                         'columns' : ['prefix'], 'elements': pd.DataFrame() }
        apidef['UseCD']         = { # if library as addional constructor accepting system directory',
                                         'columns' : ['prefix'], 'elements': pd.DataFrame() }
        apidef['generic']       = { # generic
                                         'columns' : ['prefix'], 'elements': pd.DataFrame() }
        apidef['haveTypedefs']  = { # if FuncMap
                                         'columns' : ['prefix'], 'elements': pd.DataFrame() }
        apidef['haveInt64']     = { # if int64
                                         'columns' : ['prefix'], 'elements': pd.DataFrame() }
        apidef['needF2Pas']     = { # if [oss,csi] function
                                         'columns' : ['prefix'], 'elements': pd.DataFrame() }
        apidef['needPas2F']     = { # if [oss,xss,osi] function
                                         'columns' : ['prefix'], 'elements': pd.DataFrame() }
        apidef['needC2F']       = { # if [pc] function
                                         'columns' : ['prefix'], 'elements': pd.DataFrame() }
        apidef['MaxDimStyle']   = { 'columns' : ['prefix'], 'elements': pd.DataFrame() }
        apidef['callSymbolDim'] = { 'columns' : ['name', 'dimension'], 'elements': pd.DataFrame() }
        apidef['pySpecVii']     = { # DomainIDS
                                         'columns' : ['name'], 'elements': pd.DataFrame() }
        apidef['skipPy']        = { # Functions which will be skipped in Python since they cannot be used there and have special Python versions instead',
                                         'columns' : ['name'], 'elements': pd.DataFrame() }
        apidef['useADim']       = { 'columns' : ['name'], 'elements': pd.DataFrame() }
        apidef['useCurrentDim'] = { 'columns' : ['name'], 'elements': pd.DataFrame() }
        apidef['useSymbolDim']  = { 'columns' : ['name'], 'elements': pd.DataFrame() }
        apidef['internalCS']    = { # Functions in C# which are internal instead of private so that they can be called from outside of the class directy (they are static in Java)'
                                         'columns' : ['name'], 'elements': pd.DataFrame() }
        apidef['f90Skip']       = { 'columns' : ['name'], 'elements': pd.DataFrame() }
        apidef['lfSkip']        = { 'columns' : ['name'], 'elements': pd.DataFrame() }
        apidef['f']             = { # function and procedures
                                         'columns' : ['name', 'len', 'pos', 'arg', 'type', 'text', 'details'],
                                         'elements': pd.DataFrame() }
        apidef['tfunc']         = { # function  and procedure types
                                         'columns' : ['name', 'len', 'type', 'text'],
                                         'elements': pd.DataFrame() }
        apidef['tfuncG']        = { 'columns' : ['group', 'name'],'elements': pd.DataFrame() }
        apidef['FuncNames']     = { # function and property names with r actions
                                         'columns' : ['name','len'],
                                        'elements': pd.DataFrame() }
        apidef['FuncNamesSet']  = { # function and property names with r actions
                                         'columns' : ['name','len'],
                                         'elements': pd.DataFrame() }
        apidef['pn']            = { # Property names and actions
                                         'columns' : ['group', 'name', 'len', 'type', 'pactions', 'ea', 'text', 'return'],
                                         'elements': pd.DataFrame() }
        apidef['gcon']          = { # group constants
                                         'columns' : ['group', 'constant', 'len', 'value'],
                                         'elements': pd.DataFrame() }
        apidef['gconarray']     = { # group constants
                                         'columns' : ['name'],
                                         'elements': pd.DataFrame() }
        apidef['cname']        = { # name of constant groups
                                        'columns' : ['group', 'maxlen'],
                                        'elements': pd.DataFrame() }
        apidef['gstrcon']      = { # group string constants
                                        'columns' : ['group', 'constant', 'len', 'value'],
                                        'elements': pd.DataFrame() }
        apidef['pArrLen']      = { # LW Error04(en,ea)$(not pArrLen(en,ea)) = sum(PtrF(en,tp,ea,ta)$(sameas(ta,'CPDA') or sameas(ta,'PDA') or sameas(ta,'CPLIA') or sameas(ta,'PLIA')),1);
                                        'columns' : ['name', 'arg', 'value'],
                                        'elements': pd.DataFrame() }
        apidef['csname']       = { # 'name of string constant groups',
                                        'columns' : ['group', 'maxlen'], 'elements': pd.DataFrame() }
        apidef['argtext']      = { # argument text
                                        'columns' : ['name', 'text'],    'elements': pd.DataFrame() }
        apidef['FuncPtrDef']   = { 'columns' : ['def', 'fpos', 'name', 'apos', 'arg', 'type', 'text'],
                                        'elements': pd.DataFrame() }
        apidef['FuncMap']      = { # Mapping between function or property and pointer to a function which is defined as type
                                        'columns' :  ['def', 'fpos', 'name'],
                                        'elements': pd.DataFrame() }
        apidef['PtrF']         = { # Functions which are addressed by a pointer and which are only defined as type
                                        'columns' : ['name', 'apos', 'arg', 'type'],
                                        'elements': pd.DataFrame() }
        apidef['PFtrF']        = { # Functions which are addressed by a pointer and have arguments which require translation for a Fortran client
                                        'columns' : ['name'], 'elements': pd.DataFrame() }
        apidef['tPtrFunc']     = { # Function and procedure types
                                        'columns' : ['name', 'type'],
                                        'elements': pd.DataFrame() }
        apidef['fpf']          = { # Functions containing a pointer to a function as parameter
                                        'columns' : ['def'], 'elements': pd.DataFrame() }
        apidef['fbool']        = { # Functions containing a bool parameter (var or const)
                                        'columns' : ['name'], 'elements': pd.DataFrame() }
        apidef['fvbool']       = { # Functions containing a var bool parameter
                                        'columns' : ['name'], 'elements': pd.DataFrame() }
        apidef['enInt64']      = { # funcs and procs with int64 arguments
                                        'columns' : ['name'], 'elements': pd.DataFrame() }
        apidef['farg']         = { # Number of arguments for each function
                                        'columns' : ['name', 'value'], 'elements': pd.DataFrame() }
        apidef['enstring']     = { # funcs and procs with string arguments
                                        'columns' : ['name'], 'elements': pd.DataFrame() }
        apidef['enostringa']   = { # funcs and procs with out string array arguments
                                        'columns' : ['name'],'elements': pd.DataFrame() }
        apidef['fs']           = { # functions with strings
                                        'columns' : ['name', 'pos', 'arg', 'type', 'text'],
                                        'elements': pd.DataFrame() }
        apidef['fstr']         = { # Functions dependend on string parameters
                                        'columns' : ['name'], 'elements': pd.DataFrame() }
        apidef['fost']         = { # Functions dependend on var string parameters
                                        'columns' : ['name'], 'elements': pd.DataFrame() }
        apidef['farr']         = { # Functions dependend on array parameters
                                        'columns' : ['name'], 'elements': pd.DataFrame() }
        apidef['fsti']         = { # Functions dependend on string array parameters
                                        'columns' : ['name'], 'elements': pd.DataFrame() }
        apidef['fstiV']        = { # Functions dependend on string array parameters with a vInt aDim (instead of the regular int aDim)',
                                        'columns' : ['name'], 'elements': pd.DataFrame() }
        apidef['enp']          = { 'columns' : ['prefix', 'element'], 'elements': pd.DataFrame() }
        apidef['tprop']        = { # property type
                                        'columns' : ['name', 'type'], 'elements': pd.DataFrame() }
        apidef['fargmax']         = { 'value': -1 } # Maximum number of function arguments
        apidef['gamsta' ]         = { 'value': -1 } # Indicator for special GAMS types used in API
        apidef['maxLenFuncNames'] = { 'value': -1 } # max length of functions names
        apidef['idlenF']          = { 'value': -1 } # max ident length of functions and procedures
        apidef['idlenP']          = { 'value': -1 } # max ident length of properties
        apidef['arglen']          = { 'value': -1 } # max ident length of arguments
        apidef['idlenWset']       = { 'value': -1 } # max ident length of properties with write action

        return apidef

    @staticmethod 
    def readAPIDefinitionFile(yamlfilename):
        ydata = dict()
        try:
            base_path = pathlib.Path(__file__).parent
            file_path = (base_path / yamlfilename).resolve()
            with open(file_path, 'r') as f:
               ydata = yaml.load(f, Loader) #Loader=yaml.FullLoader )
               f.close()
        except IOError:
            print(yamlfilename+' does not  exists')
        ydata = { key.lower(): value for key, value in ydata.items() }
        return ydata


class APIGenerator:
    def __init__(self):
        self.api = {
            'generator'     : 'API Generator',
            'fileVersion'   : subprocess.check_output(["git", "describe", "--always"], cwd=os.path.dirname(os.path.abspath(__file__))).strip().decode(),
            'SysYear'       : datetime.date.today().year
        }
        # control which files will be created by means of flags.
        self.api['flags'] = DataValidator.output_flags()

        ''' Initialize data definition '''
        self.datadef = Definition.data_definition()

        ''' Initialize API definition data structure '''
        self.apidef = Definition.api_definition()
        for flags in self.api['flags']:
            self.apidef[flags] = False

        self.apidefKeysBoolean = ['multi', 'doc', 'trace','FCLIB','NOFORTRANCB', 'availifdefs', 'testmode']
        self.apidefKeysString  = ['Prefix','APIVersion','prexfix','multiprefix','premulti','prexfix','prexfixl','preprefix',
                                  'OutputPath',
                                  'DelphiLib',
                                  'CLib','CCall','CDLink','CPPCall','CCB',
                                  'PySetup', 'vbaCall', 'vbnetCall', 'CSCall', 'JavaCall', 'JavaNI', 'CSCall',
                                  'F9glu','FCall','F9Call','flx','fmodule','fptr',
                                  'dcx','dox','DelphiCall','DelphiObj', 'DelphiCon', 'DelphiDec', 'CCon' ]
        self.apidefKeysList       = ['output']
        self.apidefKeysWithValue  = ['fargmax','gamsta','maxLenFuncNames', 'idlenF', 'idlenP','idlenWset']

    ''' Clear API Definition '''
    def clearAPIDefinition(self):
        for key,value in self.apidef.items():
            if key in self.api['flags']:
                value = False
            elif key in self.apidefKeysString:
                value = ''
            elif key in self.apidefKeysBoolean:
                value = False
            elif key in self.apidefKeysWithValue:
                value['value'] = -1
            elif key in self.apidefKeysList:
                value.clear()
            else:
                value['elements'] = pd.DataFrame()

    ''' Generate output file from template '''
    def generateFileFromTemplate(self, outputfilename, templatename, subdirectory='', templatepath=None):
        templatefilename = templatename+'.template.j2'
        templates_dir = os.path.join(os.path.dirname(pathlib.Path(__file__).parent), 'templates')
        include_dir   = os.path.join(os.path.dirname(pathlib.Path(__file__).parent), 'include')
        if not (templatepath is None):
            env = Environment(loader=FileSystemLoader([templates_dir, include_dir, templatepath]))
        else:
            env = Environment(loader=FileSystemLoader([templates_dir, include_dir]))
        template = env.get_template(templatefilename)

        output = template.render(api=self.api, apidef=self.apidef, datadef=self.datadef,templatename=templatename)
        if len(subdirectory)>0:
            if not os.path.exists(subdirectory):
               os.makedirs(subdirectory)
            filename = os.path.join(subdirectory, outputfilename)
        else:
            filename = outputfilename
        print('generate...', os.path.abspath(filename))
        with open(os.path.abspath(filename), 'w') as f:
           f.write(output)
        f.close()

    ''' Generate Python Wrapper '''
    def generatePythonWrapper(self, suffix, template):
        self.apidef['CCall'] = self.apidef['preprefix'] + self.apidef['Prefix'] + self.apidef['premulti'] + 'cc'
        outputfilename = self.apidef['preprefix'] + self.apidef['Prefix'] + self.apidef['premulti'] + suffix
        self.generateFileFromTemplate(outputfilename, template, self.apidef['OutputPath'])

    ''' Generate C# Wrapper '''
    def generateCSWrapper(self):
        Definition.initCSTypemapData(self.datadef)
        self.apidef['CSCall'] = self.apidef['preprefix'] + self.apidef['Prefix'] + self.apidef['premulti'] + 'cs'
        self.generateFileFromTemplate(self.apidef['CSCall']+'.cs', 'cs', self.apidef['OutputPath'])

    ''' Generate Java Wrapper '''
    def generateJavaWrapper(self):
        Definition.initJavaTypemapData(self.datadef)
        self.apidef['JavaCall'] = self.apidef['preprefix'] + self.apidef['Prefix'] + self.apidef['premulti']
        self.apidef['JavaNI']   = self.apidef['preprefix'] + self.apidef['Prefix'] + self.apidef['premulti'] + 'jni'
        self.generateFileFromTemplate(self.apidef['JavaCall']+'.java', 'java', self.apidef['OutputPath'])
        self.apidef['CCall']      = self.apidef['preprefix'] + self.apidef['Prefix'] + self.apidef['premulti'] + 'cc'
        if len(self.apidef['preprefix']) > 0:
            self.apidef['JavaCall'] = self.apidef['preprefix'] + '1' + self.apidef['Prefix'] + self.apidef['premulti']
        else:
            self.apidef['JavaCall'] = self.apidef['preprefix'] + self.apidef['Prefix'] + self.apidef['premulti']
        self.generateFileFromTemplate(self.apidef['JavaNI']+'.c', 'jni', self.apidef['OutputPath'])

    ''' Generate Visual Basic Wrapper '''
    def generateVisualBasicWrapper(self):
        Definition.initVBTypemapData(self.datadef)
        self.apidef['vbaCall']    = self.apidef['preprefix'] + self.apidef['Prefix'] + self.apidef['premulti'] + 'vba'
        self.generateFileFromTemplate(self.apidef['vbaCall']+'.bas', 'vba', self.apidef['OutputPath'])
        self.apidef['vbnetCall']  = self.apidef['preprefix'] + self.apidef['Prefix'] + self.apidef['premulti'] + 'vbnet'
        self.generateFileFromTemplate(self.apidef['vbnetCall']+'.vb', 'vbnet', self.apidef['OutputPath'])

    ''' Generate C Library '''
    def generateCLibrary(self, templatename):
        if templatename == 'cclib':
            outputfilename = self.apidef['CLib'] + '.c'
        elif templatename == 'cpplib':
            outputfilename = self.apidef['CLib'] + '.cpp'
            templatename = 'cclib'
        elif templatename == 'cclibdef':
             outputfilename = self.apidef['CLib'] + '.def'
        else:
            return
        self.generateFileFromTemplate(outputfilename,templatename,self.apidef['OutputPath'])

    ''' Generate C Interface '''
    def generateCInterface(self, templatename ):
        if templatename == 'ccc':
            self.apidef['CCall']      = self.apidef['preprefix'] + self.apidef['Prefix'] + self.apidef['premulti'] + 'cc'
            outputfilename = self.apidef['CCall'] + '.c'
        elif templatename == 'cch':
            self.apidef['CCall']      = self.apidef['preprefix'] + self.apidef['Prefix'] + self.apidef['premulti'] + 'cc'
            outputfilename = self.apidef['CCall'] + '.h'
        elif templatename == 'ccb1':
            outputfilename = self.apidef['preprefix'] + self.apidef['Prefix'] + self.apidef['premulti'] + 'cb1.h'
        elif templatename == 'ccb2':
            outputfilename = self.apidef['preprefix'] + self.apidef['Prefix'] + self.apidef['premulti'] + 'cb2.h'
        elif templatename == 'ccon':
            outputfilename = self.apidef['preprefix'] + self.apidef['Prefix'] + self.apidef['premulti'] + 'ccon.h'
        else:
            return
        self.generateFileFromTemplate(outputfilename, templatename,self.apidef['OutputPath'])

    ''' Generate output file from template '''
    def generateOutput(self, outputList):
        self.api['generatedstr'] = 'generated by {} {} for {}'.format(self.api['generator'], self.api['fileVersion'], self.apidef['Prefix'])
        if (self.apidef['APIVersion'] > 0):
            self.api['generatedstr'] += ' version {}'.format(self.apidef['APIVersion'])

        for key in outputList:
            if key in ['cclib', 'cclibdef', 'cpplib']:
                self.generateCLibrary(key)
            elif key=='cc': 
                self.generateCInterface('cch')
                self.generateCInterface('ccc')
            elif key=='cb': 
                self.generateCInterface('ccb1')
                self.generateCInterface('ccb2')
            elif key=='ccon':
                self.generateCInterface('ccon')
            elif key=='py':
                self.generatePythonWrapper('cc.i', key)
                self.generatePythonWrapper('setup.py', key+'setup')
            elif key=='vb':
                self.generateVisualBasicWrapper()
            elif key=='cs':
                self.generateCSWrapper()
            elif key=='java':
                self.generateJavaWrapper()
            elif key in self.api['flags']:
                print('Warning: output template for "{}" is not yet implemented.'.format(key))
            else:
                print('Error: unknown output flag "{}".'.format(key))

    ''' update API definition file '''
    def updateAPIDefinition(self, ydata, configuration, args, multiAPI=False, combinedAPI=False):

        def appendToDefinition(key, appendlist):
            edict = dict()
            for idx,val in enumerate(self.apidef[key]['columns']):
                edict[val] = appendlist[idx]
            df = pd.DataFrame(edict)
            self.apidef[key]['elements'] = pd.concat([self.apidef[key]['elements'], df], ignore_index=True)

        def getNameByType(name, typelist):
            namelist = []
            if name=='tfunc':
                tfunc = self.apidef['tfunc']['elements']
                if tfunc.shape[0] > 0:
                    tfnames = tfunc[tfunc['type'].isin(typelist)]
                    namelist = tfnames['name'].tolist() if tfnames.shape[0] > 0 else []
            elif name=='f':
                f = self.apidef['f']['elements']
                if f.shape[0] > 0:
                    fnames = f[f['type'].isin(typelist)]
                    namelist = fnames['name'].tolist() if fnames.shape[0] > 0 else []
            elif name=='pn':
                pn = self.apidef['pn']['elements']
                if pn.shape[0] > 0:
                    pnnames = pn[pn['type'].isin(typelist)]
                    namelist = pnnames['name'].tolist() if pnnames.shape[0] > 0 else []
            return namelist

        def updateDataDefinition(defdata, prefix) :
            for k,v in defdata.items():
                if k in ['apiversion']:
                    self.apidef[self.datadef['definition'][k]] =  v
                elif k == 'compatibleversion':
                    prefixes, rv = list(), list()
                    for i in range(len(v)):
                        prefixes.append(prefix)
                        rv.append(self.apidef['APIVersion'])
                    appendToDefinition('Version', [prefixes, rv, v] )
                elif k in ['clibuse'] and v:
                    appendToDefinition( self.datadef['definition'][k], [ [self.apidef['Prefix']] ])

        try:
            self.apidef['multi']        = multiAPI
            if multiAPI:
                self.apidef['APIVersion']   = ydata['apiversion']   if 'apiversion'  in ydata.keys() else 0
                self.apidef['output']       = ydata['output']       if 'output'      in ydata.keys() else []
                self.apidef['Prefix']       = ydata['prefix']
                self.apidef['multiprefix']  = configuration['multiprefix'] if 'multiprefix' in configuration.keys() else ''
                updateDataDefinition(ydata, ydata['prefix'])
            else:
                self.apidef['Prefix'] = configuration['prefix']
                self.apidef['multiprefix']  = ''
                self.apidef['APIVersion']   = configuration['apiversion']
                self.apidef['output']       = configuration['output']
                updateDataDefinition(configuration, self.apidef['Prefix'])

            self.apidef['preprefix']    = configuration['preprefix'] if 'preprefix' in configuration.keys() else ''
            self.apidef['testmode']     = configuration['testmode']  if 'testmode'  in configuration.keys() else False
            self.apidef['doc']          = ydata['doc']         if 'doc' in ydata.keys()         else False
            self.apidef['trace']        = ydata['trace']       if 'trace' in ydata.keys()       else False
            self.apidef['OutputPath']   = args.outputpath

        except (KeyError) as e:
            raise AssertionError('missing definition of \"'+e.args[0]+'\" in API definition file')

        for k,v in ydata.items():
            if k not in self.datadef['definition'].keys():
                continue
            if k == 'extrause':
                if not combinedAPI:
                   appendToDefinition( self.datadef['definition'][k], [[self.apidef['Prefix']], [v]])
            elif k == 'extrausem':
                if combinedAPI:
                   appendToDefinition( self.datadef['definition'][k], [[self.apidef['Prefix']], [v]])
            elif k in ['extracuse','title', 'dunit', 'dobject', 'dobjectint']:
                appendToDefinition( self.datadef['definition'][k], [[self.apidef['Prefix']], [v]])
            elif k in ['usecd', 'generic', 'maxdimstyle', 'use_xxxloadpath', 'haveinifini']:
                appendToDefinition( self.datadef['definition'][k], [ [self.apidef['Prefix']] ])
            elif k == 'symboldimensions':   # Todo e.g. gdxapi
                csdname, csddim = list(), list()
                for vitem in v:
                    for fk,fv in vitem.items():
                       csdname.append(fk)
                       csddim.append(fv)
                self.apidef[self.datadef['definition'][k]]['elements'] = pd.DataFrame(list(zip(csdname, csddim)), columns=self.apidef[self.datadef['definition'][k]]['columns'])
            elif k == 'nofortrancb':
                self.apidef[self.datadef['definition'][k]] = v
            elif k in ['useadim', 'usecurrentdim', 'usesymboldim', 'skippy','internalcs'] :
                    appendToDefinition(self.datadef['definition'][k], [v])

        if multiAPI:
            appendToDefinition( 'prex', [ [ self.apidef['Prefix']], [self.apidef['Prefix']+'X'] ] )
            self.apidef['prexfix']  = self.apidef['Prefix']+'X'
            self.apidef['prexfixl']  = self.apidef['Prefix']+'x'
            if combinedAPI:
                self.apidef['premulti'] = ''
                self.apidef['DelphiLib']  = self.apidef['multiprefix'] + 'dclib'
                self.apidef['CLib']       = self.apidef['multiprefix'] + 'cclib'
            else:
                self.apidef['premulti'] = 'm'
                self.apidef['CLib']   = self.apidef['preprefix'] + self.apidef['Prefix'] + self.apidef['premulti'] + 'cclib'
                if len(self.apidef['multiprefix'])==0 or args.multi: # forced m in output name:
                    self.apidef['DelphiLib'] = self.apidef['preprefix'] + self.apidef['Prefix'] + self.apidef['premulti'] + 'dclib'
                else:
                    self.apidef['DelphiLib'] = self.apidef['multiprefix'] + 'dclib'
        else:
            appendToDefinition( 'prex', [ [ self.apidef['Prefix']], ['X'] ] )
            self.apidef['prexfix']    = 'X'
            self.apidef['prexfixl']   = 'x'
            self.apidef['premulti']   = ''
            self.apidef['DelphiLib']  = self.apidef['preprefix'] + self.apidef['Prefix'] + self.apidef['premulti'] + 'dclib'
            self.apidef['CLib']       = self.apidef['preprefix'] + self.apidef['Prefix'] + self.apidef['premulti'] + 'cclib'

        appendToDefinition( 'pre', [ [self.apidef['Prefix']], [self.apidef['Prefix']] ] )
        if self.apidef['DObjectInt']['elements'].shape[0] < self.apidef['DObject']['elements'].shape[0] :
            self.apidef['DObjectInt']['elements'] = self.apidef['DObject']['elements'].copy()
        appendToDefinition('RecentVersion', [ [self.apidef['Prefix']], [self.apidef['APIVersion']] ])

        def evaluate(strexp, config) :
            for key in self.datadef['MultipleConfigurationKeys']:
                if strexp.lower().find(key) != -1:
                    if strexp.find(key) == -1:
                        strexp = key + strexp[len(key):]
                    if key == 'clibuse':
                        if key in config.keys():
                            clibuse = config[key]
                        else:
                            clibuse = False
                    else:
                        strexp = strexp.replace(key,'self.apidef[\''+key+'\']')
            return( eval(strexp) )

        datatype = [x.lower() for x in self.datadef['ta']['elements']['name'].tolist()]
        exceptionlist = []
        if 'functions' in ydata.keys():
            fname,fgroup,flen,fpos,ftype,farg,ftext,freturn,fdetails = list(),list(),list(),list(),list(),list(),list(),list(),list()
            for f in ydata['functions']:
                for k, v in f.items():
                    if 'condition' in v.keys():
                        if not evaluate(v['condition'], configuration):
                            continue
                    fparampos = 0
                    fname.append(k)
                    flen.append(len(k))
                    fpos.append(fparampos)
                    farg.append('result')
                    if 'type' in v.keys():
                        if v['type'].lower() in datatype:
                            ftype.append(v['type'].lower())
                        else:
                            ftype.append(v['type'])
                            exceptionlist.append('unknown type "'+v['type']+'" for function definition "'+k+'"')
                    else:
                        ftype.append('')
                        exceptionlist.append('type is missing from function definition "'+k+'"')
                    freturn.append(v['description']) if 'description' in v.keys() else freturn.append('')
                    ftext.append(v['return'])        if 'return'      in v.keys() else ftext.append('')
                    fgroup.append(v['group'])        if 'group'       in v.keys()  else fgroup.append('Not grouped')
                    fdetails.append(v['details'] if 'details' in v.keys() else '')
                    if 'parameters' in v.keys():
                        params = v['parameters']
                        for p in params:
                            for fk, fv in p.items():
                                fparampos += 1
                                fname.append(k)
                                flen.append(len(k))
                                fpos.append(fparampos)
                                farg.append(fk)
                                if 'type' in fv.keys():
                                    if fv['type'].lower() in datatype:
                                        ftype.append(fv['type'].lower())
                                    else:
                                        ftype.append(fv['type'])
                                        exceptionlist.append('unknown type "'+fv['type']+'" for parameter "'+fk+'" of function definition "'+k+'"')
                                else:
                                    ftype.append('')
                                    exceptionlist.append('type is missing from parameter '+fk+' of function definition "'+k+'"')
                                ftext.append(fv['description'])   if 'description' in fv.keys() else ftext.append('')
                                fdetails.append(fv['details'] if 'details' in fv.keys() else '')
                    fmapkeys = [ 'condition','type','parameters','return','description','group','details','static','const','code']
                    warninglist = [ key for key in list(v.keys()) if key not in fmapkeys ]
                    if len(warninglist) > 0:
                        print('Warning: Found unrecognized key(s)',warninglist, 'for',k)
            if fname:
                fposstr = list(map(str, fpos))
                frames = [ self.apidef['f']['elements'], pd.DataFrame(list(zip(fname,flen,fposstr,farg,ftype,ftext,fdetails)), columns=self.apidef['f']['columns']) ]
                self.apidef['f']['elements'] = pd.concat(frames, ignore_index=True)

                tframes = [ self.apidef['tfunc']['elements'], pd.DataFrame(list(zip(fname,flen, ftype,freturn)), columns=self.apidef['tfunc']['columns']) ]
                self.apidef['tfunc']['elements'] = pd.concat(tframes, ignore_index=True)

                df = self.apidef['f']['elements'][self.apidef['f']['elements']['arg']=='result'].copy()
                del df['pos']
                del df['arg']
#                del df['text']
                if self.apidef['tfunc']['elements'].shape[0] > len(freturn):
                   dftext = df['text'].tolist() + freturn
                else:
                   df['text'] = freturn
                self.apidef['tfunc']['elements'] = df #pd.concat(frames, ignore_index=True)

                df = pd.DataFrame(list(zip(fgroup, list(dict.fromkeys(fname)))), columns=self.apidef['tfuncG']['columns'])
                gb = df.groupby('group')
                data = pd.DataFrame()
                for k in gb.groups.keys():
                    row = gb.get_group(k).drop_duplicates()
                    data = pd.concat( [data, row ])
                self.apidef['tfuncG']['elements'] = data

                pref = [ self.apidef['Prefix'] for i in range(len(fname)) ]
                prefenp = [ self.apidef['enp']['elements'], pd.DataFrame({ 'prefix': pref, 'element' : fname }).drop_duplicates() ]
                self.apidef['enp']['elements'] = pd.concat(prefenp, ignore_index=True)

                df = self.apidef['f']['elements']
                if (df[df['type']=='int64'].shape[0] + df[df['type']=='oint64'].shape[0] + df[df['type']=='vint64'].shape[0] > 0):
                    appendToDefinition('haveInt64', [ [self.apidef['Prefix']] ])
                if (df[df['type']=='css'].shape[0]   + df[df['type']=='csi'].shape[0]                                        > 0):
                    appendToDefinition('needF2Pas', [ [self.apidef['Prefix']] ])
                if (df[df['type']=='oss'].shape[0]   + df[df['type']=='xss'].shape[0] + df[df['type']=='osi'].shape[0]       > 0):
                    appendToDefinition('needPas2F', [ [self.apidef['Prefix']] ])
                if (df[df['type']=='pc'].shape[0]                                                                            > 0):
                    appendToDefinition('needC2F', [ [self.apidef['Prefix']] ])

        if 'properties' in ydata.keys():
            pnname,pngroup,pnlen,pntype,pnaction,pnea,pntext,pnreturn = list(),list(),list(),list(),list(),list(),list(),list()
            for pn in ydata['properties']:
                for k,v in pn.items():
                    if 'condition' in v.keys():
                        if not evaluate(v['condition'], configuration):
                            continue
                    pnname.append(k)
                    pnlen.append(len(k))
                    pngroup.append(v['group'])           if 'group' in v.keys()       else pngroup.append('Not grouped')
                    if 'type' in v.keys():
                        if v['type'].lower() in datatype:
                            pntype.append(v['type'].lower())
                        else:
                            pntype.append(v['type'])
                            exceptionlist.append('unknown type "'+v['type']+'" for property "'+k+'"')
                    else:
                        pntype.append('')
                        exceptionlist.append('type is missing from property "'+k+'"')
                    pnreturn.append(v['return'].lower()) if 'return' in v.keys()      else pnreturn.append('')
                    pnea.append(v['function'])           if 'function' in v.keys()    else pnea.append('')
                    pntext.append(v['description'])      if 'description' in v.keys() else pntext.append('')
                    if 'action' in v.keys():
                        if isinstance(v['action'], list):
                            for i, actionval in enumerate(v['action']):
                               pnaction.append(actionval.lower())
                               if i>0:
                                  pnname.append(k)
                                  pnlen.append(len(k))
                                  pngroup.append(v['group'])           if 'group' in v.keys()       else pngroup.append('Not grouped')
                                  if 'type' in v.keys():
                                     if v['type'].lower() in datatype:
                                        pntype.append(v['type'].lower())
                                     else:
                                        pntype.append(v['type'])
                                        exceptionlist.append('unknown type "'+v['type']+'" for property "'+k+'"')
                                  else:
                                     pntype.append('')
                                     exceptionlist.append('type is missing from property "'+k+'"')
                                  pnreturn.append(v['return'].lower()) if 'return' in v.keys()      else pnreturn.append('')
                                  pnea.append(v['function'])           if 'function' in v.keys()    else pnea.append('')
                                  pntext.append(v['description'])      if 'description' in v.keys() else pntext.append('')
                        else:
                           pnaction.append(v['action'].lower())
                    else:
                        pnaction.append('')

            if pnname and pngroup:
                frames = [ self.apidef['pn']['elements'], pd.DataFrame(list(zip(pngroup, pnname, pnlen, pntype, pnaction, pnea, pntext,pnreturn)),
                                                         columns=self.apidef['pn']['columns']) ]
                self.apidef['pn']['elements']= pd.concat(frames, ignore_index=True)
                pref = [ self.apidef['Prefix'] for i in range(len(pnname)) ]
                prefenp = [ self.apidef['enp']['elements'], pd.DataFrame({ 'prefix': pref, 'element' : pnname }).drop_duplicates() ]
                self.apidef['enp']['elements'] = pd.concat(prefenp, ignore_index=True)

                pntype = self.apidef['pn']['elements']['type'].tolist()
                if ('int64' in pntype or 'oint64' in pntype or 'vint64' in pntype):
                    if (self.apidef['haveInt64']['elements'].shape[0] <= 0 or
                        self.apidef['Prefix'] not in self.apidef['haveInt64']['elements']['prefix'].tolist()) :
                       appendToDefinition('haveInt64', [ [self.apidef['Prefix']] ])

        if 'constants' in ydata.keys():
            ggroup,gconst,glen,gvalue = list(),list(),list(),list()
            for gc in ydata['constants']:
                for k,v in gc.items():
                    for vitem in v:
                        for gk, gv in vitem.items():
                            ggroup.append(k)
                            gconst.append(gk)
                            glen.append(len(gk))
                            gvalue.append(gv)

            self.apidef['gcon']['elements'] = pd.DataFrame(list(zip(ggroup, gconst, glen, gvalue)), columns=self.apidef['gcon']['columns'])
            group = self.apidef['gcon']['elements']['group'].drop_duplicates().tolist()
            maxLen = list()
            for g in group:
                maxLen.append( max(self.apidef['gcon']['elements'][self.apidef['gcon']['elements']['group']==g]['len'].tolist()) )
            self.apidef['cname']['elements'] = pd.DataFrame(list(zip(group, maxLen)), columns=self.apidef['cname']['columns'])

        if 'stringconstants' in ydata.keys():
            ggroup,gconst,glen,gvalue = list(),list(),list(),list()
            for gc in ydata['stringconstants'] :
                for k,v in gc.items():
                    for vitem in v:
                        for gk, gv in vitem.items():
                            ggroup.append(k)
                            gconst.append(gk)
                            glen.append(len(gk))
                            gvalue.append(gv)

            self.apidef['gstrcon']['elements']  = pd.DataFrame(list(zip(ggroup, gconst, glen, gvalue)), columns=self.apidef['gstrcon']['columns'])
            gname = self.apidef['gstrcon']['elements'].groupby('group')
            maxStrLen = list()
            for g in gname.groups.keys():
                maxStrLen.append( max(self.apidef['gstrcon']['elements'][self.apidef['gstrcon']['elements']['group']==g]['len'].tolist()) )
            self.apidef['csname']['elements'] = pd.DataFrame(list(zip(gname.groups.keys(),maxStrLen)), columns=self.apidef['csname']['columns'])

        tfnamelist = getNameByType('tfunc', ['c'])
        if len(tfnamelist) > 0:
            appendToDefinition('f90Skip', [ tfnamelist ])
        pnnamelist = getNameByType('pn', ['c'])
        if len(pnnamelist) > 0:
            appendToDefinition('f90Skip', [ pnnamelist ])
            tfnamelist = getNameByType('tfunc', ['pc','oss'])
        if len(tfnamelist) > 0:
            appendToDefinition('lfSkip', [ tfnamelist ])
        fnamelist = getNameByType('f', ['c','vc','xss'])
        if len(fnamelist) > 0:
            appendToDefinition('lfSkip', [ fnamelist ])
        pnnamelist = getNameByType('pn', ['pc','oss','c','funcptr'])
        if len(pnnamelist) > 0:
            appendToDefinition('lfSkip', [ pnnamelist ])
        tfnamelist = getNameByType('tfunc', ['c'])
        if len(tfnamelist) > 0:
            appendToDefinition('lfSkip', [ tfnamelist ])

        if 'functionpointers' in ydata.keys():
            fdef,ffpos,fapos,ffunc,farg,ftype,ftext,farrlen  = list(),list(),list(),list(),list(),list(),list(),list()
            for fptrd in ydata['functionpointers']:
                for k, v in fptrd.items():
                    fdef.append(k)
                    funcpos = v['position']    if 'position' in v.keys()   else ''
                    ffpos.append(funcpos)
                    function = v['function'] if 'function' in v.keys() else ''
                    ffunc.append(function)
                    fparampos = 0
                    farg.append('result')
                    fapos.append(fparampos)
                    if 'type' in v.keys():
                        if v['type'].lower() in datatype:
                            ftype.append(v['type'].lower())
                        else:
                            ftype.append(v['type'])
                            exceptionlist.append('unknown type "'+v['type']+'" for function pointer definition "'+k+'"')
                    else:
                        ftype.append('')
                        exceptionlist.append('type is missing from function pointer definition "'+k+'"')
                    ftext.append(v['description'])  if 'description' in v.keys() else ftext.append('')
                    farrlen.append(0)
                    if 'parameters' in v.keys():
                        params = v['parameters']
                        for p in params:
                            for fk, fv in p.items():
                                fparampos += 1
                                fdef.append(k)
                                ffpos.append(funcpos)
                                ffunc.append(function)
                                fapos.append(fparampos)
                                farg.append(fk)
                                if 'type' in fv.keys():
                                    if fv['type'].lower() in datatype:
                                        ftype.append(fv['type'].lower())
                                    else:
                                        ftype.append(fv['type'])
                                        exceptionlist.append('unknown type "'+fv['type']+'" for parameter "'+fk+'" of function pointer definition "'+k+'"')
                                else:
                                    ftype.append('')
                                    exceptionlist.append('type is missing from parameter "'+fk+'" of function pointer definition "'+k+'"')
                                ftext.append(fv['description'])   if 'description' in fv.keys() else ftext.append('')
                                farrlen.append(fv['arraylength']) if 'arraylength' in fv.keys() else farrlen.append(0)
            ffposstr = list(map(str, ffpos))
            faposstr = list(map(str, fapos))
            frames = [ self.apidef['FuncPtrDef']['elements'],
                       pd.DataFrame(list(zip(fdef, ffposstr, ffunc, faposstr, farg, ftype, ftext)),
                                    columns=self.apidef['FuncPtrDef']['columns']) ]
            self.apidef['FuncPtrDef']['elements'] = pd.concat(frames, ignore_index=True)
            if len(self.apidef['FuncPtrDef']['elements']) > 0:
                df = self.apidef['FuncPtrDef']['elements'].copy()
                del df['apos']
                del df['arg']
                del df['type']
                del df['text']
                self.apidef['FuncMap']['elements'] = df.drop_duplicates()
                self.apidef['FuncMap']['elements'].reset_index(drop=True, inplace=True)

                df = self.apidef['FuncPtrDef']['elements'].copy()
                del df['def']
                del df['fpos']
                self.apidef['PtrF']['elements'] = df.drop_duplicates()
                self.apidef['PtrF']['elements'].reset_index(drop=True, inplace=True)

            if len(farrlen) > 0:
                frames = [ self.apidef['pArrLen']['elements'],
                           pd.DataFrame(list(zip(ffunc, farg, farrlen)), columns=self.apidef['pArrLen']['columns']) ]
                self.apidef['pArrLen']['elements'] = pd.concat(frames, ignore_index=True)

                df = self.apidef['pArrLen']['elements']
                index_names = df[df['value']==0].index
                self.apidef['pArrLen']['elements'].drop(index_names, inplace=True)
                self.apidef['pArrLen']['elements'].reset_index(drop=True, inplace=True)

            if len(self.apidef['PtrF']['elements']) > 0:
                df = self.apidef['PtrF']['elements']
                tptrfunc =  pd.DataFrame( df[df['arg']=='result'] ).copy()
                del tptrfunc['apos']
                del tptrfunc['arg']
                self.apidef['tPtrFunc']['elements'] = tptrfunc

                df = self.apidef['PtrF']['elements'].copy()
                fvallist  = self.datadef['FVal']['elements']['ta'].to_list()
                pftr_fval = df[df['type'].isin(fvallist)]['name']
                pftrf_ta  = df[df['type'].isin(['c', 'cpc', 'css', 'csi'])]['name']
                self.apidef['PFtrF']['elements'] = pd.DataFrame( pd.concat( [ pftr_fval, pftrf_ta ], ignore_index=True), columns=self.apidef['PFtrF']['columns']
                                                                   ).drop_duplicates()
            df = self.apidef['FuncPtrDef']['elements']
            cols = ['def']
            self.apidef['fpf']['elements'] = pd.DataFrame(list(df.groupby('def').groups.keys()), columns=self.apidef['fpf']['columns'])

        if len(exceptionlist) > 0:
            raise Exception('Error parsing '+args.apidef+'\n' +  '\n'.join(exceptionlist))

        df = pd.DataFrame(self.apidef['f']['elements'][self.apidef['f']['elements']['arg'] != 'result' ])
        self.apidef['argtext']['elements'] = pd.DataFrame( {'name': df['arg'].to_list(), 'text':df['text'].to_list()}, columns=self.apidef['argtext']['columns'] )

        df = self.apidef['f']['elements']
        dfbool = pd.DataFrame(df[df['type']=='bool']['name'], columns=self.apidef['fbool']['columns'])
        dfVbool = pd.DataFrame(df[df['type']=='vbool']['name'], columns=self.apidef['fvbool']['columns'])
        self.apidef['fbool']['elements'] = pd.concat([dfbool,dfVbool], ignore_index=True)
        self.apidef['fvbool']['elements'] = dfVbool

        dfint64  = pd.DataFrame(df[df['type']=='int64']['name'], columns=self.apidef['fbool']['columns'])
        dfVint64 = pd.DataFrame(df[df['type']=='vint64']['name'], columns=self.apidef['fvbool']['columns'])
        dfOint64 = pd.DataFrame(df[df['type']=='oint64']['name'], columns=self.apidef['fvbool']['columns'])
        self.apidef['enInt64']['elements'] = pd.concat([dfint64,dfVint64,dfOint64], ignore_index=True)

        dictlist = list()
        if len(df) > 0:
            for e in df.groupby('name').groups.keys() :
                fpelements = df.loc[df['name'] == e]['pos']
                numelements = fpelements.shape[0]-1
                if numelements > 0:        # skip function elements without parameters (?)
                   dictlist.append([e, numelements])
                flenlist = self.apidef['f']['elements']['len'].to_list()
                self.apidef['idlenF']['value'] = max(flenlist)
        else:
            self.apidef['idlenF']['value'] = 0

        df = self.apidef['PtrF']['elements']
        if len(df) > 0:
            for e in df.groupby('name').groups.keys():
                fpelements = df.loc[df['name'] == e]['apos']
                numelements = fpelements.shape[0]-1
                if numelements > 0:        # skip function elements without parameters (?)
                   dictlist.append([e, numelements])

        self.apidef['farg']['elements'] = pd.DataFrame.from_records(dictlist, columns=self.apidef['farg']['columns'])
        self.apidef['fargmax']['value'] = self.apidef['farg']['elements']['value'].max()

        gmstalist = self.datadef['gmsta']['elements']['ta'].to_list()
        df = self.apidef['f']['elements']
        self.apidef['gamsta']['value']  = (df[df['type'].isin(gmstalist)].shape[0] + df[df['type'].isin(gmstalist)].shape[0] > 0)

        df = self.apidef['f']['elements']
        enstring = df[df['type'].isin(list(self.datadef['tass']['elements']['ta']))]['name'].copy()
        fs = df[df['name'].isin(list(enstring))]  # no record with (0.result)
        enstring.reset_index(drop=True, inplace=True)
        fs.reset_index(drop=True, inplace=True)
        enostringa = df[df['type'] == 'osi']['name'].copy()
        enostringa.reset_index(drop=True, inplace=True)

        fost = df[df['type'].isin(['osi', 'oss', 'xss' ])]['name'].copy()
        fost.reset_index(drop=True, inplace=True)
        fstr = df[df['type'].isin(list(self.datadef['tass']['elements']['ta']))]['name'].copy()
        fstr.reset_index(drop=True, inplace=True)
        farr = df[df['type'].isin(list(self.datadef['taar']['elements']['ta']))]['name'].copy()
        farr.reset_index(drop=True, inplace=True)
        fsti = df[df['type'].isin(['osi', 'csi' ])]['name'].copy()
        fsti.reset_index(drop=True, inplace=True)
        fstiV = df[ (df['name'].isin(list(fsti))) & (df['arg']=='aDim') & (df['type']=='vint') ].copy()
        fstiV.reset_index(drop=True, inplace=True)
        self.apidef['enstring']['elements'] = pd.DataFrame(enstring)
        self.apidef['enostringa']['elements'] = pd.DataFrame(enostringa)
        self.apidef['fs']['elements'] = pd.DataFrame(fs, columns=self.apidef['fs']['columns'])
        self.apidef['fstr']['elements']  = pd.DataFrame(fstr)
        self.apidef['fost']['elements']  = pd.DataFrame(fost)
        self.apidef['farr']['elements']  = pd.DataFrame(farr)
        self.apidef['fsti']['elements']  = pd.DataFrame(fsti)
        self.apidef['fstiV']['elements'] = pd.DataFrame(fstiV)
        if len(self.apidef['pn']['elements']) > 0:
            tprop = self.apidef['pn']['elements'].copy() #['name', 'type', 'pactions', 'ea', 'text']
            del tprop['pactions']
            del tprop['ea']
            del tprop['text']
            self.apidef['tprop']['elements'] = tprop.drop_duplicates()

            pnlenlist = self.apidef['pn']['elements']['len'].to_list()
            self.apidef['idlenP']['value'] = max(pnlenlist)

            tpropnlist = tprop['name'].to_list()
            self.apidef['idlenP']['value'] = len(max(tpropnlist, key=len)) if tpropnlist else 0
#            tpp        = self.datadef['tpp']['elements']['tp'].to_list()
#            delphitype = self.datadef['DelphiType']['elements']['ta'].to_list()
#            f = self.apidef['f']['elements'][ self.apidef['f']['elements']['pos'].isin(tpp)  ]
#            farglist = f[f['type'].isin(delphitype)]['arg'].to_list()

            pn = self.apidef['pn']['elements']
            pnw = pn[pn['pactions']=='w']['name'].to_list()

            def wset(x): return len(x)+3 if x in pnw else len(x)
            idlenWsetlist = [ wset(x) for x in tpropnlist ]
            self.apidef['idlenWset']['value'] = max(max(idlenWsetlist), self.apidef['idlenF']['value'])
        else:
            self.apidef['idlenP']['value'] = 0
            self.apidef['idlenWset']['value'] = 0

        wnamelist, wlenlist, namelist, lenlist  = [], [], [], []
        for index, row in self.apidef['pn']['elements'].iterrows():
            if row['pactions'] == 'r':
                namelist.append(row['name'])
                lenlist.append(len(row['name']))
            else:
                wnamelist.append(row['name']+"Set")
                wlenlist.append(len(row['name'])+3)

        namelist.extend( self.apidef['tfunc']['elements']['name'].tolist() ) 
        lenlist.extend( self.apidef['tfunc']['elements']['len'].tolist() ) 

        for f in  self.datadef['extraFuncNames']['elements']:
            if f.lower() == 'createdd':
               if self.apidef['UseCD']['elements'].shape[0] > 0 and self.apidef['Prefix'] in self.apidef['UseCD']['elements']['prefix'].tolist() :
                  name = self.apidef['Prefix']+f.lower()
                  namelist.append(name)
                  lenlist.append(len(name))
            else:
                name = self.apidef['Prefix']+f.lower()
                namelist.append(name)
                lenlist.append(len(name))

        self.apidef['maxLenFuncNames']['value'] = max(len(item) for item in namelist)
        maxwlen = max(len(item) for item in wnamelist) if len(wnamelist)>0 else 0
        if self.apidef['maxLenFuncNames']['value'] < maxwlen:
            self.apidef['maxLenFuncNames']['value'] = maxwlen

        self.apidef['FuncNames']['elements']    = pd.DataFrame(list(zip(namelist, lenlist)), columns=self.apidef['FuncNames']['columns'])
        self.apidef['FuncNamesSet']['elements'] = pd.DataFrame(list(zip(wnamelist,wlenlist)), columns=self.apidef['FuncNamesSet']['columns'])

        if self.apidef['FuncMap']['elements'].shape[0] > 0:
           appendToDefinition('haveTypedefs', [ [self.apidef['Prefix']] ])
        return

    def generate(self, args):
        ydata = Definition.readAPIDefinitionFile( args.apidef )
        validator = DataValidator()
        if 'configurations' in ydata.keys():
            validator.validate( ydata )
            for cfgdata in ydata['configurations']:
                cfgdata = { key.lower(): value for key, value in cfgdata.items() }
                configuration = dict()
                for c in cfgdata:
                    configuration[c] = dict()
                    for key in cfgdata[c].keys():
                        configuration[c][key] = cfgdata[c][key]
                    for key in self.datadef['MultipleConfigurationKeys']:
                        if key not in configuration[c].keys(): # not defined in any configuration
                            if key in ydata.keys(): # defined globally
                               configuration[c][key] = ydata[key]
#                        if key == 'compatibleversion':
#                           cfgdata[c][key] = cfgdata[c][key].sort()
                    self.updateAPIDefinition( ydata, configuration[c], args )
                    if isinstance(args.output, list) and len(args.output) > 0:
                        self.generateOutput(args.output)
                    else:
                        self.generateOutput(configuration[c]['output'])
                    self.clearAPIDefinition()

        elif 'multilist' in ydata.keys():
            validator.validate( ydata, combinedAPI=True )
            config,multidata = dict(), dict()
            config['multiprefix'] = ydata['multiprefix'] if 'multiprefix' in ydata.keys() else ''
            config['multi']       = ydata['multi']       if 'multi'       in ydata.keys() else False
            for apidata in  ydata['multilist']:
                for key,value in apidata.items():
                    dirname = os.path.dirname( args.apidef )
                    apifilename = os.path.normpath(os.path.join(dirname, os.path.normpath(value)))
                    multidata[key] = self.readAPIDefinitionFile( apifilename )
            for key,value in multidata.items():
                self.updateAPIDefinition( multidata[key], config, args, True, True)
            if isinstance(args.output, list) and len(args.output) > 0:
                self.generateOutput(args.output)
            else:
                self.generateOutput(ydata['output'])
            self.clearAPIDefinition()
        else:
            validator.validate( ydata )
            configuration, config  = dict(), dict()
            config['clibuse'], config['testmode']          = False, False
            config['output'],  config['compatibleversion'] = [], []
            config['apiversion']                           = 0 
            for key in self.datadef['MultipleConfigurationKeys'] :
                if key in ydata.keys():
#                    if key == 'compatibleversion':
#                        ydata[key] = ydata[key].sort()
                    config[key] = ydata[key]
            configuration['dummy'] = config
            multi = ydata['multi'] if 'multi' in ydata.keys() else False
            config['prefix']      = ydata['prefix']      if 'prefix'      in ydata.keys() else ''
            config['multiprefix'] = ydata['multiprefix'] if 'multiprefix' in ydata.keys() else ''
            if args.multi: # forced m in output name:
                multi=True
            self.updateAPIDefinition( ydata, config, args, multi )
            if isinstance(args.output, list) and len(args.output) > 0:
                self.generateOutput(args.output)
            else:
                self.generateOutput(config['output'])
            self.clearAPIDefinition()

    class ArgumentParserError(Exception): pass

    class ArgumentTypeError( argparse.ArgumentTypeError ): pass

    class ArgumentParser(argparse.ArgumentParser):
        def error(self, message):
            sys.stderr.write('error: %s\n' % message)
            self.print_help()
            raise APIGenerator.ArgumentParserError(message)

if __name__ == "__main__":
    parser = APIGenerator.ArgumentParser()
    parser.add_argument('--apidef', type=str, required=True, help='API definition file')
    parser.add_argument('--outputpath' , type=str, required=True, help='output directory')
    parser.add_argument('--output' , nargs='*', help='list of output to override output from API definition file')
    parser.add_argument('--multi' , default=False, type=bool, help='force m in output name. Default=False')
    try:
       args = parser.parse_args()
    except (APIGenerator.ArgumentParserError, APIGenerator.ArgumentTypeError) as e:
        sys.exit(e)

    if not os.path.exists(args.apidef):
        sys.exit('error: ' + args.apidef + ' does not exist')

    if not os.path.exists(args.outputpath):
        os.makedirs(args.outputpath)

    g = APIGenerator()
    g.generate(args)
