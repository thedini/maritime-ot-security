 #!/usr/bin/env python3

# install gitpython, pypandoc

import sys
import os
import pypandoc
import pathlib
import git
from pathlib import Path

# enable user to create and input to a working directory
path = str(sys.argv[1])
destination  = str(sys.argv[2])
index_page = str(sys.argv[3])

# a list of file paths and names of files
files = []

# get commit SHA
repo = git.Repo(search_parent_directories=True)
sha = repo.head.object.hexsha
short_sha = repo.git.rev_parse(sha, short=7)

# creates list of files names that end in .md (filter out all .git and .py)
for filename in Path(path).rglob('*.md'):
    files.append(filename)
#print(files)

def make_index(file_names, destination):
    index = ""
    links = ""
    with open('templates/index.html', 'r') as index_reader:
        index = index_reader.read()
    for files in file_names:
        print(files)
        title = ""
        site = ""
        with open(destination + files, 'r') as reader:
            site = reader.read()
            site_heading = site[site.index("<h1"):site.index("</h1>")]
            title = site_heading[site_heading.index(">")+1:]
        with open(destination + files, 'w') as site_writer:
            site = '<html><head><title>{site_title}</title><link rel="stylesheet" href="style.css"><body><a href="index.html">Home</a>{site_data}</body></html>'.format(site_title=title, site_data=site)
            site=site.replace('–', '-').replace('“', '"').replace('”', '"')
#            print(site)
            site=site.replace('–', '-').replace('“', '"').replace('”', '"')
            site_writer.write(site)
        links += '<li><a href="{filename}">{stripped_filename}</a></li>'.format(filename=files, stripped_filename=title)
    index = index.replace("{{{LINKS}}}", links)
    index=index.replace('–', '-').replace('“', '"').replace('”', '"')
    with open(destination + "/index.html", 'w') as writer:
        writer.write(index)
    os.system("cp " + os.getcwd() +"/html/css/style.css {}".format(destination))
    return
# remove comments for pandoc to create pdf for handouts
def main():
    for file in files:
        powerpoint(file)
        beamer(file)
        handout(file)
        html(file)

def create_site():
    os.system('rm '+destination+'/*.html')
    important_filenames = []
    for file in files:
        newfile = html(file)
        if "class" in newfile or "lab" in newfile:
            important_filenames.append(newfile)
    important_filenames.sort()
    make_index(important_filenames, destination)

# powerpont function
def powerpoint(file):
    medium = "pptx"
    extension = medium
    newfile = file.with_suffix('')
    newfile = newfile.name
    print(f"{destination}/{newfile}_{short_sha}.{extension}")
    pypandoc.convert_file(os.fspath(file), medium, outputfile=f"{destination}/{newfile}_{short_sha}.{extension}")
    return

# pdf presentation function
def beamer(file):
    medium = "beamer"
    extension = "pdf"
    newfile = file.with_suffix('')
    newfile = newfile.name
    theme =  "AnnArbor"
    color = "crane"
    print(f"{destination}/{newfile}_{short_sha}.{extension}")
    pypandoc.convert_file(os.fspath(file), medium, outputfile=f"{destination}/{newfile}_{short_sha}.{extension}", extra_args=['-V', f'colortheme:{color}', '-V', 'urlcolor=cyan'])
    return

# pdf handout function
def old_handout(file):
    medium = "pdf"
    extension = medium
    newfile = file.with_suffix('')
    newfile = newfile.name
    # remove comments for handout
    infile = open(os.fspath(file),'r')
    data = infile.read()
    data = data.replace("<!--", "")
    data = data.replace("-->", "")
    print(f"{destination}/{newfile}_handout_{short_sha}.{extension}")
    pypandoc.convert_text(data, medium, format='md', outputfile=f"{destination}/{newfile}_handout_{short_sha}.{extension}", extra_args=['-V', 'urlcolor=cyan'])
    return

# pdf handout function
def handout(file):
    color = "2E3B86"
    text_color = "FFFFFF"
    medium = "pdf"
    extension = medium
    newfile = file.with_suffix('')
    newfile = newfile.name
    # remove comments for handout
    infile = open(os.fspath(file),'r')
    data = infile.read()
    data = data.replace("<!--", "")
    data = data.replace("-->", "")
    print(f"{destination}/{newfile}_handout_{short_sha}.{extension}")
    pypandoc.convert_text(data, medium, format='md', outputfile=f"{destination}/{newfile}_handout_{short_sha}.{extension}", extra_args=['-V', 'urlcolor=cyan', '--data-dir=.', '--template=eisvogel.latex', '--from=markdown+yaml_metadata_block+raw_html', '--table-of-contents', '--toc-depth=6', '--highlight-style=breezedark', '--number-sections'])
    return

# HTML handout function
def html(file):
    medium = "html"
    extension = medium
    newfile = file.with_suffix('')
    newfile = newfile.name
    filenames = []
    infile = open(os.fspath(file),'r')
    data = infile.read()
    data = data.replace("<!--", "")
    data = data.replace("-->", "")
    print(newfile)
    print(f"{destination}/{newfile}.{extension}")
    pypandoc.convert_text(data, medium, format='md', outputfile=f"{destination}/{newfile}.{extension}")

    return(newfile + ".html")

if __name__ == "__main__":
    if index_page == 'true':
        create_site()
    else:
        main()
