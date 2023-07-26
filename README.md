# apigenerator

Python-based generator for GAMS API.

The Python based API generator is based on an open source programming language (Python), a language template tool for Python (jinja2) and a human-readable structured file format (yaml) for describing API data definitions. The python script can generate, for a given API, API wrapper file(s) in targeted languges using the data definition from the API data definition file and the targeted language template file(s).

The generator consists of the script (`mkapi.py`) located under `src/` and several templates of jinja2 language (`*.templates.j2`) located under `templates/`. Each template serves as a preset container to fill in data definition from a data definition and congiruation file using the Python script. For each API, the data definitions and configurations are expected to be defined in a yaml file. The output configuration that can be generated for each API are:
  - `cc` - for C Function Interface (to generate `[API]cc.c` and `[API]cc.h`),
  - `cclib` - for C Callable Library (to generate `[API]cclib.c`)
  - `cclibdef` - for Microsoft Module-Definition file for C Library (to generate `[API]cclib*.def`)
  - `cb` - for C Callback Interface (to generate `[API]ccb1.h` and `[API]ccb2.h`)
  - `py` - for (to generate `[API]cc.i`) and (to generate `[API]setup.py`)
  - `vb` - for Visual Basic for Apllication callable library (to generate `[API]vba.bas`) and Visual Basic .Net callable library (to generate `[API]vbnet.vb`)
  - `cs` - for C Sharp Callable Library (to generate `[API]cs.cs`)
  - `java` - for Java interface (to generate `[API].java`) and Java native interface (to generate `[API]jni.c`)

## Data Definition and Configuration File

An API definition and congiruation file describes a data definition of API and serves as an input for the script to fill in a template in order to create API code file(s). The definition and congiruation file is a yaml file containing: 

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
- List of targeted output to be generated (`output`)

## Usage

- To generate files for `[API]` from the data definition and configuration file `[API]api.yaml` using script `mkapi.py`:
  ```
  python [/path/to/file/]mkapi.py
      --apidef [/path/to/file/][API]api.yaml
      --outputpath [/outputpath/]
  ```
  
- To override the output to be generated from the data definition and configuration file `[API]api.yaml` using `--output` argument:
  ```
  python [/path/to/file/]mkapi.py
      --apidef [/path/to/file/][API]api.yaml
      --outputpath [/outputpath/] 
      --output cc
  ```
  will ignore the list of targeted output(`output`) from `[API]api.yaml` and generate only C Function Interface (`[API]cc.c` and `[API]cc.h`).

