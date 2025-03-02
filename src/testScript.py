import os
import time
import json
import matplotlib.pyplot as plt
import subprocess  # Use subprocess to capture output

def timeMapper(mappers, reducers):
    # Read the configuration file
    file_path = os.path.join(os.getcwd(), 'page-rank-config.json')
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)

    # Update the number of mappers and reducers
    config['mappers'] = mappers
    config['reducers'] = reducers

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
    total_time = end_time - start_time

    # Parse the output to extract mapper and reducer times
    output = result.stdout
    mapper_time = None
    reducer_time = None

    for line in output.split('\n'):
        if "Mapper Time:" in line:
            mapper_time = float(line.split(":")[1].strip().split()[0])
        elif "Reducer Time:" in line:
            reducer_time = float(line.split(":")[1].strip().split()[0])

    return mapper_time, reducer_time, total_time

def main():
    mapper_counts = [2, 4, 8, 16]
    reducer_counts = [2, 4, 8, 16]
    results = []

    # Open a text file to append the output
    with open('output.txt', 'a') as file:
        for mappers in mapper_counts:
            for reducers in reducer_counts:
                # Run the timeMapper function
                mapper_time, reducer_time, total_time = timeMapper(mappers, reducers)

                # Write the result in the desired format to the file
                print(f"Mapper count: {mappers}, Reducer count: {reducers}, Mapper Time: {mapper_time:.6f}, Reducer Time: {reducer_time:.6f}, Total Time: {total_time:.6f}")
                file.write(f"Mapper count: {mappers}, Reducer count: {reducers}, Mapper Time: {mapper_time:.6f}, Reducer Time: {reducer_time:.6f}, Total Time: {total_time:.6f}\n")
                results.append((mappers, reducers, mapper_time, reducer_time, total_time))

    # Plot the results
    plt.figure(figsize=(12, 10))
    for i, mappers in enumerate(mapper_counts):
        plt.subplot(2, 2, i + 1)
        mapper_times = [result[2] for result in results if result[0] == mappers]
        reducer_times = [result[3] for result in results if result[0] == mappers]
        total_times = [result[4] for result in results if result[0] == mappers]

        plt.plot(reducer_counts, mapper_times, marker='o', label='Mapper Time')
        plt.plot(reducer_counts, reducer_times, marker='o', label='Reducer Time')
        plt.plot(reducer_counts, total_times, marker='o', label='Total Time')
        plt.title(f'Execution Time for {mappers} Mappers')
        plt.xlabel('Number of Reducers')
        plt.ylabel('Execution Time (seconds)')
        plt.legend()
        plt.grid(True)

    # Save the entire figure with all subplots
    plt.tight_layout()
    plt.savefig('execution_time_all.png')
    plt.close()

if __name__ == "__main__":
    main()