import mercadopago

public_key = "APP_USR-b49bcf1d-9b7a-44e8-9592-432158b580ed"
token = "APP_USR-2196431973526070-092718-14d3f7e8cceadbda2ecb13f1f40972cd-2011153384"


def criar_pagamento(itens_pedido, link):
    # Adicione as credenciais
    sdk = mercadopago.SDK(token)
      
    # itens que ele está comprando no formato de dicionário
    itens = []
    for item in itens_pedido:
        quantidade = int(item.quantidade)
        nome_produto = item.item_estoque.produto.nome
        preco_unitario = float(item.item_estoque.produto.preco)
        itens.append({
                "title": nome_produto,
                "quantity": quantidade,
                "unit_price": preco_unitario

        })

        # valor total
    preference_data = {
        "items": itens,
        "auto_return": "all",
        "back_urls": {
            "success": link,
            "pending": link,
            "failure": link,
        }
    }
    resposta = sdk.preference().create(preference_data)
    link_pagamento = resposta["response"]["init_point"]
    id_pagamento = resposta["response"]["id"]
    return link_pagamento, id_pagamento
    