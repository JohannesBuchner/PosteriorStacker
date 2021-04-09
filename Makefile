run:
	python3 tutorial/run.py && rst2html5.py README.rst > README.html

clean:
	rm -rf data.txt posteriorsamples.txt* README.html posteriors_x1.txt.gz 


.PHONY: clean run
