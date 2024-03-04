from api_flask.extensions.db import db

tabela_relacionados = db.Table(
    "tabela_relacionados",
    db.Model.metadata,
    db.Column(
        "produto_id_origem", db.Integer, db.ForeignKey("cm_produtos.cod_produto")
    ),
    db.Column(
        "produto_id_destino", db.Integer, db.ForeignKey("cm_produtos.cod_produto")
    ),
)


class CmProdutosModel(db.Model):
    __tablename__ = "cm_produtos"

    portal = db.Column(db.Integer)
    cod_produto = db.Column(db.Integer, primary_key=True)
    cod_barra = db.Column(db.String(100))
    nomeproduto = db.Column(db.String(250))
    cod_ncm = db.Column(db.String(50))
    desc_cor = db.Column(db.String(50))
    desc_tamanho = db.Column(db.String(50))
    desc_setor = db.Column(db.String(50))
    desc_linha = db.Column(db.String(50))
    desc_marca = db.Column(db.String(50))
    desc_colecao = db.Column(db.String(50))
    id_cor = db.Column(db.Integer)
    id_tamanho = db.Column(db.String(50))
    id_setor = db.Column(db.Integer)
    id_linha = db.Column(db.Integer)
    id_marca = db.Column(db.Integer)
    id_colecao = db.Column(db.Integer)
    dt_cadastro = db.Column(db.Date)
    timestamp = db.Column(db.BigInteger)
    produtos_relacionados = db.relationship(
        "CmProdutosModel",
        secondary=tabela_relacionados,
        primaryjoin=(tabela_relacionados.c.produto_id_origem == cod_produto),
        secondaryjoin=(tabela_relacionados.c.produto_id_destino == cod_produto),
        backref="produtos_relacionados_in",
    )
    tempo_de_uso = db.Column(db.String(80), default="N/A")
    tempo_de_uso_dias = db.Column(db.Integer)
    recorrente = db.Column(db.String(80))
    estrategico_ou_complementar = db.Column(db.String(80))

    @classmethod
    def find_by_cod_produto(cls, cod_produto):
        return cls.query.filter_by(cod_produto=cod_produto).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_cod_barra(cls, cod_barra):
        return cls.query.filter_by(cod_barra=cod_barra).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete()
        db.session.commit()

    def json(self):
        return {
            "portal": self.portal,
            "cod_produto": self.cod_produto,
            "cod_barra": self.cod_barra,
            "nomeproduto": self.nomeproduto,
            "cod_ncm": self.cod_ncm,
            "desc_cor": self.desc_cor,
            "desc_tamanho": self.desc_tamanho,
            "desc_setor": self.desc_setor,
            "desc_linha": self.desc_linha,
            "desc_marca": self.desc_marca,
            "desc_colecao": self.desc_colecao,
            "id_cor": self.id_cor,
            "id_tamanho": self.id_tamanho,
            "id_setor": self.id_setor,
            "id_linha": self.id_linha,
            "id_marca": self.id_marca,
            "id_colecao": self.id_colecao,
            "dt_cadastro": self.dt_cadastro,
            "timestamp": self.timestamp,
            "tempo_de_uso": self.tempo_de_uso,
            "tempo_de_uso_dias": self.tempo_de_uso_dias,
            "recorrente": self.recorrente,
            "estrategico_ou_complementar": self.estrategico_ou_complementar,
        }

    def __repr__(self):
        return f"<CM_ProdutosModel {self.cod_produto} : {self.nomeproduto}>"
