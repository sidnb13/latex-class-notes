import re
import os

txt_file = 'organic-advanced-notes.md'
title = 'Advanced Organic Chemistry Notes'
headings = ['Reactions of Alkenes', 'Substitution Reactions of Alkyl Halides', 'Elimination of Alkyl Halides']

def main():
    with open(txt_file, 'r') as f:
        lines = f.readlines()

        purified = []

        for line in lines:
            if re.match(r'\s+', line):
                pass
            elif not re.match(r'\s*[\*\!]', line):
                if line.strip == title:
                    pass
                elif line.strip() in headings:
                    line = '# ' + line.strip()
                else:
                    line = '## ' + line.strip()
            elif '!' in line:
                match = re.findall(r'image\d+', line)
                line = line.replace(match[0], match[0] + '.png') + '\n'
            purified.append(line)

    
        
    with open('converted.md', 'w') as w:
        w.writelines(purified)
    
    os.system('pandoc -s converted.md -o converted.pdf')

if __name__ == '__main__':
    main()