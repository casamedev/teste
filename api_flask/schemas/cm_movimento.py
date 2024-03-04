from api_flask.extensions.serializers import ma 
from api_flask.models.cm_movimento import CmMovimentoModel
from marshmallow import pre_load, fields
from datetime import datetime

class CmMovimentoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CmMovimentoModel
        load_instance = True
        include_fk = True
        unknown = 'exclude'
       
    preco_custo = fields.Decimal(as_string=True)
    valor_liquido = fields.Decimal(as_string=True)
    desconto = fields.Decimal(as_string=True)
    valor_total = fields.Decimal(as_string=True)
    total_dinheiro = fields.Decimal(as_string=True)
    total_cheque = fields.Decimal(as_string=True)
    total_cartao = fields.Decimal(as_string=True)
    total_crediario = fields.Decimal(as_string=True)
    total_convenio = fields.Decimal(as_string=True)
    frete = fields.Decimal(as_string=True)
    desconto_total_item = fields.Decimal(as_string=True)



    @pre_load
    def preprocess(self, data , **kwargs):
        for key in data:
            if key.startswith('data'):
                data[key] = self.converter_data(data[key])
        # for key in data:
        #     if key.startswith('quantidade') or key.startswith('preco_custo') or key.startswith('valor_liquido') or key.startswith('desconto') or key.startswith('valor_total') or key.startswith('total_dinheiro') or key.startswith('total_cheque') or key.startswith('total_cartao') or key.startswith('total_crediario') or key.startswith('total_convenio') or key.startswith('frete') or key.startswith('desconto_total_item'):
        #         data[key] = self.converter_decimal(data[key])
        return data
    
    def converter_data(self, data):
        try:
            data = datetime.strptime(data, '%d/%m/%Y 00:00:00').strftime('%Y-%m-%d')
        except: # noqa
            return data
        return data
    
    # # cerificar dados com decimal para converter para float
    
    # def converter_decimal(self, data):
    #     if isinstance(data, Decimal):
    #         return float(data)
    #     return data