LATEX=rubber
FLAGS=--pdf
MAIN=thesis.tex

default:
	$(LATEX) $(FLAGS) $(MAIN)
