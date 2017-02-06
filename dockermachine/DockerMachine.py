import subprocess
import os
from io import StringIO
from PortMapping import PortMapping
from Environment import Environment

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

    def launch(self, image_name, environment, ports, daemon=True):
        portsFlag,envFlag = '',''
        for portmap in ports.mappings:
            portsFlag+=' -p {}:{} '.format(str(portmap[0]),str(portmap[1]))
        for key in environment.mappings.keys():
            envFlag+=' --env {}={} '.format(key,environment.mappings[key])
        docker_run_cmd = 'docker run -d' if daemon else 'docker run'
        docker_run_cmd+=envFlag+portsFlag+image_name
        command = StringIO('\n'.join(self.env+[docker_run_cmd]+['exit']))
        stdout, stderr = subprocess.Popen('cmd.exe',stdin=subprocess.PIPE,stdout=subprocess.PIPE).\
        communicate(command.getvalue().encode())
        return stdout.decode('utf-8').split()[-2][:12]

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
    ports = PortMapping()
    ports.add(2181,2181)
    ports.add(9092,9092)
    env = Environment()
    env.add('ADVERTISED_HOST','192.168.99.100')
    env.add('ADVERTISED_PORT','9092')
    print(m.launch('spotify/kafka',env,ports))
    # for container in m.containers(all=True).keys():
    #     m.stop(container)
