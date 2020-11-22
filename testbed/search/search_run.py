'''A script that runs a game where the search agent searches optimal path to powerup or powerups'''
import pommerman
from pommerman import agents
import json
import csv
import multiprocessing
import time


def main(env_setup_dict, search_script):
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

    # Obtain list of actions to take from search algorithm
    board = initial_state[0]['board']
    initial_position = initial_state[0]['position']

    # Create instance of search-script
    search_program = search_script.Search(board, initial_position)
    matric_number = search_program.matric_num
    script_name = search_script.__name__
    has_exceeded_time = False

    # Set time limit and start time
    TIME_LIMIT = env_setup_dict['max_duration_seconds']
    start_time = time.time()

    # Declare process and pass in relevant arguments
    run_process = multiprocessing.Process(
        target=search_program.evaluate_search, name=script_name, args=([script_name]))

    # Begin process with a set time limit before termination
    run_process.start()
    run_process.join(TIME_LIMIT)

    if(run_process.is_alive()):
        print(f"{script_name} has exceeded the time limit.")
        has_exceeded_time = True

        # Time limit exceeded, terminate method
        run_process.terminate()

        # Clean up thread
        run_process.join()

    # Monitor time elapsed
    current_time = time.time()
    elapsed_time = current_time - start_time

    # Default value of actions sequence
    actions = []

    if (not has_exceeded_time):
        # Obtain search_script output actions sequence
        with open(f'{script_name}.json') as json_file:
            output_from_script = json.load(json_file)
            if ('actions' in output_from_script.keys()):
                actions = list(output_from_script['actions'])

        # Iterate through agent actions and environment observations
        for i in range(int(env_setup_dict['max_steps'])):
            if (i >= len(actions) or done):
                break  # When agent finishes before max_steps
            curr_action = [actions[i]]
            env.render()  # comment out this line if you do not want GUI to render
            state, reward, done, info = env.step(curr_action)

    # Write output of current script into JSON
    with open(f'{script_name}.json', 'w') as outfile:
        script_data = {}
        script_data['matric_number'] = matric_number
        script_data['has_succeeded'] = done
        script_data['time_taken'] = elapsed_time
        script_data['num_steps'] = len(actions)

        json.dump(script_data, outfile)

    env.close()


if __name__ == '__main__':
    # Update following two constants that will be used to determine search script names
    # For example, the runner will iterate from search_script_1 to search_script_n
    # When NUM_SCRIPTS_TO_RUN = 2 and SCRIPT_PREFIX_NAME is 'search_script_'
    NUM_SCRIPTS_TO_RUN = 2
    SCRIPT_PREFIX_NAME = 'search_script_'

    # Load customisation parameters
    with open('env_setup.json', 'r') as f:
        env_setup_dict = json.load(f)

    # Create CSV file headers
    with open('output_file.csv', mode='w') as csv_file:
        fieldnames = ['Matric Number', 'Success?',
                      'Timing (seconds)', 'Number of Steps']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # For each search script, execute runner and collect results
        for i in range(1, NUM_SCRIPTS_TO_RUN + 1):
            script_name = SCRIPT_PREFIX_NAME + str(i)
            curr_script = __import__(script_name)

            # Execute search script, which stores its output in script_name.json
            result = main(env_setup_dict, curr_script)

            # Read output statistics from relevant json
            with open(f'{script_name}.json') as json_file:
                result = json.load(json_file)
                matric_number = result['matric_number']
                hasSucceeded = result['has_succeeded']
                time_taken = result['time_taken']
                num_steps = result['num_steps']

            writer.writerow({'Matric Number': matric_number, 'Success?': hasSucceeded,
                             'Timing (seconds)': time_taken, 'Number of Steps': num_steps})

            # Also print outcome on terminal
            if hasSucceeded:
                print(f'The algorithm of {script_name} has succeeded!')
            else:
                print(f'The algorithm of {script_name} has failed.')
