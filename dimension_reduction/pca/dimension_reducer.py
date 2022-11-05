from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import pandas as pd


class DimensionReducer:
    def __init__(self, manager):
        self.manager = manager
        self.pca = PCA()
        self.tsne = TSNE(random_state=123, perplexity=5)

    def kmeans_clustering(self, components):
        total_explained_variance = 0
        for pc, explained_variance in enumerate(self.pca.explained_variance_ratio_):
            total_explained_variance += explained_variance
            if total_explained_variance < 0.5:
                continue
            else:
                break
        X = [component[:pc] for component in components]
        x = []
        y = []
        for data_point in X:
            x.append(data_point[0])
            y.append(data_point[1])
        model = KMeans(n_clusters=3)
        # fit the model
        model.fit(X)
        # assign a cluster to each example
        yhat = model.predict(X)
        return yhat

    @staticmethod
    def explained_variance_plot(dimension_reducer, *args, **kwargs):
        plt.figure(figsize=(8, 8))
        sns.lineplot(x=['Comp_{}'.format(index) for index, _ in enumerate(dimension_reducer.explained_variance_ratio_)],
                     y=dimension_reducer.explained_variance_ratio_)
        plt.xticks(rotation=90)
        plt.ylabel('Variance explained ratio')
        if 'suffix' not in kwargs:
            plt.savefig('PCA_explained_variance.png')
            return
        plt.savefig('PCA_explained_variance_{}.png'.format(kwargs['suffix']))
        plt.close()

    def compare_group_and_cluster(self, clusters, *args, **kwargs):
        data_dict = {'0': [], '1': [], '2':[]}
        for index, cluster in enumerate(list(clusters)):
            if cluster == 0:
                data_dict['0'].append(self.original_group[index])
            elif cluster == 1:
                data_dict['1'].append(self.original_group[index])
            elif cluster == 2:
                data_dict['2'].append(self.original_group[index])
        data_to_plt = []
        groups = list(set(self.original_group))
        for k, v in data_dict.items():
            to_add = {'cluster': k}
            for group in groups:
                to_add[group] = v.count(group)
            data_to_plt.append(to_add)
        df = pd.DataFrame(data_to_plt)
        df = df.set_index(['cluster'])
        plt.figure()
        df.plot.bar(stacked=True)
        plt.xlabel("group")
        # Add a legend
        plt.legend(loc='upper left')
        if 'suffix_final' not in kwargs:
            plt.savefig('cluster_group.png')
            return
        plt.savefig('cluster_group_{}.png'.format(kwargs['suffix_final']))
        plt.close()

    @property
    def original_group(self):
        group = []
        for k, v in self.manager.data_fetcher.data.items():
            group.append(v['group'])
        return group

    @staticmethod
    def first_2_dimension_plot(components, group, *args, **kwargs):
        first_2_dimension = [component[:2] for component in components]
        x = []
        y = []
        for data_point in first_2_dimension:
            x.append(data_point[0])
            y.append(data_point[1])
        plt.figure()
        sns.scatterplot(x=x, y=y, hue=group)
        if 'suffix_final' not in kwargs:
            plt.savefig('fist_2_dimension.png')
            return
        plt.savefig('first_2_dimension_{}.png'.format(kwargs['suffix_final']))
        plt.close()

    def pca_dimension_reduction(self,  *args, **kwargs):
        if 'data' not in kwargs:
            X = np.array([v['data'] for k, v in self.manager.data_fetcher.data.items()])
        else:
            X = np.array([v['data'] for k, v in kwargs['data'].items()])
        components = self.pca.fit_transform(X)
        self.explained_variance_plot(self.pca, *args, **kwargs)
        self.first_2_dimension_plot(components,
                                    group=self.original_group,
                                    suffix_final='original_{}'.format(kwargs['suffix']))
        self.first_2_dimension_plot(components,
                                    group=self.kmeans_clustering(components),
                                    suffix_final='cluster_{}'.format(kwargs['suffix']))
        self.compare_group_and_cluster(self.kmeans_clustering(components),
                                       suffix_final='cluster_{}'.format(kwargs['suffix']))

    def tsne_dimension_reduction(self,  *args, **kwargs):
        if 'data' not in kwargs:
            X = np.array([v['data'] for k, v in self.manager.data_fetcher.data.items()])
        else:
            X = np.array([v['data'] for k, v in kwargs['data'].items()])
        components = self.tsne.fit_transform(X)
        self.first_2_dimension_plot(components, *args, **kwargs)
