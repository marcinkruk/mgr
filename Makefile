LATEX=latexmk
LFLAGS=-pdf
LWATCH=-pvc

all: thesis.pdf

thesis.pdf: thesis.tex
	$(LATEX) $(LFLAGS) thesis.tex

.PHONY: watch
watch: thesis.tex
	$(LATEX) $(LFLAGS) $(LWATCH) thesis.tex

clean:
	$(LATEX) -c thesis.tex
