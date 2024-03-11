import random
from typing import Union
import numpy as np


class Task:
    def __init__(self, task_name: str, num_cars: int, num_customers: int, depot_index: int,
                 positions: Union[list, np.ndarray], demands: Union[list, np.ndarray],
                 edge_weight: Union[list, np.ndarray], capacities: Union[list, np.ndarray], opt_cost: int):
        self.task_name = task_name
        self.num_cars = num_cars
        self.num_customers = num_customers
        self.depot_index = depot_index
        self.positions = positions
        self.demands = demands
        self.capacities = capacities
        self.edge_weights = edge_weight
        self.opt_cost = opt_cost
        self.calculated_cost = 0
        self.routes = []

    def _make_base_routes(self):
        # генерация базовых путей
        self.routes = [[] for _ in range(self.num_cars)]
        remaining_customers = set(range(self.num_customers))
        remaining_customers.remove(self.depot_index)

        # Мешаем случайно всех клиентов
        shuffled_customers = list(remaining_customers)
        random.shuffle(shuffled_customers)

        # Закидываем клиентов в валидные машины с соблюдением capacity, при этом ищем наименее загруженную
        for customer in shuffled_customers:
            #
            valid_cars = [car for car in range(self.num_cars) if self._check_capacity_constraint(car, customer)]
            if valid_cars:
                min_load_car = min(valid_cars, key=lambda x: sum(self.demands[c] for c in self.routes[x]))
                self.routes[min_load_car].append(customer)
                remaining_customers.remove(customer)

        # Добавим депо
        for i in range(self.num_cars):
            self.routes[i] = [self.depot_index] + self.routes[i] + [self.depot_index]



    def _check_capacity_constraint(self, car, customer):
        # Проверка на оставшуюся емкость при добавлении клиента
        current_load = sum(self.demands[c] for c in self.routes[car])
        return current_load + self.demands[customer] <= self.capacities[car]

    def _calc_routes_cost(self):
        # считаем стоимость пути
        total_cost = 0
        for route in self.routes:
            route_cost = 0
            for i in range(len(route) - 1):
                start_node = route[i]
                end_node = route[i + 1]
                route_cost += self.edge_weights[start_node][end_node]
            total_cost += route_cost

        self.calculated_cost = total_cost