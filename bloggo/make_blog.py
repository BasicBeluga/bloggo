import os
import glob
import markdown
import time
import shutil
import jinja2

def clean_output_dir():
    output_dir = "./generated/"
    output_files = output_dir + "*"

    is_dir = len(glob.glob(output_dir)) > 0
    
    if not is_dir:
        os.mkdir(output_dir)
    
    files_to_remove = glob.glob(output_files)
    for ftr in files_to_remove:
        os.remove(ftr)

blogs = glob.glob("./blogs/*.md")
blog_html = []

clean_output_dir()

templateLoader = jinja2.FileSystemLoader(searchpath="./templates/")
templateEnv = jinja2.Environment(loader=templateLoader)


print(f"Copying static files...")
static_files = glob.glob("./templates/*.css")
for static_file in static_files:
    filename = static_file.split("/")[-1]
    shutil.copyfile(static_file, './generated/' + filename)


for blog in list(sorted(blogs, key=lambda x: os.path.getctime(x))):
    filename = '/'.join(blog.split("/")[2:]).split('.')[0]
    created_d = time.ctime(os.path.getctime(blog))
    modified_d = time.ctime(os.path.getmtime(blog))

    with open(blog, 'r') as f:
        html = markdown.markdown(f.read())

    blog_html.append(html)

    html_filename = "./generated/" + filename + '.htm'
    print(f"Generating {html_filename}")
    with open(html_filename, 'w') as f:
        # f.write(html)
        f.write(templateEnv.get_template('base.htm').render(title="text", content=html))

print(f"Generating index.")

with open('./generated/index.htm', 'w') as f:
    for html in blog_html:
        f.write(html)
        f.write("<hr>")

print("Done!")