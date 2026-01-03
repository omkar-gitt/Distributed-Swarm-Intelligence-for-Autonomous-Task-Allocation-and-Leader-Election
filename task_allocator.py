import math
import time

class TaskAllocator:
    def __init__(self, agent_id, capabilities, position):
        self.agent_id = agent_id
        self.capabilities = capabilities          # set of capabilities
        self.position = position                  # (x, y)

        self.known_tasks = {}                     # task_id -> task
        self.task_bids = {}                       # task_id -> [(agent_id, score)]
        self.task_owner = {}                      # task_id -> agent_id
        self.owned_tasks = set()                  # tasks owned by this agent
        self.locked_tasks = set()                 # finalized tasks (stability)

    def distance(self, task_pos):
        return math.dist(self.position, task_pos)

    def receive_task(self, task):
        # Ignore if already finalized
        if task["id"] in self.locked_tasks:
            return
        self.known_tasks[task["id"]] = task

    def can_do_task(self, task):
        return task["capability"] in self.capabilities

    def compute_score(self, task):
        if not self.can_do_task(task):
            return None

        dist = self.distance(task["location"])
        time_left = max(0.1, task["deadline"] - time.time())

        # Simple & stable scoring function
        score = task["value"] - (1.5 * dist) - (2.0 / time_left)
        return score

    def create_bid(self, task):
        # Do not bid if task is locked
        if task["id"] in self.locked_tasks:
            return None

        score = self.compute_score(task)
        if score is None:
            return None

        return {
            "type": "TASK_BID",
            "task_id": task["id"],
            "agent_id": self.agent_id,
            "score": score
        }

    def receive_bid(self, task_id, agent_id, score):
        if task_id in self.locked_tasks:
            return

        if task_id not in self.task_bids:
            self.task_bids[task_id] = []

        self.task_bids[task_id].append((agent_id, score))

    def decide_winner(self, task_id):
        # Do not re-decide if already locked
        if task_id in self.locked_tasks:
            return None

        bids = self.task_bids.get(task_id, [])
        if not bids:
            return None

        # Highest score wins
        winner = max(bids, key=lambda x: x[1])[0]

        self.task_owner[task_id] = winner
        self.locked_tasks.add(task_id)

        if winner == self.agent_id:
            self.owned_tasks.add(task_id)

        return winner
