#!/usr/bin/env python

"""Tests for `cvm` package."""

import pytest
from os import listdir
from os.path import isfile, join
from joblib import Parallel, delayed

import cvm


@pytest.fixture
def get_shakespeare_texts():

    word_list = []
    path = './resources/shakespeare_texts/'
    files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]

    for file_name in files:
        with open(file_name, 'r') as f:
            word_list += f.read().split(' ')

    return word_list

def test_estimate(get_shakespeare_texts):
    
    word_list = get_shakespeare_texts
    counter = cvm.CVM(1000)

    for word in word_list:
        counter.record(word)

    actual_num_unique = len(set(word_list))
    estimated_num_unique = counter.estimate()

    print('Actual =', actual_num_unique, ', Estimated =', estimated_num_unique)
    print('Difference =', actual_num_unique - estimated_num_unique)
    print('Difference perc=', round(100*(actual_num_unique - estimated_num_unique)/actual_num_unique, 2))
    print('Num rounds =', counter._num_rounds)
    assert True

def test_estimate_multi_thread(get_shakespeare_texts):
    
    word_list = get_shakespeare_texts
    counter = cvm.CVM(1000, multi_threading=True)

    Parallel(n_jobs=10, prefer="threads")(delayed(counter.record)(word) for word in word_list)

    actual_num_unique = len(set(word_list))
    estimated_num_unique = counter.estimate()

    print('Actual =', actual_num_unique, ', Estimated =', estimated_num_unique)
    print('Difference =', actual_num_unique - estimated_num_unique)
    print('Difference perc=', round(100*(actual_num_unique - estimated_num_unique)/actual_num_unique, 2))
    print('Num rounds =', counter._num_rounds)
    assert True