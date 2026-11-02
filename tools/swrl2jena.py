# -*- coding: utf-8 -*-
"""
Konversi otomatis 303 aturan SWRL -> aturan Jena (GenericRuleReasoner) agar Apache Jena Fuseki
bisa melakukan penalaran yang sama secara langsung (live) di server SPARQL.
Pemetaan built-in SWRL -> Jena:
  greaterThan->greaterThan, lessThan->lessThan, greaterThanOrEqual->ge, lessThanOrEqual->le,
  equal->equal, notEqual->notEqual, add(r,a,b,..)->sum berantai, subtract(r,a,b)->difference(a,b,r),
  multiply(r,a,b)->product(a,b,r), divide(r,a,b)->quotient(a,b,r), abs(r,a)->product(a,-1,n) max(a,n,r)
Pemakaian: python3 tools/swrl2jena.py output/fuseki/saham_rules.rules
"""
import os, re, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "lib"))
import warnings; warnings.filterwarnings("ignore")
from rules_swrl import define_rules
import kb_market

NS = "http://kbr.kelompok9.id/ontologi/SahamExpertKB.owl#"
ATOM = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\(([^()]*)\)")
CMP = {"greaterThan": "greaterThan", "lessThan": "lessThan", "greaterThanOrEqual": "ge", "lessThanOrEqual": "le",
       "equal": "equal", "notEqual": "notEqual"}

def term(t):
    t = t.strip()
    if t.startswith("?"): return t
    if re.fullmatch(r"-?\d+", t): return t
    if re.fullmatch(r"-?\d+\.\d+", t): return f"'{t}'^^xsd:double"   # hindari literal float presisi rendah
    return "ex:" + t

def convert(code, body, counter):
    lhs, rhs = body.split("->")
    out_l, out_r = [], []
    tmp = [0]
    def fresh():
        tmp[0] += 1; return f"?_t{tmp[0]}"
    for name, args in ATOM.findall(lhs):
        a = [term(x) for x in args.split(",")]
        if name in CMP:
            out_l.append(f"{CMP[name]}({', '.join(a)})")
        elif name == "add":
            r, xs = a[0], a[1:]
            cur = xs[0]
            for i, x in enumerate(xs[1:]):
                nxt = r if i == len(xs) - 2 else fresh()
                out_l.append(f"sum({cur}, {x}, {nxt})"); cur = nxt
        elif name == "subtract": out_l.append(f"difference({a[1]}, {a[2]}, {a[0]})")
        elif name == "multiply": out_l.append(f"product({a[1]}, {a[2]}, {a[0]})")
        elif name == "divide": out_l.append(f"quotient({a[1]}, {a[2]}, {a[0]})")
        elif name == "abs":
            n = fresh(); out_l.append(f"product({a[1]}, -1, {n})"); out_l.append(f"max({a[1]}, {n}, {a[0]})")
        elif len(a) == 1: out_l.append(f"({a[0]} rdf:type ex:{name})")
        elif len(a) == 2: out_l.append(f"({a[0]} ex:{name} {a[1]})")
        else: raise ValueError((code, name))
    for name, args in ATOM.findall(rhs):
        a = [term(x) for x in args.split(",")]
        out_r.append(f"({a[0]} rdf:type ex:{name})" if len(a) == 1 else f"({a[0]} ex:{name} {a[1]})")
    rid = code.replace("-", "_")
    return f"[{rid}: {' '.join(out_l)} -> {' '.join(out_r)}]"

def main(dst):
    rules = define_rules(kb_market.FAKTOR)
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    with open(dst, "w", encoding="utf-8") as f:
        f.write("# Aturan Jena hasil konversi otomatis dari 303 aturan SWRL SahamExpertKB v2\n")
        f.write("# Dipakai Apache Jena Fuseki (GenericRuleReasoner). RDFS disertakan agar hierarki kelas ikut diturunkan.\n")
        f.write(f"@prefix ex: <{NS}>.\n@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.\n@prefix xsd: <http://www.w3.org/2001/XMLSchema#>.\n\n")
        f.write("# Hierarki kelas (RDFS subclass) sebagai aturan FORWARD agar terlihat oleh aturan pakar\n")
        f.write("[rdfs_subclass_transitif: (?a rdfs:subClassOf ?b) (?b rdfs:subClassOf ?c) -> (?a rdfs:subClassOf ?c)]\n")
        f.write("[rdfs_tipe_turunan: (?x rdf:type ?a) (?a rdfs:subClassOf ?b) -> (?x rdf:type ?b)]\n\n")
        for code, pilar, desc, body in rules:
            f.write(f"# {code} | {pilar} | {desc}\n{convert(code, body, 0)}\n\n")
    print(f"{len(rules)} aturan ditulis ke {dst}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "output", "fuseki", "saham_rules.rules"))
