from api_flask.extensions.serializers import ma 
from api_flask.models.comentarios import ComentariosModel
from marshmallow import pre_load
from datetime import datetime

class ComentariosSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ComentariosModel
        load_instance = True
        unknown = 'exclude'
        include_fk = True

    @pre_load
    def preprocess(self, data , **kwargs):
        for key in data:
            if key.startswith('data'):
                print(data[key])
                data[key] = self.converter_data(data[key])
                print(data[key])
        return data
    
    def converter_data(self, data):
        try:
            data = datetime.strptime(data, '%d/%m/%Y 00:00:00').strftime('%Y-%m-%d')
            # print(data)
        except Exception as e:# noqa
            print(e)
            return data
        return data

