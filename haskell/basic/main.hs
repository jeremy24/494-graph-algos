


connected a b graph = 
    if elem (a,b) (tail graph) 
        then True 
    else elem (b,a) graph