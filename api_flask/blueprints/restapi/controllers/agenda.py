from flask import request
from flask_restx import Resource, fields, Namespace
from api_flask.extensions.db import db
from api_flask.models.agenda import AgendaModel
from api_flask.schemas.agenda import AgendaSchema
from api_flask.extensions.auth import auth
# from api_flask.server.instance import server
# agenda_ns = server.agenda_ns
agenda_schema = AgendaSchema()
agenda_list_schema = AgendaSchema(many=True)


api = Namespace("agenda", description="Agenda related operations", path="/agendas")

item = api.model(
    "agenda",
    {
        "codigo_cliente": fields.Integer(1),
        "data_retorno_ajustada": fields.String("Return date of the client"),
        "data_documento": fields.String("Document date of the client"),
        "documento": fields.Integer(1),
    },
)
@api.route("/<int:codigo_cliente>")
class Agenda(Resource):

    @auth.login_required(role="admin")
    def get(self, codigo_cliente):
        agenda = AgendaModel.find_by_codigo_cliente(codigo_cliente)
        if agenda:
            return agenda_schema.dump(agenda), 200
        return {"message": "Agenda not found"}, 404
    @auth.login_required(role="admin")
    def delete(self, codigo_cliente):
        agenda = AgendaModel.find_by_codigo_cliente(codigo_cliente)
        if agenda:
            agenda.delete_from_db()
            return {"message": "Agenda deleted"}, 200
        return {"message": "Agenda not found"}, 404
    
    @auth.login_required(role="admin")
    @api.expect(item)
    @api.doc("Update an existing agenda")
    def put(self, codigo_cliente):
        agenda_json = request.get_json()
        agenda = AgendaModel.find_by_codigo_cliente(codigo_cliente)
        if agenda:
            for key, value in agenda_json.items():
                if value is not None:
                    setattr(agenda, key, value)
            agenda.update_in_db()
            return agenda_schema.dump(agenda), 200
        else:
            return {"message": "Agenda not found"}, 404
@api.route("/")
class AgendaList(Resource):

    @auth.login_required()
    def get(self):
        print(AgendaModel.find_all())
        return agenda_list_schema.dump(AgendaModel.find_all()), 200

    @auth.login_required(role="admin")
    @api.expect(item)
    @api.doc("Create a new agenda")
    def post(self):
        agenda_json = request.get_json()
        if isinstance(agenda_json, list):
            agenda = agenda_list_schema.load(agenda_json, session=db.session)
            try:
                for agenda in agenda:
                    agenda.save_to_db()
            except Exception as e:
                return {"message": f"An error occurred inserting the Agenda: {e}"}, 500
            return agenda_list_schema.dump(agenda), 201
        
        agenda = agenda_schema.load(agenda_json, session=db.session)
        try:
            agenda.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred inserting the Agenda: {e}"}, 500
        return agenda_schema.dump(agenda), 201
