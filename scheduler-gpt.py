# Project Group 1
# Adrian Hossen, David Fanai, Hemant Kanoujia, Istiaqul Alam

import sys
import heapq

def create_process(process_id, arrival_time, execution_time):
    return {
        'process_id': process_id,
        'arrival_time': arrival_time,
        'execution_time': execution_time,
        'remaining_time': execution_time,
        'start_time': None,
        'end_time': None,
        'wait_time': 0,
        'response_time': None,
        'status': 'Ready'  # 'Ready', 'Running', or 'Completed'
    }

def cfs_scheduler(processes, run_for):
    current_time = 0
    log = []
    processes = sorted(processes, key=lambda x: x['arrival_time'])
    process_queue = []
    processes_iter = iter(processes)
    next_process = next(processes_iter, None)
    current_process = None
    wait_turnaround_response = []  # List to store wait, turnaround, and response times

    while current_time < run_for:
        # Add newly arrived processes to the queue
        while next_process and next_process['arrival_time'] <= current_time:
            heapq.heappush(process_queue, (next_process['arrival_time'], next_process))
            log.append(f"Time {current_time: >3} : {next_process['process_id']} arrived")
            next_process = next(processes_iter, None)

        if not current_process and process_queue:
            # Select the next process in the queue if there is no current process
            _, current_process = heapq.heappop(process_queue)
            current_process['start_time'] = current_time
            log.append(f"Time {current_time: >3} : {current_process['process_id']} selected (burst {current_process['remaining_time']:>3})")

        if current_process:
            # Run the current process
            current_process['execution_time'] -= 1
            if current_process['execution_time'] == 0:
                current_process['end_time'] = current_time + 1
                log.append(f"Time {current_time + 1: >3} : {current_process['process_id']} finished")

                # Calculate wait, turnaround, and response times for the finished process
                wait_time = current_process['start_time'] - current_process['arrival_time']
                turnaround_time = current_process['end_time'] - current_process['arrival_time']
                response_time = current_process['start_time'] - current_process['arrival_time']
                wait_turnaround_response.append({
                    'process_id': current_process['process_id'],
                    'wait_time': wait_time,
                    'turnaround_time': turnaround_time,
                    'response_time': response_time
                })

                current_process = None
        else:
            log.append(f"Time {current_time: >3} : Idle")

        current_time += 1

    log.sort(key=lambda x: (int(x.split()[1]), 'Idle' in x, 'selected' in x, 'finished' in x, 'arrived' in x))
    log.append(f"Finished at time {run_for: >3}")
    wait_turnaround_response.sort(key=lambda x: x['process_id'])

    return log, wait_turnaround_response

def fcfs_scheduler(processes, run_for):
    current_time = 0
    log = []
    processes = sorted(processes, key=lambda x: x['arrival_time'])
    process_queue = []
    processes_iter = iter(processes)
    next_process = next(processes_iter, None)
    current_process = None
    wait_turnaround_response = []  # List to store wait, turnaround, and response times

    while current_time < run_for:
        # Add newly arrived processes to the queue
        while next_process and next_process['arrival_time'] <= current_time:
            process_queue.append(next_process)
            log.append(f"Time {current_time: >3} : {next_process['process_id']} arrived")
            next_process = next(processes_iter, None)

        if not current_process and process_queue:
            # Select the next process in the queue if there is no current process
            current_process = process_queue.pop(0)
            current_process['start_time'] = current_time
            log.append(f"Time {current_time: >3} : {current_process['process_id']} selected (burst {current_process['remaining_time']:>3})")

        if current_process:
            # Run the current process
            current_process['execution_time'] -= 1
            if current_process['execution_time'] == 0:
                current_process['end_time'] = current_time + 1
                log.append(f"Time {current_time + 1: >3} : {current_process['process_id']} finished")

                # Calculate wait, turnaround, and response times for the finished process
                wait_time = current_process['start_time'] - current_process['arrival_time']
                turnaround_time = current_process['end_time'] - current_process['arrival_time']
                response_time = current_process['start_time'] - current_process['arrival_time']
                wait_turnaround_response.append({
                    'process_id': current_process['process_id'],
                    'wait_time': wait_time,
                    'turnaround_time': turnaround_time,
                    'response_time': response_time
                })

                current_process = None
        else:
            log.append(f"Time {current_time: >3} : Idle")

        current_time += 1

    log.sort(key=lambda x: (int(x.split()[1]), 'Idle' in x, 'selected' in x, 'finished' in x, 'arrived' in x))
    log.append(f"Finished at time {run_for: >3}")
    wait_turnaround_response.sort(key=lambda x: x['process_id'])

    return log, wait_turnaround_response

def sjf_preemptive_scheduler(processes, run_for):
    current_time = 0
    log = []
    waiting_queue = []
    processes.sort(key=lambda x: x['arrival_time'])
    processes_iter = iter(processes)
    next_process = next(processes_iter, None)
    current_process = None
    wait_turnaround_response = []

    while current_time < run_for:
        # Add newly arrived processes to the waiting queue
        while next_process and next_process['arrival_time'] <= current_time:
            heapq.heappush(waiting_queue, (next_process['remaining_time'], next_process['process_id'], next_process))
            log.append(f"Time {current_time: >3} : {next_process['process_id']} arrived")
            next_process = next(processes_iter, None)

        # Check for preemption
        if current_process and waiting_queue:
            _, next_in_queue_id, next_in_queue = waiting_queue[0]
            if next_in_queue['remaining_time'] < current_process['remaining_time']:
                heapq.heappop(waiting_queue)
                heapq.heappush(waiting_queue, (current_process['remaining_time'], current_process['process_id'], current_process))
                current_process = next_in_queue
                if current_process['start_time'] is None:
                    current_process['start_time'] = current_time
                log.append(f"Time {current_time: >3} : {current_process['process_id']} selected (burst {current_process['remaining_time']:>3})")

        if not current_process and waiting_queue:
            _, _, current_process = heapq.heappop(waiting_queue)
            if current_process['start_time'] is None:
                current_process['start_time'] = current_time
            log.append(f"Time {current_time: >3} : {current_process['process_id']} selected (burst {current_process['remaining_time']:>3})")

        if current_process:
            current_process['remaining_time'] -= 1
            if current_process['remaining_time'] == 0:
                current_process['end_time'] = current_time + 1
                log.append(f"Time {current_time + 1: >3} : {current_process['process_id']} finished")

                wait_time = current_process['end_time'] - current_process['arrival_time'] - current_process['execution_time']
                turnaround_time = current_process['end_time'] - current_process['arrival_time']
                response_time = current_process['start_time'] - current_process['arrival_time']
                wait_turnaround_response.append({
                    'process_id': current_process['process_id'],
                    'wait_time': max(wait_time, 0),  # Ensure wait time is not negative
                    'turnaround_time': turnaround_time,
                    'response_time': response_time
                })

                current_process = None
        else:
            log.append(f"Time {current_time: >3} : Idle")

        current_time += 1

    log.sort(key=lambda x: (int(x.split()[1]), 'Idle' in x, 'selected' in x, 'finished' in x, 'arrived' in x))
    log.append(f"Finished at time {run_for: >3}")
    wait_turnaround_response.sort(key=lambda x: x['process_id'])

    return log, wait_turnaround_response

def round_robin_scheduler(processes, run_for, quantum):
    current_time = 0
    log = []
    wait_turnaround_response = []

    remaining_processes = sorted(processes, key=lambda x: x['arrival_time'])
    waiting_queue = []

    while remaining_processes or waiting_queue or current_time < run_for:
        if waiting_queue:
            process = waiting_queue.pop(0)
        elif remaining_processes:
            process = remaining_processes.pop(0)
            log.append(f"Time {process['arrival_time']: >3} : {process['process_id']} arrived")
        else:
            log.append(f"Time {current_time: >3} : Idle")
            current_time += 1
            continue
        
        if process.get('start_time') is None:
            process['start_time'] = current_time

        burst_time = min(process['remaining_time'], quantum)  # Correctly limit burst time
        log.append(f"Time {current_time: >3} : {process['process_id']} selected (burst {process['remaining_time']:>3})")

        current_time += burst_time
        process['remaining_time'] -= burst_time

        if process['remaining_time'] <= 0:
            log.append(f"Time {current_time: >3} : {process['process_id']} finished")

            wait_time = current_time - process['arrival_time'] - process['execution_time']
            turnaround_time = current_time - process['arrival_time']
            response_time = process['start_time'] - process['arrival_time']
            wait_turnaround_response.append({
                'process_id': process['process_id'],
                'wait_time': max(wait_time, 0),
                'turnaround_time': turnaround_time,
                'response_time': max(response_time, 0)
            })
        else:
            # Adjusted the condition to only add processes that have arrived before or at the current time
            while remaining_processes and remaining_processes[0]['arrival_time'] <= current_time:
                next_process = remaining_processes.pop(0)
                waiting_queue.append(next_process)
                log.append(f"Time {next_process['arrival_time']: >3} : {next_process['process_id']} arrived")
            waiting_queue.append(process)

    log.sort(key=lambda x: (int(x.split()[1]), 'Idle' in x, 'selected' in x, 'finished' in x, 'arrived' in x))
    log.insert(0, f"Quantum   {quantum}\n")  # Insert quantum value at the beginning of the log
    log.append(f"Finished at time {current_time: >3}")
    wait_turnaround_response.sort(key=lambda x: x['process_id'])

    return log, wait_turnaround_response

def is_valid_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    input_data = {}
    processes = []

    for line in lines:
        tokens = line.strip().split()

        if tokens[0] == 'processcount':
            if len(tokens) > 1 and is_valid_integer(tokens[1]):
                input_data['processcount'] = int(tokens[1])
            else:
                print("Error: Missing or invalid processcount parameter")
                sys.exit(1)
        elif tokens[0] == 'runfor':
            if len(tokens) > 1 and is_valid_integer(tokens[1]):
                input_data['runfor'] = int(tokens[1])
            else: 
                print("Error: Missing or invalid runfor parameter")
                sys.exit(1)
        elif tokens[0] == 'use':
            if len(tokens) > 1 and tokens[1] in ['fcfs', 'sjf', 'rr', 'cfs']:
                input_data['scheduler'] = tokens[1]
            else:
                print("Error: Missing or invalid scheduler parameter")
                sys.exit(1)
        elif tokens[0] == 'quantum':
            if len(tokens) > 1 and is_valid_integer(tokens[1]):
                input_data['quantum'] = int(tokens[1])
            else:
                print("Error: Missing or invalid quantum parameter when use is 'rr'")
                sys.exit(1)
        elif tokens[0] == 'process':
            if len(tokens) >= 7 and is_valid_integer(tokens[4]) and is_valid_integer(tokens[6]):
                process_info = {
                    'name': tokens[2],
                    'arrival': int(tokens[4]),
                    'burst': int(tokens[6])
                }
                processes.append(process_info)
            else:
                print("Error: Missing or invalid parameter in process line")
                sys.exit(1)

    input_data['processes'] = processes

    return input_data

def main():
    if len(sys.argv) != 2:
        print("Usage: python scheduler-gpt.py <input_file.in>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not input_file.endswith('.in'):
        print("Error: Please provide a file with a '.in' extension.")
        sys.exit(1)

    try:
        input_data = read_input_file(input_file)
        output_file = input_file.replace('.in', '.out')  # Output file name

        with open(output_file, 'w') as f:
            processes_count = input_data['processcount']
            f.write(f" {processes_count: >2} processes\n")

            processes = [create_process(p['name'], p['arrival'], p['burst']) for p in input_data['processes']]
            quantum = input_data.get('quantum', 1)  # Default quantum is 1 if not specified

            if input_data['scheduler'].lower() == 'fcfs':
                f.write("Using First-Come First-Served\n")
                log, wait_turnaround_response = fcfs_scheduler(processes, input_data['runfor'])
            elif input_data['scheduler'].lower() == 'sjf':
                f.write("Using preemptive Shortest Job First\n")
                log, wait_turnaround_response = sjf_preemptive_scheduler(processes, input_data['runfor'])
            elif input_data['scheduler'].lower() == 'rr':
                f.write("Using Round-Robin\n")
                log, wait_turnaround_response = round_robin_scheduler(processes, input_data['runfor'], quantum)
            elif input_data['scheduler'].lower() == 'cfs':
                f.write("Using CFS\n")
                log, wait_turnaround_response = cfs_scheduler(processes, input_data['runfor'])

            # Writing log to file
            for entry in log:
                f.write(entry + '\n')

            f.write('\n')

            # Writing wait, turnaround, and response times for each process
            for wt in wait_turnaround_response:
                f.write(f"{wt['process_id']} wait {wt['wait_time']: >3} turnaround {wt['turnaround_time']: >3} response {wt['response_time']: >3}\n")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scheduler-gpt.py <input_file.in>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not input_file.endswith('.in'):
        print("Error: Please provide a file with a '.in' extension.")
        sys.exit(1)

    main()

