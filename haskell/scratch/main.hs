import Data.List
import System.IO

-- add an edge
-- dont allow edges back to self
addEdge :: [(Int,Int)] -> Int -> Int -> [(Int, Int)]
addEdge list u v
    | u < v = list ++ [(u,v)]
    | v < u = list ++ [(v,u)]


equalEdge :: (Int,Int) -> (Int,Int) -> Bool
equalEdge (a,b) (c,d)
    | a == c = b == d
    | a == d = b == c
    | True = False


removeEdge :: [(Int,Int)] -> (Int,Int) -> [(Int, Int)]
removeEdge list edge = (filter p list)
    where p (x,y) = not (equalEdge (x,y) edge)

hasEdge :: [(Int,Int)] -> (Int, Int) -> Bool
hasEdge list edge
    | fst edge < snd edge = elem edge list
    | True = elem (snd edge, fst edge) list
