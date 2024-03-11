from Task import Task
import random

class LNSOptimizer:
    def __init__(self, task: Task, max_iterations: int = 100, max_no_improvement: int = 20,
                 initial_destroy_size: int = 2, max_destroy_size: int = 12):
        self.task = task
        self.max_iterations = max_iterations
        self.max_no_improvement = max_no_improvement
        self.initial_destroy_size = initial_destroy_size
        self.max_destroy_size = max_destroy_size

    def _destroy_operator(self, num_string_removals: int, max_string_size: int):
        # Удаляем часть пути с параметром количества и максимальный размер удаляемого пути
        destroyed_routes = []
        for _ in range(num_string_removals):
            route_index = random.randint(0, self.task.num_cars - 1)
            route = self.task.routes[route_index]
            if len(route) > 0:
                num_nodes_to_remove = random.randint(1, min(len(route), max_string_size))
                removed_nodes = random.sample(route, num_nodes_to_remove)
                for node in removed_nodes:
                    route.remove(node)
                destroyed_routes.append((route_index, removed_nodes))
        return destroyed_routes

    def _repair_operator(self, destroyed_routes):
        repaired_task = self.task
        for route_index, removed_nodes in destroyed_routes:
            route = repaired_task.routes[route_index]
            # Допустимое восстановление - вставляем удаленные узлы в маршрут с учетом ограничений на грузоподъемность
            for node in removed_nodes:
                best_insertion_index = self._find_best_insertion_index(node, route)
                route.insert(best_insertion_index, node)
        return repaired_task

    def _find_best_insertion_index(self, node, route):
        # Локальный поиск лучшего места для вставки
        best_index = 0
        best_cost = float('inf')
        for i in range(len(route) + 1):
            # Проверяем ограничения на грузоподъемность
            if self._check_capacity_constraint(node, route[:i] + [node] + route[i:]):
                route_cost = self._calculate_route_cost(route[:i] + [node] + route[i:], self.task)
                if route_cost < best_cost:
                    best_index = i
                    best_cost = route_cost
        return best_index

    def _check_capacity_constraint(self, node, route):
        route_demand = sum(self.task.demands[node] for node in route)
        return route_demand <= self.task.capacities[0]

    def solve(self):
        best_solution = self.task
        best_cost = self.task.calculated_cost
        no_improvement_count = 0
        num_string_removals = self.initial_destroy_size
        max_string_size = self.max_destroy_size

        for i in range(self.max_iterations):
            destroyed_routes = self._destroy_operator(num_string_removals, max_string_size)
            repaired_solution = self._repair_operator(destroyed_routes)
            repaired_solution._calc_routes_cost()

            if repaired_solution.calculated_cost < best_cost:
                best_solution = repaired_solution
                best_cost = repaired_solution.calculated_cost
                no_improvement_count = 0
            else:
                no_improvement_count += 1

            if no_improvement_count >= self.max_no_improvement:
                break

            # Попытка в адаптивность, если нет улучшений, то увеличиваем чисто разрушений
            if no_improvement_count % 5 == 0:
                num_string_removals += 1
                max_string_size = min(max_string_size + 1, self.task.num_customers)

        final_routes = best_solution.routes
        for array in final_routes:
            array[:] = [x for x in array if x != 0]
        best_solution.routes = final_routes
        return best_solution

    def _calculate_route_cost(self, route, task):
        # Подсчет стоимости одного пути
        route_cost = 0
        for i in range(len(route) - 1):
            start_node = route[i]
            end_node = route[i + 1]
            route_cost += task.edge_weights[start_node][end_node]
        return route_cost