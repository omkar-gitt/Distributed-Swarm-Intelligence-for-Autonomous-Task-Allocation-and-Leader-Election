# Distributed-Swarm-Intelligence-for-Autonomous-Task-Allocation-and-Leader-Election
Distributed Swarm Intelligence for Autonomous Task Allocation and Leader Election

## 📑 Table of Contents

- [Project Overview](#-project-overview)
- [Problem Statement](#-problem-statement)
- [Solution Approach](#-solution-approach)
  - [Leader Election](#leader-election)
  - [Capability-Aware Task Allocation](#capability-aware-task-allocation)
  - [Task Stability](#task-stability)
  - [Disciplined Communication](#disciplined-communication)
- [System Architecture](#-system-architecture)
- [Project Structure](#-project-structure)
- [Validation](#-validation)
- [How to Run the Project](#-how-to-run-the-project)
- [Integration with SWARMBENCH-30+](#-integration-with-swarmbench-30)
- [Hackathon Details](#-hackathon-details)
- [Conclusion](#-conclusion)


## 📌 Project Overview

This project implements a fully distributed swarm intelligence algorithm developed for the SWAVLAMBAN 2025 Hackathon – Challenge 1. The system enables a group of autonomous agents to coordinate without centralized control by performing dynamic leader election, capability-aware task allocation, and disciplined communication under low-bandwidth and unreliable network conditions.

The solution is designed to be fault-tolerant, scalable, and simulator-agnostic, and has been validated using a custom mock simulation environment that reflects the constraints of the SWARMBENCH-30+ evaluator.

## 🎯 Problem Statement

In distributed autonomous swarm systems:

Leaders may fail unexpectedly

Tasks require specific capabilities

Communication bandwidth is limited and unreliable

Centralized coordination creates single points of failure

The objective is to design a distributed algorithm that:

Dynamically elects a leader

Recovers quickly from leader failures

Allocates tasks based on agent capabilities

Maintains stable task ownership

Operates efficiently over low-bandwidth links

## 🧠Solution Approach
**Leader Election**

Heartbeat-based distributed leader detection

Automatic leader re-election within 10 seconds

No centralized controller

**Capability-Aware Task Allocation**

Tasks announced dynamically to the swarm

Agents bid only if they have the required capability

Auction-based task assignment using distance, urgency, and task value

**Task Stability**

Task locking mechanism prevents unnecessary reassignment

Ensures at least 95% task stability within 60 seconds

**Disciplined Communication**

Event-driven, low-overhead messaging

Designed for lossy and low-bandwidth communication (≤64 kbps per node)

## 🏗️ System Architecture

Each agent runs the same Python-based logic and consists of:

Leader Election Module

Task Allocation Module

Message Handling and Control Loop

All coordination is achieved through peer-to-peer communication, ensuring a fully distributed and fault-tolerant system.

## 📁 Project Structure

swarm_mock_simulator/

├── agent.py

├── leader.py

├── task_allocator.py

├── mock_network.py

└── run_sim.py

## 🧪 Validation

The algorithm was validated using a custom mock simulator that tested:

Leader failure and re-election (Scenario S6)

Capability-aware task allocation (Scenario S7)

Task stability under dynamic conditions

Communication loss scenarios

The system demonstrates stable task ownership and rapid recovery from failures.

## ▶️How to Run the Project
Prerequisites

Python 3.x installed

**Steps** :

git clone "repository-url"

cd swarm_mock_simulator

python run_sim.py


(Windows users may use py run_sim.py)


<img width="519" height="349" alt="image" src="https://github.com/user-attachments/assets/1e99f9ca-c0fb-4dd0-b3da-8c6b2b8b9904" />


## 🔌 Integration with SWARMBENCH-30+

The core logic is simulator-agnostic. Integration with SWARMBENCH-30+ requires replacing mock communication and observation interfaces with simulator APIs while keeping the leader election and task allocation logic unchanged.

## 🏁 Hackathon Details

Event: SWAVLAMBAN 2025

Challenge: Development of Distributed Swarm Algorithm

Language: Python

## Conclusion

This project demonstrates a robust and efficient distributed swarm algorithm that satisfies all requirements of Challenge-1. The solution is suitable for further integration with real-world swarm simulators and autonomous systems.
