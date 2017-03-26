
-- data Weight = Weight Float deriving (Show)
-- data Edge = Edge (Int, Int) Weight deriving (Show)
--
-- data GraphInfo = GraphInfo (Int, Int) deriving (Show)
--
-- data Graph = Graph GraphInfo [Edge] deriving (Show)

data Edge = Edge {
    u :: Int,
    v :: Int
} deriving (Show, Eq, Read)

data Graph = Graph {
    numVerts :: Int,
    numEdges :: Int,
    edges :: [Edge]
} deriving (Show)


makeEdgePair :: Int -> Int -> [Edge]
makeEdgePair u v = [(Edge u v), (Edge v u)]

makeGraph :: Int -> Int -> Graph
makeGraph verts edges = Graph verts edges []

inGraph :: Graph -> Edge -> Bool
inGraph graph edge = elem edge (edges graph)

addEdge :: Graph -> Int -> Int -> Graph
addEdge graph u v
    | (u < numVerts graph) && v < (numVerts graph) =
        Graph (numVerts graph) ((numEdges graph) + 1) ((edges graph) ++ (makeEdgePair u v))
    -- | (u >= numVerts graph) && v >= (numVerts graph) =
    --     graph





-- addEdge :: Graph -> Edge -> Graph
-- addEdge (Graph GraphInfo (Int Int) edges) edge = Graph
