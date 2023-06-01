import random
sig_num = 10

def main():
    counter = 0
    sctr = {0: 0, 1: 0, 2: 0}
    sig_dict = {0: 'noise', 1: 'drone', 2: 'control'}
    while True:
        label = random.randint(0, 2)
        sctr[label] += 1
        counter += 1
        if counter == sig_num:
            values = [sctr[key] for key in sctr.keys()]
            max_num = max(values)
            lbl = values.index(max_num)
            print(f'signal is {sig_dict[lbl]} because detected {max_num}/{sig_num}')
            counter = 0
            sctr = {0: 0, 1: 0, 2: 0}



if __name__ == "__main__":
    main()