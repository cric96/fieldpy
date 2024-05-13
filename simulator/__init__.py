class Scheduling:
    def __init__(self):
        self.scheduler = None

    def next_ids(self):
        pass


class Environment:

    def __init__(self):
        pass

    def nodes(self):
        pass

    def neighbours(self, node):
        pass

    def sense(self, node, what):
        pass

    def neighboringSense(self, node, what):
        pass

class Simulator:
    def __init__(self, env: Environment, scheduling: Scheduling):
        self.vms = {}
        self.env = env
        self.scheduling = scheduling
        self.time = 0

    def run(self):

        pass

