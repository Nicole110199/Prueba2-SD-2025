
import json
import re

def cargar_configuracion(ruta_rango, ruta_intereses):
    with open(ruta_rango, 'r', encoding='utf-8') as f:
        rangos = json.load(f)
    with open(ruta_intereses, 'r', encoding='utf-8') as f:
        intereses = json.load(f)
    return rangos, intereses

def determinar_grupo_etario(edad, rangos):
    for grupo, (inicio, fin) in rangos.items():
        if inicio <= edad <= fin:
            return grupo
    return None

def calcular_puntaje(documento, palabras_clave, grupo_etario, intereses):
    titulo = documento.get("titulo", "").lower()
    coincidencias = sum(1 for palabra in palabras_clave if palabra in titulo)
    categoria = documento.get("categoria", "").lower()
    puntaje_categoria = intereses.get(categoria, {}).get(grupo_etario, 0)

    # NUEVA FÓRMULA CORREGIDA
    score = coincidencias * 10 + puntaje_categoria

    return {
        "documento": documento,
        "score": score,
        "coincidencias_titulo": coincidencias,
        "puntaje_categoria": puntaje_categoria
    }

def aplicar_ranking(documentos, consulta_titulo, edad, rangos, intereses):
    palabras_clave = [p.lower() for p in re.split(r"[\s+]", consulta_titulo) if p.strip()]
    grupo_etario = determinar_grupo_etario(edad, rangos) if edad is not None else None

    resultados = []
    for doc in documentos:
        if grupo_etario:
            resultado = calcular_puntaje(doc, palabras_clave, grupo_etario, intereses)
        else:
            coincidencias = sum(1 for palabra in palabras_clave if palabra in doc.get("titulo", "").lower())
            resultado = {
                "documento": doc,
                "score": coincidencias * 10,
                "coincidencias_titulo": coincidencias,
                "puntaje_categoria": 0
            }
        resultados.append(resultado)

    resultados.sort(key=lambda x: x["score"], reverse=True)
    return resultados
