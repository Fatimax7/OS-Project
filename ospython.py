import queue
# Process class to hold process info
class Process:
    def __init__(self, pid, arrival, burst, priority, max_resources):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.priority = priority
        self.max_resources = max_resources
        self.allocated = [0] * len(max_resources)
        self.finished = False

# Simulated processes
process_list = [
    Process(1, 0, 6, 2, [5, 3]),
    Process(2, 1, 8, 1, [3, 2]),
    Process(3, 2, 7, 3, [4, 2])
]

available_resources = [7, 5]
time_quantum = 3

# Scheduler: Hybrid Round Robin + Priority
def hybrid_scheduler(processes):
    ready_queue = queue.Queue()
    time = 0
    processes.sort(key=lambda p: (p.arrival, p.priority))
    while any(p.remaining > 0 for p in processes):
        for p in processes:
            if p.arrival <= time and p.remaining > 0 and p not in list(ready_queue.queue):
                ready_queue.put(p)

        if ready_queue.empty():
            time += 1
            continue

        current = ready_queue.get()
        exec_time = min(current.remaining, time_quantum if time % 2 == 0 else current.remaining)
        print(f"Time {time}-{time + exec_time}: Process {current.pid} executed")
        current.remaining -= exec_time
        time += exec_time

        if current.remaining > 0:
            ready_queue.put(current)

# Deadlock Detection using Wait-for Graph
def detect_deadlock(processes):
    wait_for = {p.pid: [] for p in processes}
    for p in processes:
        for i, need in enumerate(p.max_resources):
            if need > available_resources[i]:
                wait_for[p.pid].append((i, need))

    deadlocked = [pid for pid, needs in wait_for.items() if needs]
    if deadlocked:
        print("Deadlock detected among processes:", deadlocked)
    else:
        print("No deadlock detected.")

# Banker's Algorithm for Deadlock Avoidance
def is_safe(processes, available):
    work = available[:]
    finish = [False] * len(processes)

    while True:
        found = False
        for i, p in enumerate(processes):
            need = [p.max_resources[j] - p.allocated[j] for j in range(len(available))]
            if not finish[i] and all(need[j] <= work[j] for j in range(len(available))):
                for j in range(len(available)):
                    work[j] += p.allocated[j]
                finish[i] = True
                found = True
        if not found:
            break

    return all(finish)

# Inter-Process Communication using Queues
ipc_queue = queue.Queue()

def send_message(sender, receiver, message):
    print(f"Process {sender} sending message to Process {receiver}")
    ipc_queue.put((receiver, message))

def receive_message(receiver):
    while not ipc_queue.empty():
        pid, msg = ipc_queue.get()
        if pid == receiver:
            print(f"Process {receiver} received message: {msg}")
            return

# Memory Management with Paging (FIFO replacement)
memory_size = 3
memory = []

def access_page(pid, page):
    global memory
    if page in memory:
        print(f"Process {pid} accessed page {page} (in memory)")
    else:
        if len(memory) >= memory_size:
            removed = memory.pop(0)
            print(f"Page {removed} removed from memory")
        memory.append(page)
        print(f"Process {pid} loaded page {page} into memory")

# Main simulation
print("---- Hybrid Scheduling Simulation ----")
hybrid_scheduler(process_list)

print("\n---- Deadlock Detection ----")
detect_deadlock(process_list)

print("\n---- Deadlock Avoidance (Banker's Algorithm) ----")
safe = is_safe(process_list, available_resources)
print("System is in a safe state" if safe else "System is NOT in a safe state")

print("\n---- Inter-Process Communication ----")
send_message(1, 2, "Hello from P1")
receive_message(2)

print("\n---- Memory Management Simulation ----")
access_page(1, "A")
access_page(1, "B")
access_page(2, "C")
access_page(3, "D")  # Triggers FIFO replacement
access_page(1, "A")  # Re-access page A

print("\n---- Simulation Complete ----")

