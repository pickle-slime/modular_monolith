from core.cart_management.domain.interfaces.i_repositories.i_cart_management import ICartRepository, IWishlistRepository
from core.cart_management.domain.dtos.cart_management import AddToWishlistDomainDTO, AddToCartDomainDTO
from core.cart_management.application.dtos.acl_dtos import ProductDTO
from core.cart_management.application.dtos.requests import AddWishlistItemRequestDTO, AddCartItemRequestDTO, DeleteWishlistItemRequestDTO, DeleteCartItemRequestDTO
from core.cart_management.application.exceptions import ProductValidationError, ProductPriceValidationError, NotFoundWishlistError, NotFoundCartError
from ..base_service import BaseService

from core.shop_management.domain.interfaces.i_acls import IProductACL
from core.shop_management.application.acl_exceptions import ProductNotFoundACLError, SizeNotFoundACLError

from typing import Any
from decimal import Decimal, ROUND_HALF_UP

class CartService(BaseService["CartService"]):
    def __init__(self, product_acl: IProductACL, cart_repository: ICartRepository, **kwargs):
        super().__init__(**kwargs)
        self.product_acl = product_acl
        self.cart_repository = cart_repository

    def delete_button_cart_service(self, request_dto: DeleteCartItemRequestDTO) -> tuple[dict[str, Any], int]:
        try:
            cart_entity = self.cart_repository.fetch_cart()
            if cart_entity.items is None:
                raise NotFoundWishlistError("missing items")
            item = cart_entity.items[request_dto.item_public_uuid]
            if item.qty is None:
                raise NotFoundWishlistError("missing qty")
        except NotFoundCartError:
            return {"message": "Sorry, we can't find your cart"}, 400

        try:
            product_dto = ProductDTO.from_product(self.product_acl.fetch_sample_of_size(request_dto.product, size_uuid=item.size))
            if product_dto.price is None or product_dto.discount is None:
                raise ProductNotFoundACLError("missing price or discount")
        except (ProductNotFoundACLError, SizeNotFoundACLError):
            return {"message": "Invalid request data"}, 400
        
        price_with_discount = Decimal(product_dto.price - (product_dto.price * product_dto.discount / 100)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        cart_entity.delete_item(item_uuid=request_dto.item_public_uuid, price=price_with_discount, qty=item.qty)
        self.cart_repository.save(cart_entity)

        return {
                'qty': cart_entity.quantity,
                'subtotal': cart_entity.total_price,
            }, 200

    def add_to_cart(self, request_dto: AddCartItemRequestDTO) -> tuple[dict[str, Any], int]:
        try:
            cart_entity = self.cart_repository.fetch_cart()
        except NotFoundWishlistError:
            return {"message": "Sorry, we can't find your cart"}, 400

        try:
            if request_dto.size:
                product_dto = ProductDTO.from_product(self.product_acl.fetch_sample_of_size(request_dto.product, size_uuid=request_dto.size))
            else:
                product_dto = ProductDTO.from_product(self.product_acl.fetch_sample_of_size(request_dto.product))
        except (ProductNotFoundACLError, SizeNotFoundACLError):
            return {"message": "invalid request data"}, 400

        compiled_cart_item = self.compile_cart_item_data(request_dto, product_dto)
        cart_entity.add_item(*compiled_cart_item)
        self.cart_repository.save(cart_entity)
        return {'message': "success"}, 200

    def compile_cart_item_data(self, request_dto: AddCartItemRequestDTO, product: ProductDTO) -> tuple[AddToCartDomainDTO, int, Decimal]:
        if product.price is None or product.color is None or product.sizes is None or product.discount is None:
            raise ProductValidationError("Product has invalid data.")

        try:
            price_with_discount = Decimal(product.price - (product.price * product.discount / 100)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        except (ValueError, TypeError):
            raise ProductPriceValidationError(f"Invalid price value: {product.price}")

        return AddToCartDomainDTO(
                color=request_dto.color or product.color[0],
                qty=request_dto.qty,
                size=request_dto.size or product.sizes[0].pub_uuid,
            ), request_dto.qty, price_with_discount

class WishlistService(BaseService["WishlistService"]):
    def __init__(self, product_acl: IProductACL, wishlist_repository: IWishlistRepository, **kwargs):
        super().__init__(**kwargs)
        self.product_acl = product_acl
        self.wishlist_repository = wishlist_repository

    def delete_button_wishlist_service(self, request_dto: DeleteWishlistItemRequestDTO) -> tuple[dict[str, Any], int]:
        try:
            wishlist_entity = self.wishlist_repository.fetch_wishlist_by_user(self.user.pub_uuid)
            if wishlist_entity.items is None:
                raise NotFoundWishlistError("missing items")
            item = wishlist_entity.items[request_dto.item_public_uuid]
            if item.qty is None:
                raise NotFoundWishlistError("missing qty")
        except NotFoundWishlistError:
            return {"message": "Sorry, we can't find your wishlist"}, 400

        try:
            product_dto = ProductDTO.from_product(self.product_acl.fetch_sample_of_size(request_dto.product, size_uuid=item.size))
            if product_dto.price is None or product_dto.discount is None:
                raise ProductNotFoundACLError("missing price or discount")
        except (ProductNotFoundACLError, SizeNotFoundACLError):
            return {"message": "Invalid request data"}, 400
        
        price_with_discount = Decimal(product_dto.price - (product_dto.price * product_dto.discount / 100)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        wishlist_entity.delete_item(item_uuid=request_dto.item_public_uuid, price=price_with_discount, qty=item.qty)
        self.wishlist_repository.save(wishlist_entity)

        return {
                'qty': wishlist_entity.quantity,
                'subtotal': wishlist_entity.total_price,
            }, 200

    def add_to_wishlist(self, request_dto: AddWishlistItemRequestDTO) -> tuple[dict[str, Any], int]:
        try:
            wishlist_entity = self.wishlist_repository.fetch_wishlist_by_user(self.user.pub_uuid)
        except NotFoundWishlistError:
            return {"message": "Sorry, we can't find your wishlist"}, 400

        try:
            if request_dto.size:
                product_dto = ProductDTO.from_product(self.product_acl.fetch_sample_of_size(request_dto.product, size_uuid=request_dto.size))
            else:
                product_dto = ProductDTO.from_product(self.product_acl.fetch_sample_of_size(request_dto.product))
        except (ProductNotFoundACLError, SizeNotFoundACLError):
            return {"message": "invalid request data"}, 400

        compiled_wishlist_item = self.compile_wishlist_item_data(request_dto, product_dto)
        wishlist_entity.add_item(*compiled_wishlist_item)
        self.wishlist_repository.save(wishlist_entity)
        return {'message': "success"}, 200

    def compile_wishlist_item_data(self, request_dto: AddWishlistItemRequestDTO, product: ProductDTO) -> tuple[AddToWishlistDomainDTO, int, Decimal]:
        if product.price is None or product.color is None or product.sizes is None or product.discount is None:
            raise ProductValidationError("Product has invalid data.")

        try:
            price_with_discount = Decimal(product.price - (product.price * product.discount / 100)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        except (ValueError, TypeError):
            raise ProductPriceValidationError(f"Invalid price value: {product.price}")

        return AddToWishlistDomainDTO(
                color=request_dto.color or product.color[0],
                qty=request_dto.qty,
                size=request_dto.size or product.sizes[0].pub_uuid,
            ), request_dto.qty, price_with_discount
