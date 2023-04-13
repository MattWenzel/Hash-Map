# Name: Matthew Wenzel
# Email: wenzelma@oregonstate.edu
# Date: 8/9/22
# Description: Implements a Hash Map class with a Dynamic Array as the underlying data structure
#              and uses a singly linked list as chaining for collision resolution


from hash_map_include import (DynamicArray, LinkedList,
                              hash_function_1, hash_function_2)

class HashMap:
    def __init__(self, capacity: int = 11, function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Takes a key / value pair as parameters and updates the hash map with the new value.
        If the key already exists, its value is updated. If not, a new key / value pair is added.
        """

        # use the hash function to calculate an index position for the given key
        index = self._hash_function(key) % self._capacity
        # use the index position to find the appropriate bucket for the key
        bucket = self._buckets[index]
        # if the bucket already contains the key, update its value
        node = bucket.contains(key)
        if node:
            node.value = value
        # else, add a new key value pair to the bucket
        else:
            bucket.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        empty_buckets = 0
        # iterate through the underlying array checking the length of each bucket
        # and incrementing the empty bucket count for each empty bucket found
        for num in range(self._capacity):
            if self._buckets[num].length() == 0:
                empty_buckets += 1
        return empty_buckets

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears the contents of the hash map.
        It does not change the underlying hash table capacity.
        """
        # set the underlying array to an empty dynamic array
        self._buckets = DynamicArray()
        # add empty linked lists to the new hash map equal to the hash map's capacity
        for num in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table.
        All existing key / value pairs remain in the new hash map, and all hash table links are rehashed.
        """
        # do nothing if the new capacity is less than 1
        if new_capacity < 1:
            return

        # if the new capacity is not a prime number, increment it to the next prime
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # create an array of all the key / value pairs in the hash map
        key_val_arr = self.get_keys_and_values()

        # update the capacity and then clear out all the buckets in the hash map
        self._capacity = new_capacity
        self.clear()

        # iterate through the key / value array adding each pair to the new hash map with updated capacity
        for num in range(key_val_arr.length()):
            key, val = key_val_arr[num]
            self.put(key, val)

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key.
        If the key is not in the hash map, the method returns None.
        """
        # use the hash function to calculate an index position for the given key
        index = self._hash_function(key) % self._capacity
        # use the index position to find the appropriate bucket for the key
        bucket = self._buckets[index]
        # if the bucket contains the key, return its value
        node = bucket.contains(key)
        if node:
            return node.value
        # else, return None
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False.
        """
        # use the hash function to calculate an index position for the given key
        index = self._hash_function(key) % self._capacity
        # use the index position to find the appropriate bucket for the key
        bucket = self._buckets[index]
        # if the bucket contains the key, return True, else return False
        node = bucket.contains(key)
        return node is not None

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        If the key is not in the hash map, the method does nothing.
        """
        # use the hash function to calculate an index position for the given key
        index = self._hash_function(key) % self._capacity
        # use the index position to find the appropriate bucket for the key
        bucket = self._buckets[index]
        # remove the key from the bucket and decrement the size of the hash map if successful
        if bucket.remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key / value pair stored in the hash map.
        """
        arr = DynamicArray()
        # iterate through each bucket in the hash map
        for num in range(self._capacity):
            bucket = self._buckets[num]
            # for every node in the bucket, add their key / value pairs to the array
            for node in bucket:
                arr.append((node.key, node.value))
        return arr




