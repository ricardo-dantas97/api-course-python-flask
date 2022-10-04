from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3

from models.site import SiteModel
from resources.filters import normalize_path_params, query_with_city, query_without_city


path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        
        data = path_params.parse_args()
        valid_arguments = {key:data[key] for key in data if data[key] is not None}
        params = normalize_path_params(**valid_arguments)

        if not params.get('cidade'):
            filters = tuple([params[key] for key in params])
            result = cursor.execute(query_without_city, filters)
        else:
            filters = tuple([params[key] for key in params])
            result = cursor.execute(query_with_city, filters)
        
        hoteis = []
        for line in result:
            hoteis.append({
                'hotel_id': line[0],
                'nome': line[1],
                'estrelas': line[2],
                'diaria': line[3],
                'cidade': line[4],
                'site_id': line[5]
            })

        return {'data': hoteis}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="Fild 'nome' cannot be empty")
    argumentos.add_argument('estrelas', type=float, required=True, help="Field 'estrelas' cannot be empty")
    argumentos.add_argument('diaria', type=float, required=True, help="Field 'diaria' cannot be empty")
    argumentos.add_argument('cidade', type=str, required=True, help="Field 'cidade' cannot be empty")
    argumentos.add_argument('site_id', type=int, required=True, help="Every hotel needs to be linked with a site")


    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json(), 200
        return {'message': 'Hotel ID not found'}, 400


    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'message': 'Hotel ID already exists.'}, 400  

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)

        if not SiteModel.find_site_by_id(dados.get('site_id')):
            return {'message': 'The hotel must be associated to a valid site id'}, 400

        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500
        return hotel.json(), 200
    

    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()        

        searched_hotel = HotelModel.find_hotel(hotel_id)
        if searched_hotel:
            searched_hotel.update_hotel(**dados)
            try:
                searched_hotel.save_hotel()
            except:
                return {'message': 'An internal error ocurred trying to save hotel.'}, 500
            return searched_hotel.json(), 200
        
        hotel = HotelModel(hotel_id, **dados)

        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500
        return hotel.json(), 201
    

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An internal error ocurred trying to save hotel.'}, 500
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel ID not found.'}, 400
