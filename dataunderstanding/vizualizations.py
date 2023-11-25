from matplotlib import pyplot as plt

plt.rcParams["figure.figsize"] = (20,10)

# plot a bar of the data
def plot_bar(data, title, xlabel, ylabel):
    plt.figure()
    plt.barh(data.index, data.values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show(block=True)

def plot_histogram(data, title, xlabel, ylabel, bins=10):
    plt.figure()
    plt.hist(data, bins=bins)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()