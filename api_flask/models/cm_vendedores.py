from api_flask.extensions.db import db
from api_flask.models.cm_movimento import CmMovimentoModel # noqa F401 preciso importar para criar o relacionamento   
from api_flask.models.comentarios import ComentariosModel # noqa F401 preciso importar para criar o relacionamento


class CmVendedoresModel(db.Model):
    __tablename__ = "cm_vendedores"

    portal = db.Column(db.Integer)
    cod_vendedor = db.Column(db.Integer, primary_key=True)
    nome_vendedor = db.Column(db.String(100))
    tipo_vendedor = db.Column(db.String(50))
    fone_vendedor = db.Column(db.String(50))
    mail_vendedor = db.Column(db.String(50))
    ativo = db.Column(db.String(50))
    data_admissao = db.Column(db.Date)
    data_saida = db.Column(db.Date)
    timestamp = db.Column(db.BigInteger)
    matricula = db.Column(db.String(50))
    movimentos = db.relationship("CmMovimentoModel", backref="vendedor", lazy=True)
    comentarios = db.relationship("ComentariosModel", backref="vendedor", lazy=True)

    @classmethod
    def find_by_cod_vendedor(cls, cod_vendedor):
        return cls.query.filter_by(cod_vendedor=cod_vendedor).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_nome_vendedor(cls, nome_vendedor):
        return cls.query.filter_by(nome_vendedor=nome_vendedor).first()

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
            "portal": self.portal,
            "cod_vendedor": self.cod_vendedor,
            "nome_vendedor": self.nome_vendedor,
            "tipo_vendedor": self.tipo_vendedor,
            "fone_vendedor": self.fone_vendedor,
            "mail_vendedor": self.mail_vendedor,
            "ativo": self.ativo,
            "data_admissao": self.data_admissao,
            "data_saida": self.data_saida,
            "timestamp": self.timestamp,
            "matricula": self.matricula,
        }
