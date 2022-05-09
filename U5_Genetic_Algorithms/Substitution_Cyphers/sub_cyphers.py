# March 15, Genetic Algorithms Lab 1
import random
import string as e
from math import log

real_alphabet = e.ascii_uppercase
POPULATION_SIZE = 500
NUM_CLONES = 1
TOURNAMENT_SIZE = 20
TOURNAMENT_WIN_PROBABILITY = .75
CROSSOVER_LOCATIONS = 5
MUTATION_RATE = .75
N_GRAMS = 3


def frequency_dictionary(filename):
    freq_dict = dict()
    with open(filename) as f:
        for line in f:
            tup = line.split()
            tup[1] = int(tup[1])
            freq_dict[tup[0]] = tup[1]
    return freq_dict


n_frequency = frequency_dictionary('ngrams.txt')


def encode(text, cipher_alphabet):
    text = text.upper()
    encoded_message = ''
    for char in text:
        if char in real_alphabet:
            encode_index = real_alphabet.index(char)
            encoded_message += cipher_alphabet[encode_index]
        else:
            encoded_message += char
    return encoded_message


def decode(text, cipher_alphabet):
    text = text.upper()
    decoded_message = ''
    for char in text:
        if char in cipher_alphabet:
            decode_index = cipher_alphabet.index(char)
            decoded_message += real_alphabet[decode_index]
        else:
            decoded_message += char
    return decoded_message


def fitness(encoded, cipher_alphabet, n):
    decoded = decode(encoded, cipher_alphabet)
    n_grams = []
    for i in range(len(decoded) - n + 1):
        gram = decoded[i:i + n]
        if gram.isalpha() and gram in n_frequency:
            n_grams.append(gram)
    return sum([log(n_frequency[x], 2) for x in n_grams])


def swap(c, i, j):
    c = list(c)
    c[i], c[j] = c[j], c[i]
    return ''.join(c)


def hill_climb(encoded_message):
    shuffler = list(real_alphabet)
    random.shuffle(shuffler)
    current_cipher = ''.join(shuffler)
    current_score = fitness(encoded_message, current_cipher, N_GRAMS)
    while True:
        temp_cipher = swap(current_cipher, random.randint(0, 25), random.randint(0, 25))
        new_score = fitness(encoded_message, temp_cipher, N_GRAMS)
        if new_score > current_score:
            current_cipher = temp_cipher


def create_population(population_size):
    population = set()
    shuffler = list(real_alphabet)
    while len(population) != population_size:
        random.shuffle(shuffler)
        current_cipher = ''.join(shuffler)
        population.add(current_cipher)
    return population


def scoring_dictionaries(encoded, current_generation):
    generation_scores = dict()
    sorted_scores = dict()
    for gen in current_generation:
        score = fitness(encoded, gen, N_GRAMS)
        generation_scores[gen] = score
        sorted_scores[score] = gen
    dominant_parents = [(k, sorted_scores[k]) for k in sorted(sorted_scores.keys(), reverse=True)]
    return generation_scores, dominant_parents


def initialize_next_generation_clones(dominant_parents):
    next_generation = []
    for i in range(NUM_CLONES):
        next_generation.append(dominant_parents[i])
    return next_generation


def natural_selection(current_generation, generation_scores):
    tournament_competitors = set()
    tournament_competitors = random.sample(current_generation, 2 * TOURNAMENT_SIZE)
    tournament_1 = random.sample(tournament_competitors, TOURNAMENT_SIZE)
    tournament_2 = [x for x in tournament_competitors if x not in tournament_1]
    tourney1_dict, tourney2_dict = dict(), dict()
    for competitor in tournament_1:
        tourney1_dict[generation_scores[competitor]] = competitor
    for competitor in tournament_2:
        tourney2_dict[generation_scores[competitor]] = competitor
    dominant_tourney1 = [(k, tourney1_dict[k]) for k in sorted(tourney1_dict.keys(), reverse=True)]
    dominant_tourney2 = [(k, tourney2_dict[k]) for k in sorted(tourney2_dict.keys(), reverse=True)]
    parent1, parent2, index1, index2 = None, None, 0, 0
    while parent1 is None or parent2 is None:
        if random.random() < TOURNAMENT_WIN_PROBABILITY:
            parent1 = dominant_tourney1[index1]
        else:
            index1 += 1
        if random.random() < TOURNAMENT_WIN_PROBABILITY:
            parent2 = dominant_tourney2[index2]
        else:
            index2 += 1
        if parent1 and parent2:
            break
    return parent1[1], parent2[1]


def breeding(parent1, parent2):
    if random.random() < .5:
        cross_parent = parent1
        other_parent = parent2
    else:
        cross_parent = parent2
        other_parent = parent1
    crossovers = random.sample(range(26), CROSSOVER_LOCATIONS)
    child = [None] * 26
    for cross in crossovers:
        child[cross] = cross_parent[cross]

    for char in other_parent:
        if char not in child:
            for i in range(len(child)):
                if not child[i]:
                    child[i] = char
                    break
    return ''.join(child)


def mutation(child):
    if random.random() < .8:
        ind1, ind2 = random.randint(0, 25), random.randint(0, 25)
        child = list(child)
        temp = child[ind1]
        child[ind1] = child[ind2]
        child[ind2] = temp
    return ''.join(child)


def genetic(encoded_message, generations):
    gen_number = 1
    initial_population = create_population(POPULATION_SIZE)
    while gen_number != generations:
        person_scores, sorted_by_scores = scoring_dictionaries(encoded_message, initial_population)
        print(decode(encoded_message, sorted_by_scores[0][1]))
        current_pop = set(initialize_next_generation_clones(sorted_by_scores))
        while len(current_pop) != POPULATION_SIZE:
            p1, p2 = natural_selection(initial_population, person_scores)
            current_pop.add(mutation(breeding(p1, p2)))
        gen_number += 1
        initial_population = current_pop
    max_fit, person_with_max_fit = 0, None
    for person in initial_population:
        fit = fitness(encoded_message, person, N_GRAMS)
        if fit > max_fit:
            max_fit = fit
            person_with_max_fit = person
    print('Solution:')
    print(decode(encoded_message, person_with_max_fit))


message = "ZFNNANWJWYBZLKEHBZTNSKDDGJWYLWSBFNSSJWYFNKBGLKOCNKSJEBDWZFNGKLJKJNQFJPFJBXHBZTNRDKNZFNPDEJWYDRPDEGCNZNWJYFZZFLZTCNBBNBZFNNLKZFSLKONWBLCCKJANKBPHGBZFNGNLOBLWSRDCSBZFNRJWLCBFDKNJWLWSWDTDSUWDTDSUOWDQBQFLZBYDJWYZDFLGGNWZDLWUTDSUTNBJSNBZFNRDKCDKWKLYBDRYKDQJWYDCSJZFJWODRSNLWEDKJLKZUJNANWZFJWODRDCSSNLWEDKJLKZUZFNRLZFNKQNWNANKRDHWSJZFJWODRSNLWEDKJLKZU"
genetic(message, 15000)
