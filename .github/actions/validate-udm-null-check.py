import os
import re
import sys

def find_yara_files(directory):
    """Recursively find all .yara and .yar files in the directory."""
    yara_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.yara') or file.endswith('.yar'):
                yara_files.append(os.path.join(root, file))
    return yara_files

def check_udm_conditions(file_path):
    """Check UDM conditions in the file."""
    with open(file_path, 'r') as file:
        content = file.read()

    # Regex to find all UDM fields with '!='
    udm_fields = re.findall(r'\$[a-zA-Z0-9_]+\.[a-zA-Z0-9_.]+ != "[^"]+"', content)
    issues = []

    for field in udm_fields:
        base_field = field.split('!=')[0].strip()
        expected_check = f'{base_field} != ""'

        if expected_check not in content:
            issues.append(f"In file {file_path}, found UDM field '{field}' without a corresponding check for '{expected_check}'.")

    return issues

def main():
    base_dir = os.getenv('GITHUB_WORKSPACE', '.')  # Get the base directory from the environment or use the current directory
    rules_folder = os.path.join(base_dir, 'rules')  # Set the path to the 'rules' folder
    yara_files = find_yara_files(rules_folder)  # Find all .yara and .yar files in the 'rules' folder
    all_issues = []

    for yara_file in yara_files:
        issues = check_udm_conditions(yara_file)  # Check UDM conditions in each YARA file
        all_issues.extend(issues)

    if all_issues:
        for issue in all_issues:
            print(issue)
        sys.exit(1)  # Exit with status 1 if there are issues
    else:
        print("All UDM field checks passed.")  # Print success message if no issues

if __name__ == "__main__":
    main()
