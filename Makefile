run:
	python3 tutorial/run.py && rst2html5.py README.rst > README.html

clean:
	rm -rf data.txt posteriorsamples.txt* README.html posteriors_x1.txt.gz 


flatdist.txt.gz: Makefile
	#python3 -c 'import numpy; numpy.savetxt("flatdist.txt.gz", numpy.random.normal(3.14,0.1,size=(30,100)))'
	python3 -c 'import numpy; numpy.savetxt("flatdist.txt.gz", numpy.vstack((numpy.random.normal(3.14,0.1,size=(30,4000)), numpy.random.uniform(-10, 10, size=(1000,4000)))))'

flatdist.txt.gz_out_gauss/plots/corner.pdf: flatdist.txt.gz
	python3 posteriorstacker.py flatdist.txt.gz 2.5 4 8

show: flatdist.txt.gz_out_gauss/plots/corner.pdf
	xdg-open $^

.PHONY: clean run show
.SECONDARY:
