
let rec wwhile (f,b) = let (b',c') = f b in if c' then wwhile (f, b') else b';;

let fixpoint (f,b) =
  wwhile (let fin (f',b') = (b', ((f' b') = b')) in ((fin (f, b)), b));;