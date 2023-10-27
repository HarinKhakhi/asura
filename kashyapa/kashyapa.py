import sys
import os
import random

ASURAS_FILE = './asuras.txt'

class Operation:
    def compile(line):
        pass

    def syntax(line):
        pass


class SayOperation(Operation):
    def compile(line):
        line = line.strip()
        string = line.split(' ', 1)[1]
        return f'''
from gtts import gTTS
import os
import playsound
tts = gTTS(text="{string}", lang='en')
filename = "abc.mp3"
tts.save(filename)
playsound.playsound(filename)
os.remove(filename)
'''

    def syntax(line):
        return "say your string here"

class ScremeOperation(Operation):
    def compile(line):
        return "compiled " + line

    def syntax(line):
        return "scream type"


class OpenOperation(Operation):
    def compile(line):
        app_name = line.split(' ')[1]
        return f"os.system('open /Applications/{app_name}.app')"

    def syntax(line):
        return "open app-name" 

class Kashyapa:
    operations = {
        'say': SayOperation,
        'scream': ScremeOperation,
        'open': OpenOperation
    }

    allowed_operations = operations.keys()

    def check_asura(self, asura_file):
        # open the asura file
        with open(sys.argv[1], 'r') as asura_file:
            # check the file line by line
            lines = asura_file.readlines()
            for line in lines:
                if not self.check_line(line):
                    return False

        # file is good if reached here
        return True


    def check_line(self, line):
        # removing extra spaces at begin / end, and \n char
        line = line.strip() 
        # empty line
        if line == '': return True

        # check if operation is supported in current version
        operation = self.get_operation(line)
        return operation in self.allowed_operations
    

    def get_operation(self, line):
        # finding operation
        operation = ''
        for char in line:
            if char == ' ':
                break
            operation += char
        return operation


    def find_dir(self):
        home_path = os.path.expanduser('~')
        curr_dir = home_path

        MAX_DEPTH = 10
        # choose random dir untill we can't
        while MAX_DEPTH != 0:
            writable_dirs = []
    
            # list all directories in current dir
            for dir in os.listdir(curr_dir):
                dir_path = os.path.join(curr_dir, dir)

                # check if directory and have write access 
                if os.path.isdir(dir_path) and os.access(dir_path, os.W_OK) and os.access(dir_path, os.R_OK):
                    writable_dirs.append(dir_path)

            # check if we have reached out limit
            if len(writable_dirs) == 0: return curr_dir

            # pick random dir
            curr_dir = random.choice(writable_dirs)

            MAX_DEPTH -= 1
        
        return curr_dir


    def compile(self, asura_file):
        compiled_lines = []
        # compile the asura_file line by line
        with open(sys.argv[1], 'r') as file:
            lines = file.readlines() 
            for line in lines:
                operation = self.get_operation(line)
                compiled = self.operations[operation].compile(line)
                compiled_lines.append(compiled)
        
        # find home for asura
        asura_home = self.find_dir()
        compiled_asura_file = os.path.join(asura_home, 'asura.py')
        with open(compiled_asura_file, 'w') as file:
            file.writelines(compiled_lines)

        with open(ASURAS_FILE, 'a+') as asuras_list:
            asuras_list.write(f'{os.path.abspath(asura_file)} {os.path.abspath(compiled_asura_file)} \n')


    def run(self, asura_name):
        with open(ASURAS_FILE, 'r') as asuras_list:
            asuras = asuras_list.readlines()
            for asura in asuras:
                asura = asura.strip()
                name, path = asura.split(' ', 1)
                if name.split('/')[-1] == asura_name:
                    os.system(f'python "{path}"')
                    break

    
    def die(self):
        with open(ASURAS_FILE, 'r') as asuras_list:
            asuras = asuras_list.readlines()
            for asura in asuras:
                asura = asura.strip()
                name, path = asura.split(' ', 1)
                os.system(f'rm "{path}"')

if len(sys.argv) != 2:
    print('how dare you call me without asura!')
    exit(0)

kashyapa = Kashyapa()
asura_file = sys.argv[1]

# check asura syntax
if not kashyapa.check_asura(asura_file):
    print('you asura is not following my rules!')
    exit(0)

# compile asura
kashyapa.compile(asura_file)
kashyapa.run('test.asura')
kashyapa.die()