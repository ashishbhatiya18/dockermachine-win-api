import subprocess
import os
from io import StringIO

class Machine:
    name = ''
    env = 'docker-machine env {} | Invoke-Expression'
    shell = 'powershell.exe'
    ip = ''

    def __init__(self, name='hadoop'):
        self.name = name
        self.__start__()
        self.ip = self.__getip__()

    def __start__(self):
        os.popen('{} {} {}'.format(self.shell, 'docker-machine start',self.name))

    def __getip__(self):
        return os.popen("docker-machine ip "+self.name).read()[:-1]

    def launch(self, container):
        command = container.launch_cmd()
        output = os.popen('{} "{};{}"'.format(self.shell, self.env.format(self.name),command)).read()
        container.id = output[:12]

    def stop(self, container):
        command = 'docker rm -f '+container
        os.popen('{} "{};{}"'.format(self.shell, self.env.format(self.name),command))

    def containers(self, all=False):
        command = 'docker ps -a' if all else 'docker ps'
        command+= ' --format \'{{.ID}},{{.Image}}\''
        output = os.popen('{} "{};{}"'.format(self.shell, self.env.format(self.name), command)).read()
        return {line.split(',')[0]:line.split(',')[1] for line in output.split('\n') if len(line) > 0}


    def images(self):
        command = 'docker images --format \'{{.Repository}},{{.Tag}}\''
        output = os.popen('{} "{};{}"'.format(self.shell, self.env.format(self.name), command)).read()
        return [(line.split(',')[0],line.split(',')[1]) for line in output.split('\n') if len(line) > 0]

if __name__=="__main__":
    from Container import Container
    m = Machine()
    print(m.images())
    kafkaContainer = Container('spotify/kafka','latest')
    kafkaContainer.add_port(2181,2181)
    kafkaContainer.add_port(9092,9092)
    kafkaContainer.add_env('ADVERTISED_HOST',m.ip)
    kafkaContainer.add_env('ADVERTISED_PORT','9092')
    m.launch(kafkaContainer)
    print(m.containers())
    for container in m.containers(all=True).keys():
        print(container)
        m.stop(container)
