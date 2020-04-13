import markdown
import time
import os
import jinja2
from config import templateEnv


class Post():
    def __init__(self, filename, created=None, modified=None):
        with open(filename, 'r') as f:
            self.body_html = markdown.markdown(f.read())

        self.nice_filename = '/'.join(filename.split("/")[2:]).split('.')[0]

        if created:
            self.created = created
        else:
            self.created = time.ctime(os.path.getctime(filename))
        
        if modified:
            self.modified = modified
        else:
            self.modified = time.ctime(os.path.getmtime(filename))


    def get_html(self):
        return templateEnv.get_template('post.htm').render(post=self)