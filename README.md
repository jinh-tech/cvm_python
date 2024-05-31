# CVM
Python implementation of the CVM algorithm which estimates the number of unique items in a stream.
The algorithm is memory efficient and can estimate unique number of elements quite accurately depending on the memory allocated to the algorithm.

A deterministic algorithm which counts the number of unique elements will need to store all unique elements seen so far. If the number of unique elements is high, then a lot of memory will be used. 

The CVM algorithm however lets you set a limit to how many elements you want to store in the memory (known as the threshold in the paper) and is still able to estimate the number of unique elements seen so for. The more elements you let the algorithm store, the better the estimate becomes.

For a list with ~150K unique elements, this algorithm is able to estimate the number of unique elements to about 2% error while storing only 1K elements. In other words, the algorithm achieved only ~2% error in estimating the number of unique elements by using only the memomry required to store 1K elements rather than 150K elements. Keep in mind the algorithm is probabilistic, you will see a different estimate each time.


For more details - 
- Link to technical paper - [Distinct Elements in Streams: An Algorithm for the (Text) Book](https://arxiv.org/abs/2301.10191)
- Link to easy to ready blog for non-technical users - [Computer Scientists Invent an Efficient New Way to Count](https://www.quantamagazine.org/computer-scientists-invent-an-efficient-new-way-to-count-20240516/)

## Installation
The package only requires `python = "^3.6"`. There are no other dependencies that require installation.
Install the package using the following command
```sh
pip install cvm-count
```

## Usage
The following code shows how to use the package.
```python
import cvm_count

def test_estimate(word_list):
    
    #create a CVM class object, specifying the threshold - the number of elemenets that can be stored in a set.
    counter = cvm_count.CVM(threshold=1000)

    for word in word_list:
        #use the method `record` to go through each element
        counter.record(word)

    actual_num_unique = len(set(word_list))
    #use the method `estimate` to estimate the number unique elements seen so far.
    estimated_num_unique = counter.estimate()

    print('Actual =', actual_num_unique, ', Estimated =', estimated_num_unique)
    print('Difference =', actual_num_unique - estimated_num_unique)
    print('Difference perc=', round(100*(actual_num_unique - estimated_num_unique)/actual_num_unique, 2))
    print('Num rounds =', counter._num_rounds)
```
The methods `record` and `estimate` can be used multiple times in a code in any order. 
Any datatype which can be handled by the Set() data structure in Python can be used here. For example, in the `record` method, we can pass `int`, `float` and `str` datatypes at the same time.

The package can also help estimate the count elements in a situation where record is being called from different threads/processes. Refer to the example below.

```python
from joblib import Parallel, delayed
import cvm_count 

def test_estimate_multi_thread(word_list):

    counter = cvm_count.CVM(1000, multi_threading=True)
    Parallel(n_jobs=10, prefer="threads")(delayed(counter.record)(word) for word in word_list)

    actual_num_unique = len(set(word_list))
    estimated_num_unique = counter.estimate()

    print('Actual =', actual_num_unique, ', Estimated =', estimated_num_unique)
    print('Difference =', actual_num_unique - estimated_num_unique)
    print('Difference perc=', round(100*(actual_num_unique - estimated_num_unique)/actual_num_unique, 2))
    print('Num rounds =', counter._num_rounds)
```
The code above will take some time to execute because a lot of threads will be created and discarded while processing.

## Issues
The package has not been stress tested. Use at your own risk. However, given the simplicity of the algorithm and the fact that python float has a 53 bit precision, I personally don't see any issue with numerical stability or any other thing for that matter.

## Github
Link to the repo - [CVM Python Implementation](https://github.com/jinh-tech/cvm_python). The core implementation is present in [this file](https://github.com/jinh-tech/cvm_python/blob/main/src/cvm.py) and is quite small and easy to read. 
Please feel free to raise issues, PRs etc in the repo.

## License

MIT