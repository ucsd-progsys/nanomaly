
let stringOfList f l =
  let fx a b = match b with | [] -> [] | h::t -> List.append a (f b) in
  let base = "" in List.fold_left fx base l;;