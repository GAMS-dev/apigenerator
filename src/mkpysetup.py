#!/usr/bin/env python3
import sys
import argparse
import os
import datetime
import yaml
import pathlib
from yamlloader import Loader
from jinja2 import Environment, FileSystemLoader

class Setup:
    def __init__(self, args):
        self.args      = args
        self.data      = dict()
        self.templates = ['setup']
        self.api       = {
            'generator'     : 'apiwrapper',
            'SysRelease'    : os.environ['GVERSIONMAJOR'],
            'SysSubRel'     : os.environ['GVERSIONMINOR'],
            'SysSubRelGold' : os.environ['GVERSIONRELEASE'],
            'SysYear'       : datetime.date.today().year
        }
        ydata = self.readFile(self.args.apiloc)
        if type(ydata) is list:
            for d in ydata:
                for k in d.keys():
                    apidata =  self.readFile(d[k], self.args.basedir)
                    apidata = { k.lower(): v for k, v in apidata.items() }
                    if apidata is not None and 'apiversion' in apidata.keys():
                       self.data[k] = apidata['apiversion']
            if apidata is not None:
                for template in self.templates:
                    self.generateFile(template,self.args.outputpath)
        else:
            print('Error loading content of '+args)

    def readFile(self, filepathname, base_path=''):
        try:
            if base_path is None or len(base_path) == 0:
                base_path = pathlib.Path(__file__).parent
            else:
                base_path = pathlib.Path(base_path)
            file_path = (base_path / filepathname).resolve()
            with open(file_path, 'r') as f:
               ydata = yaml.load(f, Loader )
               f.close()
            return ydata
        except IOError:
            print('Error loading content of '+filepathname+' or '+filepathname+' does not exist.')
            return None

    def generateFile(self, templatename, subdirectory=''):
        templatefilename = templatename+'.template.j2'
        file_loader = FileSystemLoader(pathlib.Path(__file__).parent)
        templates_dir = os.path.join(os.path.dirname(pathlib.Path(__file__).parent), 'templates')
        env = Environment(loader=FileSystemLoader(templates_dir))
        template = env.get_template(templatefilename)
        output = template.render(api=self.api, keys=self.data.keys, data=self.data,templatename=templatename)
        outputfilename = templatename+'.py'
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

    class ArgumentParserError(Exception): pass

    class ArgumentTypeError( argparse.ArgumentTypeError ): pass

    class ArgumentParser(argparse.ArgumentParser):
        def error(self, message):
            sys.stderr.write('error: %s\n' % message)
            self.print_help()
            raise Setup.ArgumentParserError(message)

if __name__ == "__main__":
    parser = Setup.ArgumentParser()
    parser.add_argument('--apiloc', type=str, required=True, help='API definition location file')
    parser.add_argument('--basedir', type=str, help='Base directory for relative file')
    parser.add_argument('--outputpath' , type=str, required=True, help='output directory')
    try:
       args = parser.parse_args()
    except (Setup.ArgumentParserError, Setup.ArgumentTypeError) as e:
        sys.exit(e)

    if not os.path.exists(args.apiloc):
        sys.exit('error: ' + args.apiloc + ' does not exist')

    if not os.path.exists(args.outputpath):
        os.makedirs(args.outputpath)

    s = Setup(args)
