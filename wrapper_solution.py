import os
import xml.etree.ElementTree as ET
import subprocess

os.system('rm -rf diff')

def main():
	xml_path = "results/production_results.xml"
	production_dir = os.path.join("workspace", "repo")
	diff_dir = "diff"

	# Parse XML
	tree = ET.parse(xml_path)
	root = tree.getroot()

	# Collect all unique version hashes
	hashes = set()
	for lineage in root.findall(".//lineage"):
		for version in lineage.findall("version"):
			hash_val = version.get("hash")
			if hash_val:
				hashes.add(hash_val)

	# Create diff directory if it doesn't exist
	os.makedirs(diff_dir, exist_ok=True)

	# For each hash, checkout and get diff
	prod_abs = os.path.abspath(production_dir)
	for h in hashes:
		# Change to repo dir, checkout, get diff
		cwd = os.getcwd()
		os.chdir(prod_abs)
		subprocess.run(["git", "checkout", h], check=True)
		diff = subprocess.run(["git", "diff", f"{h}^!"], capture_output=True, text=True, check=True)
		os.chdir(cwd)
		# Write diff to diff/<hash>.diff
		diff_filename = os.path.join(diff_dir, f"{h}.diff")
		with open(diff_filename, "w") as f:
			f.write(diff.stdout)

if __name__ == "__main__":
	main()