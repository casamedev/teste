from api_flask.extensions.serializers import ma 
from api_flask.models.cm_clientes_fornec import CmClientesFornecModel
from marshmallow import pre_load
from datetime import datetime


class CmClientesFornecSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CmClientesFornecModel
        load_instance = True
        unknown = 'exclude'

    @pre_load
    def preprocess(self, data , **kwargs):
        for key in data:
            if key.startswith('data') or key.startswith("dt"):
                data[key] = self.converter_data(data[key])
        return data
    
    def converter_data(self, data):
        try:
            data = datetime.strptime(data, '%d/%m/%Y 00:00:00').strftime('%Y-%m-%d')
        except: # noqa
            return data
        return data
    #adicionar um preload para que trate a data recebida 
        
    



    