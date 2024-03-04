from api_flask.extensions.serializers import ma 
from api_flask.models.cm_produtos import CmProdutosModel
from marshmallow import pre_load
from datetime import datetime


class CmProdutosSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CmProdutosModel
        load_instance = True
        unknown = 'exclude'


    @pre_load
    def preprocess(self, data , **kwargs):
        for key in data:
            if key.startswith('data') or  key.startswith("dt"):
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

        