from dimension_reduction.data_fetch.data_fetcher import DataFetcher
from dimension_reduction.pca.dimension_reducer import DimensionReducer
from dimension_reduction.variability_and_de.variability_calculator import VariabilityCalculator
from dimension_reduction.variability_and_de.differential_expression_runner import DERunner
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='arguments for this script')
    parser.add_argument('--input', type=str, dest='input', required=True, help='directory of the output')
    return parser.parse_args()


class ProjectManager:
    def __init__(self, data_fetcher_class, dimension_reducer_class, variability_calculator_class, de_runner_class,
                 **kwargs):
        self.data_fetcher = data_fetcher_class(kwargs['input'])
        self.dimension_reducer = dimension_reducer_class(self)
        self._variability_calculator_class = variability_calculator_class
        self.variability_calculator_class = None
        self.de_runner = de_runner_class(self)

    def run(self, number):
        print('reading data')
        self.fetch_data()
        data_variability = self.select_most_variable(number)
        print('run differntial expression')
        data_variability_de = self.run_de(number)
        print('reducing dimension')
        self.pca(suffix='{}_variable'.format(number), data=data_variability)
        self.pca(suffix='{}_de'.format(number), data=data_variability_de)

    def fetch_data(self):
        self.data_fetcher.fetch_data()

    def pca(self, *args, **kwargs):
        self.dimension_reducer.pca_dimension_reduction(*args, **kwargs)

    def select_most_variable(self, number):
        self.variability_calculator_class = self._variability_calculator_class(self)
        return self.variability_calculator_class.filter_features(number)

    def run_de(self, number):
        return self.de_runner.run_limma(number)


if __name__ == '__main__':
    args = parse_args()
    for no in [10, 50, 100, 200, 400]:
        my_project = ProjectManager(data_fetcher_class=DataFetcher,
                                    dimension_reducer_class=DimensionReducer,
                                    variability_calculator_class=VariabilityCalculator,
                                    de_runner_class=DERunner,
                                    input=args.input)
        my_project.run(no)

