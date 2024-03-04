from api_flask.extensions.serializers import ma 
from api_flask.models.agenda import AgendaModel
from datetime import datetime
from marshmallow import pre_load

class AgendaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AgendaModel
        load_instance = True
        include_fk = True
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
    

#FUTURAMENTE USAR 
#     from dateutil import parser

# data = "31/01/2024 00:00:00"
# try:
#     data_convertida = parser.parse(data)
#     print("Data convertida:", data_convertida)
# except ValueError:
#     print("Formato de data desconhecido ou inválido")
