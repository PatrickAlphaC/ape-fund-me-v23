favorite_number: uint256 # Stored at slot 0
some_bool: bool # Stored at slot 1
my_array: uint256[1000] # Length stored at slot 2
# All elements come after the length
my_map: HashMap[uint256, bool] # Length stored at slot 3 + 1000

NOT_IN_STORAGE: constant(uint256) = 123
IMMUTABLE_NOT_IN_STORAGE: immutable(uint256)

@external
def __init__():
    self.favorite_number = 25
    self.some_bool = True
    self.my_array[0] = 222
    self.my_map[0] = True # At storage slot 0x159b6e80f1cb5d8084c1accd4d8cd6bd01fc359bff98af2a17d7bbe757a2096d
    IMMUTABLE_NOT_IN_STORAGE = 123

@external
def doStuff():
    new_var: uint256 = self.favorite_number + 1 # SLOAD
    otherVar: bool = self.some_bool # memory Variable
