import os

# mkdirs if needed

if __name__ == "__main__":
    # os.mkdir("./Filtered/AverageFilter", mode=0o777, dir_fd=None)
    # os.mkdir("./Filtered/MedianFilter", mode=0o777, dir_fd=None)
    # os.mkdir("./Filtered/ExpMeanFilter", mode=0o777, dir_fd=None)
    for i in range(10, 23):
        os.mkdir("./Filtered/AverageFilter/DS00" + str(i), mode=0o777, dir_fd=None)


    for i in range(10, 23):
        os.mkdir("./Filtered/MedianFilter/DS00" + str(i), mode=0o777, dir_fd=None)


    for i in range(10, 23):
        os.mkdir("./Filtered/ExpMeanFilter/DS00" + str(i), mode=0o777, dir_fd=None)