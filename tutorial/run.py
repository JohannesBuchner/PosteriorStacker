import subprocess
import sys

with open("README.rst", "w") as fout:

	for line in open("README.rst.template"):
		if line.startswith("\t$"):
			# why, yes this is not secure
			print("running", line[2:])
			fout.write(line)
			with subprocess.Popen(
					line[2:], shell=True, universal_newlines=True,
					stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
				for line in p.stdout:
					if "%" in line:
						continue
					fout.write("\t" + line)
		else:
			fout.write(line)
