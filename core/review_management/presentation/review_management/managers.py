from django.db.models import Manager, Count, Sum

class ProductRatingManager(Manager):
    
    # def update_rating(self, product_rating, stars, increase=True):
    #     # Get or create the RatingCount for the stars provided
    #     rating_count, created = product_rating.ratingcount_set.get_or_create(
    #         stars=stars, product_rating=product_rating
    #     )
        
    #     # Increment or decrement the count
    #     rating_count.count += 1 if increase else -1
    #     rating_count.save()

    #     # Fetch all the RatingCount records related to the product rating
    #     rating_counts = product_rating.ratingcount_set.all()

    #     # Calculate total reviews and total rating
    #     total_reviews = sum(rc.count for rc in rating_counts)
    #     total_rating = sum(rc.stars * rc.count for rc in rating_counts)

    #     # Update the rating field on the ProductRating instance
    #     product_rating.rating = total_rating / total_reviews if total_reviews > 0 else None
    #     product_rating.save()

    #     return product_rating
    
    def update_rating(self, product_rating):
        # Aggregate to calculate average rating and total count of reviews
        reviews = product_rating.review_set.aggregate(
            total_reviews=Count('rating'),
            total_rating=Sum('rating')
        )

        total_reviews = reviews['total_reviews']
        total_rating = reviews['total_rating']

        # Update the rating field with the average
        product_rating.rating = total_rating / total_reviews if total_reviews > 0 else None
        product_rating.save()
