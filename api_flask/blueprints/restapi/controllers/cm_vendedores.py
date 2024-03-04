from flask import request
from flask_restx import Resource, fields, Namespace
from api_flask.extensions.db import db
from api_flask.models.cm_vendedores import CmVendedoresModel
from api_flask.schemas.cm_vendedores import CmVendedoresSchema
from api_flask.schemas.cm_movimento import CmMovimentoSchema
from api_flask.schemas.comentarios import ComentariosSchema
from api_flask.extensions.auth import auth

# from api_flask.server.instance import server

# api = server.cm_vendedores_ns
cm_vendedores_schema = CmVendedoresSchema()
cm_vendedores_list_schema = CmVendedoresSchema(many=True)
cm_movimento_list_schema = CmMovimentoSchema(many=True) 
comentarios_list_schema = ComentariosSchema(many=True)


api = Namespace("cm_vendedores", description="CM Vendedores related operations", path="/vendedores")

item = api.model(
    "CmVendedores",
    {
        "portal": fields.Integer(1),
        "cod_vendedor": fields.Integer(1),
        "nome_vendedor": fields.String("Nome do Vendedor"),
        "tipo_vendedor": fields.String("Tipo do Vendedor"),
        "fone_vendedor": fields.String("Telefone do Vendedor"),
        "mail_vendedor": fields.String("E-mail do Vendedor"),
        "ativo": fields.String("Ativo"),
        "data_admissao": fields.Date(),
        "data_saida": fields.Date(),
        "timestamp": fields.Integer(1),
        "matricula": fields.String("Matrícula"),
    },
)


class CmVendedores(Resource):


    @auth.login_required(role="admin")
    def get(self, cod_vendedor):
        cm_vendedores = CmVendedoresModel.find_by_cod_vendedor(cod_vendedor)
        if cm_vendedores:
            return cm_vendedores_schema.dump(cm_vendedores), 200
        return {"message": "CM Vendedores not found"}, 404

    @auth.login_required(role="admin")
    def delete(self, cod_vendedor):
        cm_vendedores = CmVendedoresModel.find_by_cod_vendedor(cod_vendedor)
        if cm_vendedores:
            cm_vendedores.delete_from_db()
            return {"message": "CM Vendedores deleted"}, 200
        return {"message": "CM Vendedores not found"}, 404



    @auth.login_required(role="admin")
    @api.expect(item)
    @api.doc("Update an existing cm_vendedores")
    def put(self, cod_vendedor):
        cm_vendedores_json = request.get_json()
        cm_vendedores = CmVendedoresModel.find_by_cod_vendedor(cod_vendedor)
        if cm_vendedores:
            for key, value in cm_vendedores_json.items():
                if value is not None:
                    setattr(cm_vendedores, key, value)
            cm_vendedores.update_to_db()
            return cm_vendedores_schema.dump(cm_vendedores), 200
        else:
            return {"message": "CM Vendedores not found"}, 404

@api.route("")
class CmVendedoresList(Resource):

    @auth.login_required(role="admin")
    def get(self):
        return cm_vendedores_list_schema.dump(CmVendedoresModel.find_all()), 200


    @auth.login_required(role="admin")
    @api.expect(item)
    @api.doc("Create a new cm_vendedores")
    def post(self):
        cm_vendedores_json = request.get_json()
        if isinstance(cm_vendedores_json, list):
            cm_vendedores = cm_vendedores_list_schema.load(
                cm_vendedores_json, session=db.session
            )
            for vendedor in cm_vendedores:
                if CmVendedoresModel.find_by_cod_vendedor(vendedor.cod_vendedor):
                    return {
                        "message": f"An cm_vendedores with cod_vendedor '{vendedor.cod_vendedor}' already exists."
                    }, 400
            try:
                for vendedor in cm_vendedores:
                    vendedor.save_to_db()
            except Exception as e:
                return {
                    "message": f"An error occurred inserting the cm_vendedores {e}"
                }, 500
            return cm_vendedores_list_schema.dump(cm_vendedores), 201

        cm_vendedores = cm_vendedores_schema.load(
            cm_vendedores_json, session=db.session
        )
        if CmVendedoresModel.find_by_cod_vendedor(cm_vendedores.cod_vendedor):
            return {
                "message": f"An cm_vendedores with cod_vendedor '{cm_vendedores.cod_vendedor}' already exists."
            }, 400
        try:
            cm_vendedores.save_to_db()
        except Exception as e:
            return {
                "message": f"An error occurred inserting the cm_vendedores {e}"
            }, 500
        return cm_vendedores_schema.dump(cm_vendedores), 201


class CmVendedoresMovimentosList(Resource):

    @auth.login_required(role="admin")
    def get(self, cod_vendedor):
        cm_vendedores = CmVendedoresModel.find_by_cod_vendedor(cod_vendedor)
        if cm_vendedores:
            return cm_movimento_list_schema.dump(cm_vendedores.movimentos), 200
        return {"message": "CM Vendedores not found"}, 404
    

class CmVendedoresComentariosList(Resource):

    @auth.login_required(role="admin")
    def get(self, cod_vendedor):
        cm_vendedores = CmVendedoresModel.find_by_cod_vendedor(cod_vendedor)
        if cm_vendedores:
            return comentarios_list_schema.dump(cm_vendedores.comentarios), 200
        return {"message": "CM Vendedores not found"}, 404
