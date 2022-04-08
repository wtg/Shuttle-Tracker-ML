#!/usr/bin/env python

print("Load and process training + validation data - enter Data.csv")
exec(open("preprocessing.py").read())
print("Run model")
exec(open("RNN.py").read())
print("Load and process testing data - enter Data2.csv")
exec(open("preprocessing.py").read())
print("Validate model")
exec(open("Test_RNN.py").read())