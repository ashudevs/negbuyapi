import json
from rest_framework import serializers
from .models import *


# # class ImageSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = productImages
# #         fields = ['image']

# #     def to_representation(self, instance):
# #         json_obj = super().to_representation(instance)
# #         image_list = []
# #         image_list = json_obj['image']

# #         return image_list


# # class product_serializer(serializers.ModelSerializer):

# #     class Meta:
# #         model = product
# #         fields = ['name', 'brand', 'price', 'sku', 'id', 'varients']


# # class InventorySerializer(serializers.ModelSerializer):
# #     product = product_serializer(read_only=True)

# #     class Meta:
# #         model = Inventory
# #         fields = '__all__'

# #     def to_representation(self, instance):
# #         json_obj = super().to_representation(instance)
# #         product_images = productImages.objects.filter(
# #             product=json_obj['product']['id'], color=json_obj['color'])
# #         image_serialized = ImageSerializer(product_images, many=True).data
# #         json_obj['images'] = []
# #         for image in image_serialized:
# #             json_obj['images'].append(image)

# #         varients = {
# #             "images": json_obj['images'],
# #             "size": json_obj['size'],
# #             "color": json_obj['color'],
# #             "quantity": json_obj['quantity']
# #         }
# #         json_obj['varients'] = varients
# #         del json_obj['images'], json_obj['size'], json_obj['quantity'], json_obj['color']

# #         return json_obj['varients']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = userDB
        fields = '__all__'



# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = productCategory
#         fields = ['name']


# # class ProductDetailSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = product_detail_db
# #         fields = ['heading', 'desc', 'image']


# class ReviewSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)

#     class Meta:
#         model = review_db
#         fields = '__all__'

#     # def to_representation(self, instance):
#     #     representation = super().to_representation(instance)
#     #     reviews = {
#     #         'rating': 4,
#     #         'count': 220
#     #     }
#     #     return reviews


# # class ProductSerializer(serializers.ModelSerializer):
# #     product_images = ImageSerializer(many=True, read_only=True)
# #     user = UserSerializer(read_only=True)
# #     category_id = CategorySerializer(read_only=True)
# #     image_details = ProductDetailSerializer(many=True, read_only=True)
# #     reviews = ReviewSerializer(many=True, read_only=True)

# #     class Meta:
# #         model = product
# #         fields = '__all__'

# #     def to_representation(self, instance):
# #         json_obj = super().to_representation(instance)
# #         try:
# #             json_obj['size'] = json_obj['size'].split(
# #                 ',') if json_obj['size'] is not None else []

# #             json_obj['keyword'] = json_obj['keyword'].split(
# #                 ',') if json_obj['keyword'] is not None else []

# #             json_obj['color'] = json_obj['color'].split(
# #                 ',') if json_obj['color'] is not None else []

# #             json_obj['details'] = json_obj['details'].split(
# #                 ',') if json_obj['details'] is not None else []

# #             json_obj['review'] = {'rating': 4, 'count': 220}

# #             retList = []
# #             if json_obj['details'] != []:
# #                 #print(json_obj['details'])
                
# #                 #print(each_detail)
# #                 for i in json_obj['details']:
# #                     obj = {}
# #                     newList = i.split(':')
# #                     obj['title'] = newList[0]
# #                     obj['description'] = newList[1]
# #                     retList.append(obj)

# #             json_obj['details'] = retList

# #             json_obj['category_id'] = json_obj['category_id']['name']
# #             json_obj['quantity_price'] = json_obj['quantity_price'].split(
# #                 ',') if json_obj['quantity_price'] is not None else []
# #             for k in json_obj:
# #                 if json_obj[k] == None or json_obj[k] == 'null':
# #                     json_obj[k] = ''
# #             #print(json_obj)
# #             return json_obj
# #         except Exception as e:
# #             return json_obj


# # class OrderSerializer(serializers.ModelSerializer):
# #     user = UserSerializer(read_only=True)
# #     product_info = ProductSerializer(many=True, read_only=True)

# #     class Meta:
# #         model = orders
# #         fields = '__all__'


# class PortSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = port
#         fields = '__all__'

# class UserSerializerNEW(serializers.ModelSerializer):

#     class Meta:
#         model = userDB
#         fields = ['username']

# # class ProductSerializer_new(serializers.ModelSerializer):
# #     #product_images = ImageSerializer(many=True, read_only=True)
# #     #user = UserSerializerNEW(read_only=True)
# #     class Meta:
# #         model = product
# #         fields = [
# #             'name',
# #             'sku',
# #             'featured_products',
# #             'best_selling_products',
# #             'hot_selling_products',
# #             'fast_dispatch',
# #             'ready_to_ship',
# #             'customized_product',
# #             'brand',
# #             'keyword',
# #             'color',
# #             'size',
# #             'details',
# #             'price_choice',
# #             'price',
# #             'quantity_price',
# #             'weight',
# #             'transportation_port',
# #             'packing_details',
# #             'status',
# #             'packing_address',
# #         ]

# class TransactionSerializer(serializers.ModelSerializer):
#     # product_images = ImageSerializer(many=True, read_only=True)

#     class Meta:
#         model = Orders_Id
#         fields = [
#             "ORDER_ID",
#             'Email',
#             'Mobile',
#             "MID",
#             "TXNID",
#             "TXNAMOUNT",
#             "payment_mode",
#             "CURRENCY",
#             "TXNDATE",
#             "STATUS",
#             "TXNDATE",
#             "RESPMSG",
#             "GATEWAYNAME",
#             "BANKTXNID",
#             "BANKNAME",
#             'Checksum',
#             ]

# # class ProductNEWSerializer(serializers.ModelSerializer):
# #     product_images = ImageSerializer(many=True, read_only=True)
# #     user = UserSerializer(read_only=True)
# #     category_id = CategorySerializer(read_only=True)
# #     image_details = ProductDetailSerializer(many=True, read_only=True)
# #     # reviews = ReviewSerializer(many=True, read_only=True)

# #     class Meta:
# #         model = product
# #         fields = '__all__'

# #     def to_representation(self, instance):
# #         json_obj = super().to_representation(instance)
# #         try:
# #             # json_obj['size'] = json_obj['size'].split(
# #             #     ',') if json_obj['size'] is not None else []

# #             # json_obj['keyword'] = json_obj['keyword'].split(
# #             #     ',') if json_obj['keyword'] is not None else []

# #             # json_obj['color'] = json_obj['color'].split(
# #             #     ',') if json_obj['color'] is not None else []

# #             # json_obj['details'] = json_obj['details'].split(
# #             #     ',') if json_obj['details'] is not None else []

# #             json_obj['reviews'] = {'rating': 4, 'count': 220}
# #             # retList = []
# #             # if json_obj['details'] != []:
# #             #     for i in json_obj['details']:
# #             #         obj = {}
# #             #         newList = i.split(':')
# #             #         obj['title'] = newList[0]
# #             #         obj['description'] = newList[1]
# #             #         retList.append(obj)

# #             # json_obj['details'] = retList

# #             # json_obj['category_id'] = json_obj['category_id']['name']
# #             # json_obj['quantity_price'] = json_obj['quantity_price'].split(
# #             #     ',') if json_obj['quantity_price'] is not None else []
# #             # for k in json_obj:
# #             #     if json_obj[k] == None or json_obj[k] == 'null':
# #             #         json_obj[k] = ''

# #             return json_obj
# #         except Exception as e:
# #             return json_obj

# class UserNEWSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = userDB
#         fields = [
#             'first_name',
#             'last_name',
#             'state',
#             'auth',
#             'profile_picture'
#         ]

#     def to_representation(self, instance):
#         json_obj = super().to_representation(instance)
#         for k in json_obj:
#             if json_obj[k] == None:
#                 json_obj[k] = ''
#         return json_obj


# class ReviewNEWSerializer(serializers.ModelSerializer):
#     user = UserNEWSerializer(read_only=True)
    
#     class Meta:
#         model = review_db
#         fields = ['review_title','review_description','rating','user','created_at',]

    

# # class NEWProductSerializer(serializers.ModelSerializer):
# #     reviews = ReviewNEWSerializer(many=True, read_only=True)
# #     class Meta:
# #         model = product
# #         fields = [
# #             'id',
# #             'name',
# #             'main_image',
# #             'reviews'
# #             ]

# #     def to_representation(self, instance):
# #         json_obj = super().to_representation(instance)
# #         review_list = [0]
# #         try:            
# #             count_1 = 0
# #             count_2 = 0
# #             count_3 = 0
# #             count_4 = 0
# #             count_5 = 0
# #             length_review_list = 0
# #             avg_review_list = 0
# #             for i in json_obj['reviews']:
# #                 #print(i['rating'])
# #                 if review_list[0] == 0:
# #                     review_list[0] = int(i['rating'])
# #                 else:
# #                     review_list.append(int(i['rating']))
# #                 if i['rating'] ==1:
# #                     count_1+= 1
# #                 if i['rating'] ==2:
# #                     count_2+= 1
# #                 if i['rating'] ==3:
# #                     count_3+= 1
# #                 if i['rating'] ==4:
# #                     count_4+= 1
# #                 if i['rating'] ==5:
# #                     count_5+= 1
# #                 if review_list[0]==0:
# #                     length_review_list = 0
# #                 else:
# #                     length_review_list = len(review_list)
# #                 if length_review_list == 0:
# #                     avg_review_list = 0
# #                 else:
# #                     avg_review_list= round(sum(review_list)/length_review_list)
# #             # total_ratings =(count_1*1)+(count_2*2)+(count_3*3)+(count_4*4)+(count_5*5)
# #             # total_reviews = count_1+count_2+count_3+count_4+count_5
            
# #             review_dict = {
# #                 'ratings': sum(review_list),
# #                 'reviews': length_review_list,
# #                 'average_rating':avg_review_list,
# #             }
# #             rating_stats_dict = {
# #                 'rating_1': count_1,
# #                 'rating_2': count_2,
# #                 'rating_3': count_3,
# #                 'rating_4': count_4,
# #                 'rating_5': count_5,
# #             }
# #             json_obj['statistics'] = review_dict
# #             json_obj['rating_stats'] = rating_stats_dict

# #             return json_obj
# #         except Exception as e:
# #             return json_obj

# # class NEWProdSerializer(serializers.ModelSerializer):
# #     reviews = ReviewNEWSerializer(many=True, read_only=True)
# #     class Meta:
# #         model = product
# #         fields = [
# #             'reviews'
# #             ]

# #     def to_representation(self, instance):
# #         json_obj = super().to_representation(instance)
# #         review_list = [0]
# #         # review_list1 =[5,1,5,4]
# #         try:            
# #             count_1 = 0
# #             count_2 = 0
# #             count_3 = 0
# #             count_4 = 0
# #             count_5 = 0
# #             length_review_list = 0
# #             avg_review_list = 0
# #             for i in json_obj['reviews']:
# #                 #print(i['rating'])
# #                 if review_list[0] == 0:
# #                     review_list[0] = int(i['rating'])
# #                 else:
# #                     review_list.append(int(i['rating']))
# #                 if i['rating'] ==1:
# #                     count_1+= 1
# #                 if i['rating'] ==2:
# #                     count_2+= 1
# #                 if i['rating'] ==3:
# #                     count_3+= 1
# #                 if i['rating'] ==4:
# #                     count_4+= 1
# #                 if i['rating'] ==5:
# #                     count_5+= 1
# #                 if review_list[0]==0:
# #                     length_review_list = 0
# #                 else:
# #                     length_review_list = len(review_list)
# #                 if length_review_list == 0:
# #                     avg_review_list = 0
# #                 else:
# #                     avg_review_list= round(sum(review_list)/length_review_list)
# #             # total_ratings =(count_1*1)+(count_2*2)+(count_3*3)+(count_4*4)+(count_5*5)
# #             # total_reviews = count_1+count_2+count_3+count_4+count_5
# #             review_dict = {
# #                 'ratings': sum(review_list),
# #                 'reviews': length_review_list,
# #                 'average_rating':avg_review_list,
# #             }
# #             rating_stats_dict = {
# #                 'rating_1': count_1,
# #                 'rating_2': count_2,
# #                 'rating_3': count_3,
# #                 'rating_4': count_4,
# #                 'rating_5': count_5,
# #             }
# #             json_obj['statistics'] = review_dict
# #             json_obj['rating_stats'] = rating_stats_dict

# #             return json_obj
# #         except Exception as e:
# #             return json_obj

# class ReviewStatsSerializer(serializers.ModelSerializer):
#     reviews = ReviewNEWSerializer(many=True, read_only=True)

#     class Meta:
#         model = review_db
#         fields = ['reviews','rating']

# class newsPostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = newsPost
#         fields = [
#             'image',
#             'heading',
#             'desc',
#         ]

# class teamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = teamSection
#         fields = [
#             'image',
#             'name',
#             'designation',
#             'bio'
#         ]

# # class ProductSearchSerializer(serializers.ModelSerializer):
# #     category_id = CategorySerializer(read_only=True)
# #     class Meta:
# #         model = product
# #         fields = [
# #             'id',
# #             'name',
# #             'category_id',
# #         ]

# #     def to_representation(self, instance):
# #         json_obj = super().to_representation(instance)
# #         json_obj['category_id'] = json_obj['category_id']['name']
# #         return json_obj

# class UserLatestSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = userDB
#         fields = [
#             'username',
#         ]

#     def to_representation(self, instance):
#         json_obj = super().to_representation(instance)
#         return json_obj['username']

# class AnalyticSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = sellerAnalytics
#         fields = [
#             'day',
#             'date',
#             'checked_count',
#             'search_count'
#         ]

# class TimeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TimeManagement
#         fields = [
#             'date',
#             'day',
#             'year',
#             'time'
#         ]


class ProductDBSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDB
        fields = '__all__'


class ProductColorVariationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColorVariations
        fields = '__all__'


class ProductImageDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImageDescription
        fields = '__all__'

class ProductExtraImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductExtraImages
        fields = '__all__'

class Review_Images_DBSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review_Images_DB
        fields = '__all__'


class SellerRfqReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerRfqReply
        fields = '__all__'

class MySerializer(serializers.ModelSerializer):
    file = serializers.FileField(max_length=None, allow_empty_file=False, use_url=False)
    class Meta:
        model = FileTest
        fields = ('file')


class Blogs_DBSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs_DB
        fields = '__all__'


class productCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = productCategory
        fields = '__all__'


class HomePage_Poster_BrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePage_Poster_Brands
        fields = '__all__'




# ashutosh



# class ResponseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = KeywordResponse
#         fields = '__all__'
from .models import review_db
class ReviewDBSerializer(serializers.ModelSerializer):
    class Meta:
        model = review_db
        fields = '__all__'

from .models import Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')#, 'parent_tag'

class TagIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class Tag_d_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'parent_tag', 'have_branch']

class ProductColorVariationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColorVariations
        fields = ('main_image',)

    def get_main_image(self, obj):
        if obj.main_image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.main_image.url)
        return None

class DealsProductsInfoSerializer(serializers.ModelSerializer):
    main_image = ProductColorVariationsSerializer(source='main_product_id.productcolorvariations_set.first', read_only=True)

    class Meta:
        model = DealsProductsInfo
        fields = ('id', 'product_name', 'about_product', 'main_image','main_product_id')


class warehouseinfoserializer(serializers.ModelSerializer):
    class Meta:
        model = Negbuy_Warehouse
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field_name in ['warehouse_image1', 'warehouse_image2', 'warehouse_image3', 'warehouse_image4', 'warehouse_image5', 'warehouse_image6']:
            image_field = getattr(instance, field_name)
            if image_field and hasattr(image_field, 'url'):
                representation[field_name] = self.context['request'].build_absolute_uri(image_field.url)
                
        return representation