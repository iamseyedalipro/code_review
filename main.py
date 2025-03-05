import subprocess
import os

def is_ignored(file_path: str) -> bool:
    # Run `git check-ignore` to see if the file is ignored by Git
    result = subprocess.run(
        ["git", "check-ignore", "-q", file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.returncode == 0  # If the return code is 0, it means the file is ignored

def get_project_structure(root_dir: str) -> str:
    structure = ""
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Ignore directories that are ignored by Git
        if is_ignored(dirpath):
            continue
        
        depth = dirpath.replace(root_dir, "").count(os.sep)
        indent = "  " * depth
        structure += f"{indent}{os.path.basename(dirpath)}/\n"

        # Filter out ignored files
        filenames = [f for f in filenames if not is_ignored(os.path.join(dirpath, f))]

        for file in filenames:
            structure += f"{indent}  {file}\n"
    
    return structure

def get_changed_files(branch1: str, branch2: str) -> list[str]:
    # git diff between two branches
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{branch1}..{branch2}"],
        stdout=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip().splitlines()

def get_diff(file_path: str, branch1: str, branch2: str) -> str:
    # Corrected the git diff command to specify the branches and file path for differences
    result = subprocess.run(
        ["git", "diff", f"{branch1}..{branch2}", "--", file_path],
        stdout=subprocess.PIPE,
        text=True,
    )
    return result.stdout

def main():
    # Accept branch names for comparison
    branch1 = input("Enter the name of the first branch (e.g., master): ")
    branch2 = input("Enter the name of the second branch (e.g., develop): ")

    files = get_changed_files(branch1, branch2)
    structure = get_project_structure(".")

    with open("changes.txt", "w") as f:  # Open the file once for writing
        # Write the project structure first
        with open("prompt.txt", 'r') as file:
            prompt = file.read()
            f.write(prompt)
            f.write("--------------------\n")
        f.write("Project Structure:\n")
        f.write(structure)
        f.write("\n")  # Add a newline after the project structure

        # Write diffs for each changed file
        for file in files:
            # Add a header to distinguish changes for each file
            f.write(f"\n{'-'*40}\nChanges for {file}:\n{'-'*40}\n")
            diff_content = get_diff(file, branch1, branch2)
            f.write(diff_content)
            f.write("\n")  # Add a newline after each file's diff

if __name__ == "__main__":
    main()
