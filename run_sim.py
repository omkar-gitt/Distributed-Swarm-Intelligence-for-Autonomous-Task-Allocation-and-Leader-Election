import time
from mock_network import MockNetwork
from agent import Agent

# ---------------- CONFIGURATION ----------------
NUM_AGENTS = 5
SIM_TIME = 30  # seconds

# ---------------- NETWORK ----------------
network = MockNetwork(loss_prob=0.1)
agents = []

for i in range(NUM_AGENTS):
    network.register(i)
    agents.append(Agent(i, network))

# ---------------- SIMULATION CONTROL ----------------
start = time.time()
leader_killed = False
tasks_announced = False

# ---------------- SAMPLE TASKS (Scenario S7) ----------------
sample_tasks = [
    {
        "id": 1,
        "capability": "camera",
        "location": (20, 30),
        "deadline": time.time() + 40,
        "value": 100
    },
    {
        "id": 2,
        "capability": "sonar",
        "location": (50, 10),
        "deadline": time.time() + 50,
        "value": 80
    }
]

# ---------------- MAIN SIMULATION LOOP ----------------
while time.time() - start < SIM_TIME:

    # 📢 Announce tasks after 2 seconds (only once)
    if not tasks_announced and time.time() - start > 2:
        print("\n📢 Tasks announced\n")
        for task in sample_tasks:
            network.broadcast(
                sender=-1,  # simulator
                msg={
                    "type": "TASK_ANNOUNCE",
                    "task": task
                }
            )
        tasks_announced = True

    # ---------------- AGENT EXECUTION ----------------
    for a in agents:

        # 💥 Kill leader at 10 seconds (Scenario S6)
        if not leader_killed and time.time() - start > 10:
            if a.leader.state == "LEADER":
                print(f"\n💥 Leader {a.id} killed!\n")
                a.leader.state = "DEAD"
                leader_killed = True
                continue

        # Normal agent operation
        if a.leader.state != "DEAD":
            a.step()

    # 10 Hz simulation
    time.sleep(0.1)
