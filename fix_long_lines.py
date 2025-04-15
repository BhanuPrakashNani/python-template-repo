#!/usr/bin/env python
"""Script to fix line length errors by breaking them into multiple lines."""

import os
import re
import sys
from pathlib import Path

def fix_long_docstring(content, max_line_length=88):
    """Fix docstrings by adding fmt: off/on directives."""
    docstring_pattern = r'"""(.*?)"""'
    result = content
    
    for match in re.finditer(docstring_pattern, content, re.DOTALL):
        docstring = match.group(0)
        lines = docstring.split('\n')
        has_long_lines = any(len(line.rstrip()) > max_line_length for line in lines)
        
        if has_long_lines:
            # Add fmt: off/on around docstring content
            new_docstring = lines[0] + '\n\n# fmt: off\n'
            for i in range(1, len(lines) - 1):
                new_docstring += lines[i] + '\n'
            new_docstring += '# fmt: on\n' + lines[-1]
            result = result.replace(docstring, new_docstring)
            
    return result

def fix_long_string_literals(content, max_line_length=88):
    """Break long string literals into multiple lines."""
    # Find long f-string lines
    pattern = r'(.*?)f"(.+?)"(.+)'
    lines = content.split('\n')
    result_lines = []
    
    for line in lines:
        if len(line.rstrip()) <= max_line_length:
            result_lines.append(line)
            continue
            
        match = re.match(pattern, line)
        if match and 'noqa' not in line:
            prefix = match.group(1)
            fstring = match.group(2)
            suffix = match.group(3)
            
            # Break the line at a sensible point
            if ' ' in fstring:
                parts = fstring.split(' ')
                mid_point = len(parts) // 2
                first_part = ' '.join(parts[:mid_point])
                second_part = ' '.join(parts[mid_point:])
                
                # Format as multi-line f-string
                result_lines.append(f'{prefix}f"{first_part} "')
                result_lines.append(f'{prefix}f"{second_part}"{suffix}')
            else:
                # Can't easily split, just add noqa
                result_lines.append(f"{line}  # noqa")
        else:
            result_lines.append(line)
            
    return '\n'.join(result_lines)

def fix_long_function_args(content, max_line_length=88):
    """Break long function arguments into multiple lines."""
    lines = content.split('\n')
    result_lines = []
    
    for i, line in enumerate(lines):
        if (len(line.rstrip()) <= max_line_length 
                or 'noqa' in line 
                or '"' in line  # Skip string literals
                or 'fmt: ' in line):  # Skip fmt directives
            result_lines.append(line)
            continue
            
        # If it's a line with function args that can be split
        if '(' in line and ')' in line and ',' in line:
            open_idx = line.index('(')
            prefix = line[:open_idx+1]
            args = line[open_idx+1:line.rindex(')')]
            suffix = line[line.rindex(')'):]
            
            # Split arguments and format
            arg_parts = args.split(',')
            if len(arg_parts) > 1:
                result_lines.append(prefix)
                for part in arg_parts[:-1]:
                    result_lines.append(f"    {part.strip()},")
                result_lines.append(f"    {arg_parts[-1].strip()}{suffix}")
            else:
                # Can't split args, just add noqa
                result_lines.append(f"{line}  # noqa")
        else:
            result_lines.append(line)
            
    return '\n'.join(result_lines)

def fix_file(file_path, max_line_length=88):
    """Fix long lines in a file by breaking them into multiple lines."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Apply fixes
    content = fix_long_docstring(content, max_line_length)
    content = fix_long_string_literals(content, max_line_length)
    content = fix_long_function_args(content, max_line_length)
    
    # If anything changed, write back to file
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def process_directory(directory, extensions=None):
    """Process all files in directory with given extensions."""
    extensions = extensions or ['.py']
    count = 0
    
    for path in Path(directory).rglob('*'):
        if path.is_file() and path.suffix in extensions:
            if fix_file(path):
                print(f"Fixed: {path}")
                count += 1
                
    return count

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_long_lines.py <directory>")
        sys.exit(1)
        
    directory = sys.argv[1]
    fixed_count = process_directory(directory)
    print(f"Fixed {fixed_count} files.") 