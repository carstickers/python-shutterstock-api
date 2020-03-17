import math

from shutterstock.endpoint import EndPoint, EndPointParam, ChoicesParam,\
    IntegerParam
from shutterstock.resource import Resource, ResourceObjectMethod, \
    ResourceCollectionMethod


class ImageEndPoint(EndPoint):
    """Endpoint for Shutterstock images"""
    MINIMAL = 'minimal'
    FULL = 'full'
    VIEW_CHOICES = (MINIMAL, FULL, )

    id = EndPointParam(required=True,
                       help_text='Required. The ID of the image.')
    view = ChoicesParam(required=True, default=MINIMAL, choices=VIEW_CHOICES,
                        help_text='Required. Minimal view does not return licensing options, categories, keywords')


class ImageSearchEndPoint(EndPoint):
    """Endpoint for shutterstock image search"""

    page = IntegerParam(default=1, min=1)
    per_page = IntegerParam(default=50, min=1)
    query = EndPointParam(required=True, help_text='Required. The search query')
    added_date = EndPointParam(required=False, help_text='Show images added on the specified date, in the format YYYY-MM-DD')
    added_date_start = EndPointParam(required=False, help_text='Show images added on or after the specified date, in the format YYYY-MM-DD')
    added_date_end = EndPointParam(required=False, help_text='Show images added before the specified date, in the format YYYY-MM-DD')
    category = EndPointParam(required=False, help_text='Show images with the specified Shutterstock-defined category; specify a category name or ID')
    color = EndPointParam(required=False, help_text='Specify either a hexadecimal color in the format "4F21EA" or "grayscale"; the API groups it into one of 15 color categories and returns images that primarily use that color category')
    contributor = EndPointParam(required=False, help_text='Show images with the specified contributor names or IDs, allows multiple')
    contributor_country = EndPointParam(required=False, help_text='Show images from contributors in one or more specified countries by 2-letter ISO 3166-1 alpha-2 country code, such as DE or US')
    height_from = EndPointParam(required=False, help_text='Show images with the specified height or larger, in pixels')
    height_to = EndPointParam(required=False, help_text='Show images with the specified height or smaller, in pixels')
    image_type = EndPointParam(required=False, help_text='Show images of the specified type. Valid values: photo, illustration, vector')
    language = EndPointParam(required=False, help_text='Set query and result language (uses Accept-Language header if not set). Valid values: cs, da, de, en, es, fi, fr, hu, it, ja, ko, nb, nl, pl, pt, ru, sv, th, tr, zh, zh-Hant')
    license = EndPointParam(required=False, help_text='Show only images with the specified license. Valid values: commercial, editorial, enhanced, sensitive, NOT enhanced, NOT sensitive')
    model = EndPointParam(required=False, help_text='Show image results with the specified model IDs')
    orientation = EndPointParam(required=False, help_text='Show image results with horizontal or vertical orientation. Valid values: horizontal, vertical')
    people_model_released = EndPointParam(required=False, help_text='Show images of people with a signed model release')
    people_age = EndPointParam(required=False, help_text='Show images that feature people of the specified age category, Valid values: infants, children, teenagers, 20s, 30s, 40s, 50s, 60s, older')
    people_ethnicity = EndPointParam(required=False, help_text='Show images with people of the specified ethnicity. Valid values: african, african_american, black, brazilian, chinese, caucasian, east_asian, hispanic, japanese, middle_eastern, native_american, pacific_islander, south_asian, southeast_asian, other')
    people_gender = EndPointParam(required=False, help_text='Show images with people of the specified gender. Valid values: male, female, both')
    people_number = EndPointParam(required=False, help_text='Show images with the specified number of people')
    safe = EndPointParam(required=False, default='true', help_text='Enable or disable safe search')
    sort = EndPointParam(required=False, help_text='Sort by. Valid values: newest, popular, relevance, random')
    spellcheck_query = EndPointParam(required=False, help_text='Spellcheck the search query and return results on suggested spellings')
    view = EndPointParam(required=False, help_text='Amount of detail to render in the response. Valid values: minimal, full')
    width_from = EndPointParam(required=False, help_text='Show images with the specified width or larger, in pixels')
    width_to = EndPointParam(required=False, help_text='Show images with the specified width or smaller, in pixels')


class Contributor(Resource):
    LIST = EndPoint('/contributors')
    GET = EndPoint('/contributors/{id}')


class Image(Resource):
    LIST = ImageEndPoint('/images')
    GET = ImageEndPoint('/images/{id}')
    SEARCH = ImageSearchEndPoint('/images/search')

    @classmethod
    def search(cls, **params):
        return cls.API.get(cls.SEARCH, **params)


class ImageCollectionListEndPoint(EndPoint):
    id = EndPointParam()


class ImageCollectionItemsEndPoint(EndPoint):
    id = EndPointParam()
    per_page = IntegerParam(min=1, max=150)
    page = IntegerParam(default=1, min=1)


class ImageCollection(Resource):
    LIST = ImageCollectionListEndPoint('/images/collections')
    GET = EndPoint('/images/collections/{id}')
    ITEMS = ImageCollectionItemsEndPoint('/images/collections/{id}/items')

    @ResourceCollectionMethod(resource=Image, id='id')
    def items(cls, **params):
        detail = cls.API.get(cls.GET, id=params.get('id'))
        item_count = detail['total_item_count']
        per_page = params.get('per_page', 100)
        ids = []
        for page in range(0, math.ceil(item_count / per_page)):
            response = cls.API.get(cls.ITEMS, page=page + 1, **params)
            page_ids = [item['id'] for item in response['data']]
            ids.extend(page_ids)

        results = {'data': []}
        for page in range(0, math.ceil(len(ids) / 100)):
            page_ids = ids[page * 100:page * 100 + 100]
            if len(page_ids):
                images_to_add = cls.API.get(Image.LIST, id=page_ids,
                                            view=params.get('view', 'minimal'))
                results['data'].extend(images_to_add['data'])
        return results


class ImageLicense(Resource):
    LIST = EndPoint('/images/licenses')
    DOWNLOAD = EndPoint('/images/licenses/{id}/downloads')
    LICENSE = EndPoint('/images/licenses?subscription_id={subscription_id}', params=['images'])

    @ResourceObjectMethod(id='id')
    def download(cls, **params):
        return cls.API.post(cls.DOWNLOAD, **params)

    @ResourceCollectionMethod(id='id')
    def license(cls, **params):
        return cls.API.post(cls.LICENSE, **params)


class ImageContributor(Resource):
    GET = EndPoint('/contributors/{contributor_id}')
