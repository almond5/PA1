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

def fcfs_scheduler(processes, run_for):
    current_time = 0
    log = []

    for process in sorted(processes, key=lambda x: x['arrival_time']):
        if process['arrival_time'] > current_time:
            for i in range(current_time, process['arrival_time']):
                log.append(f"Time {i} : Idle")
                current_time = i
            current_time = process['arrival_time']

        log.append(f"Time {current_time} : {process['process_id']} arrived")
        process['start_time'] = current_time
        process['end_time'] = current_time + process['execution_time']
        process['response_time'] = process['start_time'] - process['arrival_time']
        process['wait_time'] = current_time - process['arrival_time']  # Corrected wait time calculation
        process['status'] = 'Completed'
        log.append(f"Time {current_time} : {process['process_id']} selected (burst {process['execution_time']})")
        log.append(f"Time {process['end_time']} : {process['process_id']} finished")
        current_time = process['end_time']

    for i in range(current_time, run_for):
        log.append(f"Time {i} : Idle")

    log.append(f"Finished at time {run_for}\n")

    for process in processes:
        log.append(f"{process['process_id']} wait {process['wait_time']} turnaround {process['end_time'] - process['arrival_time']} response {process['response_time']}")

    return log

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
        print(f" {input_data['processcount']} processes")

        processes = [create_process(p['name'], p['arrival'], p['burst']) for p in input_data['processes']]

        if input_data['scheduler'].lower() == 'fcfs':
            print("\nUsing First-Come First-Served")
            processes = fcfs_scheduler(processes, input_data['runfor'])
            for entry in processes:
                print(entry)

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