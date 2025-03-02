import os
import time
import json
import subprocess
import sys

def timeMapper(mappers, reducers, input_path):
    # Read the configuration file
    file_path = os.path.join(os.getcwd(), 'page-rank-config.json')
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)

    # Update the number of mappers and reducers
    config['mappers'] = mappers
    config['reducers'] = reducers
    config['input_path'] = input_path

    # Write the updated configuration back to the file
    with open(file_path, 'w') as config_file:
        json.dump(config, config_file, indent=4)

    # Measure the time for the MapReduce job
    start_time = time.time()
    
    # Use subprocess to capture the output of mapreduce.py
    result = subprocess.run(
        ['python3', 'mapreduce.py', '--config_path', file_path, '--execution_mode', 'driver'],
        capture_output=True,
        text=True
    )
    
    end_time = time.time()

    # Parse the output to extract mapper and reducer times
    output = result.stdout
    mapper_time = None
    reducer_time = None

    for line in output.split('\n'):
        if "Mapper Time:" in line:
            mapper_time = float(line.split(":")[1].strip().split()[0])
        elif "Reducer Time:" in line:
            reducer_time = float(line.split(":")[1].strip().split()[0])

    # Calculate total time as the sum of mapper and reducer times
    total_time = mapper_time + reducer_time

    # Log the times for debugging
    # print(f"Mapper Time: {mapper_time:.6f} seconds")
    # print(f"Reducer Time: {reducer_time:.6f} seconds")
    # print(f"Total Time: {total_time:.6f} seconds")

    return mapper_time, reducer_time, total_time

def main(dataset_size):
    mapper_counts = [2, 4, 8, 16]
    reducer_counts = [2, 4, 8, 16]
    results = []
    # Determine the dataset path based on the dataset_size argument
    if dataset_size == 'large':
        dataset_path = 'data-pr/input-large.txt'
    elif dataset_size == 'small':
        dataset_path = 'data-pr/input-small.txt'
    elif dataset_size == 'mini':
        dataset_path = 'data-pr/input-mini.txt'
    else:
        raise ValueError("Invalid dataset size. Choose from 'large', 'small', or 'mini'.")

    # Open a text file to append the output
    with open('output.txt', 'a') as file:
        for mappers in mapper_counts:
            for reducers in reducer_counts:
                # Run the timeMapper function
                mapper_time, reducer_time, total_time = timeMapper(mappers, reducers, dataset_path)

                # Write the result in the desired format to the file
                print(f"{mappers}M-{reducers}R, Mapper Time: {mapper_time:.6f}, Reducer Time: {reducer_time:.6f}, Total Time: {total_time:.6f}")
                file.write(f"{mappers}M-{reducers}R, Mapper Time: {mapper_time:.6f}, Reducer Time: {reducer_time:.6f}, Total Time: {total_time:.6f}\n")
                results.append({
                    "mappers": mappers,
                    "reducers": reducers,
                    "mapper_time": mapper_time,
                    "reducer_time": reducer_time,
                    "total_time": total_time
                })

    # Save results to a JSON file
    with open('results.json', 'w') as json_file:
        json.dump(results, json_file, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 testScript.py <dataset_size>")
        sys.exit(1)
    dataset_size = sys.argv[1]
    main(dataset_size)