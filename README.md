# Python Hash Map Implementations: LinkedList and Quadratic Probing

This repository contains two separate implementations of a hash map data structure in Python. One implementation utilizes a singly linked list for collision resolution, and the other implementation uses quadratic probing for collision resolution. Both implementations support dynamic resizing of the hash map to maintain a reasonable load factor.

## LinkedList Hash Map

The LinkedList hash map implementation stores key-value pairs in a hash table using linked lists for collision resolution. When a collision occurs, the key-value pair is stored in the next available linked list node corresponding to the hashed index.

### Key Features

- Stores key-value pairs in a hash table
- Uses linked lists for collision resolution
- Automatic resizing of the hash table when the load factor reaches 0.5
- Implements the following methods:
  - `put(key, value)`
  - `get(key)`
  - `contains_key(key)`
  - `remove(key)`
  - `clear()`
  - `get_keys()`
  - `get_values()`
  - `table_load()`
  - `resize_table(new_capacity)`

## Quadratic Probing Hash Map

The Quadratic Probing hash map implementation stores key-value pairs in a hash table using open addressing and quadratic probing for collision resolution. When a collision occurs, quadratic probing is used to find the next available index to store the key-value pair.

### Key Features

- Stores key-value pairs in a hash table
- Uses quadratic probing for collision resolution
- Automatic resizing of the hash table when the load factor reaches 0.5
- Implements the following methods:
  - `put(key, value)`
  - `get(key)`
  - `contains_key(key)`
  - `remove(key)`
  - `clear()`
  - `get_keys_and_values()`
  - `table_load()`
  - `empty_buckets()`
  - `resize_table(new_capacity)`
  - `get_bucket_index(key)`

## Usage

Both hash map implementations allow for using custom hash functions or the provided default hash functions. Below are examples of how to enter a value into each hash map class and then retrieve the value.

### LinkedList Hash Map

```python
from hash_map_sc import HashMap

# Create a new hash map with the default hash function
hash_map = HashMap()

# Add a key-value pair to the hash map
hash_map.put("key", "value")

# Retrieve the value associated with the key
value = hash_map.get("key")
print(value)  # Output: "value"
```

### Quadratic probing Hash Map

```python
from hash_map_oa import HashMap

# Create a new hash map with the default hash function
hash_map = HashMap()

# Add a key-value pair to the hash map
hash_map.put("key", "value")

# Retrieve the value associated with the key
value = hash_map.get("key")
print(value)  # Output: "value"
```

To use a custom hash function, simply pass it as an argument when creating the hash map:
```python
def custom_hash_function(key):
    # Your custom hashing logic here
    pass

# Create a new hash map with a custom hash function
hash_map = HashMap(function=custom_hash_function)
