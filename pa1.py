import sys

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

def print_status(time, process_name, burst_time, is_idle=False):
    if is_idle:
        print(f"Time {time:3} : Idle")
    else:
        print(f"Time {time:3} : {process_name} {'arrived' if burst_time > 0 else 'selected (burst':<9} {burst_time:3})")

def print_process_metrics(processes):
    for process in processes:
        print(f"{process['name']} wait {process['wait_time']} turnaround {process['end_time'] - process['arrival']} response {process['response_time']}")

def print_status(time, process_name, burst_time, is_idle=False):
    if is_idle:
        print(f"Time {time:3} : Idle")
    else:
        print(f"Time {time:3} : {process_name} {'arrived' if burst_time > 0 else 'selected (burst':<9} {burst_time:3})")

def is_completed(process):
    return process['remaining_time'] == 0

def fifo_scheduler(processes):
    current_time = 0

    for process in processes:
        if process['arrival_time'] > current_time:
            current_time = process['arrival_time']

        process['start_time'] = current_time
        process['end_time'] = current_time + process['execution_time']
        process['response_time'] = process['start_time'] - process['arrival_time']
        process['wait_time'] = process['response_time']
        process['status'] = 'Completed'
        current_time = process['end_time']

    return processes

def sjf_scheduler(processes):
    processes.sort(key=lambda x: (x['arrival_time'], x['execution_time']))
    current_time = 0

    for process in processes:
        if process['arrival_time'] > current_time:
            current_time = process['arrival_time']

        process['start_time'] = current_time
        process['end_time'] = current_time + process['execution_time']
        process['response_time'] = process['start_time'] - process['arrival_time']
        process['wait_time'] = process['response_time']
        process['status'] = 'Completed'
        current_time = process['end_time']

    return processes

def round_robin_scheduler(processes, q_value):
    queue = processes.copy()
    current_time = 0

    while queue:
        process = queue.pop(0)

        if process['arrival_time'] > current_time:
            current_time = process['arrival_time']

        process['start_time'] = current_time

        if process['remaining_time'] <= q_value:
            current_time += process['remaining_time']
            process['end_time'] = current_time
            process['response_time'] = process['start_time'] - process['arrival_time']
            process['wait_time'] = process['response_time'] - process['execution_time']
            process['status'] = 'Completed'
        else:
            current_time += q_value
            process['remaining_time'] -= q_value
            queue.append(process)

    return processes

def calculate_metrics(processes):
    total_turnaround_time = 0
    total_wait_time = 0
    total_response_time = 0

    for process in processes:
        turnaround_time = process['end_time'] - process['arrival_time']
        total_turnaround_time += turnaround_time
        total_wait_time += process['wait_time']
        total_response_time += process['response_time']

    num_processes = len(processes)
    avg_turnaround_time = total_turnaround_time / num_processes
    avg_wait_time = total_wait_time / num_processes
    avg_response_time = total_response_time / num_processes

    return avg_turnaround_time, avg_wait_time, avg_response_time

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    input_data = {}
    processes = []

    for line in lines:
        tokens = line.strip().split()

        if tokens[0] == 'processcount':
            input_data['processcount'] = int(tokens[1])
        elif tokens[0] == 'runfor':
            input_data['runfor'] = int(tokens[1])
        elif tokens[0] == 'use':
            input_data['scheduler'] = tokens[1]
        elif tokens[0] == 'process':
            process_info = {
                'name': tokens[2],
                'arrival': int(tokens[4]),
                'burst': int(tokens[6])
            }
            processes.append(process_info)

    input_data['processes'] = processes
    return input_data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scheduler-gpt.py <input_file.in>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not input_file.endswith('.in'):
        print("Error: Please provide a file with a '.in' extension.")
        sys.exit(1)

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
        # print("Number of processes:", input_data['processcount'])
        # print("Run for:", input_data['runfor'])
        # print("Scheduler:", input_data['scheduler'])
        # print("Processes:", input_data['processes'])

        # if input_data['scheduler'].lower() == 'fcfs':
        #     processes = [create_process(p['name'], p['arrival'], p['burst']) for p in input_data['processes']]
        #     print("\nUsing First-Come First-Served")
        #     fifo_scheduler(processes)

        # if input_data['scheduler'].lower() == 'fcfs':
        #     processes = [create_process(p['name'], p['arrival'], p['burst']) for p in input_data['processes']]
        #     print("\nUsing First-Come First-Served")
        #     fifo_scheduler(processes)

        # if input_data['scheduler'].lower() == 'fcfs':
        #     processes = [create_process(p['name'], p['arrival'], p['burst']) for p in input_data['processes']]
        #     print("\nUsing First-Come First-Served")
        #     fifo_scheduler(processes)

        # if input_data['scheduler'].lower() == 'fcfs':
        #     processes = [create_process(p['name'], p['arrival'], p['burst']) for p in input_data['processes']]
        #     print("\nUsing First-Come First-Served")
        #     fifo_scheduler(processes)

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# def print_simulation_output(processes):
#     for process in processes:
#         if process['status'] == 'Completed':
#             print_status(process['start_time'], process['process_id'], 0)
#             print_status(process['end_time'], 'Idle', 0)
#         else:
#             print_status(process['arrival_time'], process['process_id'], process['execution_time'])
#             print_status(process['start_time'], process['process_id'], process['remaining_time'])
#             print_status(process['end_time'], 'Idle', 0)

#     print(f"Finished at time {processes[-1]['end_time']}\n")

#     for process in processes:
#         if process['status'] == 'Completed':
#             print_process_metrics(process)

if __name__ == "__main__":
    main()