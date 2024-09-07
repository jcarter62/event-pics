import os
from dotenv import load_dotenv

load_dotenv()

class Loader:
    base_dir = ''
    files = []
    file_text = []

    def __init__(self):
        self.base_dir = os.getenv('PICTURE_PATH')
        self.files = self.load_files()
        self.file_text = self.load_text_files()

    def load_files(self):
        # Load all graphic files in the directory
        graphic_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
        file_list = []
        prev_file = ''
        next_file = ''
        for root, dirs, files in os.walk(self.base_dir):
            for file in files:
                if os.path.splitext(file)[1].lower() in graphic_extensions:
                    obj = {
                        'file': file,
                        'prev_file': '',
                        'next_file': ''
                    }
                    file_list.append(obj)

        # sort the file_list alphabetically
        file_list = sorted(file_list, key=lambda d: d['file'])
        # fill in the prev_file and next_file values
        for i in range(len(file_list)):
            prev_file = file_list[i - 1]['file'] if i > 0 else ''
            next_file = file_list[i + 1]['file'] if i < len(file_list) - 1 else ''
            file_list[i]['prev_file'] = prev_file
            file_list[i]['next_file'] = next_file

        return file_list

    def load_text_files(self):
        # for each graphic file, load the corresponding text file if it exists.
        # the text file should have the same name as the graphic file, but with a .txt extension
        text_files = {}
        for file in self.files:
            text_file = os.path.splitext(file['file'])[0] + '.txt'
            fullpath = os.path.join(self.base_dir, text_file)
            try:
                if os.path.exists(fullpath):
                    with open(fullpath, 'r') as f:
                        text_files[file['file']] = f.read()
            except Exception as e:
                print(f'Error reading {text_file}: {e}')
        return text_files

    def get_files(self):
        return self.files

    def get_file_info(self, filename):
        for file in self.files:
            if file['file'] == filename:
                return file
        return None

    def delete_file(self,filename):
        for i, file in enumerate(self.files):
            if file['file'] == filename:
                fullpath = os.path.join(self.base_dir, filename)
                try:
                    os.remove(fullpath)
                except Exception as e:
                    print(f'Error deleting {fullpath}: {e}')
                del self.files[i]
                break
        return

    def new_file(self, filename, filedata):
        # create a new file with the given filename
        fullpath = os.path.join(self.base_dir, filename)
        try:
            with open(fullpath, 'w') as f:
                f.write(filedata)
        except Exception as e:
            print(f'Error writing {fullpath}: {e}')
        return

