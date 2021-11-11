import time
import random
import ga_tsp as ga


def calculate_distance(from_city, to_city, distance_dict):
    return float(distance_dict[f"{from_city.num}-{to_city.num}"])


def cost_function(route, distance_dict):
    total_distance = 0

    # add up the distance among all cities in the route
    for i in range(0, len(route) - 1):
        total_distance += calculate_distance(route[i], route[i + 1], distance_dict)

    # distance back to start city
    total_distance += calculate_distance(route[len(route) - 1], route[0], distance_dict)

    return total_distance


def selection_function_rank_weighting(population, distance_dict):
    # sort the population in descending order of cost
    sorted_population = sorted(population,
                               key=lambda route: cost_function(route, distance_dict),
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


def elitism_function(parent_population, child_population, elitism_size, distance_dict):
    # sort parent population in ascending order of cost
    sorted_parent_population = sorted(parent_population,
                                      key=lambda route: cost_function(route, distance_dict),
                                      reverse=False)
    # sort child population in descending order of cost
    sorted_child_population = sorted(child_population,
                                     key=lambda route: cost_function(route, distance_dict),
                                     reverse=True)

    # replace worst routes in child population by parent population
    route_count = 0
    while route_count / len(parent_population) < elitism_size:
        sorted_child_population[route_count] = sorted_parent_population[route_count]
        route_count += 1

    return sorted_child_population


def print_performance(population, generation, distance_dict):
    print(f"generation {generation} \t"
          "best route:", end=" ")
    for city in population[0]:
        print(city.num, end=" ")
    print(f"cost: {cost_function(population[0], distance_dict)}")


def run_evolution(city_list,
                  distance_dict,
                  population_size,
                  crossover_rate,
                  mutation_rate,
                  elitism_size,
                  generation_limit,
                  cost_limit):

    start_time = time.time()
    current_population = ga.generate_population(city_list, population_size)
    generation_number = 0
    # print_performance(current_population, 0, distance_dict)

    for i in range(1, generation_limit + 1):

        if cost_function(current_population[0], distance_dict) <= cost_limit:
            break

        new_population = []

        for j in range(0, population_size):
            parent_routes = selection_function_rank_weighting(population=current_population,
                                                              distance_dict=distance_dict)
            child_route = ga.crossover_function(parent_route1=parent_routes[0],
                                                parent_route2=parent_routes[1],
                                                crossover_rate=crossover_rate)
            child_route = ga.mutation_function(route=child_route,
                                               mutation_rate=mutation_rate)
            new_population.append(child_route)
        new_population = elitism_function(parent_population=current_population,
                                          child_population=new_population,
                                          elitism_size=elitism_size,
                                          distance_dict=distance_dict)

        current_population = sorted(new_population,
                                    key=lambda route: cost_function(route, distance_dict),
                                    reverse=False)
        generation_number += 1
        # print_performance(current_population, i, distance_dict)
    end_time = time.time()

    return current_population, generation_number, end_time - start_time


