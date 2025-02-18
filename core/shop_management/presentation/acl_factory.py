from ..application.acl.shop_management import *
from ..infrastructure.repositories.shop_management import *

class ShopManagementACLFactory:
    '''
    The factory is dedicated to hiding initiation details of ACLs from other bounded contexts
    '''
    @staticmethod
    def create_product_acl() -> ProductACL:
        return ProductACL(DjangoProductRepository())
    
    @staticmethod
    def create_category_acl() -> CategoryACL:
        return CategoryACL(DjangoCategoryRepository())
    
    @staticmethod
    def create_brand_acl() -> BrandACL:
        return BrandACL(DjangoBrandRepository())