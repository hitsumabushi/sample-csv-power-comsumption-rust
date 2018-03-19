# What is this

Sample rust program to compare python.
Python version is [power\_consumption.py](tools/power_consumption.py).

# How to run

```shell
./power-consumption <path to csv>
```

# Comparison

Generate sample 3,000,000 lines csv file.

```shell
python gen.py --out 3000000-lines.csv --lines 3000000
```

| Program              | Time          |
| -------------------- |:-------------:|
| Python               | 69.41 sec     |
| Rust                 | 2.155 sec     |
