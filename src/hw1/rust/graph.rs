
use std::fs::io;
use std::fs::File;
use std::io::prelude::*;

struct Edge {
    i: i8,
    j: i8
}

fn main() {
    let usage_message: String = "./graph [graph file]";
    let args: Vec<String> = env::args().collect();

    if args.len() != 2 {
        println!(usage_message)
        return 1
    }

    let filename = args[1];

    println!("Reading graph from file: {}", filename)

    let file_handle = File::open(filename)?;
    let mut fin = BufReader::new(file);
    let mut contents = String::new();
    fin.read_to_string(&mut contents)?;

    let edge: Edge = Edge { i:8, j:9 };
    println!("Edge: ({}, {})", edge.i, edge.j)

}
