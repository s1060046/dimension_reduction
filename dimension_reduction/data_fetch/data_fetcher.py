import csv
import seaborn as sns
import matplotlib.pyplot as plt


class DataFetcher:
    def __init__(self, file):
        self.file = file
        self.data = None

    def fetch_data(self):
        self.data = self.parse_data()
        self.plot_eda()

    def read_raw_data(self):
        with open(self.file, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            next(reader)
            next(reader)
            group = next(reader)[:-1]
            data = []
            for line in reader:
                data.append(line[:-1])
            data = [list(i) for i in zip(*data)]
        return group, data

    def parse_data(self):
        groups, data = self.read_raw_data()
        parsed_data = {}
        groups = [group.replace('#!{C:Grouping}' , '') for group in groups]
        for index, group in enumerate(groups):
            parsed_data['sample_{}'.format(index)] = {'group': group, 'data':[], 'boolean': [], 'some_last_number':[]}
            for dat in data[index]:
                split_data = dat.split(";")
                parsed_data['sample_{}'.format(index)]['data'].append(float(split_data[0]))
                parsed_data['sample_{}'.format(index)]['boolean'].append(split_data[1])
                parsed_data['sample_{}'.format(index)]['some_last_number'].append(split_data[2])
        return parsed_data

    def plot_eda(self):
        """
        to test if the data exists in the same scale
        :return:
        """
        plt.figure()
        for k,v in self.data.items():
            sns.kdeplot(v['data'], fill=True)
        plt.savefig('density_raw_data.png')
