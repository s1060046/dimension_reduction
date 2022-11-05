import csv
import subprocess


class DERunner:
    def __init__(self, manager):
        self.manager = manager

    def run_limma(self, number):
        self.write_data()
        self.run_r_script()
        return self.generate_data(number)

    def generate_data(self, number):
        index = []
        with open('dimension_reduction/r_scripts/tmp_data/limma_res.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for no, line in enumerate(reader):
                if no < number:
                    index.append(int(line[0].split('_')[1]))
        data_to_export = {}
        for k, v in self.manager.data_fetcher.data.items():
            data_to_export[k] = dict(v)
            data_to_export[k]['data'] = [data_to_export[k]['data'][ind] for ind in index]
        return data_to_export

    def write_data(self):
        samples = []
        metadata_to_write = []
        for k, v in self.manager.data_fetcher.data.items():
            end_of_range = len(v['data'])
            samples.append(k)
            metadata_to_write.append({'sample': k, 'group': v['group']})

        data_to_write = []
        for index in range(end_of_range):
            line = {'feature_id': 'feature_{}'.format(index)}
            for sample in samples:
                line[sample] = self.manager.data_fetcher.data[sample]['data'][index]
            data_to_write.append(line)

        with open('dimension_reduction/r_scripts/tmp_data/expression.csv', 'w+') as f:
            writer = csv.DictWriter(f, ['feature_id'] + samples)
            writer.writeheader()
            writer.writerows(data_to_write)

        with open('dimension_reduction/r_scripts/tmp_data/metadata.csv', 'w+') as f:
            writer = csv.DictWriter(f, ['sample', 'group'])
            writer.writeheader()
            writer.writerows(metadata_to_write)

    @staticmethod
    def run_r_script():
        cmd = 'Rscript dimension_reduction/r_scripts/limma.R'
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        process.wait()


