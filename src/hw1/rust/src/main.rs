extern crate rustc_serialize;

use std::env;
use std::fs::File;
use std::process;
use std::io::prelude::*;


#[derive(Debug)]
struct Edge {
    x: u64,
    y: u64
}


impl Edge {
    fn new(x: u64, y: u64) -> Edge {
        if x < y {
            println!("{} < {}", x, y);
            Edge {
                x: x,
                y: y
            }
        } else {
            println!("{} else {}", x, y);
            Edge {
                x: y,
                y: x
            }
        }
    }
}

struct Header {
    num_vertices: u64,
    num_edges: u64
}


fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        println!("Must provide a graph file");
        process::exit(1);
    }

    let ref filename = args[1];
    let mut fin = File::open(filename).expect("Cannot open input graph file");
    let mut buffer = String::new();
    fin.read_to_string(&mut buffer).expect("Unable to read graph file");

    let split_data = buffer
        .split(|c: char| !c.is_numeric());

    let mut data: Vec<u64> = Vec::new();


    let mut num_verts: u64 = 0;
    let mut num_edges: u64 = 0;


    let mut i = 0;
    for value in split_data {
        match value.parse::<u64>() {
            Ok(val) => {
                if i == 0 {
                    num_verts = val;
                } else if i == 1 {
                    num_edges = val;
                } else {
                    data.push(val);
                }
            },
            Err(_) => {}
        }
        i+=1;
    }

    println!("Number of edges: {}", num_edges);

    i = 0;
    if data.len() != (num_edges * 2) as usize {
        println!("Data len: {} != num edges {}", data.len(), num_edges);
        process::exit(2);
    }
    let header = Header{ num_vertices: num_verts, num_edges: num_edges };

    let mut outfile: String = filename.to_owned();
    outfile.push_str(".graph");


    println!("{:?}", x);
    println!("{:?}", y);

    println!("Outfile: {}", outfile);
    let fout = File::create(outfile).expect("Cannot open output file");



}
