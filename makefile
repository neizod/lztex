main:
	./lztex.py manual.lazy
	pdflatex manual.tex
	rm manual.tex manual.aux manual.log manual.out

