from generator import generate_cases
from functools import reduce
from math import factorial
from operator import add

def combination(n, r):
    return factorial(n)//factorial(n-r)//factorial(r)

def evaluate(case):
    win_rate = 0.5
    win_count = 0
    lose_count = 0
    play_count = 0
    
    score = 0
    
    for win in case :
        win_probability = combination(play_count+1, win_count+1)/(2**(play_count+1))
            
        lot = win_probability
        score += lot if win else -lot
            
        play_count += 1
        win_count += win
        lose_count += 1-win
    
    return score
        
if __name__ == '__main__' :
    n = 4
    cases = generate_cases(n)
    num_cases = len(cases)
    evaluation = list(map(evaluate, cases))
    overall_score = sum(evaluation)
    
    print(overall_score/num_cases)
    print('finished')