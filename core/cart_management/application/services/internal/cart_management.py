from core.cart_management.presentation.cart_management.forms import AddToWishlistForm, AddToCartForm

from core.cart_management.domain.aggregates.cart_management import Cart as CartEntity, Wishlist as WishlistEntity
from core.cart_management.domain.interfaces.i_acls import ICartACL, IWishlistACL
from ..base_service import BaseService

from core.shop_management.domain.interfaces.i_acls import IProductACL

from typing import Generic, Any


class ItemCollectionService(BaseService['ItemCollectionService']):

    def __init__(self, product_acl: IProductACL, cart_acl: ICartACL, wishlist_acl: IWishlistACL, **kwargs):
        super().__init__(**kwargs)
        self.product_acl = product_acl
        self.cart_acl = cart_acl
        self.wishlist_acl = wishlist_acl

    def delete_button_item_collection_service(self, data: dict[str, Any], type_of_collection: str) -> tuple[dict[str, Any], int]:
        item_pub_uuid = data.get('product')
        #type_of_collection = data['type']

        if type_of_collection == WishlistEntity.__name__:
            item_collection = self.wishlist_rep.fetch_wishlist_by_user(self.user.uuid)
            #order_product = #get_object_or_404(WishlistItem, pk=item_id)
            #item_collection = order_product.wishlist if hasattr(order_product, 'wishlist') else None
        elif type_of_collection == CartEntity.__name__:
            #order_product = #get_object_or_404(CartItem, pk=item_id)
            #item_collection = order_product.cart if hasattr(order_product, 'cart') else None
            pass
        else:
            return {'status': 'error', 'message': 'Item not associated with any collection'}, 400

        if item_collection is None:
            return {'status': 'error', 'message': 'Collection not found'}, 404

        # Compute the price and quantity changes
        qty = item_collection.quantity - order_product.qty
        price = order_product.size.product.get_price_with_discount() * order_product.qty
        response_data = {
            'qty': str(qty),
            'qty-2': f'{qty} Item(s) selected',
            'subtotal': f'SUBTOTAL: ${item_collection.total_price - price}',
        }

        # Delete the item from the collection
        
        item_collection._meta.model.objects.delete_item(item_collection, item_id)

        return response_data, 200


    def add_to_item_collection(self, data: dict[str, Any], type_of_collection: str) -> tuple[dict[str, Any], int]:
        product = self.product_acl.fetch_product_by_uuid(public_uuid=data.get('product', None), load_sizes=True)

        if type_of_collection == WishlistEntity.__name__:
            item_collection = self.wishlist_acl.fetch_wishlist_by_user(self.user.uuid)
        elif type_of_collection == CartEntity.__name__:
            item_collection = self.cart_acl.fetch_cart_by_user(self.user.uuid)
        else:
            return {'status': 'error', 'message': 'Item not associated with any collection'}, 400

        item_collection.add_item(product)
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