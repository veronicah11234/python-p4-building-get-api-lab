import json
from os import environ
import re
from server.app import db, create_app
from server.model import Bakery, BakedGood

class TestApp:
    '''Flask application in flask_app.py'''

    def setup_method(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_bakeries_route(self):
        '''has a resource available at "/bakeries".'''
        response = self.client.get('/bakeries')
        assert response.status_code == 200

    def test_bakeries_route_returns_json(self):
        '''provides a response content type of application/json at "/bakeries"'''
        response = self.client.get('/bakeries')
        assert response.content_type == 'application/json'

    def test_bakeries_route_returns_list_of_bakery_objects(self):
        '''returns JSON representing models.Bakery objects.'''
        with self.app.app_context():
            b = Bakery(name="My Bakery")
            db.session.add(b)
            db.session.commit()

            response = self.client.get('/bakeries')
            data = json.loads(response.data.decode())
            assert isinstance(data, list)
            
            contains_my_bakery = False
            for record in data:
                assert isinstance(record, dict)
                assert 'id' in record
                assert 'name' in record
                assert 'created_at' in record
                if record['name'] == "My Bakery":
                    contains_my_bakery = True
            assert contains_my_bakery

            db.session.delete(b)
            db.session.commit()

    def test_bakery_by_id_route(self):
        '''has a resource available at "/bakeries/<int:id>".'''
        with self.app.app_context():
            b = Bakery(name="My Bakery")
            db.session.add(b)
            db.session.commit()

            response = self.client.get(f'/bakeries/{b.id}')
            assert response.status_code == 200

            db.session.delete(b)
            db.session.commit()

    def test_bakery_by_id_route_returns_json(self):
        '''provides a response content type of application/json at "/bakeries/<int:id>"'''
        with self.app.app_context():
            b = Bakery(name="My Bakery")
            db.session.add(b)
            db.session.commit()

            response = self.client.get(f'/bakeries/{b.id}')
            assert response.content_type == 'application/json'

            db.session.delete(b)
            db.session.commit()

    def test_bakery_by_id_route_returns_one_bakery_object(self):
        '''returns JSON representing one models.Bakery object.'''
        with self.app.app_context():
            b = Bakery(name="My Bakery")
            db.session.add(b)
            db.session.commit()

            response = self.client.get(f'/bakeries/{b.id}')
            data = json.loads(response.data.decode())
            assert isinstance(data, dict)
            assert data['id'] == b.id
            assert data['name'] == "My Bakery"
            assert 'created_at' in data

            db.session.delete(b)
            db.session.commit()

    def test_baked_goods_by_price_route(self):
        '''has a resource available at "/baked_goods/by_price".'''
        response = self.client.get('/baked_goods/by_price')
        assert response.status_code == 200

    def test_baked_goods_by_price_route_returns_json(self):
        '''provides a response content type of application/json at "/baked_goods/by_price"'''
        response = self.client.get('/baked_goods/by_price')
        assert response.content_type == 'application/json'

    def test_baked_goods_by_price_returns_list_of_baked_goods_in_descending_order(self):
        '''returns JSON representing one models.Bakery object.'''
        with self.app.app_context():
            prices = [baked_good.price for baked_good in BakedGood.query.all()]
            highest_price = max(prices)

            b1 = BakedGood(name="Madeleine", price=highest_price + 1)
            db.session.add(b1)
            db.session.commit()
            b2 = BakedGood(name="Donut", price=highest_price - 1)
            db.session.add(b2)
            db.session.commit()

            response = self.client.get('/baked_goods/by_price')
            data = json.loads(response.data.decode())
            assert isinstance(data, list)
            for record in data:
                assert 'id' in record
                assert 'name' in record
                assert 'price' in record
                assert 'created_at' in record

            prices = [record['price'] for record in data]
            assert all(prices[i] >= prices[i+1] for i in range(len(prices) - 1))

            db.session.delete(b1)
            db.session.delete(b2)
            db.session.commit()
            

    def test_most_expensive_baked_good_route(self):
        '''has a resource available at "/baked_goods/most_expensive".'''
        response = self.client.get('/baked_goods/most_expensive')
        assert response.status_code == 200

    def test_most_expensive_baked_good_route_returns_json(self):
        '''provides a response content type of application/json at "/bakeries/<int:id>"'''
        response = self.client.get('/baked_goods/most_expensive')
        assert response.content_type == 'application/json'

    def test_most_expensive_baked_good_route_returns_one_baked_good_object(self):
        '''returns JSON representing one models.BakedGood object.'''
        with self.app.app_context():
            prices = [baked_good.price for baked_good in BakedGood.query.all()]
            highest_price = max(prices)

            b1 = BakedGood(name="Madeleine", price=highest_price + 1)
            db.session.add(b1)
            db.session.commit()
            b2 = BakedGood(name="Donut", price=highest_price - 1)
            db.session.add(b2)
            db.session.commit()

            response = self.client.get('/baked_goods/most_expensive')
            data = json.loads(response.data.decode())
            assert isinstance(data, dict)
            assert 'id' in data
            assert 'name' in data
            assert 'price' in data
            assert 'created_at' in data

            db.session.delete(b1)
            db.session.delete(b2)
            db.session.commit()

    def test_most_expensive_baked_good_route_returns_most_expensive_baked_good_object(self):
        '''returns JSON representing one models.BakedGood object.'''
        with self.app.app_context():
            prices = [baked_good.price for baked_good in BakedGood.query.all()]
            highest_price = max(prices)

            b1 = BakedGood(name="Madeleine", price=highest_price + 1)
            db.session.add(b1)
            db.session.commit()
            b2 = BakedGood(name="Donut", price=highest_price - 1)
            db.session.add(b2)
            db.session.commit()

            response = self.client.get('/baked_goods/most_expensive')
            data = json.loads(response.data.decode())
            assert data['price'] == b1.price

            db.session.delete(b1)
            db.session.delete(b2)
            db.session.commit()