
let pipe fs =
  let f a x result n = x (a n) in
  let base result n = n in List.fold_left f base fs;;

let _ = pipe [(fun x  -> x + x); (fun x  -> x + 3)] 3;;