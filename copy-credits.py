# Open the Python file
with open('run.py', 'r') as python_file:
    # Read the file line by line
    lines = python_file.read().splitlines()

# Initialize an empty list to hold the credit lines
credit_lines = []
credit_lines.append("All the Credits and hyperlinks can be found in the [run.py](run.py) file on the indicated lines.\n\n"
                    "Note that this list of credits is automatically generated from the run.py file using the [copy-credits.py](copy-credits.py) script.\n"
                    "The script was written by me, with much help from the Microsoft Edge Copilot.\n")
# Iterate over the lines with an index
for i in range(len(lines)):
    # If a line starts with "# Credit", add it and the next line to the list
    if lines[i].strip().startswith('# Credit'):
        credit_line = f"- Line: {i+1}: [{lines[i].strip().replace(":", "")[2:]}]"  # Add the line number and remove the "#"
        if i+1 < len(lines):  # Check if there is a next line
            next_line = lines[i+1].strip()
            if next_line.startswith('#'):
                next_line = next_line[2:]  # Remove the "#" from the start of the second line
            credit_line += f"({next_line})" # Add the next line
            credit_lines.append(credit_line)
            credit_lines.append("")


# Open the README file
with open('README.md', 'r') as readme_file:
    # Read the file line by line
    readme_lines = readme_file.read().splitlines()

# Find the index of the line with the "### Content" title
credits_index = next(i for i, line in enumerate(readme_lines) if '### Content' in line)

# Find the index of the line with the "### Media" title
acknowledgements_index = next(i for i, line in enumerate(readme_lines) if '### Media' in line)

# Replace the lines between these two indices with the new content
updated_content = readme_lines[:credits_index+1] + credit_lines + readme_lines[acknowledgements_index:]

# Write the updated content back to the README file
with open('README.md', 'w') as readme_file:
    readme_file.write('\n'.join(updated_content))

print("Credit lines written to README file.")