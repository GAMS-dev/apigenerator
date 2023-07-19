# apigenerator

Python-based generator for GAMS API.

The Python based API generator is based on an open source programming language (Python), a language template tool for Python (jinja2) and a human-readable structured file format (yaml) for describing API data definitions. 


## API Definition File

The Python based API generator is located under `src/`. The generator consists of the Python script (`mkapi.py`) and several templates of jinja2 language (`*.templates.j2`). Each template serves as a preset format to create API file(s) using the Python script and an API definition file. The following describes all templates implemented for the Python-based API generator up to now:

- cc - for C Function Interface (`[API]cc.c` and `[API]cc.h`),
- cclib - for C Callable Library (`[API]cclib.c`)
- cclibdef - for Microsoft Module-Definition file for C Library (`[API]cclib.def`)
- py - for (`[API]cc.i`) and (`[API]setup.py`)
- vb - for Visual Basic for Apllication callable library (`[API]vba.bas`) and Visual Basic .Net callable library (`[API]vbnet.vb`)
- cs - for C Sharp Callable Library (`[API]cs.cs`)
- java - for Java interface (`[API].java`) and Java native interface (`[API]jni.c`)

## API Data Definition File

An API definition file describes a data definition of API and serves as an input for the script to fill in a template in order to create API code file(s). The definition file is a yaml file containing: 

- Generic API title (`title`)
- Abbreviation (`prefix`)
- Boolean Flag describing whether C library is used (`CLibUse`)
- String describing C including file when C library is used (`extraCUse`)
- Name of the Delphi object (`DObject`)
- Name of the Delphi unit (`DUnit`)
- API version (`apiversion`)
- List of compatible API versions (`compatibleversion`)
- List of templating outputs to be generate (`output`)
- List of object properties name and actions (`properties`)
- List of functions and procedures (`functions`)
- List of callback function types (`functionpointers`)
- List of numeric constants (`constants`)
- List of string numeric constants (`stringconstants`)

## Usage

```
python src/mkapi.py --apidef [/path/to/apidef/]testapi.yaml --outputpath [/outputpath/]
```
 