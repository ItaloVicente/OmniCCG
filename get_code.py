import os
import xml.etree.ElementTree as ET
import subprocess

# === CONFIGURATION ===
XML_FILE = "./grasscutter_production_results.xml"       # Path to your XML file
REPO_PATH = "./workspace/repo"                      # Path to your local git repository
OUTPUT_FILE = "clones_extracted_comparison.txt"     # Output file name
ONLY_WITH_ORIGIN_TYPE = True                        # <<< New flag added here

# Remove previous output if exists
os.system(f"rm -f {OUTPUT_FILE}")

def git_checkout(repo_path, commit_hash):
    """Checkout a specific commit in the repository."""
    print(f"[INFO] Checking out commit {commit_hash}")
    subprocess.run(["git", "-C", repo_path, "checkout", commit_hash],
                   check=True, capture_output=True)

def extract_code_segment(file_path, start_line, end_line):
    """Extracts the specified range of lines from a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return "".join(lines[start_line - 1:end_line])

def safe_extract(repo_path, commit_hash, src):
    """Safely checks out a commit and extracts code from the specified file."""
    rel_path = src.attrib["file"].replace("../../workspace/repo/", "")
    full_path = os.path.join(repo_path, rel_path)
    start_line = int(src.attrib["startline"])
    end_line = int(src.attrib["endline"])
    func_name = src.attrib.get("function", "unknown")

    try:
        git_checkout(repo_path, commit_hash)
        code = extract_code_segment(full_path, start_line, end_line)
    except Exception as e:
        code = f"[ERROR reading file at commit {commit_hash}: {e}]"

    return {
        "commit": commit_hash,
        "file": full_path,
        "function": func_name,
        "lines": f"{start_line}-{end_line}",
        "code": code
    }

def main():
    # Parse XML file
    tree = ET.parse(XML_FILE)
    root = tree.getroot()

    # Prepare output file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("### Extracted and Compared Code Segments ###\n\n")

    for lineage in root.findall("lineage"):
        for version in lineage.findall("version"):
            version_nr = version.attrib.get("nr")
            current_hash = version.attrib.get("hash")
            before_hash = version.attrib.get("before_hash")
            origin_type = version.attrib.get("origin_type")

            # === Conditional filter ===
            if ONLY_WITH_ORIGIN_TYPE and origin_type is None:
                print(f"[SKIP] Version {version_nr} skipped (no 'origin_type')")
                continue

            print(f"\n[PROCESSING] Version {version_nr} | Current: {current_hash} | Before: {before_hash} | Origin: {origin_type}")

            for cls in version.findall("class"):
                for src in cls.findall("source"):
                    # Extract current code
                    current_data = safe_extract(REPO_PATH, current_hash, src)

                    # Extract previous code (if available)
                    before_data = None
                    if before_hash:
                        before_data = safe_extract(REPO_PATH, before_hash, src)

                    # Write to output file
                    with open(OUTPUT_FILE, "a", encoding="utf-8") as out:
                        out.write(f"===== VERSION {version_nr} =====\n")
                        out.write(f"File: {current_data['file']}\n")
                        out.write(f"Function: {current_data['function']}\n")
                        out.write(f"Lines: {current_data['lines']}\n")
                        out.write(f"Origin Type: {origin_type}\n")
                        out.write("----------------------------------------\n")

                        if before_data:
                            out.write(f"--- BEFORE (commit {before_hash}) ---\n")
                            out.write(before_data['code'])
                            out.write("\n")

                        out.write(f"--- AFTER (commit {current_hash}) ---\n")
                        out.write(current_data['code'])
                        out.write("\n" + "="*80 + "\n\n")

    print(f"\n✅ Comparison complete! Output saved to '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    main()
