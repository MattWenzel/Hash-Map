# Name: Matthew Wenzel
# Email: wenzelma@oregonstate.edu
# Date: 8/9/22
# Description: Implements a Hash Map class with a Dynamic Array as the underlying data structure
#              and uses Open Addressing with Quadratic Probing for collision resolution


from hash_map_include import (DynamicArray, HashEntry,
                              hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int = 11, function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        # if the load factor is equal to or greater than 0.5, resize the hash map
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # find the index position and bucket corresponding to the key
        index = self.get_bucket_index(key)
        bucket = self._buckets[index]

        # if the bucket is not empty and not a tombstone, update its value
        if bucket and not bucket.is_tombstone:
            bucket.value = value
        # else, insert the key / value pair into the empty bucket
        else:
            self._buckets[index] = HashEntry(key, value)
            self._size += 1

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        empty_count = 0
        # iterate through the hash map incrementing the empty bucket count for each empty bucket found
        for num in range(self._capacity):
            if self._buckets[num] is None:
                empty_count += 1
        return empty_count

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table.
        All existing key / value pairs remain in the new hash map, and all hash table links are rehashed.
        """
        # do nothing if new capacity is less than the size of the hash map
        if new_capacity < self._size:
            return

        # if the new capacity is not a prime number, increment it to the next prime
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # create an array of all the key / value pairs in the hashmap
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
        # find the index position and bucket corresponding to the key
        index = self.get_bucket_index(key)
        bucket = self._buckets[index]

        # if the bucket is not empty and not a tombstone, return its value
        if bucket and not bucket.is_tombstone:
            return bucket.value
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False.
        """
        # if the hash map is empty, return False
        if self._size == 0:
            return False

        # find the index position and bucket corresponding to the key
        index = self.get_bucket_index(key)
        bucket = self._buckets[index]

        # if the bucket is not empty and not a tombstone, return True
        if bucket and not bucket.is_tombstone:
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        If the key is not in the hash map, the method does nothing.
        """
        # find the index position and bucket corresponding to the key
        index = self.get_bucket_index(key)
        bucket = self._buckets[index]

        # if the bucket is not empty and not a tombstone:
        if bucket and not bucket.is_tombstone:
            # set the tombstone value to True and decrement the size of the hash map
            bucket.is_tombstone = True
            self._size -= 1
        return

    def clear(self) -> None:
        """
        Clears the contents of the hash map.
        It does not change the underlying hash table capacity.
        """
        # set the underlying array to a new empty Dynamic Array
        self._buckets = DynamicArray()
        # add 'None' values to the new hash map equal to the hash map's capacity
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key / value pair stored in the hash map.
        """
        arr = DynamicArray()
        # increment through the hash map checking each bucket
        for num in range(self._capacity):
            bucket = self._buckets[num]
            # if the bucket exists and is not a tombstone, add its key / value pair to the array
            if bucket and not bucket.is_tombstone:
                arr.append((bucket.key, bucket.value))
        return arr

    def get_bucket_index(self, key: str):
        """
        takes a key as a parameter and uses quadratic probing to
        calculate the corresponding index position in the hash map
        """
        # use the hash function to calculate an initial index position for the given key
        initial = self._hash_function(key) % self._capacity
        j, index = 1, initial
        # while a bucket exists at the current index position:
        while self._buckets[index]:
            # return the current index position if it contains the key
            if self._buckets[index].key == key:
                return index
            # use quadratic probing to calculate the next index position
            index = (initial + (j**2)) % self._capacity
            j += 1
        # return index position of empty bucket if key not found
        return index

