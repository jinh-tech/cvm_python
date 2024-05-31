"""Main module. Contains the class CVM which implements the algorithm"""
from threading import Semaphore
from src.util_funcs import coin_toss

class CVM:
    """Implements the record and estimate functions"""
    
    def __init__(self, threshold:int, multi_threading:bool=False) -> None:
        """
        threshold:int - number of elements that the set can have
        multi_threading:bool - default = False. To enable safe execution of record function in multi threading/process environment.
        """
        self._p = 1.0
        self.threshold = threshold 
        self._num_rounds = 0
        self._set_elements = set()
        self._multi_threading = multi_threading
        
        if self._multi_threading == True:
            self._semaphore = Semaphore()
        
    def record(self, element) -> None:
        """
        element - can be any datatype which can be handled by the Set() data structure in python
        """
        if self._multi_threading == True:
            with self._semaphore:
                self._algorithm(element)
        else:
            self._algorithm(element)
    
    def _algorithm(self, element) -> None:
        """
        The implementation of the algorithm.
        """
        self._set_elements.discard(element)
            
        if coin_toss(self._p) == True:
            self._set_elements.add(element)
        
        if len(self._set_elements) >= self.threshold:
            remove_set = set([ele for ele in self._set_elements if coin_toss(0.5) == True])
            self._set_elements -= remove_set
            self._p /= 2.0
            self._num_rounds += 1
        
    def estimate(self) -> int:
        """
        Returns the estimate of the number of unique items so far.
        """
        return int(len(self._set_elements)/self._p)


