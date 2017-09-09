#markov.py
#11 - July - 2017

#public for import -----------------------------------
def markov(state_sequence) :
    unique_states = find_uniques(state_sequence)
    
    transition = initialize_transition(unique_states)
    
    count_transition(transition, state_sequence)
    
    normalize(transition)

    return unique_states ,transition

#private for internal use ----------------------------
def find_uniques(state_sequence) :
    return sorted(list(set(state_sequence)))

def initialize_transition(unique_states) :
    transition = {}
    
    for state_from in unique_states :
        transition[state_from] = {}
        for state_to in unique_states :
            transition[state_from][state_to] = 0

    return transition

def count_transition(transition_dict, state_sequence) :
    current_state = state_sequence[0]
    
    for next_state in state_sequence[1:] :
        transition_dict[current_state][next_state] += 1
        current_state = next_state
    
    
def normalize(transition_dict) :
    for row_dict in transition_dict.values() :
        row_summation = sum(row_dict.values())
        
        for key in row_dict :
            row_dict[key] /= row_summation

    return transition_dict

#test and an example usage ----------------------------------------
def test_markov() :
    text = 'aassddaaffaassddffaassddffssaadd'
    states, prob = markov(text)

    print('\t' + '\t'.join(map(str, states)))
    for a in states :
        print(a,end='\t')
        for b in states :
            transition_prob = prob[a][b]
            print(format(transition_prob,'.3f'), end='\t')
        print()

    print()
    print('prob from d to a is :', prob['d']['a'])

    from nxpd import nxpdParams, draw
    import networkx as nx
    nxpdParams['show'] = 'ipynb'

    #installation fix
    #pip install --global-option=build_ext --global-option="-I/usr/local/Cellar/graphviz/2.38.0/include/"  --global-option="-L/usr/local/Cellar/graphviz/2.38.0/lib/" pygraphviz

    G = nx.DiGraph()
    # G.graph['rankdir'] = 'LR'
    G.graph['dpi'] = 120
    # G.add_cycle(range(4))
    G.add_node(0, label='a')
    # G.add_node(0, color='red', style='filled', fillcolor='pink')
    G.add_node(1, shape='square')
    G.add_node(3, style='filled', fillcolor='#00ffff')
    G.add_edge(0, 1, color='red', style='dashed')
    G.add_edge(3, 3, label='a')
    draw(G)
    
if __name__ == '__main__' :
    test_markov()


