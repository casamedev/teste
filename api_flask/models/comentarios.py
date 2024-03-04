from api_flask.extensions.db import db


class ComentariosModel(db.Model):
    # comentario,data,vendedor,razao_cliente,status
    __tablename__ = "comentarios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comentario = db.Column(db.String(250))
    cod_vendedor = db.Column(db.Integer, db.ForeignKey("cm_vendedores.cod_vendedor"))
    data = db.Column(db.Date)
    cod_cliente = db.Column(db.Integer, db.ForeignKey("cm_clientes_fornec.cod_cliente"))
    status = db.Column(db.String(80))

    def json(self):
        return {
            "comentario": self.comentario,
            "data": self.data,
            "vendedor_id": self.cod_vendedor,
            "cliente_id": self.cod_cliente,
            "status": self.status,
        }
    
    def __repr__(self) -> str:
        return f"Comentario - Status {self.status}"
    

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()   
    
    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    
