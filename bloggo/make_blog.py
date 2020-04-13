import os
import datetime
import glob
import markdown
import time
import shutil
import jinja2
import git

from config import templateEnv
from post import Post

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
posts = []

clean_output_dir()


def get_files_from_git():
    repo = git.Repo('..')
    files = {} 
    for blob in repo.tree().traverse():
        commit=next(repo.iter_commits(paths=blob.path))

        path = "." + blob.path[6:] if blob.path[:6] == 'bloggo' else blob.path
        files[path] = commit.committed_date

    return files

git_modified_times = get_files_from_git()

print(git_modified_times)
print(blogs)

print(f"Copying static files...")
static_files = glob.glob("./templates/*.css")

for static_file in static_files:
    filename = static_file.split("/")[-1]
    shutil.copyfile(static_file, './generated/' + filename)

for post_file in list(sorted(blogs, key=lambda x: -git_modified_times.get(x, 0))):
    if post_file in git_modified_times:
        modified = datetime.datetime.fromtimestamp(git_modified_times[post_file])
    else:
        modified = None

    post = Post(post_file, modified=modified)

    posts.append(post)

    blog_html.append(post.body_html)

    html_filename = "./generated/" + post.nice_filename + '.htm'
    print(f"Generating {html_filename}")
    with open(html_filename, 'w') as f:
        f.write(templateEnv.get_template('base.htm').render(title="Bloggo", content=post.get_html()))

print(f"Generating index.")

with open('./generated/index.htm', 'w') as f:
    content = templateEnv.get_template('list.htm').render(posts=[post.get_html() for post in posts])
    f.write(templateEnv.get_template('base.htm').render(title="Bloggo", content=content))

print("Done!")