# dimension_reduction

## Usage

see main.py script

ProjectManager takes data_fetcher_class, dimension_reducer_class, variability_calculator_class, de_runner_class and an input file

run method carries out the analysis with an integer as argument. this is the number of features used for dimension reduction

``` python
from dimension_reduction.data_fetch.data_fetcher import DataFetcher
from dimension_reduction.pca.dimension_reducer import DimensionReducer
from dimension_reduction.variability_and_de.variability_calculator import VariabilityCalculator
from dimension_reduction.variability_and_de.differential_expression_runner import DERunner
from dimension_reduction.manger import ProjectManager


my_project = ProjectManager(data_fetcher_class=DataFetcher,
                            dimension_reducer_class=DimensionReducer,
                            variability_calculator_class=VariabilityCalculator,
                            de_runner_class=DERunner,
                            input=<inputfile>)
my_project.run(10)
```
