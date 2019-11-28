import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plt_test():
    fig, axes = plt.subplots(2, 1)
    data = pd.Series(np.random.rand(16), index=list('abcdefghijklmnop'))
    data.plot.bar(ax=axes[0], color='k', alpha=0.7)
    data.plot.barh(ax=axes[1], color='k', alpha=0.7)
    df = pd.DataFrame(np.random.rand(6, 4),
                      index=['one', 'two', 'three', 'four', 'five', 'six'],
                      columns=pd.Index(['A', 'B', 'C', 'D'], name='Genus'))
    df.plot.bar()
    plt.show()


def np_test():
    data = np.random.randn(2, 3)
    print(data)


if __name__ == '__main__':
    # plt_test()
    np_test()


