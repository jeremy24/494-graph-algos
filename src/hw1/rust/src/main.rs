extern crate rustc_serialize;

use std::env;
use std::fs::File;
use std::process;
use std::io::prelude::*;
use std::fmt;


#[derive(Debug)]
struct Header {
    num_vertices: u64,
    num_edges: u64
}

struct Graph {
    header: Header,
    edges: Vec<Vec<u64>>
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


impl fmt::Display for Graph {
    fn fmt(&self, f: &mut fmt::Formatter) ->
    fmt::Result {
        write!(f, "{}\n{:?}", self.header, self.edges)
    }

}



impl Graph {
    fn new(num_vertices: u64, num_edges: u64) -> Graph {
        let header: Header = Header { num_edges: num_edges, num_vertices: num_vertices };
        Graph {
            edges: vec![Vec::<u64>::new(); num_vertices as usize],
            header: header
        }
    }

    fn index(a: u64, b: u64) -> (usize, u64) {
        if a < b {
            return (a as usize, b);
        }
        return (b as usize, a);
    }

    pub fn has_edge(&self, a: u64, b: u64) -> bool {
        let (x, y) = Graph::index(a, b);
        if x >= self.edges.len() {
            return false;
        }
        match self.edges[x].binary_search(&y) {
            Ok(_) => return true,
            Err(_) => return false
        }
    }
    pub fn connect(&mut self, a: u64, b: u64) {
        let (x, y) = Graph::index(a, b);
        if x < self.edges.len() {
            match self.edges[x].binary_search(&y) {
                Ok(_) => println!("({}, {}) already in graph", x, y),
                Err(pos) => {
                    self.edges[x].insert(pos, y);
                    self.header.inc_edges();
                }
            }
        } else {
            println!("Invalid vert pair passed to connect: ({}, {})", a, b);
        }
    }
    pub fn remove(&mut self, a: u64, b: u64) {
        let (x, y) = Graph::index(a, b);
        if x < self.edges.len() {
            match self.edges[x].binary_search(&y) {
                Ok(pos) => {
                    self.edges[x].remove(pos);
                    self.header.dec_edges();
                },
                Err(_) => {}
            }
        } else {
            println!("Invalid vert pair passed to connect: ({}, {})", a, b);
        }
    }
}
//fn zero_vector(size: u64) -> Vec<u8> {
//    let mut zero_vec: Vec<u8> = Vec::with_capacity(size as usize);
//    for i in 0..size {
//        zero_vec.push(0);
//    }
//    return zero_vec;
//}


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

    let mut graph = Graph::new(num_verts, num_edges);

    while i < data.len() {
        graph.connect(data[i], data[i+1]);
        i += 2;
    }

    println!("Has edge (1,7) => {}", graph.has_edge(1, 7));
    println!("Has edge (0, 5) => {}", graph.has_edge(0, 5));

    graph.remove(0, 5);
    println!("Has edge (0, 5) => {}", graph.has_edge(0, 5));

    println!("Graph: {}", graph);

    let mut outfile: String = filename.to_owned();
    outfile.push_str(".graph");


    println!("Outfile: {}", outfile);
    let fout = File::create(outfile).expect("Cannot open output file");



}
