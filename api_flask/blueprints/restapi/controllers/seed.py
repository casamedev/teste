from flask_restx import Resource, Namespace
from api_flask.extensions.auth import auth
from api_flask.scripts.seed_vendedores import seed_vendedores
from api_flask.scripts.seed_produtos import seed_produtos
from api_flask.scripts.seed_movimento import seed_movimento
from api_flask.scripts.seed_cm_clientes_fornec import seed_cm_clientes_fornec


api = Namespace("seed_data", description="seed data operations", path="/seed")


@api.route("/vendedores")
class SeedVendedores(Resource):
    @auth.login_required
    def get(self): 
        seed_vendedores()


@api.route("/produtos")
class SeedProdutos(Resource):
    @auth.login_required
    def get(self):
        seed_produtos()


@api.route("/movimento")
class SeedMovimento(Resource):
    @auth.login_required
    def get(self):
        seed_movimento()
@api.route("/clientes")
class SeedClientes(Resource):
    @auth.login_required
    def get(self):
        seed_cm_clientes_fornec()
