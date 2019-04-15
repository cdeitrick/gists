from pathlib import Path
from toolz import itertoolz

import subprocess
if __name__ == "__main__":
	fastq_folder = Path("/media/cld100/FA86364B863608A1/Users/cld100/Storage/riptide/fastqs")
	key = lambda s: "-".join(s.name.split('-')[:2])
	samples = itertoolz.groupby(key, fastq_folder.iterdir())

	for sample_name, filenames in samples.items():
		output_folder = fastq_folder.parent / "fastqc" / sample_name
		if not output_folder.exists():
			output_folder.mkdir()

		command = ["/home/cld100/applications/FastQC/fastqc", "--outdir", output_folder] + filenames
		print(sample_name)
		subprocess.run(command)
