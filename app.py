from flask import Flask, request, jsonify
from main import produtos, validar_token

app = Flask(__name__)

# Filtros
def filtrar_por_nome(produtos, nome):
    return [p for p in produtos if nome.lower() in p['product_name'].lower()]

def filtrar_por_preco_maximo(produtos, preco_max):
    return [p for p in produtos if p['product_price'] <= preco_max]

def filtrar_por_estoque_minimo(produtos, estoque_min):
    return [p for p in produtos if p['stock_quantity'] >= estoque_min]

@app.route("/produtos/filtro", methods=["GET"])
def filtrar_produtos():
    if not validar_token():
        return jsonify(message="Token inválido ou ausente"), 403

    nome = request.args.get("nome")
    preco_max = request.args.get("preco_max", type=float)
    estoque_min = request.args.get("estoque_min", type=int)

    resultado = produtos.copy()

    if nome:
        resultado = filtrar_por_nome(resultado, nome)
    if preco_max is not None:
        resultado = filtrar_por_preco_maximo(resultado, preco_max)
    if estoque_min is not None:
        resultado = filtrar_por_estoque_minimo(resultado, estoque_min)

    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)

