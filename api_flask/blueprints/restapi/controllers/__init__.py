from .agenda import api as agenda_ns
from .cm_clientes_fornec import api as cm_clientes_fornec_ns
from .cm_movimento import api as cm_movimento_ns
from .cm_produtos import api as cm_produtos_ns
from .cm_vendedores import api as cm_vendedores_ns
from .comentarios import api as comentarios_ns
from .seed import api as seed_vendedores_ns 
from flask import Blueprint
from flask_restx import Api

bp = Blueprint("api", __name__, url_prefix="/api")

api = Api(
    bp,
    title="FLASK RESTPLUS API FOR CASAMED",
    version="1.0",
    doc="/documentation",
)

api.add_namespace(agenda_ns)
api.add_namespace(cm_clientes_fornec_ns)
api.add_namespace(cm_movimento_ns)
api.add_namespace(cm_produtos_ns)
api.add_namespace(cm_vendedores_ns)
api.add_namespace(comentarios_ns)
api.add_namespace(seed_vendedores_ns)

def init_app(app):
    app.register_blueprint(bp)
    return app

