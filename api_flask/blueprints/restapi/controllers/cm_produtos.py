from flask import request
from flask_restx import Resource, fields, Namespace
from api_flask.extensions.db import db
from api_flask.models.cm_produtos import CmProdutosModel
from api_flask.schemas.cm_produtos import CmProdutosSchema
from api_flask.extensions.auth import auth
# from api_flask.server.instance import server
# cm_produtos_ns = server.cm_produtos_ns
cm_produtos_schema = CmProdutosSchema()
cm_produtos_list_schema = CmProdutosSchema(many=True)



api = Namespace("cm_produtos", description="CM Produtos related operations", path="/produtos")



item = api.model(
    "CmProdutos",
    {
        "portal": fields.Integer(1),
        "cod_produto": fields.Integer(1),
        "cod_barra": fields.String("Código de Barras"),
        "nomeproduto": fields.String("Nome do Produto"),
        "cod_ncm": fields.String("Código NCM"),
        "desc_cor": fields.String("Descrição da Cor"),
        "desc_tamanho": fields.String("Descrição do Tamanho"),
        "desc_setor": fields.String("Descrição do Setor"),
        "desc_linha": fields.String("Descrição da Linha"),
        "desc_marca": fields.String("Descrição da Marca"),
        "desc_colecao": fields.String("Descrição da Coleção"),
        "id_cor": fields.Integer(1),
        "id_tamanho": fields.String("ID do Tamanho"),
        "id_setor": fields.Integer(1),
        "id_linha": fields.Integer(1),
        "id_marca": fields.Integer(1),
        "id_colecao": fields.Integer(1),
        "dt_cadastro": fields.String("Data de Cadastro"),
        "timestamp": fields.Integer(1),
    },
)


class CmProdutos(Resource):

    @auth.login_required(role="admin")
    def get(self, cod_produto):
        cm_produtos = CmProdutosModel.find_by_cod_produto(cod_produto)
        if cm_produtos:
            return cm_produtos_schema.dump(cm_produtos), 200
        return {"message": "CM Produtos not found"}, 404

    @auth.login_required(role="admin")
    def delete(self, cod_produto):
        cm_produtos = CmProdutosModel.find_by_cod_produto(cod_produto)
        if cm_produtos:
            cm_produtos.delete_from_db()
            return {"message": "CM Produtos deleted"}, 200
        return {"message": "CM Produtos not found"}, 404


    @auth.login_required(role="admin")
    @api.expect(item)
    @api.doc("Update an existing cm_produtos")
    def put(self, cod_produto):
        cm_produtos_json = request.get_json()
        cm_produtos = CmProdutosModel.find_by_cod_produto(cod_produto)
        if cm_produtos:
            for key, value in cm_produtos_json.items():
                if value is not None:
                    setattr(cm_produtos, key, value)
            cm_produtos.update_in_db()
            return cm_produtos_schema.dump(cm_produtos), 200
        else:
            return {"message": "CM Produtos not found"}, 404

@api.route("/")
class CmProdutosList(Resource):

    @auth.login_required(role="admin")
    def get(self):
        return cm_produtos_list_schema.dump(CmProdutosModel.find_all()), 200

    @auth.login_required(role="admin")
    @api.expect(item)
    @api.doc("Create a new cm_produtos")
    def post(self):
        cm_produtos_json = request.get_json()
        if isinstance(cm_produtos_json, list):
            cm_produtos = cm_produtos_list_schema.load(
                cm_produtos_json, session=db.session
            )
            for produto in cm_produtos:
                if CmProdutosModel.find_by_cod_produto(produto.cod_produto):
                    return {
                        "message": f"An cm_produtos with cod_produto '{produto.cod_produto}' already exists."
                    }, 400
                try:
                    produto.save_to_db()
                except Exception as e:
                    return {
                        "message": f"An error occurred inserting the CM Produtos: {e}"
                    }, 500

            return cm_produtos_list_schema.dump(cm_produtos), 201

        cm_produtos = cm_produtos_schema.load(cm_produtos_json, session=db.session)
        try:
            cm_produtos.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred inserting the CM Produtos: {e}"}, 500
        return cm_produtos_schema.dump(cm_produtos), 201


class CmProdutosRelation(Resource):

    @auth.login_required(role="admin")
    def post(
        self, produto_id_origem, produto_id_destino
    ):  # MUdar isso faqui urgentemente !!!!!!!!!!!!!!!!!!!!!
        produto_origem = CmProdutosModel.find_by_cod_produto(produto_id_origem)
        produto_destino = CmProdutosModel.find_by_cod_produto(produto_id_destino)
        if produto_origem and produto_destino:
            produto_origem.produtos_relacionados.append(produto_destino)
            db.session.commit()
            return {"message": "Relacionamento criado"}, 201
        return {"message": "Produto não encontrado"}, 404


    @auth.login_required(role="admin")
    def delete(self, produto_id_origem, produto_id_destino):
        produto_origem = CmProdutosModel.find_by_cod_produto(produto_id_origem)
        produto_destino = CmProdutosModel.find_by_cod_produto(produto_id_destino)
        if produto_origem and produto_destino:
            produto_origem.produtos_relacionados.remove(produto_destino)
            db.session.commit()
            return {"message": "Relacionamento removido"}, 200
        return {"message": "Produto não encontrado"}, 404


    @auth.login_required(role="admin")
    def get(self, produto_id_origem):
        produto_origem = CmProdutosModel.find_by_cod_produto(produto_id_origem)
        if produto_origem:
            return cm_produtos_list_schema.dump(
                produto_origem.produtos_relacionados
            ), 200
        return {"message": "Produto não encontrado"}, 404

class CmProdutosRationList(Resource):


    @auth.login_required(role="admin")
    def get(self):
        produto_origem = CmProdutosModel.find_all()
        relacoes = []
        for produto in produto_origem:
            relacoes.append(
                {
                    "produto_origem": produto.cod_produto,
                    "nome_produto_origem": produto.nomeproduto,
                    "produtos_destino": [
                        produto_destino.nomeproduto
                        for produto_destino in produto.produtos_relacionados
                    ],
                    "cod_produtos_destino": [
                        produto_destino.cod_produto
                        for produto_destino in produto.produtos_relacionados
                    ],
                }
            )

        return relacoes, 200
