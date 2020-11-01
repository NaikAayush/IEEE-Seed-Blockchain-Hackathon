import random
import  itertools

def uniqueid():
    """Generates a unique ID. Tested it for 1000 numbers, all of them were unique"""
    seed = random.getrandbits(32)
    while True:
       yield seed
       seed += 1

def get_uniqueid(number_of_ids=1):
    """Wrapper for the above function
    params number_of_ids: int, enter the number of ids you want to generate
    Return: List of ids"""       
    unique_sequence = uniqueid()
    ids = list(itertools.islice(unique_sequence, number_of_ids))
    return ids

#usage
"""get_uniqueid(10)"""