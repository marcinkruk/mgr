all:
	latexmk -pdf

preview:
	latexmk -pdf -pvc

clean:
	latexmk -c
