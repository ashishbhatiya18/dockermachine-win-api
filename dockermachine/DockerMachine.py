import subprocess
import os
from io import StringIO

class machine:
    name = ''
    env = []

    def __init__(self, name='hadoop'):
        self.name = name
        self.__start__()
        self.env = self.__get_win_env__() + self.__get_docker_env__()

    def __start__(self):
        subprocess.Popen("docker-machine start "+self.name,stdout=None)

    def getip(self):
        return os.popen("docker-machine ip "+self.name).read()[:-1]

    def __get_docker_env__(self):
        proc = subprocess.Popen("docker-machine env "+self.name,shell=True, stdout=subprocess.PIPE)
        out, err = proc.communicate()
        return out.decode('utf-8').split('\n')[:4]

    def __get_win_env__(self):
        return ['@echo off']

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

    def containers(self, all=False):
        command = 'docker ps -a' if all else 'docker ps'
        command = StringIO('\n'.join(self.env+[command]+['exit']))
        stdout, stderr = subprocess.Popen('cmd.exe',stdin=subprocess.PIPE,stdout=subprocess.PIPE).\
        communicate(command.getvalue().encode())
        output = stdout.decode('utf-8').split('\n')[10:-1]
        return dict([(line.split(" ")[0], line) for line in output])

    def images(self):
        command = 'docker images'
        command = StringIO('\n'.join(self.env+[command]+['exit']))
        stdout, stderr = subprocess.Popen('cmd.exe',stdin=subprocess.PIPE,stdout=subprocess.PIPE).\
        communicate(command.getvalue().encode())
        output = stdout.decode('utf-8').split('\n')[10:-1]
        return dict([(line.split(" ")[0], line) for line in output])

if __name__=="__main__":
    m = machine()
    # for i in range(5):
    #     cid = m.launch('docker run -d --env ADVERTISED_HOST=192.168.99.100 --env ADVERTISED_PORT=9092 spotify/kafka')
    # print(m.containers(all=True).keys())
    # for container in m.containers(all=True).keys():
    #     m.stop(container)
    # print(m.containers(all=True))
    print(m.images().keys())
