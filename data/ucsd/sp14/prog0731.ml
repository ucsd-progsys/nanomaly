
let rec listReverse l =
  match l with | h::t -> h :: (l listReverse t) | [] -> l;;