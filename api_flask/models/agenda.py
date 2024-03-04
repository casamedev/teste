from api_flask.extensions.db import db


class AgendaModel(db.Model):
    __tablename__ = "agenda"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo_cliente = db.Column(
        db.Integer,
        db.ForeignKey("cm_clientes_fornec.cod_cliente", ondelete="CASCADE"),
        nullable=False,
    )
    data_retorno_ajustada = db.Column(db.Date)
    data_documento = db.Column(db.Date)
    documento = db.Column(db.Integer)
    marcado_por_admin = db.Column(db.Boolean, default=False)
    tipo_retorno = db.Column(db.String(50)) # marcado por admin, produto estratéico ou produto recorrente 
    timestamp = db.Column(db.BigInteger)

    def __repr__(
        self,
    ):
        return f"<Agenda: {self.razao_cliente}>"

    def json(
        self,
    ):
        return {
            "id": self.id,
            "codigo_cliente": self.codigo_cliente,
            "data_retorno_ajustada": self.data_retorno_ajustada,
            "data_documento": self.data_documento,
            "documento": self.documento,
            "marcado_por_admin": self.marcado_por_admin,
            "tipo_retorno": self.tipo_retorno,
        }

    @classmethod
    def find_by_razao_cliente(cls, razao_cliente):
        return cls.query.filter_by(razao_cliente=razao_cliente).first()

    @classmethod
    def find_by_cod_cliente(cls, cod_cliente):
        return cls.query.filter_by(cod_cliente=cod_cliente).first()

    @classmethod
    def find_all(
        cls,
    ):
        return cls.query.all()

    @classmethod
    def find_by_timestamp(
        cls,
        timestamp,
    ):
        return cls.query.filter(cls.timestamp >= timestamp).all()
    

    def save_to_db(
        self,
    ):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(
        self,
    ):
        db.session.delete(self)
        db.session.commit()

    def update_in_db(
        self,
    ):
        db.session.commit()
