from core.review_management.application.acl.review_management import ProductRatingACL, ReviewACL
from core.review_management.infrastructure.repositories.review_management import DjangoProductRatingRepository, DjangoReviewRepository, DjangoReviewReadModel

class ReivewManagementACLFactory:
    @staticmethod
    def create_product_rating_acl():
        return ProductRatingACL(DjangoProductRatingRepository(), DjangoReviewReadModel())

    @staticmethod
    def create_review_acl():
        return ReviewACL(DjangoReviewRepository())