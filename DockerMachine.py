import subprocess
import os
from io import StringIO

class DockerMachine:
    name = ''
    env = []

    def __init__(self, name='hadoop'):
        self.name = name
        self.__start__()
        self.env = self.__getenv__()

    def __start__(self):
        subprocess.Popen("docker-machine start "+self.name)

    def getip(self):
        return os.popen("docker-machine ip "+self.name).read()[:-1]

    def __getenv__(self):
        proc = subprocess.Popen("docker-machine env "+self.name,shell=True, stdout=subprocess.PIPE)
        out, err = proc.communicate()
        return out.decode('utf-8').split('\n')[:4]

    def launch(self, command):
        command = StringIO('\n'.join(self.env+[command]+['exit']))
        stdout, stderr = subprocess.Popen('cmd.exe',stdin=subprocess.PIPE,stdout=subprocess.PIPE).\
        communicate(command.getvalue().encode())
        return stdout.decode('utf-8').split('\n')[-3][:12]

    def stop(self, container_id):
        command = 'docker rm -f '+container_id
        command = StringIO('\n'.join(self.env+[command]+['exit']))
        stdout, stderr = subprocess.Popen('cmd.exe',stdin=subprocess.PIPE,stdout=subprocess.PIPE).\
        communicate(command.getvalue().encode())
