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

def get_changed_files(branch: str) -> list[str]:
    # git diff master..develop
    result = subprocess.run(
        ["git", "diff", "--name-only", f"master..{branch}"],
        stdout=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip().splitlines()

def get_diff(file_path: str, branch: str) -> str:
    # Corrected the git diff command to specify the branch and get differences
    result = subprocess.run(
        ["git", "diff", f"master..{branch}"],
        stdout=subprocess.PIPE,
        text=True,
    )
    return result.stdout

def main():
    branch = "develop"  # برنچ مورد نظر رو وارد کن
    files = get_changed_files(branch)
    print(f"تغییرات فایل‌ها در برنچ {branch}:")
    for file in files:
        print(f"- {file}")
    
    print("\nساختار پروژه:")
    structure = get_project_structure(".")
    # print(structure)

    for file in files:
        print(f"\nبررسی تغییرات فایل: {file}")
        diff_content = get_diff(file, branch)
        with open("changes.txt", "w") as f:
            f.write(diff_content)
        # print(f"\nتغییرات فایل {file} در برنچ {branch}:\n{diff_content}")
        
        print(f"\nکدهای تابع/کلاس مورد نیاز برای بررسی بیشتر:\n")

if __name__ == "__main__":
    main()
