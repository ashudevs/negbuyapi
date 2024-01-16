from types import TracebackType
from django.db import models
from traitlets import default

from negbuy import settings
from django.utils import timezone


class userDB(models.Model):
    user_roles = (("Seller", "Seller"), ("Buyer", "Buyer"), ("Admin", "Admin"))
    gender_choices = (("Male", "Male"), ("Female", "Female"))
    user_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(
        max_length=50, choices=gender_choices, null=True, blank=True
    )
    profile_picture = models.ImageField(
        upload_to="profile_images",
        default="/profile_images/default.jpg",
        blank=True,
        null=True,
    )
    phone = models.CharField(max_length=100, null=True, blank=True, unique=True)
    role = models.CharField(max_length=50, choices=user_roles, default="Buyer")
    auth = models.BooleanField(default=True)
    seller_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True, unique=True)
    company = models.CharField(max_length=1000, null=True, blank=True)
    address_verified = models.BooleanField(default=False)
    document_verification = models.ImageField(
        upload_to="Documents_images", null=True, blank=True
    )
    gst_number = models.CharField(max_length=100, null=True, blank=True)
    telephone = models.CharField(max_length=100, null=True, blank=True)
    address_line1 = models.CharField(max_length=1000, null=True, blank=True)
    address_line2 = models.CharField(max_length=1000, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    countrycode = models.CharField(max_length=2, null=True, blank=True)
    state = models.CharField(
        max_length=100, null=True, blank=True
    )  # New Field added on 27 June 2022
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    search_count = models.IntegerField(default=0)
    recently_viewed_products = models.ManyToManyField("ProductDB", null=True, blank=True)

    def __str__(self):
        return f"{self.seller_name}   |   {self.phone}"

    class Meta:
        verbose_name_plural = "Users"


class productCategory(models.Model):
    name = models.CharField(max_length=50)
    app_name = models.CharField(max_length=50, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to="category_images", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Category"


# class productInventory(models.Model):
#     quantity = models.PositiveIntegerField(null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now=True)
#     deleted_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return "Inventory: " + str(self.id) + " --- Capacity: " + str(self.quantity)

#     class Meta:
#         verbose_name_plural = "Inventory"

class ProductDB(models.Model):
    status_choice = (
        ("draft", "draft"),
        ("verified", "verified"),
        ("under verification", "under verification"),
        ("rejected", "rejected"),
        ("deleted", "deleted"),
    )
    price_choices = (
        ("Add Price", "Add Price"),
        ("Price according to quantity", "Price according to quantity"),
    )

    seller_id = models.ForeignKey(
        userDB, on_delete=models.SET_NULL, null=True, blank=True
    )
    main_sku_id = models.CharField(max_length=100, null=True, blank=True)
    product_title = models.CharField(max_length=1000, null=True, blank=True)
    category_id = models.ForeignKey(
        productCategory, on_delete=models.CASCADE, null=True, blank=True
    )
    subcategory = models.CharField(max_length=1000, null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)
    packing_address = models.TextField(null=True, blank=True)
    brand = models.CharField(max_length=500, null=True, blank=True)
    video = models.FileField(upload_to="product_videos", null=True, blank=True)
    detailed_description = models.TextField(null=True, blank=True)
    transportation_port = models.CharField(max_length=500, null=True, blank=True)
    verification_status = models.CharField(
        max_length=100, choices=status_choice, default="draft"
    )
    price_choice = models.CharField(
        max_length=100,
        choices=price_choices,
        default="Add Price",
        null=True,
        blank=True,
    )
    sale_startdate = models.CharField(max_length=1000, null=True, blank=True)
    sale_enddate = models.CharField(max_length=1000, null=True, blank=True)
    verify_reject_date = models.DateTimeField(null=True, blank=True)
    gst = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Product DB"

    def __str__(self):
        return str(self.id) + str(self.product_title)


class ProductImageDescription(models.Model):
    main_product_id = models.ForeignKey(ProductDB, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to="New_Images", null=True, blank=True)
    heading = models.CharField(max_length=1000, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Product Image Description"


class ProductDetails(models.Model):
    main_product_id = models.ForeignKey(ProductDB, on_delete=models.CASCADE, default=1)
    heading = models.CharField(max_length=1000, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Product Details"


class ProductColorVariations(models.Model):
    main_product_id = models.ForeignKey(ProductDB, on_delete=models.CASCADE, default=1)
    main_variant = models.BooleanField(default=False)
    color = models.CharField(max_length=500, null=True, blank=True)
    main_image = models.ImageField(
        upload_to="main_images", default=None, blank=True, null=True
    )

    class Meta:
        verbose_name_plural = "Product Color Variations"

    def __str__(self):
        return f"{self.color} | {self.main_product_id}"


class FileTest(models.Model):
    file = models.FileField(upload_to="uploads", null=True, blank=True)


class ProductExtraImages(models.Model):
    variant_id = models.ForeignKey(ProductColorVariations, on_delete=models.CASCADE, default=1)
    image = models.ImageField(
        upload_to="Product_images", default=None, blank=True, null=True
    )

    class Meta:
        verbose_name_plural = "Product Extra Images"


class ProductSizeVariations(models.Model):
    variant_id = models.ForeignKey(ProductColorVariations, on_delete=models.CASCADE, default=1)
    size = models.CharField(max_length=500, null=True, blank=True)
    mrp = models.FloatField(max_length=500, null=True, blank=True)
    selling_price = models.FloatField(max_length=500, null=True, blank=True)
    sale_price = models.FloatField(max_length=500, null=True, blank=True)
    weight = models.FloatField(max_length=500, null=True, blank=True)
    packing_details = models.TextField(max_length=10000, null=True, blank=True)
    dim_length = models.FloatField(null=True, blank=True)
    dim_width = models.FloatField(null=True, blank=True)
    dim_height = models.FloatField(null=True, blank=True)
    manufacturing_time = models.IntegerField(null=True, blank=True)
    max_order_quantity = models.CharField(max_length=500, null=True, blank=True)
    main_size = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Product Size Variations"

    def __str__(self):
        return f"{self.id} | {self.variant_id} | {self.size}"


class ProductBulkPurchaseDetails(models.Model):
    product_id = models.ForeignKey(ProductSizeVariations, on_delete=models.CASCADE, default=1)
    min_quantity = models.IntegerField(null=True, blank=True)
    max_quantity = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    manufacturing_time = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Product Bulk Purchase Details"


class ProductInventoryDB(models.Model):
    product_id = models.ForeignKey(ProductSizeVariations, on_delete=models.CASCADE, default=1)
    stock = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Product Inventory DB"


class ProductEditRemarks(models.Model):
    issue_status = (
        ("New", "New"),
        ("Updated", "Updated"),
        ("Resolved", "Resolved"),
        ("Unresolved", "Unresolved"),
        ("Rejected", "Rejected"),
    )
    seller_id = models.ForeignKey(
        userDB, on_delete=models.SET_NULL, null=True, blank=True
    )
    main_product_id = models.ForeignKey(ProductDB, on_delete=models.CASCADE, default=1)
    field_name = models.CharField(
        max_length=100, null=True, blank=True
    )  # the key or field whose value has to be changed
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=issue_status, default="New")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Product Edit Remarks"


class SubSkuIdDB(models.Model):
    product_id = models.OneToOneField(ProductSizeVariations, on_delete=models.CASCADE, default=1)
    sub_sku_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sub-SKU IDs"


class SellerNoticeBoard(models.Model):
    sender_choices = (("admin", "admin"), ("negbuy", "negbuy"), ("other", "other"))
    seller_id = models.ForeignKey(
        userDB, on_delete=models.SET_NULL, null=True, blank=True
    )
    subject = models.TextField()
    message = models.TextField()
    read = models.BooleanField(default=False)
    sender = models.CharField(max_length=15, choices=sender_choices, default="admin")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Seller Notice Board"


class BuyerNoticeBoard(models.Model):
    sender_choices = (("admin", "admin"), ("negbuy", "negbuy"), ("other", "other"))
    Buyer_id = models.ForeignKey(
        userDB, on_delete=models.SET_NULL, null=True, blank=True
    )
    subject = models.TextField()
    message = models.TextField()
    read = models.BooleanField(default=False)
    sender = models.CharField(max_length=15, choices=sender_choices, default="admin")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Buyer Notice Board"


def get_hrs():
    hrs = ((timezone.now()).astimezone(timezone.get_default_timezone())).strftime(
        "%I %p"
    )
    return str(
        [
            {
                "hrs": hrs,
                "browser": 0,
                "app": 0,
                "screen_time": 0,
                "searched_clicks": 0,
                "other_clicks": 0,
            }
        ]
    )


def get_day():
    weekday = ((timezone.now()).astimezone(timezone.get_default_timezone())).strftime(
        "%A"
    )
    return str(
        [
            {
                "day": weekday,
                "browser": 0,
                "app": 0,
                "screen_time": 0,
                "searched_clicks": 0,
                "other_clicks": 0,
            }
        ]
    )


def get_month():
    month = ((timezone.now()).astimezone(timezone.get_default_timezone())).strftime(
        "%B"
    )
    return str(
        [
            {
                "month": month,
                "browser": 0,
                "app": 0,
                "screen_time": 0,
                "searched_clicks": 0,
                "other_clicks": 0,
            }
        ]
    )


class ViewsTrackingDB(models.Model):
    main_product_id = models.OneToOneField(ProductDB, on_delete=models.CASCADE, default=1)
    total_searched_clicks = models.IntegerField(default=0)
    total_other_clicks = models.IntegerField(default=0)
    total_screen_time = models.FloatField(default=0)
    last_week_screen_time = models.FloatField(default=0)
    browser_views = models.IntegerField(default=0)
    app_views = models.IntegerField(default=0)
    hourly_views = models.TextField(default=get_hrs)
    daily_views = models.TextField(default=get_day)
    monthly_views = models.TextField(default=get_month)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Views Tracking DB"


# class Orders_Id(models.Model):

#     TRUE_FALSE_CHOICES = (
#     (True, 'Yes'),
#     (False, 'No')
# )
#     ORDER_ID = models.CharField(max_length=200,blank=True, null=True, unique=True)
#     CURRENCY =models.CharField(max_length=200,blank=True, null=True)
#     GATEWAYNAME = models.CharField(max_length=200,blank=True, null=True)
#     TXNID = models.CharField(max_length=200,blank=True, null=True)
#     RESPMSG = models.CharField(max_length=200,blank=True, null=True)
#     BANKNAME = models.CharField(max_length=200,blank=True, null=True)
#     MID = models.CharField(max_length=200,blank=True, null=True)
#     User_Id = models.CharField(max_length=200,blank=True, null=True)
#     Username = models.CharField(max_length=200,blank=True, null=True)
#     Mobile = models.BigIntegerField(blank=True, null=True)
#     Email = models.EmailField(max_length=200,blank=True, null=True)
#     Address = models.CharField(max_length=1000,blank=True, null=True)
#     Date_Time = models.DateTimeField(auto_now_add=True)
#     Payment_Status = models.BooleanField(choices=TRUE_FALSE_CHOICES,default=False,blank=True, null=True)
#     TXNAMOUNT = models.FloatField(blank=True, null=True)
#     Refund_Amount = models.PositiveSmallIntegerField(default=0,blank=True, null=True)
#     Product_Name = models.CharField(max_length=130,blank=True, null=True)
#     Checksum = models.CharField(max_length = 1000, null= True, blank=True)
#     #payment_mode = models.CharField(max_length = 1000, null= True, blank=True)
#     BANKTXNID =models.CharField(max_length=200,blank=True, null=True)
#     STATUS =  models.CharField(max_length=100, null= True, blank=True)
#     TXNDATE = models.CharField(max_length=250,blank=True, null=True)
#     CHANNEL_ID = models.CharField(max_length=250,blank=True, null=True)
#     txnToken= models.CharField(max_length=100, null= True, blank= True)

#     def __str__(self):
#         return self.ORDER_ID
#         # return self.Order_ID+' '+str(self.User_Id)


# class TransactionDB(models.Model):
#     status_choices = (
#         ('success', 'success'),
#         ('failed', 'failed'),
#         ('ongoing', 'ongoing')
#     )
#     buyer_id = models.ForeignKey(userDB, on_delete=models.SET_NULL, null=True, blank=True)
#     product_id = models.ForeignKey(ProductSizeVariations, on_delete=models.SET_NULL, null=True, blank=True)
#     order_id = models.ForeignKey(Orders_Id, to_field='ORDER_ID', on_delete=models.SET_NULL, null=True, blank=True)
#     payment_id = models.CharField(max_length=500, null=True, blank=True)
#     status = models.CharField(
#         max_length=100, choices=status_choices, null=True, blank=True)
#     total_amount = models.FloatField(null=True, blank=True)
#     discount = models.FloatField(null=True, blank=True)
#     delivery_charges = models.FloatField(null=True, blank=True)
#     amount_paid = models.FloatField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name_plural = "Transactions DB"


# class cart(models.Model):

#     status_choice = (
#         ('Running', 'Running'),
#         ('Completed', 'Completed'),
#     )

#     order_number = models.PositiveIntegerField(null=True, blank=False)
#     buyer_info = models.ForeignKey(userDB, on_delete=models.CASCADE)
#     product = models.ForeignKey(ProductDB, on_delete=models.CASCADE)
#     order_quantity = models.PositiveIntegerField(null=True, blank=True)
#     order_price = models.DecimalField(
#         null=True, blank=True, decimal_places=4, max_digits=12)
#     logistics_charges = models.DecimalField(
#         null=True, decimal_places=4, max_digits=12)
#     total_price = models.DecimalField(
#         null=True, blank=True, decimal_places=4, max_digits=12)
#     order_date = models.CharField(max_length=20, null=True, blank=True)
#     order_status = models.CharField(
#         max_length=1000, null=True, blank=True, choices=status_choice)
#     order_note = models.CharField(max_length=1000, null=True, blank=True)
#     billing_address = models.TextField(max_length=1000, null=True, blank=True)
#     billing_landmark = models.CharField(max_length=100, null=True, blank=True)
#     billing_zipcode = models.CharField(max_length=100, null=True, blank=True)
#     billing_city = models.CharField(max_length=1000, null=True, blank=True)
#     billing_state = models.CharField(max_length=1000, null=True, blank=True)
#     billing_country = models.CharField(max_length=1000, null=True, blank=True)
#     shipping_adress = models.TextField(max_length=1000, null=True, blank=True)
#     shipping_landmark = models.CharField(
#         max_length=100, null=True, blank=True)
#     shipping_zipcode = models.CharField(max_length=100, null=True, blank=True)
#     shipping_city = models.CharField(max_length=1000, null=True, blank=True)
#     shipping_state = models.CharField(max_length=1000, null=True, blank=True)
#     shipping_country = models.CharField(max_length=1000, null=True, blank=True)

#     class Meta:
#         verbose_name_plural = "Cart"


class bankDetail(models.Model):
    user = models.ForeignKey(
        userDB, on_delete=models.CASCADE, related_name="user_bankDetails"
    )
    accountName = models.CharField(max_length=1000, null=True, blank=True)
    accountNumber = models.CharField(max_length=1000, null=True, blank=True)
    accountIfsc = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Bank"


class port(models.Model):
    name = models.CharField(max_length=1000, null=True, blank=True)
    country = models.CharField(max_length=1000, null=True, blank=True)
    latitude = models.CharField(max_length=1000, null=True, blank=True)
    longitude = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Port"


class DDP_Orders_DB(models.Model):
    buyer_status_choices = (
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("On the Way", "On the Way"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
        ("Refunded", "Refunded"),
    )
    seller_status_choices = (
        ("Schedule Pick Up", "Schedule Pick Up"),
        ("Unshipped", "Unshipped"),
        ("Shipped", "Shipped"),
        ("Shipped - Arrived at Negbuy", "Shipped - Arrived at Negbuy"),
        ("Shipped - Shipped from Negbuy", "Shipped - Shipped from Negbuy"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    )
    payment_choices = (
        ("Wallet", "Wallet"),
        ("UPI", "UPI"),
        ("Debit Card", "Debit Card"),
        ("Credit Card", "Credit Card"),
        ("Net Baking", "Netbanking"),
    )
    is_same = (("True", "True"), ("False", "False"))
    ddp_buyer_id = models.ForeignKey(
        userDB,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ddp_buyer_id",
    )
    ddp_seller_id = models.ForeignKey(
        userDB,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ddp_seller_id", 
    )
    product_id = models.ForeignKey(
        ProductSizeVariations, on_delete=models.SET_NULL, null=True, blank=True
    )
    order_id = models.CharField(max_length=100, null=True, blank=True)
    buyer_status = models.CharField(
        max_length=20, choices=buyer_status_choices, default="Pending"
    )
    seller_status = models.CharField(
        max_length=30, choices=seller_status_choices, default="Unshipped"
    )
    product_price = models.FloatField(max_length=20)
    quantity = models.IntegerField(default=1)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(
        max_length=20, choices=payment_choices, null=True, blank=True
    )
    shipping_address = models.TextField(null=True, blank=True)
    billing_address = models.TextField(null=True, blank=True)
    is_ship_bill_add_same = models.CharField(
        max_length=10, choices=is_same, default=True
    )
    seller_shipped_on = models.DateTimeField(null=True, blank=True)
    arrived_at_negbuy = models.DateTimeField(null=True, blank=True)
    buyer_shipped_on = models.DateTimeField(null=True, blank=True)
    buyer_out_for_delivery = models.DateTimeField(null=True, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    company_courier_id = models.IntegerField(null=True, blank=True)
    company_courier_name = models.CharField(max_length=50, null=True, blank=True)
    expected_delivery_date = models.CharField(max_length=50, null=True, blank=True)
    transport_mode = models.CharField(max_length=10, null=True, blank=True)
    courier_charges = models.FloatField(null=True, blank=True)
    total_weight = models.IntegerField(null=True, blank=True)
    gst = models.FloatField(null=True, blank=True)
    service_charge = models.FloatField(null=True, blank=True)
    total_amount = models.FloatField(null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=50, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=50, null=True, blank=True)
    shiprocket_oder_id = models.CharField(max_length=50, null=True, blank=True)
    shiprocket_shipment_id = models.CharField(max_length=50, null=True, blank=True)
    awb_no = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "DDP Orders"


class Exwork_Orders_DB(models.Model):
    buyer_status_choices = (
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Confirmed", "Confirmed"),
        ("Ready For Pick Up", "Ready For Pick Up"),
        ("Picked Up", "Picked Up"),
        ("Cancelled", "Cancelled"),
        ("Refunded", "Refunded"),
    )
    seller_status_choices = (
        ("Pending", "Pending"),
        ("Schedule Pick Up", "Schedule Pick Up"),
        ("Unshipped", "Unshipped"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    )
    payment_choices = (
        ("Wallet", "Wallet"),
        ("UPI", "UPI"),
        ("Debit Card", "Debit Card"),
        ("Credit Card", "Credit Card"),
        ("Net Baking", "Netbanking"),
    )
    is_same = (("True", "True"), ("False", "False"))
    exwork_buyer_id = models.ForeignKey(
        userDB,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="exwork_buyer_id",
    )
    exwork_seller_id = models.ForeignKey(
        userDB,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="exwork_seller_id",
    )
    product_id = models.ForeignKey(
        ProductSizeVariations, on_delete=models.SET_NULL, null=True, blank=True
    )
    order_id = models.CharField(max_length=100, null=True, blank=True)
    buyer_status = models.CharField(
        max_length=20, choices=buyer_status_choices, default="Pending"
    )
    seller_status = models.CharField(
        max_length=20, choices=seller_status_choices, default="Pending"
    )
    product_price = models.FloatField(max_length=20)
    quantity = models.IntegerField(default=1)
    docket_number = models.CharField(max_length=100, null=True, blank=True)
    docket_file = models.FileField(
        upload_to="exwork-logistics-doc", blank=True, null=True
    )
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    payment_method = models.CharField(
        max_length=20, choices=payment_choices, blank=True, null=True
    )
    shipping_address = models.TextField(null=True, blank=True)
    billing_address = models.TextField(null=True, blank=True)
    is_ship_bill_add_same = models.CharField(
        max_length=10, choices=is_same, default=True
    )
    pincode = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    transport_mode = models.CharField(max_length=10, null=True, blank=True)
    total_weight = models.IntegerField(null=True, blank=True)
    gst = models.FloatField(null=True, blank=True)
    service_charge = models.FloatField(null=True, blank=True)
    total_amount = models.FloatField(null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=50, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=50, null=True, blank=True)
    seller_shipped_on = models.DateTimeField(null=True, blank=True)
    arrived_at_negbuy = models.DateTimeField(null=True, blank=True)
    expected_delivery_date = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Ex-Work Orders"


class Pick_Up_Schedules(models.Model):
    ddp_order_id = models.OneToOneField(
        DDP_Orders_DB, on_delete=models.CASCADE, null=True, blank=True
    )
    exwork_order_id = models.OneToOneField(
        Exwork_Orders_DB, on_delete=models.CASCADE, null=True, blank=True
    )
    weight = models.CharField(max_length=20, null=True, blank=True)
    dim_lenght = models.CharField(max_length=20, null=True, blank=True)
    dim_width = models.CharField(max_length=20, null=True, blank=True)
    dim_height = models.CharField(max_length=20, null=True, blank=True)
    pick_up_time1 = models.DateTimeField(null=True, blank=True)
    pick_up_time2 = models.DateTimeField(null=True, blank=True)


# class orders(models.Model):

#     status_choice = (
#         ('Running', 'Running'),
#         ('Completed', 'Completed'),
#     )

#     order_number = models.CharField(max_length=1000, null=True, blank=True)
#     order_date = models.DateTimeField(auto_now=True, null=True)
#     order_time = models.TimeField(auto_now_add=False, null=True)
#     user = models.ForeignKey(userDB, on_delete=models.CASCADE)
#     product_id = models.ForeignKey(ProductSizeVariations, on_delete=models.CASCADE)
#     order_quantity = models.CharField(max_length=1000, null=True, blank=True)
#     shipping_date = models.CharField(max_length=1000, null=True, blank=True)
#     delivery_date = models.CharField(max_length=1000, null=True, blank=True)
#     # in future choice fields
#     status = models.CharField(
#         max_length=1000, null=True, blank=True, choices=status_choice)
#     feedback = models.TextField(max_length=1000, null=True, blank=True)
#     order_note = models.CharField(max_length=1000, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True, null=True)
#     modified_at = models.DateTimeField(auto_now=True, null=True)

#     def __str__(self):
#         return str(self.user)

#     class Meta:
#         verbose_name_plural = "Orders"


# class contact_data(models.Model):
#     message = models.CharField(max_length=1000, blank=True, null=True)

#     class Meta:
#         verbose_name_plural = "Contact Data"


class primary_category(models.Model):
    name = models.CharField(max_length=1000, blank=True, null=True)
    prod_category = models.ManyToManyField("productCategory")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Primary Category"


class review_db(models.Model):
    rating_choices = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    user = models.ForeignKey(userDB, on_delete=models.CASCADE)
    main_product_id = models.ForeignKey(ProductDB, on_delete=models.CASCADE, default=1)
    review_title = models.CharField(max_length=1000, blank=True, default=None)
    review_description = models.CharField(max_length=1000, blank=True, default=None)
    rating = models.IntegerField(null=True, blank=True, choices=rating_choices)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = "Product Reviews"


class Review_Images_DB(models.Model):
    review_id = models.ForeignKey(review_db, on_delete=models.CASCADE)
    file = models.FileField(upload_to="product_review_files", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Review Images and Videos"


# class Inventory(models.Model):
#     product = models.ForeignKey(
#         product, on_delete=models.CASCADE, related_name='inventory_product')
#     quantity = models.PositiveIntegerField(null=True, blank=True)
#     color = models.CharField(max_length=1000, null=True, blank=True)
#     size = models.CharField(max_length=1000, null=True, blank=True)

#     class Meta:
#         verbose_name_plural = "Inventory"


class rfq(models.Model):
    status_choices = (
        ("ongoing", "ongoing"),
        ("closed", "closed"),
        ("completed", "completed"),
    )
    rfq_acc_choices = (
        ("pending", "pending"),
        ("accepted", "accepted"),
        ("rejected", "rejected"),
    )
    user = models.ForeignKey(userDB, on_delete=models.CASCADE)
    requirement = models.CharField(max_length=1000, blank=True, null=True)
    target_price = models.IntegerField(blank=True, null=True)
    quantity = models.CharField(max_length=1000, blank=True, null=True)
    delivery_expected_date = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=status_choices, default="ongoing")
    rfq_status = models.CharField(
        max_length=20, choices=rfq_acc_choices, default="pending"
    )
    reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "RFQs"


class SellerRfqReply(models.Model):
    seller_id = models.ForeignKey(
        userDB, on_delete=models.SET_NULL, null=True, blank=True
    )
    rfq_id = models.ForeignKey(rfq, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to="rfq_reply_files", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Seller RFQ Reply"


# class ExcelFileUpload(models.Model):
#     excel_file_upload = models.FileField(upload_to='excel')


# class newsPost(models.Model):
#     image = models.ImageField(upload_to='NewsPost_Images', default=None, blank=True)
#     heading = models.CharField(max_length=100, null=True, blank=True)
#     desc = models.CharField(max_length=999, null=True, blank=True)

#     def __str__(self):
#         return self.heading


# class teamSection(models.Model):
#     image = models.ImageField(upload_to='Team_Images', default=None, blank=True)
#     name = models.CharField(max_length=100,null= True, blank = True)
#     designation = models.CharField(max_length=150, null =True, blank=True)
#     bio = models.CharField(max_length=500, null= True, blank= True)

#     def __str__(self):
#         return self.name


# class Courierdb(models.Model):
#     uniqueid = models.CharField(max_length=200, null= True, blank = True)
#     user = models.ForeignKey(userDB, on_delete=models.CASCADE, null=True)
#     prod = models.ForeignKey(ProductDB, on_delete=models.CASCADE, null = True)
#     courierid = models.CharField(max_length=100, null= True, blank=True)
#     couriername = models.CharField(max_length=200, null=True, blank= True)
#     deliveryCharge = models.DecimalField(
#         max_digits=12, decimal_places=2, null=True, blank=True)
#     quantity = models.CharField(max_length=100, null=True, blank=True)

#     def __str__(self):
#         return str(self.user)

# class transDB(models.Model):
#     seller = models.ForeignKey(userDB, on_delete=models.CASCADE, null=True)
#     month = models.CharField(max_length=100000, null=True, blank=True)
#     year = models.CharField(max_length=100000, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True, null=True)
#     units_sold = models.CharField(max_length=100000, null=True, blank=True, default = 0)
#     total_revenue = models.CharField(max_length=100000, null=True, blank=True)

#     def __str__(self):
#         return str(self.seller)

#     class Meta:
#         verbose_name_plural = "Transaction DB"

# class sellerAnalytics(models.Model):
#     seller = models.ForeignKey(userDB, on_delete=models.CASCADE, null=True)
#     day = models.CharField(max_length=100000, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True, null=True)
#     date = models.CharField(max_length=100000, null=True, blank=True)
#     checked_count = models.IntegerField(default=0)
#     search_count = models.IntegerField(default=0)

#     class Meta:
#         verbose_name_plural = "Seller Analytics DB"

# class TimeManagement(models.Model):
#     seller = models.ForeignKey(userDB, on_delete=models.CASCADE, null=True)
#     prod = models.ForeignKey(ProductDB, on_delete= models.CASCADE, null=True,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True, null=True)
#     date = models.CharField(max_length=100000, null=True, blank=True)
#     day = models.CharField(max_length=100000, null=True, blank=True)
#     year =models.CharField(max_length=100000, null=True, blank=True)
#     time = models.IntegerField(default= 0)

#     class Meta:
#         verbose_name_plural = "Time Analytics DB"

#     def __str__(self):
#         return f"{self.seller} | {self.time}"

# class Razorpay(models.Model):
#     user = models.ForeignKey(userDB, on_delete=models.CASCADE, null=True)
#     prod = models.ForeignKey(ProductDB, on_delete= models.CASCADE, null=True,blank=True)
#     order_id = models.CharField(max_length=200,blank=True, null=True)
#     currency =models.CharField(max_length=200,blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True, null=True)
#     amount = models.FloatField(null= True, blank=True)
#     unique_id = models.CharField(max_length =100, null=True, blank=True)
#     signature = models.CharField(max_length = 300,null=True, blank=True)
#     payment_id = models.CharField(max_length = 100, null=True, blank=True)
#     paid = models.BooleanField(null=True, blank=True, default = False)


class Negbuy_Warehouse(models.Model):
    address = models.TextField(null=True, blank=True)
    # ashutosh
    warehouse_image1 = models.ImageField(upload_to="ware_house_img", null=True, blank=True)
    warehouse_image2 = models.ImageField(upload_to="ware_house_img", null=True, blank=True)
    warehouse_image3 = models.ImageField(upload_to="ware_house_img", null=True, blank=True)
    warehouse_image4 = models.ImageField(upload_to="ware_house_img", null=True, blank=True)
    warehouse_image5 = models.ImageField(upload_to="ware_house_img", null=True, blank=True)
    warehouse_image6 = models.ImageField(upload_to="ware_house_img", null=True, blank=True)
    warehouse_image7 = models.ImageField(upload_to="ware_house_img", null=True, blank=True)
    warehouse_image8 = models.ImageField(upload_to="ware_house_img", null=True, blank=True)
    warehouse_image9 = models.ImageField(upload_to="ware_house_img", null=True, blank=True)
    store_manager_details = models.CharField(max_length=255, null=True, blank=True)
    contact_number = models.CharField(max_length=100, null=True, blank=True)
    employee_id = models.CharField(max_length=255,null=True,blank=True)
    person_profile_img = models.ImageField(upload_to="warehouse_personal_profile", null=True,blank=True)
    store_manager_id_proof = models.ImageField(upload_to="warehouse_id_proof", null=True, blank=True)
    identification_type = models.CharField(max_length=255,null=True,blank=True)
    identification_number = models.CharField(max_length=255,null=True,blank=True)
    company_name = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    company_gst_number = models.CharField(max_length=255,null=True,blank=True)
    total_deliveries = models.IntegerField(null=True,blank=True)


    class Meta:
        verbose_name_plural = "Negbuy Warehouse"


class Wishlist_DB(models.Model):
    buyer_id = models.ForeignKey(
        userDB, on_delete=models.CASCADE, related_name="buyer_id"
    )
    seller_id = models.ForeignKey(
        userDB,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="seller_id",
    )
    product_id = models.ForeignKey(
        ProductDB,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlist DB"


class Blogs_DB(models.Model):
    image = models.ImageField(upload_to="blog_images", null=True, blank=True)
    heading = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.heading)
    
    class Meta:
        verbose_name_plural = "Blogs"

class Detailed_blogs_DB(models.Model):
    blog = models.ForeignKey(Blogs_DB,on_delete=models.CASCADE, related_name="Detailed_blogs")
    heading = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.heading)
    
    class Meta:
        verbose_name_plural = "Detailed_blogs"


class HomePage_Poster_Brands(models.Model):
    choices = (("brand", "brand"), ("poster", "poster"))
    statuses = (("active", "active"), ("inactive", "inactive"))
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to="homepage_brands_posters_images")
    choice = models.CharField(max_length=10, choices=choices)
    status = models.CharField(max_length=10, choices=statuses)

    class Meta:
        verbose_name_plural = "Brands and Posters for Homepage"


#####      Purchase_Process      ######


class Purchase_Process_DP(models.Model):
    options = (("ongoing", "ongoing"), ("failed", "failed"), ("success", "success"))
    act = (('active', 'active'), ('processing', 'processing'), ('done', 'done'))
    user_id = models.ForeignKey(
        userDB, on_delete=models.SET_NULL, null=True, blank=True
    )
    product_id = models.ForeignKey(
        ProductSizeVariations, on_delete=models.SET_NULL, null=True
    )
    quantity = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    order_type = models.CharField(max_length=10, null=True, blank=True)
    transport_mode = models.CharField(max_length=10, null=True, blank=True)
    delivery_address = models.TextField(null=True, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    company_courier_id = models.IntegerField(null=True, blank=True)
    company_courier_name = models.CharField(max_length=50, null=True, blank=True)
    courier_charges = models.FloatField(null=True, blank=True)
    estimated_delivery_days = models.IntegerField(null=True, blank=True)
    total_weight = models.IntegerField(null=True, blank=True)
    gst = models.FloatField(null=True, blank=True)
    service_charge = models.FloatField(null=True, blank=True)
    total_amount = models.FloatField(null=True, blank=True)
    payment_status = models.CharField(
        max_length=10, choices=options, null=True, blank=True
    )
    status = models.CharField(max_length=20, choices=act, default='active')
    razorpay_order_id = models.CharField(max_length=50, null=True, blank=True)
    razorpay_currency = models.CharField(max_length=50, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=50, null=True, blank=True)


class test_image(models.Model):
    image = models.ImageField(
        upload_to="test_images", null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "test_image"

class buyer_returned_products(models.Model):
    options = (("DDP","DDP"), ("Ex-work","Ex-work"))
    status_options = (("pending","pending"), ("returned","returned"), ("rejected","rejected"))

    buyer = models.ForeignKey(userDB, on_delete=models.CASCADE, null=True, blank=True)
    shipment_type = models.CharField(
        max_length=10, choices=options, null=True, blank=True
    )
    ddp_order = models.ForeignKey(DDP_Orders_DB, on_delete=models.CASCADE, null=True, blank=True)
    Exwork_order = models.ForeignKey(Exwork_Orders_DB, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=status_options, null=True, blank=True
    )
    action = models.CharField(max_length=100, null=True, blank=True)
    refund_amount = models.CharField(max_length=100, null=True, blank=True)
    reason = models.CharField(max_length=100, null=True, blank=True)
    breif_reason = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return (str(self.buyer )+ "    Shipment Type: " + self.shipment_type)
    
    class Meta:
        verbose_name_plural = "Buyer Returns"


class return_images(models.Model):
    return_item = models.ForeignKey(buyer_returned_products, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="return_images", null=True, blank=True)

    def __str__(self):
        return (str(self.return_item))
    
    class Meta:
        verbose_name_plural = "Buyer Returns Images"



# Ashutosh



class MesasgeToSupplier(models.Model):
    user_id = models.ForeignKey(userDB, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField( null=True, blank=True)
    checkbox = models.BooleanField(default=False)


class clientreview(models.Model):
    user_id = models.ForeignKey(userDB, on_delete=models.SET_NULL, null=True, blank=True)
    main_product_id = models.ForeignKey(ProductDB, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.FloatField(null = True)
    review_headline = models.CharField(max_length=255)
    written_review = models.TextField()
    image = models.ImageField(upload_to="review_images", null=True, blank= True)

    class Meta:
        verbose_name_plural = "Client's Review"
    
     
class Tag(models.Model):
    name = models.CharField(max_length=255)
    parent_tag = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    have_branch = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
class topclients(models.Model):
    
    client_name = models.CharField(max_length=255, null= True)
    order_quantity = models.IntegerField(null=False, blank=False)
    order_location = models.CharField(max_length=255, null= True)
    client_status = models.BooleanField(default=False)
    

    class Meta:
        verbose_name_plural = "Top Clients"
    
    def __str__(self):
        return self.client_name



class DealsProductsInfo(models.Model):
    main_product_id = models.ForeignKey(ProductDB, on_delete=models.CASCADE, null=True, blank=True)
    product_name = models.CharField(max_length=255)
    about_product = models.TextField(null=True,blank=True)
    
    class Meta:
        verbose_name_plural = "Deals of the day Products"
    def __str__(self):
        return self.product_name
    
    




