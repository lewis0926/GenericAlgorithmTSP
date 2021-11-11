import ga_tsp as ga
import random
import time


def generate_route(city_list, start_city, end_city):
    route = random.sample(city_list, len(city_list))

    for i in range(len(route)):
        if int(route[i].num) == end_city:
            route[i], route[-1] = route[-1], route[i]
        if int(route[i].num) == start_city:
            route[i], route[0] = route[0], route[i]

    return route


def generate_population(city_list, population_size, start_city, end_city):
    population = []

    for i in range(0, population_size):
        population.append(generate_route(city_list, start_city, end_city))

    return population


def cost_function(route):
    total_distance = 0

    # add up the distance among all cities in the route
    for i in range(0, len(route) - 1):
        total_distance += ga.calculate_distance(route[i], route[i + 1])

    return total_distance


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
            if city not in parent_route1[start:end + 1]\
                    and city is not parent_route1[0]\
                    and city is not parent_route1[len(parent_route1) - 1]:
                temp_route.append(city)

        # copy city in temp list to child_route from position end to start, except start and end cities
        i = -len(child_route) + end + 1
        j = 0
        while j < len(temp_route):
            if i != 0 and i != -1:
                child_route[i] = temp_route[j]
                j += 1
            i += 1

        return child_route


def mutation_function(route, mutation_rate):

    if random.random() < mutation_rate:
        # generate two random numbers and swap the cities at these two positions
        random_num1 = random.randint(1, len(route) - 2)
        random_num2 = random.randint(1, len(route) - 2)

        route[random_num1], route[random_num2] = route[random_num2], route[random_num1]

    return route


def run_evolution(city_list,
                  population_size,
                  crossover_rate,
                  mutation_rate,
                  elitism_size,
                  generation_limit,
                  cost_limit,
                  start_city,
                  end_city):

    start_time = time.time()
    current_population = generate_population(city_list=city_list,
                                             population_size=population_size,
                                             start_city=start_city,
                                             end_city=end_city)

    generation_number = 0
    # ga.print_performance(current_population, 0)

    for i in range(1, generation_limit + 1):

        if cost_function(current_population[0]) <= cost_limit:
            break

        new_population = []

        for j in range(0, population_size):
            parent_routes = ga.selection_function_rank_weighting(population=current_population)
            child_route = crossover_function(parent_route1=parent_routes[0],
                                             parent_route2=parent_routes[1],
                                             crossover_rate=crossover_rate)
            child_route = mutation_function(route=child_route,
                                            mutation_rate=mutation_rate)
            new_population.append(child_route)
        new_population = ga.elitism_function(current_population, new_population, elitism_size)

        current_population = sorted(new_population,
                                    key=lambda route: cost_function(route),
                                    reverse=False)
        generation_number += 1
        # ga.print_performance(current_population, i)
    end_time = time.time()

    return current_population, generation_number, end_time - start_time
