from api_flask.extensions.db import db

class CmMovimentoModel(db.Model):
    __tablename__ = "cm_movimento"
    portal = db.Column(db.Integer)
    cnpj_emp = db.Column(db.String(50))
    documento = db.Column(db.Integer)
    data_documento = db.Column(db.Date)
    codigo_cliente = db.Column(
        db.Integer, db.ForeignKey("cm_clientes_fornec.cod_cliente")
    )
    cod_vendedor = db.Column(db.Integer, db.ForeignKey("cm_vendedores.cod_vendedor"))
    quantidade = db.Column(db.Float)
    preco_custo = db.Column(db.Numeric(19, 4))
    valor_liquido = db.Column(db.Numeric(19, 4))
    desconto = db.Column(db.Numeric(19, 4))
    valor_total = db.Column(db.Numeric(19, 4))
    forma_dinheiro = db.Column(db.Boolean)
    total_dinheiro = db.Column(db.Numeric(19, 4))
    forma_cheque = db.Column(db.Boolean)
    total_cheque = db.Column(db.Numeric(19, 4))
    forma_cartao = db.Column(db.Boolean)
    total_cartao = db.Column(db.Numeric(19, 4))
    forma_crediario = db.Column(db.Boolean)
    total_crediario = db.Column(db.Numeric(19, 4))
    forma_convenio = db.Column(db.Boolean)
    total_convenio = db.Column(db.Numeric(19, 4))
    frete = db.Column(db.Numeric(19, 4))
    operacao = db.Column(db.String(50))
    tipo_transacao = db.Column(db.String(50))
    cod_produto = db.Column(db.Integer, db.ForeignKey("cm_produtos.cod_produto"))
    cancelado = db.Column(db.String(50))
    excluido = db.Column(db.String(50))
    desconto_total_item = db.Column(db.Numeric(19, 4))
    timestamp = db.Column(db.BigInteger, primary_key=True)

    @classmethod
    def find_by_timestamp(cls, timestamp):
        return cls.query.filter_by(timestamp>=timestamp).all()
    
    @classmethod
    def find_max_timestamp(cls):
        return cls.query.order_by(cls.timestamp.desc()).first() 

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_to_db(self):
        db.session.commit

    def json(self):

        return {
            "portal": self.portal,
            "cnpj_emp": self.cnpj_emp,
            "documento": self.documento,
            "data_documento": self.data_documento.strftime("%Y-%m-%d"),
            "codigo_cliente": self.codigo_cliente,
            "cod_vendedor": self.cod_vendedor,   
            "quantidade": self.quantidade,
            
        }
