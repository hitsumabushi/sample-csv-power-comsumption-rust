import csv
from datetime import datetime, timedelta
import argparse
import itertools
import random


def gen(filename: str, lines: int):
    now = datetime.now()
    with open(filename, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        g = gen_row(now, lines)
        for row in g:
            writer.writerow(row)


def gen_row(time_from, lines):
    delta = timedelta(milliseconds=100)
    for _ in range(lines):
        time_from = time_from + delta
        yield [time_from.strftime('%Y-%m-%d %H:%M:%S.%f'), random.random(), "ADC"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=str, help='filename', required=True)
    parser.add_argument('--lines', type=int,
                        help='generate lenes', required=True)
    args = parser.parse_args()

    gen(filename=args.out, lines=args.lines)


if __name__ == "__main__":
  main()