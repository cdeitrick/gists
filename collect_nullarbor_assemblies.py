from pathlib import Path

def collect():
	nullarbor_folder = Path("/home/cld100/projects/lipuma/nullarbor_output/")
	output_folder = Path("/home/cld100/projects/lipuma/assemblies/")
	for sample_folder in nullarbor_folder.iterdir():
		if not sample_folder.is_dir(): continue
		sample_name = sample_folder.name.split('_')[0]

		assembly_file = sample_folder / "prokka" / f"{sample_folder.name}.fna"
		if assembly_file.exists():
			destination = output_folder / f"{sample_name}.fna"

			assembly_file.rename(destination)
def listfiles():
	assembly = Path("/home/cld100/projects/lipuma/assemblies/")
	output_filename = assembly / "ksnp_samplelist.tsv"
	with output_filename.open('w') as output:
		for filename in assembly.iterdir():
			if not filename.suffix == '.fna': continue
			line = f"{filename}\t{filename.stem}\n"
			output.write(line)
if __name__ == "__main__":
	listfiles()

