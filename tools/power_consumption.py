import csv
import logging
import os
from datetime import datetime, timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def main():
    filename = os.environ.get("POWER_CONSUMPTION_FILE", None)
    if filename is None:
        logger.fatal("Please set env: POWER_CONSUMPTION_FILE")
        return

    # 前提条件
    # * ファイルに記載されているのは、時刻順にソート済み

    # 隣あう2点を線で結ぶモデル
    # つまり面積は台形から計算できると思って計算することにする
    datetime_format = "%Y-%m-%d %H:%M:%S.%f"
    total_consumption = 0.0
    total_time = 0.0
    prev_data = None
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            logging.debug(f"prev: {prev_data}")
            logging.debug(f"row: {row[0:1]}")
            t_str = row[0]
            data_a = float(row[1])
            t = datetime.strptime(t_str, datetime_format)
            # 最初のデータでないとき
            if prev_data is not None:
                delta = t - prev_data[0]
                logging.debug(f"delta: {delta.total_seconds()}")
                total_time += delta.total_seconds()
                total_consumption += area_trapezoid(prev_data[1], data_a, delta.total_seconds())
            # 次のために更新
            prev_data = (t, data_a)
    logging.debug(f"total_consumption: {total_consumption}[A]")
    logging.debug(f"total_time: {total_time}")
    logging.debug(f"result: {total_consumption / total_time}")
    result = {
        "total_consumption[A*sec]": total_consumption,
        "total_time[sec]": total_time,
        "avg_consumption[A]": total_consumption / total_time,
    }
    return result


def area_trapezoid(upper_length, lower_length, height):
    """台形の面積出すやつ"""
    return (upper_length + lower_length) * height / 2.0


if __name__ == "__main__":
    result = main()
    print(result)
