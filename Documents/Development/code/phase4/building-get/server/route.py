from flask import jsonify, request, Blueprint, Response
from sqlalchemy.exc import IntegrityError
from server.model import Bakery, BakedGood  # Adjusted import
import json

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@main_bp.route('/bakeries', methods=['GET'])
def get_bakeries():
    bakeries = Bakery.query.all()
    bakeries_data_list = []
    for bakery in bakeries:
        bakery_data = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at.strftime('%Y-%m-%d %H:%M:%S') if bakery.created_at else None,
            'updated_at': bakery.updated_at.strftime('%Y-%m-%d %H:%M:%S') if bakery.updated_at else None,
            'baked_goods': [baked_good.serialize() for baked_good in bakery.baked_goods]
        }
        bakeries_data_list.append(bakery_data)

    json_data = json.dumps(bakeries_data_list, indent=2)
    return Response(json_data, mimetype='application/json')


    

@main_bp.route('/bakeries/<int:id>', methods=['GET'])
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery:
        bakery_json = jsonify(bakery.serialize())
        return bakery_json
    else:
        return jsonify({'error': 'Bakery not found'}), 404

@main_bp.route('/baked_goods/by_price', methods=['GET'])
def get_baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return jsonify([baked_good.serialize() for baked_good in baked_goods])

@main_bp.route('/baked_goods/most_expensive', methods=['GET'])
def get_most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive:
        return jsonify(most_expensive.serialize())
    else:
        return jsonify({'error': 'No baked goods found'}), 404



@main_bp.route('/favicon.ico')
def favicon():
    return "", 404