def test_app_is_created(app):
    assert app.name == "api_flask.app"
    assert not app.config["DEBUG"] 
    assert app.config["TESTING"]


def test_produto_is_created(client):

    ''' Tests if the route /produtos is working '''

    new_product_data =  {
    "portal": 123,
    "cod_produto": 6,
    "cod_barra": "7890123456789",
    "nomeproduto": "Nome do Produto",
    "cod_ncm": "123456789012345",
    "desc_cor": "Cor do Produto",
    "desc_tamanho": "Tamanho do Produto",
    "desc_setor": "Setor do Produto",
    "desc_linha": "Linha do Produto",
    "desc_marca": "Marca do Produto",
    "desc_colecao": "Coleção do Produto",
    "id_cor": 101,
    "id_tamanho": "M",
    "id_setor": 202,
    "id_linha": 303,
    "id_marca": 404,
    "id_colecao": 505,
    "dt_cadastro": "2024-01-31",
    "timestamp": 1643587200
  }
    
    response = client.post("/api/produtos/", json=new_product_data)

    assert response.status_code == 201
    assert response.json["cod_produto"] == 6
    assert not response.json["cod_produto"] == 1

    
