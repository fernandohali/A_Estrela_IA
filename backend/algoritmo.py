import sys
import copy

listaAberta = []    # Lista com as coordenadas que não tiveram seus vizinhos verificados
listaFechada = []   # Lista com as coordenadas que tiveram seus vizinhos verificados

def desenhar(lista_coordenadas):
    global mapa, inicio, final

    print(f"### PERCURSO de {inicio} até {final} ###")
    print(lista_coordenadas)
    print()

    simbolo_cima = '^'
    simbolo_baixo = 'v'
    simbolo_esquerda = '<'
    simbolo_direita = '>'

    simbolo_obstaculo = '■'  # 1 no mapa
    simbolo_livre = '-'      # 0 no mapa
    simbolo_inicio = 'A'
    simbolo_final = 'B'

    resultado = copy.deepcopy(mapa)
    atual = inicio
    simbolo = ''

    for pos in range(1, len(lista_coordenadas)):
        proximo = lista_coordenadas[pos]
        if proximo != inicio:
            if atual[0] > proximo[0]:
                simbolo = simbolo_cima
            elif atual[0] < proximo[0]:
                simbolo = simbolo_baixo
            elif atual[1] > proximo[1]:
                simbolo = simbolo_esquerda
            elif atual[1] < proximo[1]:
                simbolo = simbolo_direita

            if proximo == final:
                x, y = lista_coordenadas[pos - 1]
            else:
                x, y = proximo

            resultado[x][y] = simbolo
            atual = proximo

    resultado[inicio[0]][inicio[1]] = simbolo_inicio
    resultado[final[0]][final[1]] = simbolo_final

    print()
    for linha in resultado:
        print(' '.join(str(cell if isinstance(cell, str) else simbolo_obstaculo if cell == 1 else simbolo_livre) for cell in linha))
    print()

    return resultado


def recuperar_caminho(atual):
    global dicPosicoesCalculadas
    percurso = [atual]
    while atual != inicio:
        atual = dicPosicoesCalculadas[atual][3]
        percurso.append(atual)
    percurso.reverse()
    return percurso


def encontra_vizinhos(atual):
    global mapa
    global listaFechada

    vizinhos = []
    x, y = atual
    linhas = len(mapa)
    colunas = len(mapa[0])

    movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dx, dy in movimentos:
        nx, ny = x + dx, y + dy
        if 0 <= nx < linhas and 0 <= ny < colunas and mapa[nx][ny] != 1 and (nx, ny) not in listaFechada:
            vizinhos.append((nx, ny))

    return vizinhos


def ordena_pelo_custo():
    global listaAberta, dicPosicoesCalculadas
    listaAberta.sort(key=lambda coord: dicPosicoesCalculadas[coord][1] + dicPosicoesCalculadas[coord][2])


def calcula_custos(pai, vizinhos):
    global dicPosicoesCalculadas

    for vizinho in vizinhos:
        heuristica = distanciaManhattan(vizinho, final)
        custo = dicPosicoesCalculadas.get(pai, (None, 0))[1] + 1
        dicPosicoesCalculadas[vizinho] = (vizinho, custo, heuristica, pai)

    return dicPosicoesCalculadas


def criaMapa():
    matriz = []
    with open("backend/mapa.txt", "r") as arquivo:
        for linha in arquivo:
            if linha.strip():
                matriz.append([int(x) for x in linha.strip().split()])
    return matriz


def distanciaManhattan(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def buscar():
    global listaAberta, listaFechada, dicPosicoesCalculadas
    listaAberta.clear()
    listaFechada.clear()
    dicPosicoesCalculadas.clear()

    listaAberta.append(inicio)
    achou = False
    resultado = []

    while listaAberta and not achou:
        atual = listaAberta[0]
        vizinhos = encontra_vizinhos(atual)
        calcula_custos(atual, vizinhos)

        for vizinho in vizinhos:
            if vizinho not in listaAberta:
                listaAberta.append(vizinho)

        listaAberta.remove(atual)
        listaFechada.append(atual)

        if final in listaFechada:
            achou = True
            caminho = recuperar_caminho(final)
            resultado = desenhar(caminho)

        ordena_pelo_custo()

    return resultado


def entrada_de_dados():
    global inicio, final
    print("Exemplo de entrada (x y): = '0 0'\n")

    for i in range(2):
        ponto = 'inicial' if i == 0 else 'final'
        while True:
            entrada = input(f"Entre com o ponto {ponto} do trajeto: ")
            try:
                x, y = map(int, entrada.split())
                if mapa[x][y] == 1:
                    print(f"\nVocê escolheu um obstáculo como ponto {ponto}, escolha novamente\n")
                else:
                    if i == 0:
                        inicio = (x, y)
                    else:
                        final = (x, y)
                    break
            except Exception as e:
                print(f"Entrada inválida! Tente novamente. Erro: {e}")


def main():
    entrada_de_dados()
    if inicio == final:
        print("Você já chegou na sua meta. Já pode dobrá-la!")
    else:
        resultado = buscar()
        for linha in resultado:
            print(' '.join(str(cell) for cell in linha))
    return 0


# Variáveis Globais
mapa = criaMapa()
inicio = ()
final = ()
dicPosicoesCalculadas = {}

if __name__ == "__main__":
    main()
