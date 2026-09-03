#include <iostream>
#include <map>
#include <string>
#include <vector>

using namespace std;

string boardToString(const vector<char>& board) {
    return string(board.begin(), board.end());
}

void backtracking(
    const vector<char>& tabuleiroAtual,
    const vector<char>& tabuleiroFinal,
    const vector<vector<int>>& adj,
    vector<vector<char>>& caminhoAtual,
    vector<vector<char>>& melhorCaminho,
    map<vector<char>, int>& melhoresDistancias
) {
    if (!melhorCaminho.empty() && caminhoAtual.size() >= melhorCaminho.size()) {
        return;
    }

    if (caminhoAtual.size() > 20) {
        return;
    }

    if (tabuleiroAtual == tabuleiroFinal) {
        melhorCaminho = caminhoAtual;
        return;
    }

    for (int i = 0; i < 9; ++i) {
        if (tabuleiroAtual[i] != 'V') {
            for (int vizinho : adj[i]) {
                if (tabuleiroAtual[vizinho] == 'V') {
                    vector<char> novoEstado = tabuleiroAtual;
                    swap(novoEstado[i], novoEstado[vizinho]);

                    int novaDistancia = static_cast<int>(caminhoAtual.size()) + 1;

                    if (melhoresDistancias.find(novoEstado) == melhoresDistancias.end() ||
                        novaDistancia < melhoresDistancias[novoEstado]) {
                        melhoresDistancias[novoEstado] = novaDistancia;
                        caminhoAtual.push_back(novoEstado);
                        backtracking(
                            novoEstado,
                            tabuleiroFinal,
                            adj,
                            caminhoAtual,
                            melhorCaminho,
                            melhoresDistancias
                        );
                        caminhoAtual.pop_back();
                    }
                }
            }
        }
    }
}

int main() {
    vector<char> tabuleiroInicio = {
        'B', 'V', 'B',
        'V', 'V', 'V',
        'P', 'V', 'P'
    };

    vector<char> tabuleiroFinal = {
        'P', 'V', 'P',
        'V', 'V', 'V',
        'B', 'V', 'B'
    };

    vector<vector<int>> adj = {
        {5, 7}, {6, 8}, {3, 7}, {2, 8}, {}, {0, 6}, {1, 5}, {0, 2}, {1, 3}
    };

    vector<vector<char>> caminhoAtual;
    vector<vector<char>> melhorCaminho;
    map<vector<char>, int> melhoresDistancias;

    caminhoAtual.push_back(tabuleiroInicio);
    melhoresDistancias[tabuleiroInicio] = 1;

    backtracking(tabuleiroInicio, tabuleiroFinal, adj, caminhoAtual, melhorCaminho, melhoresDistancias);

    if (melhorCaminho.empty()) {
        cout << "{\"success\":false}";
        return 0;
    }

    cout << "{\"success\":true,\"steps\":[";
    for (size_t i = 0; i < melhorCaminho.size(); ++i) {
        if (i > 0) {
            cout << ",";
        }
        cout << "\"" << boardToString(melhorCaminho[i]) << "\"";
    }
    cout << "]}";

    return 0;
}
