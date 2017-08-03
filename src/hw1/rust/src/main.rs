extern crate rustc_serialize;

use std::env;
use std::fs::File;
use std::process;
use std::io::prelude::*;
use std::fmt;

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord)]
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


impl fmt::Display for Edge {
    fn fmt(&self, f: &mut fmt::Formatter) ->
    fmt::Result {
        write!(f, "({}, {})", self.x, self.y)
    }
}

#[derive(Debug)]
struct Header {
    num_vertices: u64,
    num_edges: u64
}



impl Header {
    pub fn inc_edges(&mut self) { self.num_edges += 1; }
    pub fn dec_edges(&mut self) { self.num_edges -= 1; }
}

impl fmt::Display for Header {
    fn fmt(&self, f: &mut fmt::Formatter) ->
    fmt::Result {
        write!(f, "Num Vertices: {}  Num Edges: {}", self.num_vertices, self.num_edges)
    }
}


struct Graph {
    header: Header,
    edges: Vec<Edge>
}

impl fmt::Display for Graph {
    fn fmt(&self, f: &mut fmt::Formatter) ->
    fmt::Result {
        write!(f, "{}\n{:?}", self.header, self.edges)
    }
}


impl Display for NumVec {
    fn fmt(&self, f: &mut Formatter) -> Result<(), Error> {
        write!(f, "{}\n{:?}", self.header);
        write!(f, "{}", comma_separated)
    }
}



impl Graph {
    pub fn connect(&mut self, a: u64, b: u64) {
        let edge = Edge::new(a, b);
        match self.edges.binary_search(&edge) {
            Ok(_) => println!("{} already in graph", edge),
            Err(pos) => {
                self.edges.insert(pos, edge);
                self.header.inc_edges();
            }
        }
    }
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
    let mut graph = Graph { header: header, edges: Vec::<Edge>::new() };

    while i < data.len() {
        graph.connect(data[i], data[i+1]);
        i += 2;
    }

    println!("Graph: {}", graph);

    let mut outfile: String = filename.to_owned();
    outfile.push_str(".graph");


    println!("Outfile: {}", outfile);
    let fout = File::create(outfile).expect("Cannot open output file");



}
