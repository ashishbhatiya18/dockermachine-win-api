class Container:

    def __init__(self, name, tag, daemon=True, id=0):
        self.name = name
        self.tag = tag
        self.ports = []
        self.env = {}
        self.daemon = daemon
        self.id = id

    def launch_cmd(self):
        docker_run_cmd = 'docker run -d' if self.daemon else 'docker run'
        portsFlag,envFlag = '',''
        for portmap in self.ports:
            portsFlag+=' -p {}:{} '.format(str(portmap[0]),str(portmap[1]))
        for key in self.env.keys():
            envFlag+=' --env {}={} '.format(key,self.env[key])
        docker_run_cmd+='{} {} {}:{}'.format(envFlag, portsFlag, self.name, self.tag)
        return docker_run_cmd

    def add_env(self, key, value):
        self.env[key] = value

    def add_port(self, container_port, host_port):
        self.ports.append((container_port, host_port))
