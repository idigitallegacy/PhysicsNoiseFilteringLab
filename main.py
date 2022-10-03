import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.style as style
import numpy as np


# Loading data from CSV
def load_data(filename):
    return pd.read_csv(filename, header=24, encoding='utf8', engine='python')


# For debug purposes only - displays graph
def plot_show(title, x_data, y_data):
    fig = plt.figure(dpi=128, figsize=(8, 6))
    style.use('ggplot')
    plt.plot(x_data, y_data, c='xkcd:azure', alpha=0.6)
    # Установить графический формат
    plt.title(title, fontsize=16)  # Графическое название
    plt.xlabel("Time", fontsize=12)  # заголовок оси X и размер шрифта
    plt.ylabel("Wave data", fontsize=12)
    plt.tick_params(axis='both', which='major', labelsize=8)  # Формат оси
    # Показать диаграмму
    plt.show()
    plt.close(fig)


# Save single graph into file
def plt_save(file, title, x_data, y_data):
    fig = plt.figure(dpi=128, figsize=(8, 6))
    style.use('ggplot')
    plt.plot(x_data, y_data, c='xkcd:azure', alpha=0.6)
    plt.title(title, fontsize=16)
    plt.xlabel("Time", fontsize=12)
    plt.ylabel("Wave data", fontsize=12)
    plt.tick_params(axis='both', which='major', labelsize=9)
    # Показать диаграмму
    plt.savefig(file)
    plt.close(fig)


# Saves 2 graphs at one graph.
def plt_multiple_save(file, title, x_data1, y_data1, x_data2, y_data2):
    style.use('ggplot')
    fig = plt.figure(dpi=128, figsize=(8, 6))
    ax = fig.add_subplot()
    ax.plot(x_data1, y_data1, c='xkcd:azure', alpha=0.5)
    ax.plot(x_data2, y_data2, c="xkcd:purple", alpha=0.8)
    # Установить графический формат
    plt.title(title, fontsize=16)  # Графическое название
    plt.xlabel("Time", fontsize=12)  # заголовок оси X и размер шрифта
    plt.ylabel("Wave data", fontsize=12)
    plt.tick_params(axis='both', which='major', labelsize=9)  # Формат оси
    # Показать диаграмму
    plt.savefig(file)
    plt.close(fig)


# Bufsize is used to define the buffer size. Large buffer size means better quality, but low performance
def average_filter(data, bufsize):
    filtered_data = []
    buffer = [data[i] for i in range(bufsize)]

    for i in range(len(data)):
        average = 0
        for j in buffer:
            average += j
        average /= bufsize
        filtered_data.append(average)
        buffer = buffer[1:]
        buffer.append(data[(bufsize + i) % len(data)])
    return filtered_data


# Default median value is defined for 3 values. At this lab, we could use multiple values array (its length is bufsize)
# It is defined as "The number with the minimal distance to an average value of buffer array".
# But it leads to less random signal stability. E.g.: avg. value = 15, buffer = [10, 20, 30].
# Default median is 20, but ours is 10 (actually, it could be fixed fine, I'm free to get any pull requests)
def median_filter(data, bufsize):
    filtered_data = []
    buffer = [data[i] for i in range(bufsize)]

    for i in range(len(data)):
        average = 0
        for j in buffer:
            average += j
        average /= bufsize

        abs_distance = 1e9
        median = 0
        for j in buffer:
            if abs(average - j) < abs_distance:
                abs_distance = abs(average - j)
                median = j
        filtered_data.append(median)
        buffer = buffer[1:]
        buffer.append(data[(bufsize + i) % len(data)])
    return filtered_data


# Filter that is working for O(N), k value displays how important current value, comparing to the previous one, is
# (the less k the greater quality, at least, for this lab)
def easy_mean(data, k=0.1):
    filtered_data = []
    normalised = 1.0

    for i in range(len(data)):
        normalised = k * data[i] + (1 - k) * normalised
        filtered_data.append(normalised)

    return filtered_data


if __name__ == '__main__':
    for filenum in range(1, 23):
        data = load_data("./Waveform/DS" + '{:04}'.format(filenum) + ".CSV")
        x_source = data["Time"]
        y_source = data["Waveform Data"]

        for i in range(10, 300, 10):
            y = average_filter(y_source, i)
            x = np.resize(x_source, len(y))
            plt_save("./Filtered/AverageFilter/DS" + '{:04}'.format(filenum) + "/buff_size_" + str(i),
                     "Wave filtered by average filter",
                     x, np.array(y))

        y_average_filter_best = average_filter(y_source, 300)
        x_average_filter_best = np.resize(x_source, len(y_average_filter_best))
        plt_multiple_save("./Filtered/AverageFilter/DS" + '{:04}'.format(filenum) +"/comparison",
                          "Comparing source wave to the filtered one",
                          x_source.to_numpy(), y_source.to_numpy(),
                          x_average_filter_best, y_average_filter_best)

        for i in range(5, 100, 5):
            y = median_filter(y_source, i)
            plt_save("./Filtered/MedianFilter/DS" + '{:04}'.format(filenum) + "/buff_size_" + str(i),
                     "Wave filtered by median filter",
                     x_source.to_numpy(), np.array(y))

        y_median_filter_best = median_filter(y_source, 100)
        plt_multiple_save("./Filtered/MedianFilter/DS" + '{:04}'.format(filenum) + "/comparison",
                          "Comparing source wave to the filtered one",
                          x_source.to_numpy(), y_source.to_numpy(),
                          x_source.to_numpy(), np.array(y_median_filter_best))

        for i in range(99, 1, -5):
            y = easy_mean(y_source, i / 100)
            plt_save("./Filtered/ExpMeanFilter/DS" + '{:04}'.format(filenum) + "/k_" + str(i),
                     "Wave filtered by exponential mean filter",
                     x_source.to_numpy(),
                     np.array(y))

        y_easy_mean_filter = easy_mean(y_source)
        plt_multiple_save("./Filtered/ExpMeanFilter/DS" + '{:04}'.format(filenum) + "/comparison",
                          "Comparing source wave to the filtered one",
                          x_source.to_numpy(), y_source.to_numpy(),
                          x_source.to_numpy(), np.array(y_easy_mean_filter))

