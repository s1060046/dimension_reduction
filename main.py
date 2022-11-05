from dimension_reduction.data_fetch.data_fetcher import DataFetcher
from dimension_reduction.pca.dimension_reducer import DimensionReducer
from dimension_reduction.variability_and_de.variability_calculator import VariabilityCalculator
from dimension_reduction.variability_and_de.differential_expression_runner import DERunner
from dimension_reduction.manger import ProjectManager
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='arguments for this script')
    parser.add_argument('--input', type=str, dest='input', required=True, help='directory of the output')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    for no in [10, 50, 100, 200, 400]:
        my_project = ProjectManager(data_fetcher_class=DataFetcher,
                                    dimension_reducer_class=DimensionReducer,
                                    variability_calculator_class=VariabilityCalculator,
                                    de_runner_class=DERunner,
                                    input=args.input)
        my_project.run(no)

