import ga_tsp as ga
import random
import time


def check_sequence(route, sequence):
    sequence_to_check = []

    for city in route:
        if int(city.num) in sequence:
            sequence_to_check.append(int(city.num))

    return sequence_to_check == sequence


def generate_route(city_list, sequence):
    route = random.sample(city_list, len(city_list))

    while not check_sequence(route, sequence):
        route = random.sample(city_list, len(city_list))

    return route


def generate_population(city_list, population_size, sequence):
    population = []

    for i in range(0, population_size):
        population.append(generate_route(city_list, sequence))

    return population


def crossover_operation(parent_route1, parent_route2):

    child_route = []
    for city in parent_route1:
        child_route.append(city)

    random_num1 = random.randint(0, len(parent_route1) - 1)
    random_num2 = random.randint(0, len(parent_route1) - 1)

    start = min(random_num1, random_num2)
    end = max(random_num1, random_num2)

    # store city in route 2 which does not include
    # city in parent_route1[start:end + 1] to a temp list
    temp_route = []
    for city in parent_route2:
        if city not in parent_route1[start:end + 1]:
            temp_route.append(city)

    # copy city in temp list to child_route from position end to start
    i = -len(child_route) + end + 1
    for j in range(0, len(temp_route)):
        child_route[i] = temp_route[j]
        i += 1

    return child_route


def crossover_function(parent_route1, parent_route2, crossover_rate, sequence):

    # do not crossover and return cities from parent_route1 directly
    if random.random() > crossover_rate:
        child_route = []

        for city in parent_route1:
            child_route.append(city)

        return child_route
    else:
        child_route = crossover_operation(parent_route1, parent_route2)
        while not check_sequence(child_route, sequence):
            child_route = crossover_operation(parent_route1, parent_route2)

        return child_route


def mutation_operation(route):

    # initiate output route
    mutated_route = []
    for city in route:
        mutated_route.append(city)

    # generate two random numbers and swap the cities at these two positions
    random_num1 = random.randint(0, len(mutated_route) - 1)
    random_num2 = random.randint(0, len(mutated_route) - 1)

    mutated_route[random_num1], mutated_route[random_num2] = mutated_route[random_num2], mutated_route[random_num1]

    return mutated_route


def mutation_function(route, mutation_rate, sequence):

    if random.random() > mutation_rate:
        return route
    else:
        mutated_route = mutation_operation(route)
        while not check_sequence(mutated_route, sequence):
            mutated_route = mutation_operation(route)

    return mutated_route


def run_evolution(city_list,
                  population_size,
                  crossover_rate,
                  mutation_rate,
                  elitism_size,
                  generation_limit,
                  cost_limit,
                  sequence):

    start_time = time.time()
    current_population = generate_population(city_list=city_list,
                                             population_size=population_size,
                                             sequence=sequence)

    generation_number = 0
    # ga.print_performance(current_population, 0)

    for i in range(1, generation_limit + 1):

        if ga.cost_function(current_population[0]) <= cost_limit:
            break

        new_population = []

        for j in range(0, population_size):
            parent_routes = ga.selection_function_rank_weighting(current_population)
            child_route = crossover_function(parent_route1=parent_routes[0],
                                             parent_route2=parent_routes[1],
                                             crossover_rate=crossover_rate,
                                             sequence=sequence)
            child_route = mutation_function(route=child_route,
                                            mutation_rate=mutation_rate,
                                            sequence=sequence)
            new_population.append(child_route)
        new_population = ga.elitism_function(parent_population=current_population,
                                             child_population=new_population,
                                             elitism_size=elitism_size)

        current_population = sorted(new_population,
                                    key=lambda route: ga.cost_function(route),
                                    reverse=False)
        generation_number += 1
        # ga.print_performance(current_population, i)
    end_time = time.time()

    return current_population, generation_number, end_time - start_time
