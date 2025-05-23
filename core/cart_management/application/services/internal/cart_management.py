from core.cart_management.domain.aggregates.cart_management import Wishlist as WishlistEntity
from core.cart_management.domain.entities.cart_management import Cart as CartEntity
from core.cart_management.domain.interfaces.i_repositories.i_cart_management import ICartRepository, IWishlistRepository
from core.cart_management.domain.dtos.cart_management import AddToWishlistDomainDTO
from core.cart_management.application.dtos.acl_dtos import ProductDTO
from core.cart_management.application.dtos.requests import AddWishlistItemRequestDTO, DeleteWishlistItemRequestDTO
from core.cart_management.application.exceptions import WishlistPriceValidationError, NotFoundWishlistError
from ..base_service import BaseService

from core.shop_management.domain.interfaces.i_acls import IProductACL

from typing import Any
from decimal import Decimal

class CartService(BaseService["CartService"]):
    def __init__(self, product_acl: IProductACL, cart_repository: ICartRepository, **kwargs):
        super().__init__(**kwargs)
        self.product_acl = product_acl
        self.cart_repository = cart_repository

    def delete_button_cart_service(self, raw_cart: dict[str, Any]) -> tuple[dict[str, Any], int]:
        item_pub_uuid = raw_cart.get('product')
        
        cart_entity = self.cart_repository.fetch_cart()

        if cart_entity is None:
            return {'status': 'error', 'message': 'Cart not found'}, 404

        # Compute the price and quantity changes
        cart_entity.remove_item()
        #qty = item_collection.quantity - order_product.qty
        #price = order_product.size.product.get_price_with_discount() * order_product.qty
        response_data = {
            'qty': str(qty),
            'qty-2': f'{qty} Item(s) selected',
            'subtotal': f'SUBTOTAL: ${item_collection.total_price - price}',
        }

        # Delete the item from the collection
        
        item_collection._meta.model.objects.delete_item(item_collection, item_id)

        return response_data, 200

    def add_to_cart(self, data: dict[str, Any]) -> tuple[dict[str, Any], int]:
        product = ProductDTO.from_product(self.product_acl.fetch_sample_of_size(product_uuid=data.get('product', None), size_uuid=data.get('size', None)))

        if not product.sizes or len(product.sizes) < 1:
            raise ValueError("Product has no available sizes")
        if not product.images or len(product.images) < 1:
            raise ValueError("Product has no available images")

        if type_of_collection == WishlistEntity.__name__:
            wishlist = self.wishlist_repository.fetch_wishlist_by_user(self.user.uuid)
            wishlist, new_item = wishlist.add_item(product.price, data.get('color', None), data.get('qty', 0), product.images[0], product.sizes[0].to_size_vo())
            self.wishlist_repository.save(wishlist_items=new_item)
            return {'status': "success", 'item_of_collection': wishlist}, 200
        elif type_of_collection == CartEntity.__name__:
            cart = self.cart_repository.fetch_cart(self.user.uuid)
            cart = cart.add_item(product.price, data.get('color', None), data.get('qty', None), product.images[0], product.sizes[0].to_size_vo())
            self.cart_repository.save(cart)
            return {'status': "success", 'item_of_collection': cart}, 200
        else:
            return {'status': 'error', 'message': 'Item not associated with any collection'}, 400

        return None
        if form.is_valid():
            form.save()

            collection_item = form.cleaned_data["product"]

            items_of_collection = {
                "name": collection_item.name,
                "price_with_discount": collection_item.get_price_with_discount(),
                "price": collection_item.price,
                "imageUrl": collection_item.image.url,
                "url": collection_item.get_absolute_url(),
            }
                
            return {'status': "success", 'item_of_collection': items_of_collection}, 200
        return {'status': 'error', 'message': 'Something went wrong'}, 400

class WishlistService(BaseService["WishlistService"]):
    def __init__(self, product_acl: IProductACL, wishlist_repository: IWishlistRepository, **kwargs):
        super().__init__(**kwargs)
        self.product_acl = product_acl
        self.wishlist_repository = wishlist_repository

    def delete_button_wishlist_service(self, request_dto: DeleteWishlistItemRequestDTO) -> tuple[dict[str, Any], int]:
        if not self.user.is_authenticated:
            return {"message": "You must register or log in to use this feature"}, 401

        try:
            wishlist_entity = self.wishlist_repository.fetch_wishlist_by_user(self.user.pub_uuid)
        except NotFoundWishlistError:
            return {"message": "Sorry, we can't find your wishlist"}, 404

        wishlist_entity.delete_item(item_uuid=request_dto.item_public_uuid, price=request_dto.price, qty=request_dto.qty)
        self.wishlist_repository.save(wishlist_entity)
        return {'status': "success"}, 200

    def add_to_wishlist(self, request_dto: AddWishlistItemRequestDTO) -> tuple[dict[str, Any], int]:
        if not self.user.is_authenticated:
            return {"message": "You must register or log in to use this feature"}, 401

        try:
            wishlist_entity = self.wishlist_repository.fetch_wishlist_by_user(self.user.pub_uuid)
        except NotFoundWishlistError:
            return {"message": "Sorry, we can't find your wishlist"}, 404

        product_dto = ProductDTO.from_product(self.product_acl.fetch_sample_of_size(request_dto.product, size_uuid=request_dto.size))
        compiled_wihslist_item = self.compile_wishlist_item_data(request_dto, product_dto)
        wishlist_entity.add_item(*compiled_wihslist_item)
        self.wishlist_repository.save(wishlist_entity)
        return {'message': "success"}, 200

    def compile_wishlist_item_data(self, request_dto: AddWishlistItemRequestDTO, product: ProductDTO) -> tuple[AddToWishlistDomainDTO, int, Decimal]:
        if product.price is None:
            raise WishlistPriceValidationError("Product price is required to add to wishlist.")

        try:
            price = Decimal(product.price)
        except (ValueError, TypeError):
            raise WishlistPriceValidationError(f"Invalid price value: {product.price}")

        return AddToWishlistDomainDTO(
                color=request_dto.color or "Black",
                qty=request_dto.qty or 1,
                size=product.sizes[0].pub_uuid if product.sizes and product.sizes[0] else None
            ), request_dto.qty, price
