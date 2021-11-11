import ga_tsp as ga
import ga_given_start_end as ga_gse
import time
import utility as util


def map_clustering(city_list, clustering_list):
    cluster1 = []
    cluster2 = []
    cluster3 = []

    i = 0
    for cluster_result in clustering_list:
        if int(cluster_result) == 0:
            cluster1.append(city_list[i])
        elif int(cluster_result) == 1:
            cluster2.append(city_list[i])
        elif int(cluster_result) == 2:
            cluster3.append(city_list[i])
        i += 1

    return cluster1, cluster2, cluster3


def combine_route(route_list):
    result_route_list = []
    for route in route_list:
        for city in route:
            result_route_list.append(city)

    return result_route_list


def run_evolution(city_list,
                  population_size,
                  crossover_rate,
                  mutation_rate,
                  elitism_size,
                  generation_limit,
                  cost_limit):

    start_time = time.time()
    current_population = ga.generate_population(city_list, population_size)
    generation_number = 0
    # print_performance(current_population, 0)

    for i in range(1, generation_limit + 1):

        if ga_gse.cost_function(current_population[0]) <= cost_limit:
            break

        new_population = []

        for j in range(0, population_size):
            parent_routes = ga.selection_function_rank_weighting(population=current_population)
            child_route = ga.crossover_function(parent_route1=parent_routes[0],
                                                parent_route2=parent_routes[1],
                                                crossover_rate=crossover_rate)
            child_route = ga.mutation_function(route=child_route,
                                               mutation_rate=mutation_rate)
            new_population.append(child_route)
        new_population = ga.elitism_function(current_population, new_population, elitism_size)

        current_population = sorted(new_population,
                                    key=lambda route: ga_gse.cost_function(route),
                                    reverse=False)
        generation_number += 1
        # print_performance(current_population, i)
    end_time = time.time()

    return current_population, generation_number, end_time - start_time


def run_evolution_clustering(population_size,
                             crossover_rate,
                             mutation_rate,
                             elitism_size,
                             generation_limit,
                             cost_limit,
                             cluster_list):
    cluster_route_list = []

    for cluster in cluster_list:
        best_route_list = []

        for i in range(10):
            result = run_evolution(city_list=cluster,
                                   population_size=population_size,
                                   crossover_rate=crossover_rate,
                                   mutation_rate=mutation_rate,
                                   elitism_size=elitism_size,
                                   generation_limit=generation_limit,
                                   cost_limit=cost_limit)
            print(f"run: {i + 1}", end="\t")
            util.print_route_cost(result[0][0], one_way=True)
            best_route_list.append(result[0][0])

        cluster_route_list.append(best_route_list)
        # cluster_route_list.append(util.find_global_min(best_route_list, one_way=True))

    result_route_list = []
    for route1 in cluster_route_list[0]:
        for route2 in cluster_route_list[1]:
            for route3 in cluster_route_list[2]:
                result_route = []
                for city in route1:
                    result_route.append(city)
                for city in route2:
                    result_route.append(city)
                for city in route3:
                    result_route.append(city)
                result_route_list.append(result_route)

    util.find_global_min(result_route_list, one_way=True)

