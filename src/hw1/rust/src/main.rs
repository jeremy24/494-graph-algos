extern crate rustc_serialize;
extern crate bincode;
extern crate rand;

#[macro_use] extern crate serde_derive;
#[macro_use] extern crate cached;
#[macro_use] extern crate lazy_static;

use std::sync::Mutex;
use std::env;
use std::f64;
use std::u64;
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
//use std::collections::BinaryHeap;

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
    weights: Vec<HashMap<u64, f64>>,
    default_weight: f64,
    neighbor_cache: HashMap<usize, Vec<usize>>
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
            weights: vec![HashMap::<u64, f64>::new(); num_vertices as usize],
            default_weight: 1.0,
            neighbor_cache: HashMap::<usize, Vec<usize>>::new()
        }
    }

    #[allow(dead_code)]
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


    pub fn dfs(&self, start: u64) -> (Vec<u64>) {
        /*

        */
        let mut visited_order = Vec::<u64>::new();
        let mut visited = HashSet::new();
        let mut stack = VecDeque::<usize>::new();

        println!("Running a DFS");
        stack.push_back(start as usize);
        while !stack.is_empty() {
            let vert: usize = stack.pop_front().unwrap();
            if !visited.contains(&(vert)) {
                visited.insert(vert);
                visited_order.push(vert as u64);
                for neighbor in 0..self.edges.len() {
                    if self.has_edge(vert as u64, neighbor as u64) &&
                            !visited.contains(&neighbor){
                        stack.push_front(neighbor);
                    }
                }
            }
        }
        return visited_order;
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

    #[allow(dead_code)]
    fn neighbors(&mut self, vertex: usize) -> Vec<usize> {
        let x = vertex;
        assert!(x < self.header.num_vertices as usize);

        if self.neighbor_cache.contains_key(&vertex) {
            let cached = self.neighbor_cache.get(&vertex).unwrap();
            println!("using cached");
            return cached.clone();
        }

        let mut neighbors = Vec::<usize>::new();
        for possible in 0..self.header.num_vertices {
            if self.has_edge(vertex as u64, possible as u64) {
                neighbors.push(possible as usize)
            }
        }
        self.neighbor_cache.insert(vertex, neighbors.clone());
        return neighbors;
    }


    fn min_dist(&self, distances: &Vec<f64>, to_visit: &BTreeSet<usize>) -> (usize, f64) {
        let mut min_distance: f64 = f64::MAX;
        let mut vertex: usize = 0;

        for i in 0..distances.len() {
            if to_visit.contains(&i) {
               if distances[i] < min_distance {
                   min_distance = distances[i];
                   vertex = i as usize;
               }
            }
        }
        let ret = (vertex, min_distance);
        return ret;
    }

    pub fn dij_path(&mut self, start: u64, end: u64) -> (f64, Vec<u64>) {
        let mut prev: Vec<u64> = vec![u64::MAX ; self.header.num_vertices as usize];
        let mut distance: Vec<f64> = vec![f64::MAX ; self.header.num_vertices as usize];


        let mut not_visited = BTreeSet::<usize>::new();

        for i in 0..self.header.num_vertices as usize{
            not_visited.insert(i);
        }

        distance[start as usize] = 0.0;

        loop {
            if not_visited.is_empty() {
                println!("Done all vertices, exiting...");
                break;
            }

            let (vertex, _) = self.min_dist(&distance, &not_visited);

            not_visited.remove(&vertex);

            if vertex == end as usize {
                println!("Found target");
                break;
            }

            for neighbor in self.neighbors(vertex) {
                let alt = distance[vertex] + self.weight(vertex as u64, neighbor as u64);
                if alt < distance[neighbor] {
                    distance[neighbor] = alt;
                    prev[neighbor] = vertex as u64;
                }
            }
        }

        // reconstruct the path
        let mut path = Vec::<u64>::new();
        let mut pre_idx = end;
        path.push(end);

        loop {
            let val = prev[pre_idx as usize];
            path.push(val);
            pre_idx = val;
            if val == start { break; }
        }

        path.reverse();

        println!("Path: {:?}", path);
        println!("Distance: {}", distance[end as usize]);
        return (distance[end as usize], path);
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

        let weight = rand::random::<f64>() * (rand::random::<f64>() * 10.0);

        self.connect_with_weight(a, b, weight);
    }


    pub fn add_weight(&mut self, a: u64, b: u64, weight: f64) {
        let (x, y) = Graph::index(a, b);
        assert!(self.has_edge(x as u64, y as u64));
        self.weights[x].insert(y, weight);
    }

    pub fn weight(&self, a: u64, b: u64) -> (f64) {
        let (x, y) = Graph::index(a, b);
        assert!(self.has_edge(x as u64, y as u64));
        if self.weights[x].contains_key(&y) {
            return *self.weights[x].get(&y).expect("Unable to get a weight");
        }
        return self.default_weight;
    }

    pub fn connect_with_weight(&mut self, a: u64, b: u64, weight: f64) {
        let (x, y) = Graph::index(a, b);
        if x < self.edges.len() {
            match self.edges[x].binary_search(&y) {
                Ok(_) => println!("({}, {}) already in graph", x, y),
                Err(pos) => {
                    self.edges[x].insert(pos, y);
                    self.header.inc_edges();
                    self.add_weight(a, b, weight);
                }
            }
        } else {
            println!("Invalid vert pair passed to connect: ({}, {}), Edges Len: {}", a, b, self.edges.len());
            process::exit(1);
        }
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

    let num_verts: u64 = header[0];
    let num_edges: u64 = header[1];

    let mut graph = Graph::new(num_verts);


    println!("Header: {:?}", header);

    let mut split: Vec<Vec<String>> = Vec::new();

    for line in lines {
        let split_line: Vec<String> = line.split("\t").map(|val| String::from(val)).collect();
        split.push(split_line);
    }


    let have_weights = split[0].len() == 3;

    if have_weights {
        for line in split {
            assert!(line.len() == 3);
            let x = line[0].parse::<u64>().expect("Can't parse first vertex value");
            let y = line[1].parse::<u64>().expect("Can't parse last vertex value");
            let weight = line[2].parse::<f64>().expect("Can't parse weight value");
            graph.connect_with_weight(x, y, weight);
        }
    } else {
        for line in split {
            assert!(line.len() == 2);
            let x = line[0].parse::<u64>().expect("Can't parse first vertex value");
            let y = line[1].parse::<u64>().expect("Can't parse last vertex value");
            graph.connect(x, y);
        }
    }

    assert_eq!(graph.header.num_edges, num_edges);

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

    let mut graph: Graph;

    if ext == "graph" {
        graph = graph_from_serialized(&fin_path);
    } else {
        graph = graph_from_text(&fin_path);
    }

    let mut user_input = String::new();

    graph.dij_path(0, 728);

    while true {
        println!("Enter a command:");
        let _ =stdout().flush();
        user_input.clear();
        stdin().read_line(&mut user_input).expect("Unable to read user input.");
        user_input = user_input.replace("\n", "");


        println!("User entered: [{}]", user_input);

        if user_input == "bfs" {
            println!("\nBFS:");
            println!("{:?}", graph.bfs(0));
        } else if user_input == "dfs" {
            println!("\nDFS:");
            println!("{:?}", graph.dfs(0));
        } else if user_input == "exit" {
            println!("\nExiting...");
            break;
        } else if user_input == "weights" {
            println!("Weights:");
            for a in 0..graph.header.num_vertices {
                for b in 0..graph.header.num_vertices {
                    if graph.has_edge(a, b) && a < b{
                        println!("({}, {}): {}", a, b, graph.weight(a, b));
                    }
                }
            }
        } else if user_input == "degree" {
            println!("Density: {}", graph.density());
            println!("Max Degree: {}", graph.max_degree());
            println!("Min Degree: {}", graph.min_degree());
        } else if user_input == "components" {
            let comps = graph.comps();
            println!("Number of components: {}", comps.len());
            println!("Comps: {:?}", comps);
        } else if user_input == "path" {
            graph.dij_path(0, 728);
        }
    }



    println!();

//
//    let mut outpath = fin_path.to_path_buf();
//    outpath.set_extension("output");
//    graph.dump_to_file(&outpath);
}
