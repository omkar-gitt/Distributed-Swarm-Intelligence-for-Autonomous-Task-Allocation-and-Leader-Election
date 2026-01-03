from leader import LeaderElection
from task_allocator import TaskAllocator

class Agent:
    def __init__(self, agent_id, network):
        self.id = agent_id
        self.network = network

        # ---------------- LEADER ELECTION ----------------
        self.leader = LeaderElection(agent_id, network)

        # ---------------- CAPABILITIES ----------------
        capability_sets = [
            {"camera"},
            {"sonar"},
            {"tool"},
            {"camera", "tool"},
            {"sonar", "camera"}
        ]
        self.capabilities = capability_sets[agent_id % len(capability_sets)]

        # ---------------- POSITION ----------------
        self.position = (agent_id * 10, agent_id * 5)

        # ---------------- TASK ALLOCATOR ----------------
        self.task_allocator = TaskAllocator(
            agent_id=self.id,
            capabilities=self.capabilities,
            position=self.position
        )

    def step(self):
        # ---------------- RECEIVE MESSAGES ----------------
        for sender, msg in self.network.receive(self.id):

            # ---- Leader election messages ----
            if msg["type"] == "HEARTBEAT":
                self.leader.receive_heartbeat(msg["leader_id"])

            elif msg["type"] == "ELECTION":
                self.leader.receive_election(msg["candidate_id"])

            elif msg["type"] == "LEADER_ANNOUNCE":
                self.leader.receive_leader_announce(msg["leader_id"])

            # ---- Task messages ----
            elif msg["type"] == "TASK_ANNOUNCE":
                self.task_allocator.receive_task(msg["task"])

                bid = self.task_allocator.create_bid(msg["task"])
                if bid:
                    self.network.broadcast(self.id, bid)

            elif msg["type"] == "TASK_BID":
                self.task_allocator.receive_bid(
                    msg["task_id"],
                    msg["agent_id"],
                    msg["score"]
                )

            elif msg["type"] == "TASK_CLAIM":
                task_id = msg["task_id"]
                owner = msg["agent_id"]

                # Lock task locally
                self.task_allocator.task_owner[task_id] = owner
                self.task_allocator.locked_tasks.add(task_id)

                if owner == self.id:
                    print(f"🟢 Agent {self.id} owns Task {task_id}")

        # ---------------- LEADER DUTIES ----------------
        if self.leader.state == "LEADER":
            self.leader.send_heartbeat()

        # ---------------- LEADER CHECK ----------------
        self.leader.check_leader_timeout()
        self.leader.election_step()

        # ---------------- TASK DECISION (LEADER ONLY) ----------------
        if self.leader.state == "LEADER":
            for task_id in list(self.task_allocator.task_bids.keys()):
                if task_id not in self.task_allocator.locked_tasks:
                    winner = self.task_allocator.decide_winner(task_id)
                    if winner is not None:
                        self.network.broadcast(
                            self.id,
                            {
                                "type": "TASK_CLAIM",
                                "task_id": task_id,
                                "agent_id": winner
                            }
                        )
