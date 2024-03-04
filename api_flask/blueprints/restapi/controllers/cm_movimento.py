from flask import request
from flask_restx import Resource, fields, Namespace
from api_flask.extensions.db import db
from api_flask.models.cm_movimento import CmMovimentoModel
from api_flask.schemas.cm_movimento import CmMovimentoSchema
# from api_flask.server.instance import server
from api_flask.extensions.auth import auth

# cm_movimento_ns = server.cm_movimento_ns
cm_movimento_schema = CmMovimentoSchema()
cm_movimento_list_schema = CmMovimentoSchema(many=True)



api = Namespace("cm_movimento", description="CM Movimento related operations", path="/movimentos")


item = api.model(
    "CmMovimento",
    {
        "portal": fields.Integer(1),
        "cnpj_emp": fields.String("CNPJ da Empresa"),
        "documento": fields.Integer(1),
        "data_documento": fields.Date(),
        "codigo_cliente": fields.Integer(1),
        "cod_vendedor": fields.Integer(1),
        "quantidade": fields.Float(1.0),
        "preco_custo": fields.Float(1.0),
        "valor_liquido": fields.Float(1.0),
        "desconto": fields.Float(1.0),
        "valor_total": fields.Float(1.0),
        "forma_dinheiro": fields.Boolean("Forma Dinheiro"),
        "total_dinheiro": fields.Float(1.0),
        "forma_cheque": fields.Boolean("Forma Cheque"),
        "total_cheque": fields.Float(1.0),
        "forma_cartao": fields.Boolean("Forma Cartão"),
        "total_cartao": fields.Float(1.0),
        "forma_crediario": fields.Boolean("Forma Crediário"),
        "total_crediario": fields.Float(1.0),
        "forma_convenio": fields.Boolean("Forma Convênio"),
        "total_convenio": fields.Float(1.0),
        "frete": fields.Float(1.0),
        "operacao": fields.String("Operação"),
        "tipo_transacao": fields.String("Tipo de Transação"),
        "cod_produto": fields.Integer(1),
        "cancelado": fields.String("Cancelado"),
        "excluido": fields.String("Excluído"),
        "desconto_total_item": fields.Float(1.0),
        "timestamp": fields.Integer(1),
    },
)


class CmMovimento(Resource):

    @auth.login_required(role="admin")
    def get(self, timestamp):
        cm_movimento = CmMovimentoModel.find_by_timestamp(timestamp)
        if cm_movimento:
            return cm_movimento_schema.dump(cm_movimento), 200
        return {"message": "CM Movimento not found"}, 404
    
    @auth.login_required(role="admin")
    def delete(self, timestamp):
        cm_movimento = CmMovimentoModel.find_by_timestamp(timestamp)
        if cm_movimento:
            cm_movimento.delete_from_db()
            return {"message": "CM Movimento deleted"}, 200
        return {"message": "CM Movimento not found"}, 404

    @auth.login_required(role="admin")
    @api.expect(item)
    @api.doc("Update an existing cm_movimento")
    def put(self, timestamp):
        cm_movimento_json = request.get_json()
        cm_movimento = CmMovimentoModel.find_by_timestamp(timestamp)
        if cm_movimento:
            for key, value in cm_movimento_json.items():
                if value is not None:
                    setattr(cm_movimento, key, value)
            cm_movimento.update_to_db()
            return cm_movimento_schema.dump(cm_movimento), 200
        else:
            return {"message": "CM Movimento not found"}, 404

@api.route("")
class CmMovimentoList(Resource):

    @auth.login_required(role="admin")
    def get(self):
        movimentos = CmMovimentoModel.find_all()
        dto = [movimento.json() for movimento in movimentos]
        return dto, 200


    @auth.login_required(role="admin")
    @api.expect(item)
    @api.doc("Create a new cm_movimento")
    def post(self):
        cm_movimento_json = request.get_json()
        if isinstance(cm_movimento_json, list):
            cm_movimento = cm_movimento_list_schema.load(
                cm_movimento_json, session=db.session
            )
            for movimento in cm_movimento:
                try:
                    movimento.save_to_db()
                except Exception as e:
                    return {
                        "message": f"An error occurred inserting the CM Movimento: {e}"
                    }, 500
            return cm_movimento_list_schema.dump(cm_movimento), 201
        
        print(cm_movimento_json)
        cm_movimento = cm_movimento_schema.load(cm_movimento_json, session=db.session)
        cm_movimento.save_to_db()
        return cm_movimento_schema.dump(cm_movimento), 201
