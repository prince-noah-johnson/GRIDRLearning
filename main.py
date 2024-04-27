import rl
import numpy as np
import os

def main():
    mode = str(input("Train (t) or Exploit (e): "))
    if mode not in ["t", "e"]:
        exit()

    world = int(input("Enter World: "))
    iterations = 2
    v = True
    epsilon = 0.9

    if mode == "t":
        q_table = rl.init_q_table()
        os.makedirs(f"./runs/world_{world}/", exist_ok=True)
        run_num = len(os.listdir(f"runs/world_{world}"))
        file_path = f"./runs/Q-table_world_{world}"
        good_term_states, bad_term_states, obstacles = [], [], []

    else:
        file_path = f"./runs/Q-table_world_{world}"
        q_table = np.load(file_path + ".npy")
        obstacles = np.load(f"./runs/obstacles_world_{world}.npy").tolist()
        good_term_states = np.load(f"./runs/good_term_states_world_{world}.npy").tolist()
        bad_term_states = np.load(f"./runs/bad_term_states_world_{world}.npy").tolist()
        run_num = len(os.listdir(f"runs/world_{world}"))

    for epoch in range(iterations):
        print(f"EPOCH #{epoch}:\n\n")
        mode_type = 'train' if mode == 't' else 'expl'
        q_table, good_term_states, bad_term_states, obstacles = rl.qlearning(
            q_table, worldId=world, mode=mode_type, learning_rate=0.0001, gamma=0.9, epsilon=epsilon,
            good_term_states=good_term_states, bad_term_states=bad_term_states, epoch=epoch, obstacles=obstacles,
            run_num=run_num, verbose=v)
        epsilon = epsilon_decay(epsilon, epoch, iterations)

    np.save(file_path, q_table)
    np.save(f"./runs/obstacles_world_{world}", obstacles)
    np.save(f"./runs/good_term_states_world_{world}", good_term_states)
    np.save(f"./runs/bad_term_states_world_{world}", bad_term_states)

def epsilon_decay(epsilon, epoch, epochs):
    return epsilon * np.exp(-0.01 * epoch)

if __name__ == "__main__":
    main()
