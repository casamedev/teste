from api_flask.extensions.db import db
from flask import request
from flask_restx import Resource, fields, Namespace
from api_flask.models.comentarios import ComentariosModel
from api_flask.schemas.comentarios import ComentariosSchema
# from api_flask.server.instance import server
from api_flask.extensions.auth import auth

# comentarios_ns = server.comentarios_ns

comentarios_schema = ComentariosSchema()
comentarios_list_schema = ComentariosSchema(many=True)


api = Namespace("comentarios", description="Comentarios related operations", path="/comentarios")


item = api.model(
    "Comentarios",
    {
        "comentario": fields.String("Comentário"),
        "vendedor_id": fields.Integer(1),
        "data": fields.Date(),
        "cliente_id": fields.Integer(1),
        "status": fields.String("Status"),
    },
)


class Comentarios(Resource):

    @auth.login_required(role="admin")
    def get(self, id_comentario):
        comentario = ComentariosModel.find_by_id(id_comentario)
        if comentario:
            return comentarios_schema.dump(comentario), 200
        return {"message": "Comentario not found"}, 404


    @auth.login_required(role="admin")
    def delete(self, id_comentario):
        comentario = ComentariosModel.find_by_id(id_comentario)
        if comentario:
            comentario.delete_from_db()
            return {"message": "Comentario deleted"}, 200
        return {"message": "Comentario not found"}, 404
    
    @auth.login_required(role="admin")
    def put(self, id_comentario):
        comentario_json = request.get_json()
        comentario = ComentariosModel.find_by_id(id_comentario)
        if comentario:
            for key, value in comentario_json.items():
                print (key, value)
                if value is not None:
                    setattr(comentario, key, value)
            comentario.update()
            return comentarios_schema.dump(comentario), 200
        return {"message": "Comentario not found"}, 404


class ComentariosList(Resource):

    @auth.login_required(role="admin")
    def get(self):
        return comentarios_list_schema.dump(ComentariosModel.find_all()), 200


    @auth.login_required(role="admin")
    @api.expect(item)
    @api.doc("Create a new comentario")
    def post(self):
        comentario_json = request.get_json()
        if isinstance(comentario_json, list):
            comentarios_list_schema.load(
                comentario_json, session=db.session, unknown="exclude"
            )
            for comentario in comentario_json:
                if ComentariosModel.find_by_id(comentario["id"]):
                    return {
                        "message": f"An comentario with id '{comentario['id']}' already exists."
                    }, 400
                try:
                    comentarios_list_schema.save_to_db()
                except Exception as e:
                    return {
                        "message": f"An error occurred inserting the comentario. Error: {e}"
                    }, 500
            return comentarios_list_schema.dump(comentario_json), 201
        else:
            comentario = comentarios_schema.load(
                comentario_json, session=db.session, unknown="exclude"
            )
            if ComentariosModel.find_by_id(comentario.id):
                return {
                    "message": f"An comentario with id '{comentario.id}' already exists."
                }, 400
            try:
                comentario.save_to_db()
            except Exception as e:
                return {
                    "message": f"An error occurred inserting the comentario. Error: {e}"
                }, 500
            return comentarios_schema.dump(comentario), 201
