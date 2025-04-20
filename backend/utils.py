def valida_coordenadas(inicio: tuple[int, int], final: tuple[int, int], mapa: list[list[int]]) -> bool:
    linhas = len(mapa)
    colunas = len(mapa[0]) if linhas > 0 else 0
    
    # Verifica se as coordenadas estão dentro dos limites do mapa
    if (inicio[0] < 0 or inicio[0] >= linhas or inicio[1] < 0 or inicio[1] >= colunas or
        final[0] < 0 or final[0] >= linhas or final[1] < 0 or final[1] >= colunas):
        return False
    
    # Verifica se as coordenadas não são obstáculos
    if mapa[inicio[0]][inicio[1]] == 1 or mapa[final[0]][final[1]] == 1:
        return False
    
    return True