# Course: CS261 - Data Structures
# Assignment: 5
# Student: Jaime Justo
# Description: Min heap implementation using a dynamic array to store heap content.


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initializes a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'HEAP ' + str(self.heap)

    def is_empty(self) -> bool:
        """
        Return True if no elements in the heap, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.heap.length() == 0

    def add(self, node: object) -> None:
        """
        Adds a new object to the MinHeap maintaining heap property.
        """
        # add element at the end of the array
        self.heap.append(node)

        # check if we maintained the heap property
        self.bubble_up(self.heap.length() - 1)

    def get_min(self) -> object:
        """
        Returns an object with a minimum key without removing it from the heap. If the heap is empty, the method raises
        a MinHeapException.
            :return: minimum key from the heap.
            :rtype: object.
        """
        # check if heap is empty
        if self.is_empty():
            raise MinHeapException

        return self.heap[0]

    def remove_min(self) -> object:
        """
        Returns an object with a minimum key and removes it from the heap. If the heap is empty, the method raises a
        MinHeapException.
            :return: minimum key from the heap.
            :rtype: object.
        """
        if self.is_empty():
            raise MinHeapException

        # replace root with last element
        last_element_index = self.heap.length() - 1
        self.heap.swap(0, last_element_index)

        # store and remove minimum key
        min_key = self.heap.pop()

        # swap the last element with its child until reaching the correct spot
        self.trickle_down(0)

        return min_key

    def build_heap(self, da: DynamicArray) -> None:
        """
        TODO: Write this implementation
        """
        pass

    def bubble_up(self, new_element_index):
        parent_index = ((new_element_index - 1) // 2)
        # swap new element with its parent until it is no longer smaller than its parent
        while new_element_index > 0 and self.heap[new_element_index] < self.heap[parent_index]:
            self.heap.swap(parent_index, new_element_index)
            new_element_index = parent_index
            parent_index = ((new_element_index - 1) // 2)

    def trickle_down(self, replacement_element_index):
        size = self.heap.length() - 1

        # swap the replacement element with its minimum child
        while replacement_element_index >= 0:
            j = -1
            right_index = 2 * replacement_element_index + 2
            if right_index < size and self.heap[right_index] < self.heap[replacement_element_index]:
                left_index = 2 * replacement_element_index + 1
                if self.heap[left_index] < self.heap[right_index]:
                    j = left_index
                else:
                    j = right_index
            else:
                left_index = 2 * replacement_element_index + 1
                if left_index < size and self.heap[left_index] < self.heap[replacement_element_index]:
                    j = left_index
            if j >= 0:
                self.heap.swap(j, replacement_element_index)
            replacement_element_index = j


# BASIC TESTING
if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)


    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())


    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty():
        print(h, end=' ')
        print(h.remove_min())


    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)
    da.set_at_index(0, 500)
    print(da)
    print(h)
