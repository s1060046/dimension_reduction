import numpy as np


class VariabilityCalculator:
    def __init__(self, manager):
        self.manager = manager
        self.cv_list = None

    def calculate_variability(self):
        X = np.array([list(i) for i in zip(*[v['data'] for k, v in self.manager.data_fetcher.data.items()])])
        self.cv_list = [abs(np.std(i)/np.mean(i)) for i in X]

    def filter_features(self, number):
        self.calculate_variability()
        sort_list = list(sorted(self.cv_list, reverse=True))
        index = [index for index, cv in enumerate(self.cv_list) if cv > sort_list[number]]
        data_to_export = {}
        for k, v in self.manager.data_fetcher.data.items():
            data_to_export[k] = dict(v)
            data_to_export[k]['data'] = [data_to_export[k]['data'][ind] for ind in index]
        return data_to_export