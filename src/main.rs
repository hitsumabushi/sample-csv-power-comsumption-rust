extern crate chrono;
extern crate csv;

use std::env;
use chrono::NaiveDateTime;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        println!("csv file not given!");
        return;
    }

    let filename = &args[1];
    // initialize
    let datetime_format = "%Y-%m-%d %H:%M:%S%.f";
    let mut total_consumption: f64 = 0.0;
    let mut total_time: i64 = 0;
    let mut prev_time: (i64, u32) = (0, 0);
    let mut prev_value: f64 = 0.0;
    let mut is_first = true;
    let mut t: (i64, u32);
    let mut f: f64;
    let mut delta: i64;

    let micro: u32 = 1_000_000;

    // CSVパーサを生成し fからデータを読む
    let mut rdr = csv::ReaderBuilder::new()
        .has_headers(false)
        .from_path(filename)
        .unwrap();

    // それぞれのレコード上をループする
    for result in rdr.records() {
        let record = result.unwrap();
        let v = &record[0];
        let tt = NaiveDateTime::parse_from_str(&v, &datetime_format).unwrap();

        t = (tt.timestamp(), tt.timestamp_subsec_micros());
        f = record[1].parse().unwrap();
        if !is_first {
            let carry = if t.1 < prev_time.1 { 1 } else { 0 };
            delta = (t.0 - prev_time.0 - carry) * micro as i64;
            delta = delta + (if carry == 0 {
                (t.1 - prev_time.1) as i64
            } else {
                (micro + t.1 - prev_time.1) as i64
            });
            total_time = total_time + delta;
            total_consumption += area_trapezoid(prev_value, f, delta);
        }
        prev_time = t;
        prev_value = f;
        is_first = false;
    }
    // println!(
    //     "{{'total_consumption[A*microsec]': {}, 'total_time[microsec]': {}, 'avg_consumption[A]': {}}}",
    //     total_consumption,
    //     total_time,
    //     (total_consumption / (total_time as f64))
    // );
    println!(
        "{{'total_consumption[A*sec]': {}, 'total_time[sec]': {}, 'avg_consumption[A]': {}}}",
        (total_consumption as f64) / micro as f64,
        (total_time as f64) / micro as f64,
        (total_consumption / (total_time as f64))
    );
}

fn area_trapezoid(upper_length: f64, lower_length: f64, height: i64) -> f64 {
    (upper_length + lower_length) * (height as f64) / 2.0
}
