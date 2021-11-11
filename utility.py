import random
import ga_tsp as ga
import ga_given_start_end as ga_gse
import matplotlib.pyplot as plt
import ga_atsp


def read_file(filename):
    city_list = []
    file = open(filename, "r")
    lines = file.readlines()

    # skip line 1 of column titles
    del lines[0]

    for line in lines:
        data = line.split(',')
        city_list.append(ga.City(data[0].strip(),
                                 float(data[1].strip()),
                                 float(data[2].strip())))

    return city_list


def read_file_distance_atsp(filename):
    distance_dict = {}
    file = open(filename, "r")
    lines = file.readlines()

    # skip line 1 of column titles
    del lines[0]

    for line in lines:
        data = line.split(',')
        distance_dict[f"{data[0]}-{data[1]}"] = data[2]

    return distance_dict


def read_file_only_coordinates(filename):
    city_list = []
    file = open(filename, "r")
    lines = file.read().splitlines()

    i = 1

    # hard code to extract data because string.strip() does not work
    for line in lines:
        if line.strip() != "":
            if line[0] == ' ':
                x = line[1]
            else:
                x = line[0:1]
            if line[3] == ' ':
                y = line[4]
            else:
                y = line[3:4]
            city_list.append(ga.City(i,
                                     float(x),
                                     float(y)))
            i += 1

    return city_list


def read_clustering_result(filename):
    cluster_result_list = []
    file = open(filename, "r")
    lines = file.read().splitlines()

    for line in lines:
        cluster_result_list.append(line.strip())

    return cluster_result_list


def print_route_cost(route, one_way):
    print("best route:", end=" ")
    for city in route:
        print(city.num, end=" ")
    if one_way:
        print(f"\tcost: {ga_gse.cost_function(route)}")
    else:
        print(f"\tcost: {ga.cost_function(route)}")


def print_route_cost_atsp(route, distance_dict):
    print("best route:", end=" ")
    for city in route:
        print(city.num, end=" ")
    print(f"\tcost: {ga_atsp.cost_function(route, distance_dict)}")


def find_global_min(route_list, one_way):
    min_route = None
    for route in route_list:
        if min_route is None:
            min_route = route
        if one_way:
            if ga_gse.cost_function(route) < ga_gse.cost_function(min_route):
                min_route = route
        else:
            if ga.cost_function(route) < ga.cost_function(min_route):
                min_route = route
    print("global min ", end="")
    print_route_cost(min_route, one_way)
    return min_route


def find_global_min_atsp(route_list, distance_dict):
    min_route = None
    for route in route_list:
        if min_route is None:
            min_route = route
        if ga_atsp.cost_function(route, distance_dict) < ga_atsp.cost_function(min_route, distance_dict):
            min_route = route
    print("global min ", end="")
    print_route_cost_atsp(min_route, distance_dict)
    return min_route


def average(num_list):
    return sum(num_list) / len(num_list)


def plot_performance_double(x, y1, y2, x_label, y1_label, y2_label, title, log_flag):
    fig, ax1 = plt.subplots()

    color = "tab:blue"

    if log_flag:
        ax1.set_xscale("log")
    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y1_label, color=color)
    ax1.plot(x, y1, color=color)
    ax1.tick_params(axis='y')

    ax2 = ax1.twinx()

    color = "tab:orange"
    ax2.set_ylabel(y2_label, color=color)
    ax2.plot(x, y2, color=color)
    ax2.tick_params(axis='y')

    fig.suptitle(title)
    plt.show()


def plot_performance(x, y, x_label, y_label, title):
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


def add_more_cities(city_list, add_city_num):
    for i in range(11, 11 + add_city_num):
        city_list.append(ga.City(i, random.random(), random.random()))

