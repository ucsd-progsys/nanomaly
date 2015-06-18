module NanoML.Pretty
  (pretty, prettyProg, hsep, vsep, vcat, Doc, render, (==>), (=:), nest)
  where

import Prelude hiding ( (<$>) )
import Data.List hiding (group)
import Text.PrettyPrint.ANSI.Leijen hiding (Pretty, pretty)
import qualified Text.PrettyPrint.ANSI.Leijen as PP

import NanoML.Types

class Pretty a where
  pretty :: a -> Doc
  pretty = prettyPrec 0

  prettyPrec :: Int -> a -> Doc
  prettyPrec _ = pretty

-- | Wrap the enclosed 'Doc' in parentheses only if the condition holds.
parensIf True  = parens
parensIf False = id

instance Pretty Value where
  prettyPrec z v = case v of
    VI i -> pretty i
    VD d -> pretty d
    VC c -> pretty c
    VS s -> text $ show s
    VB b -> text (if b then "true" else "false")
    VU   -> text "()"
    VL l -> brackets $ hcat $ intersperse semi $ map pretty l
    VT _ xs -> parens $ hcat $ intersperse comma $ map pretty xs
    VF (Func e _) -> prettyPrec z e


instance Pretty Literal where
  pretty l = case l of
    LI i -> pretty i
    LD d -> pretty d
    LC c -> pretty c
    LS s -> text $ show s
    LB b -> text (if b then "true" else "false")
    LU   -> text "()"

instance Pretty Expr where
  prettyPrec z e = case e of
    Var v -> text v
    Lam p e -> group $ parensIf (z > zl) $ nest 2 $
               text "fun" <+> pretty p <+> text "->" <$> pretty e
      where zl = 5
    App (Var f) [x, y]
      | isInfix f
        -> parensIf (z > zf) $
           prettyPrec (zf+1) x <+> text f <+> prettyPrec (zf+1) y
      where zf = opPrec f
    App f xs -> parensIf (z > za) $
                prettyPrec za f <+> hsep (map (prettyPrec (za+1)) xs)
      where za = 26
    Lit l -> pretty l
    Let r bnds body -> group $ parensIf (z > zl) $
                       align $ text "let" <> pretty r <+> prettyBinds bnds
                               <+> text "in" <$> pretty body
      where zl = 4
    Ite b t f -> group $ parensIf (z > zi) $ align $
                 text "if"   <+> pretty b <$>
                 text "then" <+> pretty t <$>
                 text "else" <+> pretty f
      where zi = 7
    Seq x y -> parensIf (z > zs) $
               prettyPrec (zs+1) x <> semi </> prettyPrec (zs+1) y
      where zs = 3
    Case e alts -> parensIf (z > zc) $
                   text "match" <+> pretty e <+> text "with"
                     <$> vsep (map prettyAlt alts)
      where zc = 5
    Nil -> text "[]"
    Cons x xs -> parensIf (z > zc) $
                 prettyPrec (zc+1) x <+> text "::" <+> prettyPrec (zc+1) xs
      where zc = 20
    Tuple xs -> parens $ hcat $ intersperse comma $ map pretty xs
    Prim1 p x -> parens (text (show p) <+> pretty x)
    Prim2 p x y -> parens (text (show p) <+> pretty x <+> pretty y)
    Val v -> prettyPrec z v
    Bop bop x y -> parensIf (z > zb) $
                   prettyPrec (zb+1) x <+> pretty bop <+> prettyPrec (zb+1) y
      where zb = opPrec undefined

instance Pretty Bop where
  pretty Eq = text "=#"
  pretty Neq = text "<>#"
  pretty Lt = text "<#"
  pretty Le = text "<=#"
  pretty Gt = text ">#"
  pretty Ge = text ">=#"
  pretty And = text "&&#"
  pretty Or = text "||#"
  pretty Plus = text "+#"
  pretty Minus = text "-#"
  pretty Times = text "*#"
  pretty Div = text "/#"
  pretty Mod = text "mod#"
  pretty FPlus = text "+.#"
  pretty FMinus = text "-.#"
  pretty FTimes = text "*.#"
  pretty FDiv = text "/.#"
  pretty FExp = text "exp#"

isInfix :: Var -> Bool
isInfix = all (`elem` "!$%&*+-./:<=>?@^|~")

opPrec :: Var -> Int
opPrec = const 5 -- FIXME

instance Pretty RecFlag where
  pretty Rec = text " rec"
  pretty _   = empty

instance Pretty Pat where
  pretty p = case p of
    VarPat v -> text v
    LitPat l -> pretty l
    ConsPat x xs -> pretty x <+> text "::" <+> pretty xs
    ConPat c (TuplePat []) -> text c
    ConPat c p -> text c <+> pretty p
    ListPat l -> brackets $ encloseSep lbracket rbracket semi $ map pretty l
    TuplePat l -> parens $ hcat $ intersperse comma $ map pretty l
    WildPat -> text "_"

prettyBind (p, e) = group $ nest 2 $ pretty p <+> text "=" <$> pretty e

prettyBinds [b] = prettyBind b
prettyBinds (b:bs) = prettyBind b <$> text "and" <+> prettyBinds bs

prettyAlt (p, g, e) = text "|" <+> pretty p
                      <> maybe empty (\g -> text " when" <+> pretty g) g
                      <+> text "->" <+> pretty e

instance Pretty Decl where
  pretty d = case d of
    DFun r bnds -> text "let" <> pretty r <+> prettyBinds bnds <+> text ";;"

prettyProg :: Prog -> Doc
prettyProg = vsep . map pretty


instance Pretty Int where
  pretty = PP.pretty

instance Pretty Double where
  pretty = PP.pretty

instance Pretty Char where
  pretty = PP.pretty

expr ==> val = nest 2 $ pretty expr <$> (text "==>" <+> pretty val)
var =: val   = group $ nest 2 $ text var    <+> (text ":="  <$> pretty val)

render :: Doc -> String
render d = displayS (renderSmart 0.5 72 d) ""


instance Pretty Type where
  prettyPrec z t = case t of
    TVar v -> squote <> text v
    TCon c -> text c
    TApp t1 t2 -> pretty t2 <+> pretty t1
    TTup ts -> parens $ hsep $ intersperse (text "*") $ map pretty ts
    ti :-> to -> parensIf (z > zf) $
                 prettyPrec (zf+1) ti <+> text "->" <+> prettyPrec zf to
      where zf = 5