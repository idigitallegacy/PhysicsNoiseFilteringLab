# Physics. Noise Filtering Lab
## Data used
I got data for ./Waveform folder using GDS-71000B oscillograph during lab execution. Unfortunately, data output is hard to extract correctly using Python module Pandas. So I decided to replace line 25 "Waveform data," with "Time,Waveform data," for each file.

## Dependencies
To run `./main.py`, you need to install the following modules:
```batchfile
pip install matplotlib
pip install Pandas
```

## Project structure
- Filtered/
  - \*Filter/\*/\*.png - *Files filtered by some filter method (see also 'filter methods'), filter buffer size is at the file name*
  - \*Filter/comparison.png - *Compare best filtered result to the source wave*
- Waveform/
  - DS*.csv - *Source csv files, but a bit modified (see 'data used')
- main.py - *Mainfile*
- support.py - *Script to make directories that are required at main.py*

## Filter methods
| Filter name   | Filter options  | Options range                 | Description                                                                                          |
|:------------- |:---------------:|:-----------------------------:|:-----------------------------------------------------------------------------------------------------|
| AverageFilter | data<br>bufsize | Any Iterable<br>0 - len(data) | Average filter method. Uses average value of **bufsize** elements amount.<br><br>See also *buffering*|
| MedianFilter  | data<br>bufsize | Any Iterable<br>0 - len(data) | Median filter method. Uses **bufsize** values median value (e.g. [0, 10, 20, 100] => 20).<br>Default median filter **bufsize** value is 3.<br><br>See also *buffering*|
| ExpMeanFilter | data<br>k       | Any Iterable<br>0 - 1         | Exponential moving average value filter method. **K** is a degree of weighting decrease.<br>Uses E_i = **k** * data[i] + (1 - **k**) * E_(i-1) formula.<br>E_i is a normalised output. Initially, E_0 = 1.0|

## Buffering
Some filter methods are using buffering to work fine. All of the methods that are using buffering are requiring specidying a bufsize parameter. Inititial value:
```python
buffer = [data[i] for i in range(bufsize)]
```
Swapping buffer while data processing:
```python
buffer = buffer[1:]
buffer.append(data[ (bufsize + i) % len(data) ])
```
This swapping method allows me to process data without losing dimentions (eg., if I remove `% len(data)` part, input data length = n, output filtered length = n - bufsize). `i` variable is at [0..len(data)] range.

**Important note** This buffering method requires `data[0] = data[ len(data) ]` to work fine. Be careful.

### Data processing at Average filter method
The more **buffsize** value set, the more quality you get as the result, but it slows down method.
```python
average = 0
for i in buffer:
    average += i
average /= bufsize
filtered_data.append(average)
# <...> buffer swapping here; cycle goes to 'average = 0' line
```

### Data processing at Median filter method
The more **buffsize** value set, the more quality you get as the result, but it slows down method.
```python
average = 0
min_distance = 1e9
median = buffer[0]
for i in buffer:
    average += i
average /= bufsize
for i in buffer:
    if abs(i - average) < min_distance:
        median = i
        min_distance = abs(i - average)
filtered_data.append(median)
# <...> buffer swapping here; cycle goes to 'average = 0' line
```

### Data processing at Exponential mean value filter method
The less **k** value set, the more quality you get.
```python
normalised = 1.0
for i in data:
    normalised = k * i + (1 - k) * normalised
    filtered_data.append(normalised)
```

## Conclusion
Source code provided by Michael @idigitallegacy Makarov. This project is **educational and non-commercial use** only. Feel free to make pull requests at this project, if you see something ambigious or weak moments.

Files stored at `/Filtered/` directory is a `/main.py` script output, these files are unversioned. The ony reason these files were uploaded is a full script execution time (**~10 min**).
