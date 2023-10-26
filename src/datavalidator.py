import pprint
from cerberus import Validator

class DataValidator(object):
    def type_arguments():
        return \
        [   ['ptr', 'pointer'],
            ['Vptr', 'var pointer'],
            ['int', 'integer'],
            ['oint', 'out integer'],
            ['vint', 'var integer'],
            ['int64', 'integer64'],
            ['vint64', 'var integer64'],
            ['oint64', 'out integer64'],
            ['cpda', 'const pointer to double array'],
            ['pda', 'pointer to double array'],
            ['cplia', 'const pointer to 32 bit integer array'],
            ['plia', 'Pointer to 32 bit integer array'],
            ['cpc', 'const pointer to char'],
            ['pc', 'pointer to char'],
            ['css', 'const short string'],
            ['oss', 'out short string'],
            ['xss', 'out string with variable length for C clients'],
            ['d', 'double'],
            ['od', 'out double'],
            ['vd', 'var double'],
            ['bool', 'boolean (1=true, 0=false)'],
            ['vbool', 'boolean (1=true, 0=false)'],
            ['cii', 'TgdxUELIndex'],
            ['vii', 'TgdxUELIndex'],
            ['crv', 'TgdxValues'],
            ['vrv', 'TgdxValues'],
            ['csi', 'TgdxStrIndex'],
            ['osi', 'TgdxStrIndex'],
            ['csva', 'TgdxSVals'],
            ['vsva', 'TgdxSVals'],
            ['funcptr', 'Pointer to a function'],
            ['void', 'used to indicate procedures'],
            ['c', 'char'],
            ['vc', 'var char']
        ]

    def string_type_arguments():
        return [ 'css', 'oss', 'xss', 'csi', 'osi' ]

    def pchar_type_arguments():
        return [ 'cpc','pc' ]

    def array_type_arguments():
        return ['cpda', 'pda', 'cplia', 'plia', 'cii', 'vii', 'crv', 'vrv', 'csi', 'osi', 'csva', 'vsva' ]

    def output_flags():  # control which files will be created by means of flags.
        return \
        [   'all',
            'cb',
            'cc',
            'cclib',
            'cclibdef',
            'ccon',
            'cpplib',
            'dcb',
            'dclib',
            'dcdef',
            'dcpdef',
            'dcdefex',
            'dodef',
            'dodefex',
            'ddec',
            'dcon',
            'cs',
            'py',
            'java',
            'vb',
            'f9def',
            'f9glu',
            'doc'
        ]

    def pactions():
        return [ ['r', 'read'],
                 ['w', 'write'],
                 ['read', 'read'],
                 ['write', 'write'] ]

    def output(field, value, error):
        validate_list = [v in DataValidator.output_flags() for v in value]
        if not all(validate_list):
            index_list   = [index for index, element in enumerate(validate_list) if not element]
            element_list = [value[index] for index in index_list] 
            error(field, "unallowed value [{}]".format(", ".join(element_list)))

    def type_argument(field, value, error):
        ta_list = [ta[0].lower() for ta in DataValidator.type_arguments()]
        if value.lower() not in ta_list:
           error(field, "unallowed value {}".format(value))

    def property_action(field, value, error):
        pa_list = [pa[0].lower() for pa in DataValidator.pactions()]
        if isinstance(value, list):
            validate_list = [v.lower() in pa_list for v in value]
            if not all(validate_list):
               index_list   = [index for index, element in enumerate(validate_list) if not element]
               element_list = [value[index] for index in index_list] 
               error(field, "unallowed value [{}]".format(", ".join(element_list)))
        elif value.lower() not in pa_list:
             error(field, "unallowed value {}".format(value))

    def multiapi_schema():
        return \
        {
            'title'            : { 'type': 'string' , 'required': True },
            'multiprefix'      : { 'type': 'string'  },
            'output'           : {
                'type'     : 'list',
                'required' : True,
                'check_with'  : DataValidator.output
            },
            'multi'            : { 'type': 'boolean' },
            'multilist'        : {
                'type'       : 'list',
                'schema'     : { 
                    'type'        : 'dict',
                    'keysrules'   : { 'type': 'string' }
                }
            }
        }

    def api_schema():
        return \
        {
            'title'            : { 'type': 'string' , 'required': True             },
            'prefix'           : { 'type': 'string' , 'required': True             },
            'apiversion'       : { 'type': 'integer', 'excludes': 'configurations' },
            'compatibleversion': { 'type': 'list'   , 'excludes': 'configurations' },
            'extracuse'        : { 'type': 'string'  },
            'extrause'         : { 'type': 'string'  },
            'extrausem'        : { 'type': 'string'  },
            'dobject'          : { 'type': 'string'  },
            'dobjectint'       : { 'type': 'string'  },
            'dunit'            : { 'type': 'string'  },
            'clibuse'          : { 'type': 'boolean', 'excludes': 'configurations' },
            'use_xxxloadpath'  : { 'type': 'boolean' },
            'usecd'            : { 'type': 'boolean' },
            'multi'            : { 'type': 'boolean' },
            'doc'              : { 'type': 'boolean' },
            'nofortrancb'      : { 'type': 'boolean' },
            'multiprefix'      : { 'type': 'string'  },
            'maxdimstyle'      : { 'type': 'string'  },
            'output'           : {
                'type'       : 'list',
                'check_with' : DataValidator.output,
                'excludes'   : 'configurations'
            },
            'configurations' : {
                'type'       : 'list',
                'excludes'   : [ 'apiversion', 'compatibleversion', 'output', 'clibuse' ],
                'schema'     : {
                    'type'        : 'dict',
                    'keysrules'   : { 'type': 'string' },
                    'valuesrules' : {
                        'type'       : 'dict',
                        'schema'     : {
                           'apiversion'       : { 'type': 'integer' },
                           'compatibleversion': { 'type': 'list'    },
                           'dobject'          : { 'type': 'string'  },
                           'dobjectint'       : { 'type': 'string'  },
                           'dunit'            : { 'type': 'string'  },
                           'clibuse'          : { 'type': 'boolean' },
                           'testmode'         : { 'type': 'boolean' },
                           'output'           : {
                               'type'       : 'list',
                               'check_with' : DataValidator.output
                           },
                           'preprefix'        : { 'type': 'string'  },
                        }
                    }
                }
            },
            'functions': { #function and procedures
                'type'       : 'list',
                'schema'     : { 
                    'type'        : 'dict',
                    'keysrules'   : { 'type': 'string' },
                    'valuesrules' : {
                        'type'       : 'dict',
                        'schema'     : { 
                            'type'        : { 
                                'check_with' : DataValidator.type_argument,
                                'required'   : True 
                            },
                            'return'      : { 'type' : 'string'},
                            'description' : { 'type' : 'string'},
                            'details' : { 'type' : 'string'},
                            'static'  : { 'type' : 'boolean' },
                            'const'   : { 'type' : 'boolean' },
                            'code'    : {
                                'type' : 'dict',
                                'allowed': ['c','cpp','cs','py','java','f90','pas', 'jl', 'vb', 'r', 'm', 'vba'],
                                'keysrules': { 'type': 'string' },
                                'valuesrules': { 'type': 'string' }
                            },
                            'parameters'  : { 
                                'type'        : 'list',
                                'schema'     : { 
                                    'type'        : 'dict',
                                    'keysrules'   : { 'type': 'string' },
                                    'valuesrules' : { 
                                        'type'       : 'dict',
                                        'schema'     : { 
                                            'type'        : { 
                                                'check_with' : DataValidator.type_argument,
                                                'required'   : True 
                                            },
                                            'description' : { 'type' : 'string'}
                                        }
                                    }
                                },
                            },
                            'description' : { 'type' : 'string' },
                            'group'       : { 'type' : 'string' },
                            'condition'   : { 'type' : 'string' }
                        }
                    }
                }
            },
           'properties'        : { # property names and actions
                'type'        : 'list',
                'schema'     : { 
                    'type'       : 'dict',
                    'valuesrules'      : {
                        'type'       : 'dict',
                        'schema'     : { 
                            'type'        : { 
                                'check_with' : DataValidator.type_argument,
                                'required'   : True 
                            },
                            'action'      : { 
                                'check_with' : DataValidator.property_action,
                                'required'   : True 
                            },
                            'function'    : { 'type' : 'string'  , 'required': True },
                            'description' : { 'type' : 'string' },
                            'group'       : { 'type' : 'string' },
                            'condition'   : { 'type' : 'string' }
                         }
                    }
                }
            },
            'functionpointers': { #function pointer definitions
                'type'       : 'list',
                'keysrules'  : { 'type': 'string' },
                'valuesrules': {
                   'type'       : 'dict',
                   'keysrules'  : { 'type': 'string' },
                   'schema'     : { 
                       'function' : { 'type' : 'string'  , 'required': True },
                       'position' : { 'type' : 'integer' , 'required': True },
                       'type'     : { 'type' : 'string'  , 'required': True },
                   }
                }
            },
            'constants'        : { #constants
                'type'       : 'list',
                'keysrules'  : { 'type': 'string' },
                'valuesrules': {
                   'type'       : 'list',
                   'keysrules'  : { 'type': 'string' },
                   'valuesrules': {
                       'type'       : 'dict',
                       'valuesrules': { 'type' : 'integer' }
                   }
                }
            },
            'stringconstants'        : { # string constants
                'type'       : 'list',
                'keysrules'  : { 'type': 'string' },
                'valuesrules': {
                   'type'       : 'list',
                   'keysrules'  : { 'type': 'string' },
                   'valuesrules': {
                       'type'       : 'dict',
                       'valuesrules': { 'type' : 'string' }
                   }
                }
            },
            'symboldimensions' : { # Call Symbol Dimensions
                'type'       : 'list',
                'keysrules'  : { 'type': 'string' },
                'valuesrules': {
                   'type'       : 'list',
                   'keysrules'  : { 'type': 'string' },
                   'valuesrules': {
                       'type'       : 'dict',
                       'keysrules'  : { 'type' : 'string' },
                       'valuesrules': { 'type' : 'string' }
                   }
                }
            },
            'internalcs' : { 'type' : 'list', 'keysrules': { 'type' : 'string' } },
            'skippy'     : { 'type' : 'list', 'keysrules': { 'type' : 'string' } },
            'useadim'    : { 'type' : 'list', 'keysrules': { 'type' : 'string' } },
            'usecurrentdim' : { 'type' : 'list', 'keysrules': { 'type' : 'string' } },
            'usesymboldim'  : { 'type' : 'list', 'keysrules': { 'type' : 'string' } }
        }

    def __init__(self):
        self.validator = Validator( )

    def validate(self, data, combinedAPI=False):
        if not self.validator.validate( data, 
                                        DataValidator.multiapi_schema() if combinedAPI else DataValidator.api_schema() ):
            pp = pprint.PrettyPrinter()
            raise AssertionError('Invalid schema\n' + pp.pformat(self.validator.errors))


