"""Integrador da tarefa 14.5: ler -> 3-conexo? -> trilha de contracoes -> reconstruir -> saida.
Uso: python planar_contract.py exemplos/cubo.txt"""
import sys
from common.graphs import ler
from m1_conexidade.m1 import is_3connected, find_separator
from m2_contracao.m2 import contraction_trace, branch_sets
from m3_faces.m3 import reconstruct, check_embedding
from m4_certificado.m4 import obstruction, model_from_tk, lift_model, verify_minor, certificate_ops
from m5_base_ciclos.m5 import face_basis, verify_basis


def decidir(adj, log=None):
    """Supoe is_3connected(adj)."""
    trace, k4 = contraction_trace(adj)                    # M1 + M2
    faces, falha = reconstruct(trace, k4, log)            # M3
    if faces is not None:
        return dict(planar=True, trace=trace, k4=k4, faces=faces)
    k, C, Ao = falha
    x, y, A, B = trace[k]
    tk = obstruction(C, x, y, A, B, Ao)                   # M4
    modelo = lift_model(model_from_tk(tk), branch_sets(trace, k, list(adj)))
    return dict(planar=False, trace=trace, k4=k4, k=k, C=C, A=Ao, B=B, tk=tk, kind=tk["kind"], model=modelo)


def fmt(s):
    return "{" + ",".join(map(str, sorted(s))) + "}"


def main():
    if len(sys.argv) < 2:
        print("uso: python planar_contract.py exemplos/arquivo.txt")
        return 0
    adj = ler(sys.argv[1])
    if not is_3connected(adj):
        sep = find_separator(adj)
        if sep is None:
            print("ENTRADA INVALIDA: menos de 4 vertices")
        else:
            print("ENTRADA INVALIDA: nao e 3-conexo; separador", " ".join(map(str, sep)) or "(vazio: desconexo)")
        return 2
    log = []
    r = decidir(adj, log)
    print("PLANAR" if r["planar"] else "NAO PLANAR")
    print(f"contracoes: {len(r['trace'])}")
    from m2_contracao.m2 import contract
    J = adj
    for k, (x, y, A, B) in enumerate(r["trace"]):
        J = contract(J, x, y)
        print(f"  passo {k}: contrai ({x},{y})  N(x)-y={A}  N(y)-x={B}  ->  {len(J)} vertices, "
              f"3-conexo: {'sim' if is_3connected(J) else 'NAO'}")
    print(f"  K4 final: {sorted(r['k4'])}")
    print("reconstrucao:")
    for item in log:
        k, x, y, C, Ao, B, i = item[:7]
        if i is None:
            print(f"  passo {k}: ({x},{y}) C={C} Ao={Ao} B={B} -> FALHA no teste de intervalo")
        else:
            print(f"  passo {k}: ({x},{y}) C={C} Ao={Ao} B={B} i={i} -> {item[7]} faces")
    if r["planar"]:
        msg = check_embedding(adj, r["faces"])
        assert msg is None, msg
        print("faces:")
        for f in r["faces"]:
            print("  face", " ".join(map(str, f)))
        vecs, eid = face_basis(adj, r["faces"], outer=0)
        v = verify_basis(adj, vecs, eid)
        assert v["ok"], v
        print(f"base esparsa: {v['count']} ciclos; posto F2 = {v['rank']} = m-n+1 = {v['expected']}; "
              f"max aresta em {v['maxuse']}; verificacao: ok")
    else:
        print(f"falhou no passo {r['k']} (teste de intervalo); menor {r['kind']} (caso {r['tk']['caso']})")
        print(f"C = {' '.join(map(str, r['C']))} | A = {' '.join(map(str, r['A']))} | B = {' '.join(map(str, r['B']))}")
        ops, H = certificate_ops(adj, r["model"], r["kind"])
        txt = []
        for op in ops:
            if op[0] == "del_vertex":
                txt.append(f"del_vertex {op[1]}")
            else:
                txt.append(f"{op[0]} {op[1]} {op[2]}")
        print("operacoes:", " / ".join(txt) if txt else "nenhuma")
        print("conjuntos:", " ".join(fmt(s) for s in r["model"].values()))
        msg = verify_minor(adj, r["model"], r["kind"])
        assert msg is None, msg
        print("verificacao: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
