from flask_restful import Resource
from models.site import SiteModel


class Sites(Resource):
    def get(self):
        return {'sites': [site.json() for site in SiteModel.query.all()]}, 200


class Site(Resource):
    def get(self, url):
        site = SiteModel.find_site(url)
        if site:
            return site.json()
        return {'message', 'Site not found.'}, 400


    def post(self, url):
        if SiteModel.find_site(url):
            return {'message': 'The site already exists.'}, 400
        site = SiteModel(url)
        try:
            site.save_site()
        except:
            return {'message': 'An internal error ocurred trying to create a new site.'}, 500
        return site.json()


    def delete(self, url):
        site = SiteModel.find_site(url)
        if site:
            try:
                site.delete_site()
            except:
                return {'message': 'An internal error ocurred trying to create a new site.'}, 500
            return {'message': 'Site deleted'}, 200
        return {'message': 'Site not found.'}, 400