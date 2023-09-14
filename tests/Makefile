SRC_DIR     := .
INCLUDE_DIR := ../include
OUTPUT_DIR  := ./wrptest

.PHONY: all clean

all: $(OUTPUT_DIR) $(OUTPUT_DIR)/libc_wrpcclib64.so $(OUTPUT_DIR)/libc_wrpjni64.so $(OUTPUT_DIR)/wrpccctest java python

$(OUTPUT_DIR):
	mkdir -p $@

$(OUTPUT_DIR)/%lib.o: $(OUTPUT_DIR)/%lib.c | $(OUTPUT_DIR)
	gcc -c -DLEG -DCIA_LEX -DSUB_ -O -Wall -Werror-implicit-function-declaration -Wreturn-type -Wmissing-prototypes -Wmissing-declarations -DFNAME_LCASE_DECOR -fPIC -fvisibility=hidden -I$(SRC_DIR) -I$(INCLUDE_DIR) -I$(OUTPUT_DIR) -o $@ $<

$(OUTPUT_DIR)/%test.o: $(SRC_DIR)/%test.c | $(OUTPUT_DIR)
	gcc -c -DLEG -DCIA_LEX -DSUB_ -O -Wall -Werror-implicit-function-declaration -Wreturn-type -Wmissing-prototypes -Wmissing-declarations -DFNAME_LCASE_DECOR -fPIC -fvisibility=hidden -I$(SRC_DIR) -I$(INCLUDE_DIR) -I$(OUTPUT_DIR) -o $@ $<

$(OUTPUT_DIR)/libc_wrpcclib64.so: $(OUTPUT_DIR)/c_wrpcclib.o $(OUTPUT_DIR)/wrptest.o | $(OUTPUT_DIR)
	gcc -o $@ -nostartfiles -shared -Wl,-Bsymbolic -pthread  -Wl,-rpath,\$ORIGIN  $(OUTPUT_DIR)/c_wrpcclib.o  $(OUTPUT_DIR)/wrptest.o  -lm -ldl

$(OUTPUT_DIR)/%cc.o: $(OUTPUT_DIR)/%cc.c | $(OUTPUT_DIR)
	gcc -c -DCLibUse -fPIC -DLEG -DCIA_LEX -DSUB_FR -O -Wall -Werror-implicit-function-declaration -Wreturn-type -Wmissing-prototypes -Wmissing-declarations -I$(INCLUDE_DIR) -o $@ $<

$(OUTPUT_DIR)/c_wrpjni.o: $(OUTPUT_DIR)/c_wrpjni.c $(OUTPUT_DIR)/c_wrpcc.h | $(OUTPUT_DIR)
	gcc -c -fPIC -DLEG -DCIA_LEX -DSUB_ -O -Wall -Werror-implicit-function-declaration -Wreturn-type -Wmissing-prototypes -Wmissing-declarations -DFNAME_LCASE_DECOR -fPIC -fvisibility=hidden -I$(INCLUDE_DIR) -I"/usr/lib/jvm/java-11-openjdk/bin//../include" -I"/usr/lib/jvm/java-11-openjdk/bin//../include/linux" -I$(OUTPUT_DIR) -o $@ $<

$(OUTPUT_DIR)/libc_wrpjni64.so: $(OUTPUT_DIR)/c_wrpjni.o $(OUTPUT_DIR)/c_wrpcc.o  | $(OUTPUT_DIR)
	gcc -o $@ -nostartfiles -shared -Wl,-Bsymbolic -pthread  -Wl,-rpath,\$ORIGIN  $(OUTPUT_DIR)/c_wrpjni.o  $(OUTPUT_DIR)/c_wrpcc.o    -lm -ldl

$(OUTPUT_DIR)/testercc.o: $(SRC_DIR)/testercc.c | $(OUTPUT_DIR)
	cp $< $(OUTPUT_DIR)/testercc.c
	gcc -c -DCLibUse -fPIC -DLEG -DCIA_LEX -DSUB_FR -O -Wall -Werror-implicit-function-declaration -Wreturn-type -Wmissing-prototypes -Wmissing-declarations -I$(SRC_DIR) -I$(INCLUDE_DIR) -I$(OUTPUT_DIR) -o $@ $<

$(OUTPUT_DIR)/wrpccctest: $(OUTPUT_DIR)/testercc.o $(OUTPUT_DIR)/c_wrpcc.o
	gcc -pthread -o $@ -Wl,-rpath,\$ORIGIN $(OUTPUT_DIR)/testercc.o $(OUTPUT_DIR)/c_wrpcc.o -lm -ldl

$(OUTPUT_DIR)/com/gams/api:
	mkdir -p $@
	cp $(INCLUDE_DIR)/gamsglobals.java $(OUTPUT_DIR)/com/gams/api
	cp $(OUTPUT_DIR)/c_wrp.java $(OUTPUT_DIR)/com/gams/api/

$(OUTPUT_DIR)/com/gams/tester:
	mkdir -p $@
	cp $(SRC_DIR)/testerjava*.java $(OUTPUT_DIR)/com/gams/tester

java: $(SRC_DIR)/*.java $(OUTPUT_DIR)/com/gams/api $(OUTPUT_DIR)/com/gams/tester
	javac -d $(OUTPUT_DIR) $(OUTPUT_DIR)/com/gams/api/*.java $(OUTPUT_DIR)/com/gams/tester/*.java

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
		CC=gcc CFLAGS="-DLEG -DCIA_LEX -O -Wall -DFNAME_LCASE_DECOR -fPIC -fvisibility=hidden -DGC_NO_MUTEX" LDSHARED="gcc -nostartfiles -shared -Wl,-Bsymbolic -pthread  -Wl,-rpath,\$ORIGIN" python c_wrpsetupx.py build --build-lib . \
	)

clean:
	rm -rf $(OUTPUT_DIR)
