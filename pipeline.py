import sys
import pandas as pd

#print(sys.argv)

# Create variable why fuction is select principal argument entry 
# example input: python3 pipeline.py 29-03-23, output: job finished 29-03-23

day = sys.argv[1]

# some interesting things with pandas

print(f'job finished = {day}')
