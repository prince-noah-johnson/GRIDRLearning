import numpy as np
import Requests

def init_q_table():
      return (np.zeros((40, 40, 4)))

def direction(index):
    actions = ['N', 'S', 'E', 'W', 'ERROR!']
    return actions[index] if index < 4 else actions[-1]


def qlearning(q_table, worldId=0, learning_rate=0.001, gamma=0.9, epsilon=0.9, good_term_states=[], bad_term_states=[], epoch=0, obstacles=[], run_num=0, verbose=True):
    a = Requests.Requests(worldId=worldId)
    a.enter_world()

    end_state = False
    good = False
    rewards_acquired = []
    visited = []
    
    loc_world, loc_state = a.get_location()
    location = tuple(map(int, loc_state.split(':')))

    board_size = 40
    grid = [[float('-inf')] * board_size for _ in range(board_size)]
    visited.append(location)

    while not end_state:
        grid[location[1]][location[0]] = 1
        for i in range(board_size):
            for j in range(board_size):
                if grid[i][j] != 0:
                    grid[i][j] -= .1
        
        obstacles = [obs for obs in obstacles if obs not in visited]

        unexplored = np.where(q_table[location[0]][location[1]].astype(int) == 0)[0]
        explored = np.where(q_table[location[0]][location[1]].astype(int) != 0)[0]
        move_num = int(np.random.choice(unexplored)) if np.random.uniform() < epsilon else np.argmax(q_table[location[0]][location[1]])
       
        move_response = a.make_move(move=direction(move_num), worldId=str(worldId)) 

        if verbose:
            print("move_response", move_response)
        
        if move_response["code"] != "OK":
            while move_response["code"] != 'OK':
                move_response = a.make_move(move=direction(move_num), worldId=str(worldId))
                print("\nReset world\n")
        
        if move_response["newState"] is not None:
            new_state = tuple(map(int, (move_response["newState"]["x"], move_response["newState"]["y"])))
            recent_move = direction(move_num)
            expected_loc = (location[0] + (recent_move == "E") - (recent_move == "W"), location[1] + (recent_move == "N") - (recent_move == "S"))
            if verbose:
                print(f"Current cell: {new_state}")
            obstacles.append(expected_loc)
            visited.append(new_state)
            obstacles = [obs for obs in obstacles if obs not in visited]
        else:
            end_state = True
       
        reward = float(move_response["reward"])
        rewards_acquired.append(reward) 

        q_table_modify(location, q_table, reward, gamma, new_state, learning_rate, move_num)
        
        location = new_state

        if end_state:
            print(f"REWARD: {reward}")
            good = reward > 0
            if location not in good_term_states and location not in bad_term_states:
                (good_term_states if good else bad_term_states).append(location)
            break

    return q_table, good_term_states, bad_term_states, obstacles 


def q_table_modify(current_pos, q_table, reward, discount_factor, next_pos, alpha, action_index):
    max_future_q = q_table[next_pos[0], next_pos[1], :].max()
    current_q = q_table[current_pos[0], current_pos[1], action_index]
    q_table[current_pos[0], current_pos[1], action_index] = current_q + alpha * (reward + discount_factor * max_future_q - current_q)
