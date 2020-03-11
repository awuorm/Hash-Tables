# '''
# Linked List hash table key/value pair
# '''


class LinkedPair:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    '''
    A hash table that with `capacity` buckets
    that accepts string keys
    '''

    def __init__(self, capacity):
        self.count = 0
        self.capacity = capacity  # Number of buckets in the hash table
        self.storage = [None] * capacity
        self.minCapacity = capacity
        self.minLoadFactor = 0.2
        self.maxLoadFactor = 0.7

    def _hash(self, key):
        '''
        Hash an arbitrary key and return an integer.

        You may replace the Python hash with DJB2 as a stretch goal.
        '''
        return self._hash_djb2(key)

    def _hash_djb2(self, key):
        '''
        Hash an arbitrary key using DJB2 hash

        OPTIONAL STRETCH: Research and implement DJB2
        '''
        hashVal = 5381
        for char in key:
            hashVal += hashVal << 5 + ord(char)
        return hashVal

    def _hash_mod(self, key):
        '''
        Take an arbitrary key and return a valid integer index
        within the storage capacity of the hash table.
        '''
        return self._hash(key) % self.capacity

    def insert(self, key, value, resizing=False):
        '''
        Store the value with the given key.

        # Part 1: Hash collisions should be handled with an error warning. (Think about and
        # investigate the impact this will have on the tests)

        # Part 2: Change this so that hash collisions are handled with Linked List Chaining.

        Fill this in.
        '''
        self.count += 1
        if not resizing:
            self.resize()
        index = self._hash_mod(key)
        newPair = LinkedPair(key, value)
        bucket = self.storage[index]
        if bucket is None:
            self.storage[index] = newPair
            return newPair.value

        # colision handling
        prev = bucket
        keyExists = False
        while bucket is not None:
            prev = bucket
            if bucket.key == key:
                keyExists = True
                break
            bucket = bucket.next
        if keyExists:
            bucket.value = value
        else:
            prev.next = newPair
        return newPair.value

    def remove(self, key):
        '''
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Fill this in.
        '''
        index = self._hash_mod(key)
        bucket = self.storage[index]
        prev = None
        while bucket is not None and bucket.key != key:
            prev = bucket
            bucket = bucket.next
        if bucket is None:
            return None
        else:
            self.count -= 1
            value = bucket.value
            if prev is None:
                self.storage[index] = None
            else:
                prev.next = prev.next.next
            return value

    def retrieve(self, key):
        '''
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Fill this in.
        '''
        index = self._hash_mod(key)
        bucket = self.storage[index]
        while bucket is not None and bucket.key != key:
            bucket = bucket.next
        if bucket is not None:
            return bucket.value
        else:
            return None

    def shouldResize(self):
        shouldResize = False
        # grow
        if self.count > self.maxLoadFactor * self.capacity:
            self.capacity = self.capacity * 2
            shouldResize = True
        # shrink
        elif self.count < self.minLoadFactor * self.capacity and self.capacity >= self.minCapacity * 2:
            self.capacity = self.capacity // 2
            shouldResize = True
        return shouldResize

    def resize(self):
        '''
        Doubles the capacity of the hash table and
        rehash all key/value pairs.

        Fill this in.
        '''
        if self.shouldResize():
            oldStorage = self.storage
            oldCount = self.count
            self.count = 0
            self.storage = [None] * self.capacity
            for i in range(0, oldCount):
                bucket = oldStorage[i]
                if bucket is not None:
                    while bucket is not None:
                        self.insert(bucket.key, bucket.value, True)
                        bucket = bucket.next
        else:
            return False 


if __name__ == "__main__":
    ht = HashTable(2)

    ht.insert("line_1", "Tiny hash table")
    ht.insert("line_2", "Filled beyond capacity")
    ht.insert("line_3", "Linked list saves the day!")

    print("")

    # Test storing beyond capacity
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    # Test resizing
    old_capacity = len(ht.storage)
    ht.resize()
    new_capacity = len(ht.storage)

    # print(f"\n Resized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    print("")
