'''A script that runs a game where the simple agent searches optimal path to powerup'''
import pommerman
from pommerman import agents
import json
import csv
import multiprocessing
import time
# from a0123456Z import Search
from a6543210Z import Search


def main(env_setup_dict):
    '''Simple function to bootstrap a game.'''

    # Create a Search Agent
    agent_list = [
        agents.SearchAgent()
    ]

    # Make the "Search" environment using the agent list and setup parameters
    env = pommerman.make('Search-v0', agent_list, env_setup=env_setup_dict)

    # Construct a clean slate environment
    initial_state = env.reset()
    done = False

    # Set time limit and start time
    time_limit = env_setup_dict['max_duration_seconds']
    start_time = time.time()

    # obtain list of actions to take from search algorithm
    board = initial_state[0]['board']
    initial_position = initial_state[0]['position']

    search_program = Search(board, initial_position)
    matric_number = search_program.matric_num
    actions = search_program.search()

    # Monitor time elapsed
    current_time = time.time()
    elapsed_time = current_time - start_time

    # Terminate program if time limit exceeded
    if elapsed_time > time_limit:
        print("Your algorithm has exceeded the time limit.")
        return (matric_number, elapsed_time, '-', done)

    # Iterate through agent actions and environment observations
    for i in range(int(env_setup_dict['max_steps'])):
        # When agent finishes before max_steps
        if (done):
            break

        curr_action = [actions[i]]
        env.render()
        state, reward, done, info = env.step(curr_action)

    return (matric_number, elapsed_time, len(actions), done)

    env.close()


if __name__ == '__main__':
    # Load customisation parameters
    with open('env_setup.json', 'r') as f:
        env_setup_dict = json.load(f)

    # Execute main runner script and collect results
    result = main(env_setup_dict)
    matric_number = result[0]
    time_taken = result[1]
    num_steps = result[2]
    hasSucceeded = result[3]

    # Output statistics into a CSV file
    with open('output_file.csv', mode='w') as csv_file:
        fieldnames = ['Matric Number', 'Success?',
                      'Timing (seconds)', 'Number of Steps']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Matric Number': matric_number, 'Success?': hasSucceeded,
                         'Timing (seconds)': time_taken, 'Number of Steps': num_steps})

    # Also print outcome on terminal
    if hasSucceeded:
        print('The algorithm has succeeded!')
    else:
        print('The algorithm has failed.')
