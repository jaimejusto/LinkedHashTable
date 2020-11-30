# Course: CS261 - Data Structures
# Assignment: 5
# Student: Jaime Justo
# Description: Hash map implementation using a dynamic array to store the hash table. Chaining implemented using a
#               singly linked list for collision resolution.


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        Clears the content of the hash map. It does not change underlying hash table capacity.
        TODO: retest after resize() implemented.
        """
        self.buckets = DynamicArray()
        self.size = 0
        for _ in range(self.capacity):
            self.buckets.append(LinkedList())

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. If the key is not in the hash map, the method returns None.
            :param str key: value to look for in hash map.
            :return: value associated with the given key.
            :rtype: object.
        """
        # get bucket where given key may be found
        bucket = self.get_bucket(key)

        # search the bucket for the given key
        key_in_bucket = bucket.contains(key)

        # if the given key is in the bucket, return its value
        if key_in_bucket:
            return key_in_bucket.value

        # given key was not in the bucket
        return None

    def put(self, key: str, value: object) -> None:
        """
        Updates the key / value pair in the hash map. If a given key already exists in the hash map, its associated
        value is replaced with the new value. If a given key is not in the hash map, a key / value pair is then added.
            :param str key: value to look for in hash map.
            :param object value: replaces old value if given key already exists, otherwise gets added with the given key
                to the hash map.
        """
        # get the bucket to place key in
        bucket = self.get_bucket(key)

        # check if bucket already contains the given key
        key_in_bucket = bucket.contains(key)

        # if given key already exists, replace its current value with the given value
        if key_in_bucket:
            key_in_bucket.value = value

        # if given key not in hash map, add it
        elif key_in_bucket is None:
            bucket.insert(key, value)
            self.size += 1

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map. If a given key is not in the hash map, the
        method does nothing.
            :param str key: value to look for in hash map.
        """
        # get the bucket where the given key may be found
        bucket = self.get_bucket(key)

        # search the bucket for the given key
        if bucket.contains(key):
            # key was found, remove the key/value pair
            bucket.remove(key)
            self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False. An empty hash map does not contain
         any keys.
            :param str key: value to look for in hash map.
            :return: True if given key is in the hash map, otherwise False.
            :rtype: bool.
        """
        # hash map is empty, therefore it doesn't contain any keys
        if self.size == 0:
            return False

        # hash map isn't empty, get the bucket where the key may be found
        bucket = self.get_bucket(key)

        # search the bucket for the given key
        if bucket.contains(key):
            # key was found
            return True

        # key was not found
        return False

    def empty_buckets(self) -> int:
        """
        Returns a number of empty buckets in the hash table.
            :return: number of empty buckets in the hash table
            :rtype: int
        """
        empty_bucket_count = 0

        # iterate through buckets
        for i in range(self.buckets.length()):
            # check if bucket is empty
            if self.buckets[i].length() == 0:
                empty_bucket_count += 1

        return empty_bucket_count

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
            :return: average number of elements in each bucket (load factor).
            :rtype: float.
        """
        # load factor = total number of elements stored in the table / number of buckets
        load_factor = self.size / self.capacity

        return load_factor

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing key / value pairs must remain in the new hash
        map and all hash table links must be rehashed. If new_capacity is less than 1, this method should do nothing.
            :param int new_capacity: new capacity of hash table.
        """
        if new_capacity >= 1:
            # store old table
            old_table = self.buckets

            # resize table with new capacity
            self.buckets = DynamicArray()
            for _ in range(new_capacity):
                self.buckets.append(LinkedList())

            # update capacity
            self.capacity = new_capacity

            # rehash table links with new capacity
            # iterate through old buckets
            for bucket in old_table:
                # check for keys in current bucket
                if bucket.length() != 0:
                    # get key / value pairs in non-empty bucket
                    for node in bucket:
                        new_bucket = self.get_bucket(node.key)          # new bucket to place key / value pair
                        new_bucket.insert(node.key, node.value)         # insert key / value pair

    def get_keys(self) -> DynamicArray:
        """
        Returns a DynamicArray that contains all keys stored in your hash map. The order of the keys in the DA does not
        matter.
            :return: all the keys in the hash map.
            :rtype: DynamicArray.
        """
        # storage for keys
        keys = DynamicArray()

        # iterate through the buckets
        for bucket in self.buckets:
            # check for keys in current bucket
            if bucket.length() != 0:
                # get each key in non-empty bucket and add it to list
                for node in bucket:
                    keys.append(node.key)

        return keys

    def get_bucket(self, key: str) -> LinkedList:
        """
        Returns a bucket where the given key should be placed based on the results of the hash function.
            :param str key: value passed to hash function for placement into hash table.
            :return: bucket for given key.
            :rtype: LinkedList.
        """
        # get hash
        hash = self.hash_function(key)
        # compute index for hash table
        index = hash % self.capacity

        # return bucket
        return self.buckets[index]


# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())


    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))


    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)


    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))


    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)


    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')


    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))


    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))


    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
