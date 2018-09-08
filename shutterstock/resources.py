from shutterstock.endpoint import EndPoint, EndPointParam
from shutterstock.resource import Resource, ResourceObjectMethod, \
    ResourceCollectionMethod


class Image(Resource):
    LIST = EndPoint('/images')
    GET = EndPoint('/images/{id}')


class ImageCollectionListEndPoint(EndPoint):
    id = EndPointParam()


class ImageCollection(Resource):
    LIST = ImageCollectionListEndPoint('/images/collections')
    GET = EndPoint('/images/collections/{id}')
    ITEMS = EndPoint('/images/collections/{id}/items')

    @ResourceCollectionMethod(resource=Image, id='id')
    def items(cls, **params):
        response = cls.API.get(cls.ITEMS, **params)
        ids = [item['id'] for item in response['data']]
        return cls.API.get(Image.LIST, id=ids, view=params.get('view', 'minimal'))


class ImageLicense(Resource):
    LIST = EndPoint('/images/licenses')
    DOWNLOAD = EndPoint('/images/licenses/{id}/downloads')
    LICENSE = EndPoint('/images/licenses')

    @ResourceObjectMethod(id='id')
    def download(cls, **params):
        return cls.API.post(cls.DOWNLOAD, **params)

    @ResourceObjectMethod(id='id')
    def license(cls, **params):
        return cls.API.post(cls.LICENSE, **params)
