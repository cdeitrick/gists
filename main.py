from pathlib import Path
from typing import List
import pandas
import sys
github_folder = Path.home() / "Documents/github/"
sys.path.append(str(github_folder))



def get_nullarbor_status() -> List[Path]:
	nullarbor_folder = "/media/cld100/FA86364B863608A1/Users/cld100/Storage/projects/lipuma/nullarbor_output/"
	nullarbor_folder = Path(nullarbor_folder)

	nullarbor_files = [i.name.split('_')[0] for i in nullarbor_folder.iterdir() if '_' in i.name]
	return nullarbor_files


def get_image_status() -> List[Path]:
	folder = Path("/home/cld100/Documents/projects/lipuma/images/")
	images = [i.name for i in folder.iterdir()]
	return images

def get_breseq_status():
	folder = Path("/media/cld100/FA86364B863608A1/Users/cld100/Storage/projects/lipuma/pipeline_output/")
	files = list()
	for filename in folder.iterdir():
		if not filename.is_dir(): continue
		index_filename = filename / "breseq_output" / "output" / "index.html"
		if index_filename.exists():
			files.append(filename.name)
	return files

def get_estimated_fold_coverage_fastq():
	sequence_folder = Path("/home/cld100/Documents/projects/lipuma/sequences/")

	from sequence_delivery_workflow import filestats
	for filename in sequence_folder.iterdir():
		if not filename.is_dir(): continue
		try:
			fnames = [i for i in filename.iterdir()]
			left = [i for i in fnames if 'R1' in i.name][0]
			right = [i for i in fnames if 'R2' in i.name][0]
			cov = filestats.calculate_paired_coverage(left, right, 7702840)
		except IndexError:
			cov = "N/A"
		print(f"{filename.name}\t{cov}")
def get_estimated_fold_coverage_bam():
	from sequence_delivery_workflow import filestats
	folder = Path("/media/cld100/FA86364B863608A1/Users/cld100/Storage/projects/lipuma/nullarbor_output/")
	for sample_folder in folder.iterdir():
		expected_bam = sample_folder / sample_folder.name / "snps.bam"
		if not expected_bam.exists(): continue
		coverage = filestats.calculate_coverage_bam(expected_bam)
		print(sample_folder.name.split('_')[0], "\t", coverage)
if __name__ == "__main__":
	nullarbor = get_nullarbor_status()
	images = get_image_status()
	breseq = get_breseq_status()
	print(nullarbor)
	filename = Path("/home/cld100/Documents/projects/lipuma/genome_coverage.xlsx")
	table = pandas.read_excel(filename, sheetname = "bamCoverageHI2424")
	print(table.columns)
	table = table.set_index("sample")
	table["breseqStatus"] = [s in breseq for s in table.index]
	table["nullarborStatus"] = [s in nullarbor for s in table.index]
	table["imageStatus"] = [s in images for s in table.index]

	merged_table = pandas.read_excel("/home/cld100/Documents/projects/lipuma/LiPuma-PHDC/merged_table.xlsx")

	merged_table = merged_table.set_index('RepositoryNumber')
	subset = merged_table[["group #", "Category"]]

	table = table.join(subset)
	table['group #'] = table['group #'].astype(str)
	table = table.sort_values(by = 'group #')
	table.to_csv(filename.with_name("sample_status.tsv"), sep = "\t")
	print(table.to_string())
