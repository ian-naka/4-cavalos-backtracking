import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CPP_SOURCE = ROOT / "solver.cpp"
CPP_BINARY = ROOT / "solver"


def executar_solver():
    subprocess.run(
        ["g++", "-std=c++17", str(CPP_SOURCE), "-o", str(CPP_BINARY)],
        check=True,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    resultado = subprocess.run(
        [str(CPP_BINARY)],
        check=True,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return json.loads(resultado.stdout)


def imprimir_tabuleiro(estado):
    for linha in range(0, 9, 3):
        print(" ".join(estado[linha:linha + 3]))
    print("------")


payload = executar_solver()

if payload.get("success"):
    passos = payload["steps"]
    print(f"Solução encontrada em {len(passos) - 1} passos!\n")
    for indice, estado in enumerate(passos):
        print(f"Passo {indice}:")
        imprimir_tabuleiro(list(estado))
else:
    print("Nenhuma solução possível.")
