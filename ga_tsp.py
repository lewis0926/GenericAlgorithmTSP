import random
import numpy as np
import time


class City:
    def __init__(self, num, x, y):
        self.num = num
        self.x = x
        self.y = y


def calculate_distance(from_city, to_city):
    return np.sqrt((to_city.x - from_city.x) ** 2 +
                   (to_city.y - from_city.y) ** 2)


def generate_route(city_list):
    return random.sample(city_list, len(city_list))


def generate_population(city_list, population_size):
    population = []

    for i in range(0, population_size):
        population.append(generate_route(city_list))

    return population


def cost_function(route):
    total_distance = 0

    # add up the distance among all cities in the route
    for i in range(0, len(route) - 1):
        total_distance += calculate_distance(route[i], route[i + 1])

    # distance back to start city
    total_distance += calculate_distance(route[len(route) - 1], route[0])

    return total_distance


def selection_function_rank_weighting(population):
    # sort the population in descending order of cost
    sorted_population = sorted(population,
                               key=lambda route: cost_function(route),
                               reverse=True)

    # arrange rank to every route
    # route with lower cost has higher rank
    rank_prob = []
    for i in range(1, len(sorted_population) + 1):
        rank_prob.append(i / ((1 + len(sorted_population)) * len(sorted_population) / 2))

    # select two routes by rank weighting selection
    return random.choices(population=sorted_population,
                          weights=rank_prob,
                          k=2)


def crossover_function(parent_route1, parent_route2, crossover_rate):

    # initiate child_route by copy all cities from parent_route1 first
    child_route = []
    for city in parent_route1:
        child_route.append(city)

    # do not crossover and return cities from parent_route1 directly
    if random.random() > crossover_rate:
        return child_route
    else:
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


def mutation_function(route, mutation_rate):

    if random.random() < mutation_rate:
        # generate two random numbers and swap the cities at these two positions
        random_num1 = random.randint(0, len(route) - 1)
        random_num2 = random.randint(0, len(route) - 1)

        route[random_num1], route[random_num2] = route[random_num2], route[random_num1]

    return route


def elitism_function(parent_population, child_population, elitism_size):
    # sort parent population in ascending order of cost
    sorted_parent_population = sorted(parent_population,
                                      key=lambda route: cost_function(route),
                                      reverse=False)
    # sort child population in descending order of cost
    sorted_child_population = sorted(child_population,
                                     key=lambda route: cost_function(route),
                                     reverse=True)

    # replace worst routes in child population by parent population
    route_count = 0
    while route_count / len(parent_population) < elitism_size:
        sorted_child_population[route_count] = sorted_parent_population[route_count]
        route_count += 1

    return sorted_child_population


def print_performance(population, generation):
    print(f"generation {generation} \t"
          "best route:", end=" ")
    for city in population[0]:
        print(city.num, end=" ")
    print(f"cost: {cost_function(population[0])}")


def run_evolution(city_list,
                  population_size,
                  crossover_rate,
                  mutation_rate,
                  elitism_size,
                  generation_limit,
                  cost_limit):

    start_time = time.time()
    current_population = generate_population(city_list, population_size)
    generation_number = 0
    # print_performance(current_population, 0)

    for i in range(1, generation_limit + 1):

        if cost_function(current_population[0]) <= cost_limit:
            break

        new_population = []

        for j in range(0, population_size):
            parent_routes = selection_function_rank_weighting(population=current_population)
            child_route = crossover_function(parent_route1=parent_routes[0],
                                             parent_route2=parent_routes[1],
                                             crossover_rate=crossover_rate)
            child_route = mutation_function(route=child_route,
                                            mutation_rate=mutation_rate)
            new_population.append(child_route)
        new_population = elitism_function(current_population, new_population, elitism_size)

        current_population = sorted(new_population,
                                    key=lambda route: cost_function(route),
                                    reverse=False)
        generation_number += 1
        # print_performance(current_population, i)
    end_time = time.time()

    return current_population, generation_number, end_time - start_time
