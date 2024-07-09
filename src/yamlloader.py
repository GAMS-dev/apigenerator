#!/usr/bin/env python3
import sys
import argparse
import os
import yaml
import pathlib

class Loader(yaml.Loader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(Loader, self).__init__(stream)
        Loader.add_constructor('!include', Loader.include)

    def include(self, node):
        if   isinstance(node, yaml.ScalarNode):
            return self.extractFile(self.construct_scalar(node))

        elif isinstance(node, yaml.SequenceNode):
            result = []
            for filename in self.construct_sequence(node):
                result += self.extractFile(filename)
            return result

        elif isinstance(node, yaml.MappingNode):
            result = {}
            for k,v in self.construct_mapping(node).items():
                result[k] = self.extractFile(v)
            return result

        else:
            print('Error:: unrecognised node type in !include statement.')
            raise yaml.constructor.ConstructorError

    def extractFile(self, filename):
        try:
            filepath = os.path.join(self._root, filename)
            with open(filepath, 'r') as f:
                return yaml.load(f, Loader)
        except IOError:
            print('The included file '+filepath+' does not exist.')
            raise IOError

if __name__ == "__main__":
    try:
        base_path = pathlib.Path(__file__).parent
        file_path = (base_path / 'apilist.yaml').resolve()
        print(file_path)
        with open(file_path, 'r') as f:
           print( yaml.load(f, Loader ) )
           f.close()
    except IOError:
        print('Error loading content of apilist.yaml or apilist.yaml does not exist.')
