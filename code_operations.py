import re
import git
import subprocess

_HEADER_RE = re.compile(
    r"""
    (?P<header>
        ^\s*
        (?:(?:public|protected|private|static|final|abstract|synchronized|
             native|strictfp|default|sealed|non-sealed)\s+)*
        (?:<[^>;{}()]*>\s*)?              # leading generics (e.g. <T>)
        [\w$<>\[\].?]+\s+                 # return type
        (?P<name>[A-Za-z_]\w*)\s*         # method name
        \(
            (?P<params>[^()]*)            # params blob (flat, heur.)
        \)
        \s*
        (?:throws\s+[\w$<>\[\].?,\s]+)?   # optional throws
    )
    \s*\{                                  # body starts
    """,
    re.VERBOSE | re.MULTILINE,
)

def _strip_comments(code: str) -> str:
    """Remove /* ... */ and // ... comments while preserving line breaks."""
    code = re.sub(r'/\*.*?\*/', lambda m: '\n' * m.group(0).count('\n'), code, flags=re.S)
    code = re.sub(r'//.*?$', '', code, flags=re.M)
    return code


def java_function_exists_by_name(function_name: str, java_file_content: str) -> bool:
    cleaned = _strip_comments(java_file_content)
    for m in _HEADER_RE.finditer(cleaned):
        if m.group('name') == function_name:
            return True
    return False

import git
import os

import os
import subprocess

import re

# def extract_added_code(diff_content, target_file):
#     # Initialize an empty list to store the added code blocks
#     added_code_blocks = []

#     # Flag to track when we are in the section of the diff for the target file
#     in_target_file_diff = False
    
#     # Split the diff content into lines
#     diff_lines = diff_content.splitlines()

#     # Loop through the diff content line by line
#     current_block = []
#     for line in diff_lines:
#         # Detect the beginning of the diff for the target file (it starts with '--- <file_name>')
#         if line.startswith(f'--- {target_file}'):
#             in_target_file_diff = True  # We are now in the diff for the specified file
#             continue  # Skip this line (just a header for the diff)

#         # If we're inside the diff for the target file, start processing the changes
#         if in_target_file_diff:
#             # End of the diff for the target file (starts with '+++ <file_name>')
#             if line.startswith(f'+++ {target_file}'):
#                 break  # Exit the diff section for the file

#             # Identify added lines (those starting with '+')
#             if line.startswith('+'):
#                 current_block.append(line[1:].strip())  # Remove the '+' and strip the line

#             # If we reach a line that isn't an added line, we complete the current block
#             elif current_block:
#                 added_code_blocks.append("\n".join(current_block))  # Add the block as a single string
#                 current_block = []  # Reset the current block

#     # If there was any remaining block (e.g., file ended with added lines)
#     if current_block:
#         added_code_blocks.append("\n".join(current_block))

#     return added_code_blocks


# def check_commit_for_code(repo_path, fragment, commit_sha):
#     # Ensure the provided path is a valid git repository
#     if not os.path.isdir(os.path.join(repo_path, '.git')):
#         raise ValueError(f"The provided path '{repo_path}' is not a valid git repository.")

#     local_path = fragment.file.replace('../../workspace/repo/', '')

#     # Git command to get the diff of the commit against its parent
#     cmd = f"git -C {repo_path} show {commit_sha}"

#     # Run the git show command and capture the diff output
#     diff_content = subprocess.check_output(cmd, shell=True, text=True)

#     added_code = extract_added_code(diff_content, fragment.file.split('/')[-1])

#     # Start and end lines from the fragment object
#     start_line = fragment.ls
#     end_line = fragment.le

#     # Fill here 

#     if all_added:
#         return "Code fully added"
#     elif part_added:
#         return "Part of the code was added"
#     else:
#         return "Code already existed"



import os
import subprocess

def extract_added_code(diff_content, target_file):
    # Initialize an empty list to store the added code blocks
    added_code_blocks = []

    # Flag to track when we are in the section of the diff for the target file
    in_target_file_diff = False
    
    # Remove the 'a/' and 'b/' prefixes from the file paths in the diff content
    target_file = target_file.replace('a/', '').replace('b/', '')

    # Split the diff content into lines
    diff_lines = diff_content.splitlines()

    # Loop through the diff content line by line
    current_block = []
    for line in diff_lines:
        # Detect the beginning of the diff for the target file (it starts with '--- a/<file_name>')
        if line.startswith(f'--- a/{target_file}') or line.startswith(f'+++ b/{target_file}'):
            in_target_file_diff = True  # We are now in the diff for the specified file
            continue  # Skip this line (just a header for the diff)

        # If we're inside the diff for the target file, start processing the changes
        if in_target_file_diff:
            # End of the diff for the target file (starts with '+++ <file_name>' or '--- <file_name>')
            if line.startswith('+++ ') or line.startswith('--- '):
                continue  # Skip this line (file path with a/ or b/ prefix)

            # Identify added lines (those starting with '+')
            if line.startswith('+'):
                current_block.append(line[1:].strip())  # Remove the '+' and strip the line

            # If we reach a line that isn't an added line, we complete the current block
            elif current_block:
                added_code_blocks.append("\n".join(current_block))  # Add the block as a single string
                current_block = []  # Reset the current block

    # If there was any remaining block (e.g., file ended with added lines)
    if current_block:
        added_code_blocks.append("\n".join(current_block))

    return added_code_blocks

def check_commit_for_code(repo_path, fragment, commit_sha):
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        raise ValueError(f"The provided path '{repo_path}' is not a valid git repository.")


    cmd = f"git -C {repo_path} show {commit_sha}"
    diff_content = subprocess.check_output(cmd, shell=True, text=True)

    added_code = extract_added_code(diff_content, fragment.file.replace('../../workspace/repo/', ''))

    start_line = fragment.ls
    end_line = fragment.le

    # Get the fragment lines from the local file (lines to compare with the diff)
    local_path = fragment.file.replace('../../', './')
    with open(local_path, 'r') as file:
        lines_in_file = file.readlines()[start_line - 1:end_line]  # 0-indexed

    fragment_lines = [line.strip() for line in lines_in_file]

    # Initialize flags for determining the state of the code
    all_added = all(line in "\n".join(added_code) for line in fragment_lines)
    part_added = any(line in "\n".join(added_code) for line in fragment_lines)

    # Return the result based on the flags
    if all_added:
        return "Code fully added"
    elif part_added:
        return "Part of the code was added"
    else:
        return "Code already existed"
