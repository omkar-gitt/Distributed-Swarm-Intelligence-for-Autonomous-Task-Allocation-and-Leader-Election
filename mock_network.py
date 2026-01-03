import random

class MockNetwork:
    def __init__(self, loss_prob=0.1):
        self.queues = {}
        self.loss_prob = loss_prob

    def register(self, agent_id):
        self.queues[agent_id] = []

    def send(self, sender, receiver, msg):
        if random.random() > self.loss_prob:
            self.queues[receiver].append((sender, msg))

    def broadcast(self, sender, msg):
        for r in self.queues:
            if r != sender:
                self.send(sender, r, msg)

    def receive(self, agent_id):
        msgs = self.queues[agent_id][:]
        self.queues[agent_id].clear()
        return msgs
