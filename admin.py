from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin




class cartFields(admin.ModelAdmin):
    list_display = ('buyer_info', 'product', 'order_number',
                    'order_price', 'order_status')


class portFields(ImportExportModelAdmin):
    list_display = ('id', 'name', 'country', 'latitude', 'longitude')


class orderFields(admin.ModelAdmin):
    list_display = ('product_id', 'order_number',
                    'status', 'user', 'order_date', 'id')


class bankFields(admin.ModelAdmin):
    list_display = ('accountName', 'accountNumber', 'accountIfsc', 'user')


class userFields(ImportExportModelAdmin):
    search_fields=('phone','seller_name',)
    list_display = ('id', 'seller_name', 'user_id', 'phone', 'role','created_at','search_count','username')

class Review_Images_DBInline(admin.TabularInline):
    model = Review_Images_DB
    extra = 1

class reviewFields(admin.ModelAdmin):
    inlines = [Review_Images_DBInline]
    list_display = ('review_title', 'main_product_id', 'rating', 'user', 'created_at')


class newsPostFields(admin.ModelAdmin):
    list_display = ('desc', 'heading',)

class teamFields(admin.ModelAdmin):
    list_display = ('name', 'designation', 'id')

class contactFields(admin.ModelAdmin):
    list_display = ('message',)

class monthadmin(admin.ModelAdmin):
    list_display = ('name',)

class transactionDBFields(admin.ModelAdmin):
    list_display = ('seller', 'month', 'year', 'units_sold', 'total_revenue',)

class inventoryFields(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'color', 'size',)

class rfqFields(admin.ModelAdmin):
    list_display = ('requirement', 'quantity', 'target_price')

class Orders_IDFields(admin.ModelAdmin):
    list_display = ('ORDER_ID','TXNID','Mobile','TXNAMOUNT','Payment_Status',)

class Ordered_ProductFields(admin.ModelAdmin):
    list_display = ('Orders_ID','Product_Id','Product_Name','Product_Price',)

@admin.register(primary_category)
class CategoryAdmin(ImportExportModelAdmin):
    pass


class CourierFields(admin.ModelAdmin):
    list_display = ('uniqueid', 'user', 'prod', 'couriername','courierid','deliveryCharge',)

class sellerAnalyticsFields(admin.ModelAdmin):
    list_display = ('seller', 'created_at','day','date','checked_count','search_count',)
    ordering = ['created_at', ]

class TimeAnalyticsFields(admin.ModelAdmin):
    list_display = ('seller','day','created_at','date','time',)
    ordering = ['-created_at', ]

class RazorpayFields(admin.ModelAdmin):
    list_display = ('user','prod','amount','payment_id','paid',)

    
admin.site.register(userDB, userFields)
admin.site.register(bankDetail, bankFields)
admin.site.register(port, portFields)
admin.site.register(review_db, reviewFields)
admin.site.register(rfq, rfqFields)


class ProductImageDescriptionInline(admin.TabularInline):
    model = ProductImageDescription
    extra = 1

class ProductDetailsInline(admin.TabularInline):
    model = ProductDetails
    extra = 1

class ProductColorVariationsInline(admin.TabularInline):
    model = ProductColorVariations
    extra = 1

class ProductEditRemarksInline(admin.TabularInline):
    model = ProductEditRemarks
    extra = 1

class ViewsTrackingDBInline(admin.TabularInline):
    model = ViewsTrackingDB
    extra = 1

class review_dbInline(admin.TabularInline):
    model = review_db
    extra = 1


@admin.register(ProductDB)
class ProductDBModelAdmin(ImportExportModelAdmin):
    inlines = [ProductDetailsInline, ProductImageDescriptionInline, ProductColorVariationsInline, ViewsTrackingDBInline, ProductEditRemarksInline, review_dbInline]
    search_fields=('product_title',)
    list_display = ('id', 'seller_id', 'product_title', 'verification_status', 'brand', 'category_id', 'gst', 'created_at')
    actions = ["change_to_verified"]

    def change_to_verified(self, request, queryset):
        queryset.update(verification_status="verified")
        #create views tracking db obj
        productdb_instance = ProductDB.objects.get(id=queryset.values_list('id', flat=True)[0])
        views_obj = ViewsTrackingDB.objects.create(main_product_id=productdb_instance)

@admin.register(ProductImageDescription)
class ProductImageDescriptionModelAdmin(admin.ModelAdmin):
    list_display= ('id', 'main_product_id', 'image', 'heading', 'description')


@admin.register(ProductDetails)
class ProductDetailsModelAdmin(admin.ModelAdmin):
    list_display= ('id', 'main_product_id', 'heading', 'description')


class ProductExtraImagesInline(admin.TabularInline):
    model = ProductExtraImages
    extra = 1

class ProductSizeVariationsInline(admin.TabularInline):
    model = ProductSizeVariations
    extra = 1


@admin.register(ProductColorVariations)
class ProductColorVariationsModelAdmin(admin.ModelAdmin):
    inlines = [ProductExtraImagesInline, ProductSizeVariationsInline]
    list_display= ('id', 'main_product_id', 'color', 'main_image')


@admin.register(ProductExtraImages)
class ProductExtraImagesModelAdmin(admin.ModelAdmin):
    list_display= ('id', 'variant_id', 'image')


class ProductBulkPurchaseDetailsInline(admin.TabularInline):
    model = ProductBulkPurchaseDetails
    extra = 1

class ProductInventoryDBInline(admin.TabularInline):
    model = ProductInventoryDB
    extra = 1

class SubSkuIdDBInline(admin.TabularInline):
    model = SubSkuIdDB
    extra = 1


@admin.register(ProductSizeVariations)
class ProductSizeVariationsModelAdmin(admin.ModelAdmin):
    inlines = [ProductInventoryDBInline, SubSkuIdDBInline, ProductBulkPurchaseDetailsInline]
    list_display= ('id', 'variant_id', 'size', 'weight', 'manufacturing_time')


@admin.register(ProductBulkPurchaseDetails)
class ProductBulkPriceDetailsModelAdmin(admin.ModelAdmin):
    list_display= ('id', 'product_id', 'min_quantity', 'min_quantity', 'price', 'manufacturing_time')


@admin.register(ProductInventoryDB)
class ProductInventoryDBModelAdmin(admin.ModelAdmin):
    list_display= ('id', 'product_id', 'stock', 'created_at', 'modified_at')


@admin.register(ProductEditRemarks)
class ProductEditRemarksModelAdmin(admin.ModelAdmin):
    list_display= ('id', 'main_product_id', 'field_name', 'remarks', 'created_at', 'modified_at')


@admin.register(SubSkuIdDB)
class SubSkuIdDBModelAdmin(admin.ModelAdmin):
    list_display= ('id', 'product_id', 'sub_sku_id', 'created_at', 'modified_at')


@admin.register(Review_Images_DB)
class Review_Images_DBModelAdmin(admin.ModelAdmin):
    list_display= ('id', 'review_id', 'file')


@admin.register(SellerNoticeBoard)
class SellerNoticeBoardModelAdmin(admin.ModelAdmin):
    list_display= ('id', 'seller_id', 'subject', 'message', 'created_at')

@admin.register(BuyerNoticeBoard)
class BuyerNoticeBoardModelAdmin(admin.ModelAdmin):
    list_display= ('id', 'Buyer_id', 'subject', 'message', 'created_at')


@admin.register(ViewsTrackingDB)
class ViewsTrackingDBModelAdmin(admin.ModelAdmin):
    list_display= ('id', 'main_product_id', 'total_screen_time', 'browser_views', 'app_views', 'created_at')


@admin.register(SellerRfqReply)
class SellerRfqReplyModelAdmin(admin.ModelAdmin):
    list_display= ('id', 'seller_id', 'rfq_id', 'file', 'created_at')   


@admin.register(FileTest)
class FileTestModelAdmin(admin.ModelAdmin):
    list_display= ('id', 'file')   


@admin.register(DDP_Orders_DB)
class DDP_Orders_DBModelAdmin(admin.ModelAdmin):
    list_display= ('id', 'product_id', 'created_at')   


@admin.register(Exwork_Orders_DB)
class Exwork_Orders_DBModelAdmin(admin.ModelAdmin):
    list_display= ('id', 'product_id', 'created_at')   


@admin.register(Negbuy_Warehouse)
class Negbuy_WarehouseModelAdmin(admin.ModelAdmin):
    list_display= ('id', 'address')


@admin.register(Pick_Up_Schedules)
class Pick_Up_SchedulesModelAdmin(admin.ModelAdmin):
    list_display= ('id', 'ddp_order_id', 'exwork_order_id', 'weight', 'pick_up_time1', 'pick_up_time2')


@admin.register(Wishlist_DB)
class Wishlist_DBModelAdmin(admin.ModelAdmin):
    list_display= ('id', 'buyer_id', 'seller_id', 'product_id', 'created_at')


@admin.register(Blogs_DB)
class Blogs_DBModelAdmin(admin.ModelAdmin):
    list_display= ('id', 'author', 'heading', 'created_at')

@admin.register(Detailed_blogs_DB)
class Blogs_DBModelAdmin(admin.ModelAdmin):
    list_display= ('id','heading', 'created_at')


@admin.register(productCategory)
class productCategoryModelAdmin(ImportExportModelAdmin):
    list_display= ('id', 'name', 'app_name', 'desc', 'image')


@admin.register(HomePage_Poster_Brands)
class HomePage_Poster_BrandsModelAdmin(ImportExportModelAdmin):
    list_display= ('id', 'name', 'choice', 'status', 'image')
    list_filter = ['choice', 'status']


@admin.register(Purchase_Process_DP)
class Purchase_Process_DPModelAdmin(ImportExportModelAdmin):
    list_display= ('id', 'user_id', 'product_id', 'quantity', 'price')

@admin.register(test_image)
class test_imageModelAdmin(ImportExportModelAdmin):
    list_display= ('id', 'image')  

@admin.register(buyer_returned_products)
class buyer_returned_productsModelAdmin(ImportExportModelAdmin):
    list_display= ('id', 'buyer', 'shipment_type')  

@admin.register(return_images)
class return_imagesModelAdmin(ImportExportModelAdmin):
    list_display= ('id', 'return_item')  



#--------------------------------------------------------------------------------------------------------------------------
# Contributed by Ashutosh Tiwari
class clientsfld(ImportExportModelAdmin):
    search_fields=('client_name','order_quantity','order_location',)
    list_display = ('client_name','order_quantity','order_location')

class Tagfld(ImportExportModelAdmin):
    search_fields=('name','parent_tag',)
    list_display = ('name','parent_tag','have_branch')

admin.site.register(MesasgeToSupplier)
admin.site.register(clientreview)
admin.site.register(Tag,Tagfld)
admin.site.register(topclients,clientsfld)
admin.site.register(DealsProductsInfo)