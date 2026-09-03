from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
import subprocess
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent
CPP_SOURCE = ROOT.parent / "solver.cpp"
CPP_BINARY = ROOT / "solver"
ADJ = {
    0: [5, 7],
    1: [6, 8],
    2: [3, 7],
    3: [2, 8],
    4: [],
    5: [0, 6],
    6: [1, 5],
    7: [0, 2],
    8: [1, 3],
}
CODIGO_FONTE = CPP_SOURCE.read_text(encoding="utf-8")


def carregar_solucao_cpp():
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
    payload = json.loads(resultado.stdout)
    if not payload.get("success"):
        raise RuntimeError("Não foi possível encontrar uma solução no solver C++.")
    return payload["steps"]


def gerar_passos():
    caminho = carregar_solucao_cpp()
    passos = []

    for indice, estado in enumerate(caminho):
        movimento = None
        if indice > 0:
            anterior = caminho[indice - 1]
            origem_movimento = None
            destino_movimento = None
            for posicao, (origem, destino) in enumerate(zip(anterior, estado)):
                if origem != destino and origem != "V":
                    origem_movimento = {"peca": origem, "de": posicao + 1}
                if origem != destino and destino != "V":
                    destino_movimento = posicao + 1

            if origem_movimento is not None and destino_movimento is not None:
                movimento = {
                    **origem_movimento,
                    "para": destino_movimento,
                }

        estado_formatado = {f"casa{posicao + 1}": valor for posicao, valor in enumerate(estado)}

        if movimento is None:
            descricao = (
                "Estado inicial do tabuleiro. O solver em C++ começa nesta configuração e "
                "explora os movimentos válidos usando backtracking com poda por melhor caminho e por profundidade."
            )
            analise = {
                "estadoAnterior": None,
                "casasOcupadas": [indice + 1 for indice, valor in enumerate(estado) if valor != "V"],
                "movimentosPossiveis": [],
                "movimentoEscolhido": None,
            }
        else:
            estado_anterior = caminho[indice - 1]
            casas_ocupadas = [i + 1 for i, valor in enumerate(estado_anterior) if valor != "V"]
            conexoes_disponiveis = [posicao + 1 for posicao in ADJ[movimento["de"] - 1]]
            movimentos_possiveis = [
                casa
                for casa in conexoes_disponiveis
                if estado_anterior[casa - 1] == "V"
            ]

            descricao = (
                f"Comparando os estados, a peça {movimento['peca']} saiu da casa "
                f"{movimento['de']} e foi para a casa {movimento['para']}. No estado anterior, as casas "
                f"ocupadas eram {casas_ocupadas}. A peça {movimento['peca']} estava na casa {movimento['de']} "
                f"e podia tentar {conexoes_disponiveis}; dessas, {movimentos_possiveis} estavam livres. "
                f"O solver escolheu {movimento['para']} e seguiu a busca em profundidade a partir desse novo estado."
            )

            analise = {
                "estadoAnterior": {
                    f"casa{posicao + 1}": valor for posicao, valor in enumerate(estado_anterior)
                },
                "casasOcupadas": casas_ocupadas,
                "movimentosPossiveis": movimentos_possiveis,
                "movimentoEscolhido": movimento["para"],
                "conexoesAnalisadas": conexoes_disponiveis,
            }

            if estado == "PVPVVVBVB":
                descricao += (
                    " Neste ponto, o tabuleiro atingiu a configuração final, então o solver encontrou a solução."
                )

        passos.append({
            "indice": indice,
            "estado": estado_formatado,
            "movimento": movimento,
            "descricao": descricao,
            "analise": analise,
        })

    return passos


PASSOS = gerar_passos()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path

        if path in ("/", "/index.html"):
            html = (ROOT / "index.html").read_text(encoding="utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
            return

        if path == "/api/passos":
            payload = {
                "titulo": "Visualizador de Backtracking do Tabuleiro 3x3",
                "totalPassos": len(PASSOS),
                "solucaoEmMovimentos": len(PASSOS) - 1,
                "passos": PASSOS,
                "conexoes": {str(chave + 1): [valor + 1 for valor in valores] for chave, valores in ADJ.items()},
                "codigoFonte": CODIGO_FONTE,
            }
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_response(404)
        self.end_headers()


def main():
    host = "127.0.0.1"
    port = int(os.environ.get("PORT", "8000"))
    server = HTTPServer((host, port), Handler)
    print(f"Servidor iniciado em http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
