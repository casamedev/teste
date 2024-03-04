from flask import request
from flask_restx import Resource, fields, Namespace
# from scripts.seed_data import seed_cm_clientes_fornec
from api_flask.models.cm_clientes_fornec import CmClientesFornecModel
from api_flask.schemas.cm_clientes_fornec import CmClientesFornecSchema
from api_flask.schemas.cm_movimento import CmMovimentoSchema
from api_flask.schemas.comentarios import ComentariosSchema
# from api_flask.server.instance import server
from api_flask.extensions.db import db
from api_flask.extensions.auth import auth
# import json

# cm_clientes_fornec_ns = server.cm_clientes_fornec_ns
cm_clientes_fornec_schema = CmClientesFornecSchema()
cm_clientes_fornec_list_schema = CmClientesFornecSchema(many=True)
cm_movimento_schema = CmMovimentoSchema(many=True)
comentarios_list_schema = ComentariosSchema(many=True)

api = Namespace("cm_clientes_fornec", description="CM Clientes Fornec related operations", path="/clientes")

item = api.model(
    "CmClientesFornec",
    {
        "nportal": fields.Integer(1),
        "cliente_identificado": fields.Integer(1),
        "cod_cliente": fields.Integer(1),
        "razao_cliente": fields.String("Razão Social do Cliente"),
        "nome_cliente": fields.String("Nome do Cliente"),
        "tipo_cliente": fields.String("Tipo do Cliente"),
        "cidade_cliente": fields.String("Cidade do Cliente"),
        "uf_cliente": fields.String("UF do Cliente"),
        "fone_cliente": fields.String("Telefone do Cliente"),
        "email_cliente": fields.String("Email do Cliente"),
        "sexo": fields.String("Sexo"),
        "data_nascimento": fields.Date(),
        "fone_celular": fields.String("Telefone Celular"),
        "timestamp": fields.Integer(1),
    },
)

@api.route("/<int:cod_cliente>")
class CmClientesFornecedor(Resource):

    @auth.login_required()
    def get(self, cod_cliente):
        cm_clientes_fornec = CmClientesFornecModel.find_by_cod_cliente(cod_cliente)
        if cm_clientes_fornec:
            return cm_clientes_fornec_schema.dump(cm_clientes_fornec), 200
        return {"message": "CM Clientes Fornec not found"}, 404

    @auth.login_required(role="admin")
    def delete(self, cod_cliente):
        cm_clientes_fornec = CmClientesFornecModel.find_by_cod_cliente(cod_cliente)
        if cm_clientes_fornec:
            cm_clientes_fornec.delete_from_db()
            return {"message": "CM Clientes Fornec deleted"}, 200
        return {"message": "CM Clientes Fornec not found"}, 404


    @auth.login_required(role="admin")
    @api.expect(item)
    @api.doc("Update an existing cm_clientes_fornec")
    def put(self, cod_cliente):
        cm_clientes_fornec_json = request.get_json()
        cm_clientes_fornec = CmClientesFornecModel.find_by_cod_cliente(cod_cliente)
        if cm_clientes_fornec:
            for key, value in cm_clientes_fornec_json.items():
                if value is not None: 
                    setattr(cm_clientes_fornec, key, value)
            cm_clientes_fornec.update_to_db()
            return cm_clientes_fornec_schema.dump(cm_clientes_fornec), 200
        else:
            return {"message": "CM Clientes Fornec not found"}, 404

@api.route("/")
class CmClientesFornecedorList(Resource):
    @auth.login_required(role="admin")
    def get(self):
        return (
            cm_clientes_fornec_list_schema.dump(CmClientesFornecModel.find_all()),
            200,
        )

    @auth.login_required(role="admin")
    @api.expect(item)
    @api.doc("Create a new cm_clientes_fornec")
    def post(self):
        cm_clientes_fornec_json = request.get_json()
        if isinstance(cm_clientes_fornec_json, list):
            cm_clientes_fornec = cm_clientes_fornec_list_schema.load(
                cm_clientes_fornec_json, session=db.session, unknown="exclude"
            )
            for cliente in cm_clientes_fornec:
                if CmClientesFornecModel.find_by_cod_cliente(cliente["cod_cliente"]):
                    return {
                        "message": f"An cm_clientes_fornec with cod_cliente '{cliente['cod_cliente']}' already exists."
                    }, 400
                try:
                    cliente.save_to_db()
                except Exception as e:
                    return {
                        "message": f"An error occurred inserting the cm_clientes_fornec :{e}"
                    }, 500

            return cm_clientes_fornec_list_schema.dump(cm_clientes_fornec_json), 201
        else:
            cm_clientes_fornec = cm_clientes_fornec_schema.load(
                cm_clientes_fornec_json, session=db.session, unknown="exclude"
            )
            if CmClientesFornecModel.find_by_cod_cliente(
                cm_clientes_fornec.cod_cliente
            ):
                return {
                    "message": f"An cm_clientes_fornec with cod_cliente '{cm_clientes_fornec.cod_cliente}' already exists."
                }, 400
            else:
                try:
                    cm_clientes_fornec.save_to_db()
                except Exception as e:
                    return {
                        "message": f"An error occurred inserting the cm_clientes_fornec: {e}"
                    }, 500
                return cm_clientes_fornec_schema.dump(cm_clientes_fornec), 201


class CmClientesFornecedorTimestamp(Resource):
    @auth.login_required()
    def get(self):
        return (
            cm_clientes_fornec_schema.dump(
                CmClientesFornecModel.find_by_max_timestamp()
            ),
            200,
        )


# class CmClientesFornecSeed(Resource):
#     def get(self):
#         cm_clientes_fornec_json = seed_cm_clientes_fornec()
#         print("Tipo de entrada:", type(cm_clientes_fornec_json))
#         print("Conteúdo da entrada:", cm_clientes_fornec_json)

#         try:
#             cm_clientes_fornec_data = json.loads(cm_clientes_fornec_json)

#             # Carregar os dados usando o esquema
#             cm_clientes_fornec = cm_clientes_fornec_list_schema.load(
#                 cm_clientes_fornec_data, session=db.session
#             )
#             db.session.bulk_save_objects(cm_clientes_fornec)
#             db.session.commit()
#             return cm_clientes_fornec_list_schema.dump(cm_clientes_fornec), 201
#         except Exception as e:
#             print("Erro ao carregar os dados:", e)
#             return {"error": str(e)}, 400

@api.route("/<int:cod_cliente>/movimentos")
class CmClientesFornecMovimento(Resource):
    @auth.login_required(role="admin")
    def get(self, cod_cliente):
        cliente = CmClientesFornecModel.find_by_cod_cliente(cod_cliente)
        if cliente:
            movimentos = cliente.movimentos
            return cm_movimento_schema.dump(movimentos), 200

@api.route("/<int:cod_cliente>/comentarios")
class CmClientesFornecComentarios(Resource):

    @auth.login_required()
    def get(self, cod_cliente):
        cliente = CmClientesFornecModel.find_by_cod_cliente(cod_cliente)
        if cliente:
            comentarios = cliente.comentarios
            return comentarios_list_schema.dump(comentarios), 200
