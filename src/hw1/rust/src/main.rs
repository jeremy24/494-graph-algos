extern crate rustc_serialize;

#[macro_use]
extern crate serde_derive;
extern crate bincode;

use std::env;
use std::fs::File;
use std::process;
use std::io::prelude::*;
use std::fmt;
use std::path::Path;
use std::io::{stdin,stdout,Write};

use std::collections::VecDeque;
use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::BTreeSet;

use bincode::{serialize, deserialize, Infinite};

#[derive(Serialize, Deserialize, Debug)]
struct Header {
    num_vertices: u64,
    num_edges: u64
}

#[derive(Serialize, Deserialize)]
struct Graph {
    header: Header,
    edges: Vec<Vec<u64>>,
    weights: Vec<HashMap<u64, i64>>
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
    fn new(num_vertices: u64) -> Graph {
        let header: Header = Header { num_edges: 0, num_vertices: num_vertices };
        Graph {
            edges: vec![Vec::<u64>::new(); num_vertices as usize],
            header: header,
            weights: vec![HashMap::<u64, i64>::new(); num_vertices as usize]
        }
    }

    fn dump_to_file(&self, filename: &Path) {
        let mut fout = File::create(filename).expect("Cannot open output file");
        match serialize(&self, Infinite) {
            Ok(encoded) => {
                match fout.write_all(&encoded) {
                    Ok(_) => println!("Graph serialized successfully"),
                    Err(_) => println!("Unable to serialize graph")
                }
            }
            Err(_) => println!("Unable to serialize graph")
        }
    }
    fn index(a: u64, b: u64) -> (usize, u64) {
        if a < b {
            return (a as usize, b);
        }
        return (b as usize, a);
    }

    pub fn bfs(&self, start: u64) -> (Vec<u64>) {
        /*

        */
        let mut visited_order = Vec::<u64>::new();
        let mut visited = HashSet::new();
        let mut queue = VecDeque::<usize>::new();

        println!("Running a BFS");
        queue.push_back(start as usize);
        while !queue.is_empty() {
            let vert: usize = queue.pop_front().unwrap();
            if !visited.contains(&(vert)) {
                visited.insert(vert);
                visited_order.push(vert as u64);
                for neighbor in 0..self.edges.len() {
                    if self.has_edge(vert as u64, neighbor as u64) &&
                            !visited.contains(&neighbor){
                        queue.push_back(neighbor);
                    }
                }
            }
        }
        return visited_order;
    }

    pub fn dfs(&self, start: u64) -> (Vec<u64>) {
        /*

        */
        let mut visited_order = Vec::<u64>::new();
        let mut visited = HashSet::new();
        let mut queue = VecDeque::<usize>::new();

        println!("Running a DFS");
        queue.push_back(start as usize);
        while !queue.is_empty() {
            let vert: usize = queue.pop_front().unwrap();
            if !visited.contains(&(vert)) {
                visited.insert(vert);
                visited_order.push(vert as u64);
                for neighbor in 0..self.edges.len() {
                    if self.has_edge(vert as u64, neighbor as u64) &&
                            !visited.contains(&neighbor){
                        queue.push_front(neighbor);
                    }
                }
            }
        }
        return visited_order;
    }

    pub fn comps(&self) -> Vec<BTreeSet<u64>> {
        let mut ret = Vec::new();
        let mut seen = BTreeSet::new();

        while seen.len() != self.header.num_vertices as usize {

            for index in 0..self.header.num_vertices {
                if !seen.contains(&index) {
                    let mut conns = BTreeSet::new();
                    for value in self.bfs(index as u64) {
                        conns.insert(value);
                        seen.insert(value);
                    }
                    ret.push(conns);
                }
            }
        }
        return ret;
    }

    pub fn density(&self) -> f64 {
        if self.header.num_edges == 0 { return 0.0; }
        let top = 2.0 * self.header.num_edges as f64;
        let bottom: u64 = self.header.num_vertices * (self.header.num_vertices - 1);
        return top / bottom as f64;
    }

    pub fn min_degree(&self) -> i64 {
        return self.edges
            .iter()
            .map(|row| row.len() as i64)
            .min()
            .unwrap_or(-1);
    }

    pub fn max_degree(&self) -> i64 {
        return self.edges
            .iter()
            .map(|row| row.len() as i64)
            .max()
            .unwrap_or(-1);
    }


    #[allow(dead_code)]
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


    pub fn add_weight(&mut self, a: u64, b: u64, weight: i64) {
        let (x, y) = Graph::index(a, b);
        assert!(self.has_edge(x as u64, y as u64));
        self.weights[x].insert(y, weight);
    }

    pub fn weight(&self, a: u64, b: u64) -> (i64) {
        let (x, y) = Graph::index(a, b);
        assert!(self.has_edge(x as u64, y as u64));
        return *self.weights[x].get(&y).expect("Unable to get a weight");
    }

    pub fn connect_with_weight(&mut self, a: u64, b: u64, weight: i64) {
        self.connect(a, b);
        self.add_weight(a, b, weight);
    }

    #[allow(dead_code)]
    pub fn remove(&mut self, a: u64, b: u64) {
        let (x, y) = Graph::index(a, b);
        if x < self.edges.len() {
            match self.edges[x].binary_search(&y) {
                Ok(pos) => {
                    self.edges[x].remove(pos);
                    self.header.dec_edges();
                }
                Err(_) => {}
            }
        } else {
            println!("Invalid vert pair passed to connect: ({}, {})", a, b);
        }
    }
}


fn graph_from_text(filename: &Path) -> (Graph) {
    let mut fin = File::open(filename).expect("Cannot open input graph file");
    let mut buffer = String::new();
    fin.read_to_string(&mut buffer).expect("Unable to read graph file");


    let mut lines = buffer
        .lines()
        .peekable()
        .map(|val|String::from(val));

    let raw_header = lines
        .next().expect("Cannot extract header");

    let header: Vec<u64> = raw_header.split("\t")
        .map(|value| String::from(value))
        .map(| value: String| value.parse::<u64>().expect("Cannot parse header"))
        .collect();

    if header.len() != 2 {
        println!("Invalid header in file: {:?}", header);
        process::exit(2);
    }

//    let data_by_line: Vec<u64> = Vec::new();
    let mut graph = Graph::new(10);

    let num_verts: u64 = header[0];
    let num_edges: u64 = header[1];


    let first_line = lines
        .next()
        .expect("Can't retrieve line");
//        .split("\t").count();

    let have_weights = first_line.split("\t").count() == 3;

    let mut graph = Graph::new(header[0]);

    if have_weights {
        for line in lines {
            let split: Vec<String> = line.split("\t").map(|val| String::from(val)).collect();
            let x = split[0].parse::<u64>().expect("Can't parse first vert value");
            let y = split[1].parse::<u64>().expect("Can't parse last vert value");
            let weight = split[2].parse::<i64>().expect("Can't parse weight value");
            graph.connect_with_weight(x, y, weight);
        }
    }

    println!("First line length: {:?}", first_line);

    println!("Header: {:?}", header);


//    let raw_lines: Vec<String> = lines.collect();


    //    println!("Data: {:?}", data_by_line.next().expect("blah"));
    //
//    .map(|v|String::from(v)))
//        .collect();
////        .split("\t").collect();


//    let has_weights = data_by_line[0].len() == 3;
//
//
//    println!("Has weights: {:?}:   {:?}", has_weights, data_by_line[0]);
//
//
//    if !has_weights {
//        assert!(data_by_line[0].len() == 2);
//    }



//    let has_weights = first_line
//        .split_whitespace().count() == 3;
////        .count() == 3;

//    let split_data = buffer
////        .split("\t")
////        .map(|chunk: str| String::new(str) );
//            .split(|c: char| !c.is_numeric());
//
//
//
//
//    let mut num_tabs = 0;
//    for j in 0..500 {
//        let character: char = split_data
//    }


//    let mut i: usize = 0;
//    for value in split_data {
//        match value.parse::<u64>() {
//            Ok(val) => {
//                if i == 0 {
//                    num_verts = val;
//                } else if i == 1 {
//                    num_edges = val;
//                } else {
//                    data.push(val);
//                }
//            }
//            Err(_) => {}
//        }
//        i += 1;
//    }
    println!("Number of edges: {}", num_edges);

    let mut i = 0;


//    let mut graph = Graph::new(num_verts);

//    while i < data.len() {
//        graph.connect(data[i], data[i + 1]);
//        i += 2;
//    }
    return graph;
}


fn graph_from_serialized(filename: &Path) -> (Graph) {
    let mut fin = File::open(filename).expect("Cannot open input graph file");

    let mut buffer = Vec::<u8>::new();
    fin.read_to_end(&mut buffer).expect("Unable to read serialized graph file");

    match deserialize(&buffer) {
        Ok(value) => return value,
        Err(_) => {
            println!("Invalid serialized graph file provided");
            process::exit(1);
        }
    }
}


fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        println!("Must provide a graph file");
        process::exit(1);
    }

    let fin_path = Path::new(&args[1]);

    if fin_path.extension().is_none() {
        println!("Unable to get file extension of input file: {}", fin_path.display());
    }
    let ext = fin_path.extension().unwrap();
    println!("ext: {:?}", ext);

    let graph: Graph;

    if ext == "graph" {
        graph = graph_from_serialized(&fin_path);
    } else {
        graph = graph_from_text(&fin_path);
    }

    let mut user_input = String::new();
    loop {
        println!("Enter a command:");
        stdout().flush();
        user_input.clear();
        stdin().read_line(&mut user_input).expect("Unable to read user input.");
        user_input = user_input.replace("\n", "");


        println!("User entered: [{}]", user_input);
        println!(" dfs == {}: {}", user_input, user_input == "dfs");

        if user_input == "bfs" {
            println!("\nBFS:");
            println!("{:?}", graph.bfs(0));
        } else if user_input == "dfs" {
            println!("\nDFS:");
            println!("{:?}", graph.dfs(0));
        } else if user_input == "exit" {
            println!("\nExiting:");
            break;
        }
    }


//    println!("Graph: \n{}", graph);
    println!("Density: {}", graph.density());
    println!("Max Degree: {}", graph.max_degree());
    println!("Min Degree: {}", graph.min_degree());

//    println!("DFS: {:?}", graph.dfs(0));
//
//    println!("BFS: {:?}", graph.bfs(0));

    let comps = graph.comps();
    println!("Number of components: {}", comps.len());
    println!("Comps: {:?}", comps);
    println!();

    //    println!("Max Degree: {}", graph.max_degree());

//    let mut outpath = fin_path.to_path_buf();
//    outpath.set_extension("output");
//    graph.dump_to_file(&outpath);
}
