import time

class LeaderElection:
    def __init__(self, agent_id, network):
        self.agent_id = agent_id
        self.network = network
        self.leader_id = None
        self.last_heartbeat = time.time()
        self.state = "FOLLOWER"
        self.election_start = None
        self.candidates = set()

    def send_heartbeat(self):
        self.network.broadcast(
            self.agent_id,
            {"type": "HEARTBEAT", "leader_id": self.agent_id}
        )

    def receive_heartbeat(self, leader_id):
        self.leader_id = leader_id
        self.last_heartbeat = time.time()
        self.state = "FOLLOWER"

    def check_leader_timeout(self):
        if time.time() - self.last_heartbeat > 3:
            self.start_election()

    def start_election(self):
        if self.state != "CANDIDATE":
            self.state = "CANDIDATE"
            self.election_start = time.time()
            self.candidates = {self.agent_id}
            self.network.broadcast(
                self.agent_id,
                {"type": "ELECTION", "candidate_id": self.agent_id}
            )

    def receive_election(self, candidate_id):
        self.candidates.add(candidate_id)

    def election_step(self):
        if self.state == "CANDIDATE":
            if time.time() - self.election_start > 2:
                self.leader_id = max(self.candidates)
                self.state = "LEADER" if self.leader_id == self.agent_id else "FOLLOWER"
                if self.state == "LEADER":
                    print(f"✅ New leader elected: Agent {self.agent_id}")
                    self.network.broadcast(
                        self.agent_id,
                        {"type": "LEADER_ANNOUNCE", "leader_id": self.agent_id}
                    )

    def receive_leader_announce(self, leader_id):
        self.leader_id = leader_id
        self.last_heartbeat = time.time()
        self.state = "FOLLOWER"
