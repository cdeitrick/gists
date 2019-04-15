from pathlib import Path
from typing import Tuple
def get_sample_files(folder:Path)->Tuple[Path,Path]:

	forward = [i for i in folder.iterdir() if 'R1' in i.name][0]
	reverse = [i for i in folder.iterdir() if 'R2' in i.name][0]

	return forward, reverse

if __name__ == "__main__":
	folder = Path("/home/cld100/projects/lipuma/samples/")
	filename = folder / "lipuma_samples.tsv"
	with filename.open('w') as file1:
		for sample_folder in folder.iterdir():
			f, r = get_sample_files(sample_folder)
			sample_name = sample_folder.name.split('_')[0]
			file1.write(f"{sample_name}\t{f}\t{r}\n")


