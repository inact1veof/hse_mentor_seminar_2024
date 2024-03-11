from Task import Task
from LNSOptimizer import LNSOptimizer
import vrplib
import os
import time
import json
import matplotlib.pyplot as plt


def draw_graph(points, lines, task_name, cost, n, q):
    # Построение графика маршрутов по аналогу с версией сайта
    x = [point[0] for point in points]
    y = [point[1] for point in points]

    plt.figure(figsize=(8, 6))

    route_colors = {}
    for i, line in enumerate(lines):
        color = plt.cm.jet(i / len(lines))
        route_colors[i] = color

    for i, line in enumerate(lines):
        if len(line) > 1:
            color = route_colors[i]
            plt.plot([x[j] for j in line], [y[j] for j in line], marker='o', linestyle='-', color=color,
                     label=f'Route {i + 1}')

    plt.scatter(x, y, color='blue')

    for line in lines:
        if len(line) > 1:
            color = route_colors[lines.index(line)]
            for endpoint in [line[0], line[-1]]:
                plt.plot([x[0], x[endpoint]], [y[0], y[endpoint]], linestyle='--', color=color)

    plt.title(f'{task_name} (n={n}, Q = {q}), cost = {cost}')
    plt.grid(True)
    plt.legend()
    plt.show()

def calculate_mape(actual, forecast):
    return abs((actual - forecast) / actual)

def solution_proccess(directory, inst_ext, sol_ext):
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if file.endswith(inst_ext):
            if file.endswith(inst_ext):
                instance = vrplib.read_instance(file_path)
                solution = solution = vrplib.read_solution(file_path[:-4] + sol_ext)

                task = Task(task_name=instance['name'],
                            num_cars=len(solution['routes']),
                            num_customers=instance['dimension'],
                            depot_index=instance['depot'][0],
                            positions=[],
                            demands=instance['demand'],
                            edge_weight=instance['edge_weight'],
                            capacities=[instance['capacity']] * len(solution['routes']),
                            opt_cost=solution['cost'])
                iteration_start = time.time()
                # бейзлайн
                task._make_base_routes()
                task._calc_routes_cost()
                best_baseline = task
                best_accuracy = 0.2       # затычка
                final_sol = best_baseline
                start_time = time.time()
                while best_accuracy < 0.8:
                    task = best_baseline
                    task.routes = []
                    task._make_base_routes()
                    task._calc_routes_cost()
                    lns_optimizer = LNSOptimizer(task, max_iterations=1000, max_no_improvement=1000,
                                                 initial_destroy_size=1, max_destroy_size=22)
                    best_solution = lns_optimizer.solve()
                    best_solution._calc_routes_cost()
                    new_accuracy = 1 - calculate_mape(solution['cost'], best_solution.calculated_cost)
                    if new_accuracy > best_accuracy:
                        best_accuracy = new_accuracy
                        final_sol = best_solution
                    if time.time() - start_time >= 180:
                        break

                best_solution = final_sol
                iteration_end = time.time()
                result_item = {'task_name': best_solution.task_name, 'routes': best_solution.routes,
                               'cost': best_solution.calculated_cost,
                               'accuracy': 1 - calculate_mape(solution['cost'], best_solution.calculated_cost),
                               'n': instance['dimension'], 'time': iteration_end - iteration_start}
                results.append(result_item)
                print(
                    f"Task: {result_item['task_name']} | Accuracy: {result_item['accuracy']} | Time: {iteration_end - iteration_start}")

data_path = "/home/inact1ve/HSE/pmii_folder/cvrp/data"
sets = ['A', 'B', 'E']
instance_ext = '.vrp'
solution_ext = '.sol'

results = []
solution_proccess(data_path + '/' + sets[1], instance_ext, solution_ext)








