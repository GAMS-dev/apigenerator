# enable this to get output of determined variable values
#DEBUGMAKEVARS=true

# macro to print variable name and value if debug is enabled
PRINTVAR = $(if $(DEBUGMAKEVARS), $(info $(strip $(1)) = $($(strip $(1)))))

# determinate operating system: linux, macos, windows
# also CIACODE, as long as this is still needed
ifeq ($(shell uname -s),Darwin)
  OSTYPE := macos
  PLATFORMDETECT := d
  CIACODE := D
else ifeq ($(shell uname -s),Linux)
  OSTYPE := linux
  PLATFORMDETECT := l
  CIACODE := L
else ifeq ($(shell uname -o),Msys)
  OSTYPE := windows
  PLATFORMDETECT := w
  CIACODE := W
else
  $(error Cannot determine operating system)
endif
$(call PRINTVAR, OSTYPE)

# set buildcode to GSYS (leg, wei, deg, dac)
ifndef GSYS
  $(error GSYS not defined)
endif
BUILDCODE := $(GSYS)
$(call PRINTVAR, BUILDCODE)

# determine CPU architecture
ARCH := $(shell uname -m)
$(call PRINTVAR, ARCH)
PLATFORMDETECT := $(PLATFORMDETECT)$(subst x86_64,e,$(subst arm64,a,$(ARCH)))
CIACODE := $(CIACODE)$(subst x86_64,E,$(subst arm64,A,$(ARCH)))

# set platform to GCIA (lex, wex, dex, dax)
ifndef GCIA
  $(error GCIA not defined)
endif
PLATFORM := $(GCIA)
$(call PRINTVAR, PLATFORM)

# check that OSTYPE+ARCH matches PLATFORM
PLATFORMDETECT := $(PLATFORMDETECT)x
$(call PRINTVAR, PLATFORMDETECT)
ifneq ($(PLATFORM),$(PLATFORMDETECT))
  $(warning Detected platform $(PLATFORMDETECT) (from OSTYPE=$(OSTYPE), ARCH=$(ARCH)) does not match PLATFORM=$(PLATFORM))
endif
CIACODE := $(CIACODE)X

SUBSYSCIA = FR

MORELIBS +=
OBJDIR    = .

CFLAGS   += -D$(MNEMONIC) -DCIA_$(CIACODE) -DSUB_$(SUBSYSCIA)

# decide compiler
ifeq ($(BUILDCODE),dac)
  HOSTTYPE  = unix
  CCOMP    ?= CLANG
  CXXCOMP  ?= CLANGXX
  LD          = clang
  LDFLAGS    += -Wl,-rpath,@executable_path/.
  CFLAGS     += -O
  CFLAGS     += -Wall -Werror-implicit-function-declaration -Wreturn-type
  CFLAGS     += -Wmissing-prototypes -Wmissing-declarations
  CFLAGS     += -DFNAME_LCASE_DECOR
  CFLAGS     += -fPIC
  CFLAGS     += -fvisibility=hidden
  SHLIBFLAGS  = -dynamiclib -shared
  SHLIBFLAGS += -install_name @rpath/$(LIBNAME) -Wl,-rpath,@loader_path/.
  SHLIBFLAGS += -headerpad_max_install_names
  SHLIBFLAGS += -undefined dynamic_lookup
  MORELIBS   += -lm -ldl
  OBJEXT    = o
  SHLIBEXT  = dylib
  EXEEXT    =
else ifeq ($(BUILDCODE),deg)
  HOSTTYPE  = unix
  CCOMP    ?= GCC
  CXXCOMP  ?= GXX
  CFLAGS   += -O
  CFLAGS   += -Wall -Werror-implicit-function-declaration -Wreturn-type
  CFLAGS   += -Wmissing-prototypes -Wmissing-declarations
  LD        = gcc
  LDFLAGS  += -Wl,-rpath,@executable_path/.
  SHLIBFLAGS  = -dynamiclib -shared
  SHLIBFLAGS += -install_name @rpath/$(LIBNAME) -Wl,-rpath,@loader_path/.
  SHLIBFLAGS += -headerpad_max_install_names
  SHLIBFLAGS += -undefined dynamic_lookup
  MORELIBS   += -lm -ldl
  OBJEXT      = o
  SHLIBEXT    = dylib
  EXEEXT      =
else ifeq ($(BUILDCODE),leg)
  HOSTTYPE  = unix
  CCOMP    ?= GCC
  CXXCOMP  ?= GXX
  CFLAGS   += -O -Wall
  CFLAGS   += -Werror-implicit-function-declaration -Wreturn-type
  CFLAGS   += -Wmissing-prototypes -Wmissing-declarations
  CFLAGS   += -DFNAME_LCASE_DECOR
  CFLAGS   += -fPIC
  CFLAGS   += -fvisibility=hidden
  LD        = gcc -pthread
  LDFLAGS  += -Wl,-rpath,\$$ORIGIN
  SHLIBFLAGS += -nostartfiles -shared -Wl,-Bsymbolic -pthread $(ADDSHLIBFLAGS)
  SHLIBFLAGS += -Wl,-rpath,\$$ORIGIN
  MORELIBS   += -lm -ldl
# to define which glibc functions we expect
  CFLAGS     += -D_XOPEN_SOURCE=700
  OBJEXT      = o
  SHLIBEXT    = so
  EXEEXT      =
else ifeq ($(BUILDCODE),wei)
  HOSTTYPE  = windows
  CCOMP    ?= ICL
  CXXCOMP  ?= ICLXX
  CFLAGS   += -c -nologo -MD
  CFLAGS   += -DFNAME_UCASE_NODECOR -DF_CALLCONV=__cdecl -D_CRT_DISABLE_PERFCRIT_LOCKS
  CFLAGS   += -D_CRT_SECURE_NO_WARNINGS
  CFLAGS   += -W3
  CFLAGS   += -O3
  LD	    = link
  SHLIBFLAGS  = -LD -link -nodefaultlib:libc.lib
  OBJEXT      = obj
  SHLIBEXT    = dll
  EXEEXT      = .exe
endif

CFLAGS   += -DCLibUse

# define compiler executable
CC = $(subst GCC,gcc,$(subst CL,cl,$(subst CLANG,clang,$(subst ICL,icl,$(CCOMP)))))
CXX = $(subst GXX,g++,$(subst CLANGXX,clang++,$(subst CLXX,cl,$(subst ICLXX,icl,$(CXXCOMP)))))
$(call PRINTVAR, CC)
$(call PRINTVAR, CXX)

# set mnenomic to BUILDCODE upper case (still used in Delphi codes only)
MNEMONIC := $(shell echo $(BUILDCODE) | tr [a-z] [A-Z])
$(call PRINTVAR, MNENOMIC)

CC = $(subst GCC,gcc,$(subst CL,cl,$(subst CLANG,clang,$(subst ICL,icl,$(CCOMP)))))

SRC_DIR     := .
INCLUDE_DIR := ../include
OUTPUT_DIR  := ./wrptest

ifneq ($(JPATH),)
ifeq ($(OSTYPE),linux)
  JAVA_INCLUDE=$(dir $(realpath $(JPATH)/javac))../include
  JNI_IDIRS=-I"$(JAVA_INCLUDE)" -I"$(JAVA_INCLUDE)/linux"
else ifeq ($(OSTYPE),macos)
  # it's not so good that this ignores JPATH
  JAVA_INCLUDE=$(shell /usr/libexec/java_home)/include
  JNI_IDIRS=-I"$(JAVA_INCLUDE)" -I"$(JAVA_INCLUDE)/darwin"
else ifeq ($(OSTYPE),windows)
  JAVA_INCLUDE=$(JPATH)/../include
  JNI_IDIRS=-I"$(JAVA_INCLUDE)" -I"$(JAVA_INCLUDE)/win32"
endif
endif

.PHONY: all clean

ifeq ($(HOSTTYPE), unix)
all: $(OUTPUT_DIR) $(OUTPUT_DIR)/libc_wrpcclib64.$(SHLIBEXT) $(OUTPUT_DIR)/libc_wrpjni64.$(SHLIBEXT) $(OUTPUT_DIR)/wrpccctest java python
endif
ifeq ($(HOSTTYPE), windows)
all: $(OUTPUT_DIR) $(OUTPUT_DIR)/c_wrpcclib64.$(SHLIBEXT) $(OUTPUT_DIR)/c_wrpjni64.$(SHLIBEXT) $(OUTPUT_DIR)/wrpccctest$(EXEEXT) java python
endif

$(OUTPUT_DIR):
	mkdir -p $@

ifeq ($(HOSTTYPE), unix)
$(OUTPUT_DIR)/testercc.$(OBJEXT): $(SRC_DIR)/testercc.c | $(OUTPUT_DIR)
	cp $< $(OUTPUT_DIR)/testercc.c
	$(CC) -c $(CFLAGS) -I$(SRC_DIR) -I$(INCLUDE_DIR) -I$(OUTPUT_DIR) -o $@ $<

$(OUTPUT_DIR)/%cc.$(OBJEXT): $(OUTPUT_DIR)/%cc.c | $(OUTPUT_DIR)
	$(CC) -c $(CFLAGS) -I$(INCLUDE_DIR) -o $@ $<

$(OUTPUT_DIR)/%lib.$(OBJEXT): $(OUTPUT_DIR)/%lib.c | $(OUTPUT_DIR)
	$(CC) -c $(CFLAGS) -I$(SRC_DIR) -I$(INCLUDE_DIR) -I$(OUTPUT_DIR) -o $@ $<

$(OUTPUT_DIR)/%test.$(OBJEXT): $(SRC_DIR)/%test.c | $(OUTPUT_DIR)
	$(CC) -c $(CFLAGS) -I$(SRC_DIR) -I$(INCLUDE_DIR) -I$(OUTPUT_DIR) -o $@ $<

$(OUTPUT_DIR)/c_wrpjni.$(OBJEXT): $(OUTPUT_DIR)/c_wrpjni.c $(OUTPUT_DIR)/c_wrpcc.h | $(OUTPUT_DIR)
	$(CC) -c $(CFLAGS) -I$(INCLUDE_DIR) $(JNI_IDIRS) -I$(OUTPUT_DIR) -o $@ $<

$(OUTPUT_DIR)/libc_wrpcclib64.$(SHLIBEXT): $(OUTPUT_DIR)/c_wrpcclib.$(OBJEXT) $(OUTPUT_DIR)/wrptest.$(OBJEXT) | $(OUTPUT_DIR)
	$(LD) -o $@ $(SHLIBFLAGS) $(LDFLAGS) $(OUTPUT_DIR)/c_wrpcclib.$(OBJEXT)  $(OUTPUT_DIR)/wrptest.$(OBJEXT) $(MORELIBS)

$(OUTPUT_DIR)/libc_wrpjni64.$(SHLIBEXT): $(OUTPUT_DIR)/c_wrpjni.$(OBJEXT) $(OUTPUT_DIR)/c_wrpcc.$(OBJEXT)  | $(OUTPUT_DIR)
	$(LD) -o $@ $(SHLIBFLAGS) $(LDFLAGS) $(OUTPUT_DIR)/c_wrpjni.$(OBJEXT)  $(OUTPUT_DIR)/c_wrpcc.$(OBJEXT)  $(MORELIBS)

$(OUTPUT_DIR)/wrpccctest$(EXEEXT): $(OUTPUT_DIR)/testercc.$(OBJEXT) $(OUTPUT_DIR)/c_wrpcc.$(OBJEXT)
	$(LD) -o $@ $(LDFLAGS) $(OUTPUT_DIR)/testercc.$(OBJEXT) $(OUTPUT_DIR)/c_wrpcc.$(OBJEXT) $(MORELIBS)

endif

ifeq ($(HOSTTYPE), windows)
$(OUTPUT_DIR)/testercc.$(OBJEXT): $(SRC_DIR)/testercc.c | $(OUTPUT_DIR)
	cp $< $(OUTPUT_DIR)/testercc.c
	$(CC) -Fo$@ $(CFLAGS) -DDLL -I$(SRC_DIR) -I$(INCLUDE_DIR) -I$(OUTPUT_DIR) $<

$(OUTPUT_DIR)/%cc.$(OBJEXT): $(OUTPUT_DIR)/%cc.c | $(OUTPUT_DIR)
	$(CC) -Fo$@ $(CFLAGS) -DDLL -I$(INCLUDE_DIR) $<

$(OUTPUT_DIR)/%lib.$(OBJEXT): $(OUTPUT_DIR)/%lib.c | $(OUTPUT_DIR)
	$(CC) -Fo$@ $(CFLAGS) -I$(SRC_DIR) -I$(INCLUDE_DIR) -I$(OUTPUT_DIR) $<

$(OUTPUT_DIR)/%test.$(OBJEXT): $(SRC_DIR)/%test.c | $(OUTPUT_DIR)
	$(CC) -Fo$@ $(CFLAGS) -I$(SRC_DIR) -I$(INCLUDE_DIR) -I$(OUTPUT_DIR) $<

$(OUTPUT_DIR)/c_wrpjni.$(OBJEXT): $(OUTPUT_DIR)/c_wrpjni.c $(OUTPUT_DIR)/c_wrpcc.h | $(OUTPUT_DIR)
	$(CC) -Fo$@ $(CFLAGS) -I$(INCLUDE_DIR) $(JNI_IDIRS) -I$(OUTPUT_DIR) $<

$(OUTPUT_DIR)/c_wrpcclib64.$(SHLIBEXT): $(OUTPUT_DIR)/c_wrpcclib.$(OBJEXT) $(OUTPUT_DIR)/wrptest.$(OBJEXT) | $(OUTPUT_DIR)
	$(LD) -out:$@ $(LDFLAGS) -dll $(OUTPUT_DIR)/c_wrpcclib.$(OBJEXT) $(OUTPUT_DIR)/wrptest.$(OBJEXT)

$(OUTPUT_DIR)/c_wrpjni64.$(SHLIBEXT): $(OUTPUT_DIR)/c_wrpjni.$(OBJEXT) $(OUTPUT_DIR)/c_wrpcc.$(OBJEXT)  | $(OUTPUT_DIR)
	$(LD) -out:$@ $(LDFLAGS) -dll $(OUTPUT_DIR)/c_wrpjni.$(OBJEXT) $(OUTPUT_DIR)/c_wrpcc.$(OBJEXT)

$(OUTPUT_DIR)/wrpccctest$(EXEEXT): $(OUTPUT_DIR)/testercc.$(OBJEXT) $(OUTPUT_DIR)/c_wrpcc.$(OBJEXT)
	$(LD) -out:$@ $(LDFLAGS) $(OUTPUT_DIR)/testercc.$(OBJEXT) $(OUTPUT_DIR)/c_wrpcc.$(OBJEXT)
endif

$(OUTPUT_DIR)/com/gams/api:
	mkdir -p $@
	cp $(INCLUDE_DIR)/gamsglobals.java $(OUTPUT_DIR)/com/gams/api
	cp $(OUTPUT_DIR)/c_wrp.java $(OUTPUT_DIR)/com/gams/api/

$(OUTPUT_DIR)/com/gams/tester:
	mkdir -p $@
	cp $(SRC_DIR)/testerjava*.java $(OUTPUT_DIR)/com/gams/tester

java: $(SRC_DIR)/*.java $(OUTPUT_DIR)/com/gams/api $(OUTPUT_DIR)/com/gams/tester
	$(JPATH)/javac -d $(OUTPUT_DIR) $(OUTPUT_DIR)/com/gams/api/*.java $(OUTPUT_DIR)/com/gams/tester/*.java

$(OUTPUT_DIR)/%: $(SRC_DIR)/%
	cp $< $@

$(OUTPUT_DIR)/%: $(INCLUDE_DIR)/%
	cp $< $@

python: $(OUTPUT_DIR)/_c_wrpcc.*
	cp $(SRC_DIR)/testerpy.py $(OUTPUT_DIR)/testerpy.py

$(OUTPUT_DIR)/_c_wrpcc.*: $(OUTPUT_DIR)/c_wrpcc.i $(OUTPUT_DIR)/c_wrpsetup.py $(OUTPUT_DIR)/c_wrpcc.c $(OUTPUT_DIR)/gclgms.h
	(cd $(OUTPUT_DIR) && \
	    sed "s/..\/..\/C\/api\///g" c_wrpsetup.py > c_wrpsetupx.py     && \
		swig -python c_wrpcc.i                                         && \
		sed -i -E "s/^.*import.*_c_wrpcc/import _c_wrpcc/g" c_wrpcc.py && \
		CC=$(CC) CFLAGS="$(CFLAGS) -DGC_NO_MUTEX $(IDIRS)" LDFLAGS="$(LDFLAGS)" LDSHARED="$(CC) $(SHLIBFLAGS)" python c_wrpsetupx.py build --build-lib . \
	)
#		CC=$(CC) CFLAGS="-DLEG -DCIA_LEX -O -Wall -DFNAME_LCASE_DECOR -fPIC -fvisibility=hidden -DGC_NO_MUTEX" LDSHARED="$(CC) -nostartfiles -shared -Wl,-Bsymbolic -pthread  -Wl,-rpath,\$ORIGIN" python c_wrpsetupx.py build --build-lib . \

clean:
	rm -rf $(OUTPUT_DIR)/com $(OUTPUT_DIR)/build
	rm -rf $(OUTPUT_DIR)/*.o $(OUTPUT_DIR)/*.obj
	rm -rf $(OUTPUT_DIR)/_c*.*
	rm -rf $(OUTPUT_DIR)/tester*.*
	rm -rf $(OUTPUT_DIR)/wrptest*.*
	rm -rf $(OUTPUT_DIR)/wrpccctest*
	rm -rf $(OUTPUT_DIR)/*wrpcclib64*.*
	rm -rf $(OUTPUT_DIR)/*wrpjni64*.*
