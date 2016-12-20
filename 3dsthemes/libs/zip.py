import zipfile
from io import BytesIO
class InMemoryZip(object):
    def __init__(self):
        self.in_memory_zip = BytesIO()
    
    def append(self, filename_in_zip, file_contents):
        zf = zipfile.ZipFile(self.in_memory_zip, "a", zipfile.ZIP_DEFLATED, False)
        zf.writestr(filename_in_zip, file_contents)
        for zfile in zf.filelist:
            zfile.create_system = 0
        return self
    def read(self):
        return self.in_memory_zip.getvalue()
        
import os.path
def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        for member in zf.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            words = member.filename.split('/')
            path = dest_dir
            for word in words[:-1]:
                while True:
                    drive, word = os.path.splitdrive(word)
                    head, word = os.path.split(word)
                    if not drive:
                        break
                if word in (os.curdir, os.pardir, ''):
                    continue
                path = os.path.join(path, word)
            zf.extract(member, path)
