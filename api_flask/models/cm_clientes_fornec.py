from api_flask.extensions.db import db 
from api_flask.models.cm_movimento import CmMovimentoModel # noqa F401 preciso importar para criar o relacionamento
from api_flask.models.comentarios import ComentariosModel # noqa F401 preciso importar para criar o relacionamento


class CmClientesFornecModel(db.Model):
    __tablename__ = "cm_clientes_fornec"

    nportal = db.Column(db.Integer)
    cliente_identificado = db.Column(db.Integer)
    cod_cliente = db.Column(db.Integer, primary_key=True)
    razao_cliente = db.Column(db.String(1000))
    nome_cliente = db.Column(db.String(1000))
    tipo_cliente = db.Column(db.String(100)) 
    cidade_cliente = db.Column(db.String(100))
    uf_cliente = db.Column(db.String(50))
    fone_cliente = db.Column(db.String(50))
    email_cliente = db.Column(db.String(50))
    sexo = db.Column(db.String(50))
    data_nascimento = db.Column(db.Date)
    fone_celular = db.Column(db.String(50))
    timestamp = db.Column(db.BigInteger)
    movimentos = db.relationship("CmMovimentoModel", backref="cliente", lazy=True)
    comentarios = db.relationship("ComentariosModel", backref="cliente", lazy=True, primaryjoin="CmClientesFornecModel.cod_cliente == ComentariosModel.cod_cliente")

    @classmethod
    def find_by_cod_cliente(cls, cod_cliente):
        return cls.query.filter_by(cod_cliente=cod_cliente).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_nome_cliente(cls, nome_cliente):
        return cls.query.filter_by(nome_cliente=nome_cliente).first()

    @classmethod
    def find_by_max_timestamp(cls):
        return cls.query.order_by(cls.timestamp.desc()).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_to_db(self):
        db.session.commit()

    def json(self):
        return {
            "nportal": self.nportal,
            "cliente_identificado": self.cliente_identificado,
            "cod_cliente": self.cod_cliente,
            "razao_cliente": self.razao_cliente,
            "nome_cliente": self.nome_cliente,
            "tipo_cliente": self.tipo_cliente,
            "cidade_cliente": self.cidade_cliente,
            "uf_cliente": self.uf_cliente,
            "fone_cliente": self.fone_cliente,
            "email_cliente": self.email_cliente,
            "sexo": self.sexo,
            "data_nascimento": self.data_nascimento,
            "fone_celular": self.fone_celular,
            "timestamp": self.timestamp,
        }
