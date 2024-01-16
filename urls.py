from django.conf import settings
from django.conf.urls.static import static
from django.urls import path



from . import logistics

from . import payments, shiprocket, razorpay
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("api/login", views.login, name="negbuy_login"),
    path("api/seller_login", views.seller_login, name="negbuy_seller_login"),
    path("api/seller_signup", views.seller_signup, name="negbuy_seller_signup"),
    path("api/check_phone_status", views.check_phone_status, name="check_phone_status"),
    # path('api/product_info', views.product_info, name="product_info"),
    # path('api/product_upload_api', views.product_upload_api,
    #      name="product_upload_api"),
    # path('api/featured_product', views.featured_product_api,
    #      name="featured_product"),
    # path('api/fast_dispatch', views.fast_dispatch_api, name="fast_dispatch"),
    # path('api/ready_to_ship', views.ready_to_ship_api, name="ready_to_ship"),
    # path('api/customized_product', views.customized_product_api,
    #      name="customized_product"),
    # path('api/new_arrivals', views.new_arrivals_api, name="new_arrivals"),
    # path('api/top_selling', views.top_selling_api, name="top_selling"),
    # path('api/user_products', views.user_products_api, name="user_products"),
    # path('api/add_to_cart', views.add_to_cart, name="add_to_cart"),
    # path('api/remove_from_cart', views.remove_from_cart, name="remove_from_cart"),
    # path('api/my_cart', views.my_cart, name="my_cart"),
    path("api/verify_gst", views.verify_gst, name="verify_gst"),
    path("api/bank_details", views.bank_details, name="bank_details"),
    path("api/seller_details", views.seller_details, name="seller_details"),
    # path('api/search_category', views.search_category, name="search_category"),
    # path('api/get_ports', views.get_ports, name="get_ports"),
    # path('api/get_categories', views.get_categories, name="get_categories"),
    # path('api/get_orders', views.get_orders, name="get_orders"),
    # path('api/contactus', views.contactus_function, name="contactus_function"),
    # path('api/delete_product', views.delete_product, name="delete_product"),
    # path('api/product_detail', views.product_detail, name="product_detail"),
    # path('api/best_selling', views.best_selling, name="best_selling_product"),
    # path('api/hot_selling', views.hot_selling, name="hot_selling_product"),
    # path('api/categorized_product',
    #      views.categorized_product, name="product_category"),
    # path('api/read_json', views.read_json, name="read_json"),
    # path('api/add_ports', views.add_ports, name="add_ports"),
    # path('api/my_orders', views.my_orders, name="my_orders"),
    # path('api/order_history', views.order_history, name="order_history"),
    # path('api/order_note', views.order_note, name="order_note"),
    # path('api/order_details', views.order_details, name="order_details"),
    # path('api/read_csv', views.read_csv, name="read_csv"),
    # path('api/port_distance', views.port_distance, name="port_distance"),
    # path('api/post_review', views.post_review, name="post_review"),
    # #path('api/product_reviews', views.product_reviews, name="product_reviews"),
    # path('api/upload_product', views.upload_product, name="upload_product"),
    # path('api/video_upload', views.video_upload, name="video_upload"),
    # path('api/size_api', views.size_api),
    # path('api/update_inventory', views.update_inventory, name="update_inventory"),
    # path('api/get_inventory', views.get_inventory, name="get_inventory"),
    # path('api/db_rfq', views.db_rfq),
    # path('api/inventory_detail', views.inventory_detail, name="inventory_detail"),
    # path('api/all_products', views.AllProducts, name="all_products"), # fetch all products from DB
    # path('api/update_address', views.address_update_api, name="update_address"), # update address api
    # path('api/update_password', views.password_update_api, name="update_password"), # update password api
    # path('api/update_email', views.email_update_api, name="update_email"), # email update api
    # path('api/verify/<uidb64>/<new_email>/<token>', views.email_verify_api, name ='verify' ), # email verify api
    # path('api/distance_track', views.lat_long_location, name ='distance_track' ), # distance calculate api
    # path('api/create_rfq', views.rfq_create_api, name ='create_rfq' ), # RFQ Update API
    # path('api/payment', views.payment, name ='payment'), # payment
    # path('api/callback', views.callback, name ='callback'), # to receive callback response from paytm
    # path('api/transaction_status', views.transaction_api, name ='transaction_status'), # returns the details of transaction
    # path('api/reviews', views.reviews, name = 'reviews'), # Calculate reviews of the file
    # path('api/product_stats',views.product_review_stats, name='product_stats'),
    # path('api/review_stats', csrf_exempt(views.review_stats), name= 'review_stats'),
    # path('api/excel', views.ExportImportExcel.as_view()), # upload products in productDB
    path("api/privacy_policy", views.privacy_policy, name="privacy_policy"),
    path(
        "api/refund_cancellation", views.refund_cancellation, name="refund_cancellation"
    ),
    path("api/terms_of_service", views.terms_of_service, name="terms_of_service"),
    path("api/terms_of_use", views.terms_of_use, name="terms_of_use"),
    path("api/payment_flow", views.payment_flow, name="payment_flow"),
    # path('api/news', views.news, name="news"),
    # path('api/categories', views.categories, name="categories"),
    # path('api/aboutUS', views.aboutUS, name="aboutUS"),
    # path('api/product_api', views.product_api, name="product_api"),# search product api
    # path('api/Searchproductlist', views.Searchproductlist, name="Searchproductlist"),# search product api
    # path('api/product_search', csrf_exempt(views.Search), name="product_search"), # fetch serialized products
    # path('api/supplychain', csrf_exempt(views.supplychain), name="supplychain"), # fetch serialized products
    # path('api/seller_dashv1', csrf_exempt(views.seller_dashv1), name="seller_dashv1"),
    # path('api/seller_dashv2', csrf_exempt(views.seller_dashv2), name="seller_dashv2"),
    # path('api/product_screen_time', csrf_exempt(views.product_screen_time), name="product_screen_time"), # fetch serialized products
    # path('api/seller_analyticsV1', csrf_exempt(views.seller_analyticsV1), name="seller_analyticsV1"), # fetch serialized products
    # path('api/seller_analyticsV2', csrf_exempt(views.seller_analyticsV2), name="seller_analyticsV2"), # fetch serialized products
    # path('api/seller_analyticsV3', csrf_exempt(views.seller_analyticsV3), name="seller_analyticsV3"), # fetch serialized products
    # ########## payment urls ############
    # # InitiateTransactionAPI is common to generate txnToken
    # path('api/InitiateTransactionAPI',payments.InitiateTransactionAPI,name = "InitiateTransactionAPI"),
    # path('api/transactionStatusAPI', payments.transactionStatusAPI, name="transactionStatusAPI"),
    # path('api/CardprocessTransactionAPI', payments.CardprocessTransactionAPI, name="CardprocessTransactionAPI"),
    # path('api/WalletprocessTransactionAPI', payments.WalletprocessTransactionAPI, name="WalletprocessTransactionAPI"),
    # path('api/NetBankingprocessTransaction',payments.NetBankingprocessTransaction, name="NetBankingprocessTransaction"),
    # path('api/UPIprocessTransaction', payments.UPIprocessTransaction, name="UPIprocessTransaction"),
    # # Wallet Payment Urls
    # path('api/SendOtpAPI', payments.SendOtpAPI, name ='SendOtpAPI'), # send otp api
    # path('api/verifyOtpAPI', payments.verifyOtpAPI, name ='verifyOtpAPI'), # send otp api
    # # Card Payment Urls
    # path('api/fetchBinDetail', payments.fetchBinDetail, name ='fetchBinDetail'), # fetch type of card (Triggered as soon as user enters 6 digits of card)
    # path('api/CardPaymentAPI', payments.CardPaymentAPI, name = "CardPaymentAPI"), # Card detail receive and send response
    # # Net Banking Urls
    # path('api/FetchPaymentOptionsAPI',payments.FetchPaymentOptionsAPI, name="FetchPaymentOptionsAPI"),
    # path('api/FetchNBpaymentAPI', payments.FetchNBpaymentAPI, name="FetchNBpaymentAPI"), # to fetch more banks
    # path('api/NetBankingAPI', payments.NetBankingAPI, name="NetBankingAPI"), # To send response to frontend for processing the transaction
    # ##### UPI Payment Urls
    # path('api/UPIPayment', csrf_exempt(payments.UPIPayment), name = "UPIPayment"), # to be sent to the frontend
    # ######### RAZORPAY ###########
    # path('api/razorpayment', csrf_exempt(payments.razorpayment), name = "razorpayment"),
    # path('api/success', csrf_exempt(payments.callbackrazor), name = "callbackrazor"),
    # path('api/razorpay_transaction', csrf_exempt(payments.razorpay_transaction), name = "razorpay_transaction"),
    # ######## DHL #######
    # path('api/trackShipment', logistics.trackShipment, name="trackShipment"),
    # path('api/shipmentrates', logistics.shipmentrates, name="shipmentrates"),
    # path('api/createShipment', csrf_exempt(logistics.createShipment), name="createShipment"),
    # path('api/addressValidation',logistics.addressValidation, name='addressValidation'),
    # ######### SHIPROCKET ########
    path("api/SRauth", csrf_exempt(payments.SRauth), name="SRauth"),
    path("api/SRrates", payments.SRrates, name="SRrates"),
    path(
        "api/SRinternationalRates",
        payments.SRinternationalRates,
        name="SRinternationalRates",
    ),
    path("api/get_all_channels", shiprocket.get_all_channels, name="get_all_channels"),
    path(
        "api/create_custom_order",
        shiprocket.create_custom_order,
        name="create_custom_order",
    ),
    path("api/generate_AWB", shiprocket.generate_AWB, name="generate_AWB"),
    path("api/generate_pickup", shiprocket.generate_pickup, name="generate_pickup"),
    path(
        "api/generate_manifest", shiprocket.generate_manifest, name="generate_manifest"
    ),
    path("api/print_manifest", shiprocket.print_manifest, name="print_manifest"),
    path("api/generate_label", shiprocket.generate_label, name="generate_label"),
    path("api/generate_invoice", shiprocket.generate_invoice, name="generate_invoice"),
    path(
        "api/generate_auth_token",
        shiprocket.generate_auth_token,
        name="generate_auth_token",
    ),
    path(
        "api/domestic_couriers_available",
        shiprocket.domestic_couriers_available,
        name="domestic_couriers_available",
    ),
    path(
        "api/international_couriers_available",
        shiprocket.international_couriers_available,
        name="international_couriers_available",
    ),
    path("api/tracking_via_AWB", shiprocket.tracking_via_AWB, name="tracking_via_AWB"),
    # path('api/courierAPI', csrf_exempt(payments.courierAPI), name='courierAPI'),
    # path('api/courierAPIv2', csrf_exempt(payments.courierAPIv2), name='courierAPIv2'),
    # path('api/SRcreateorder', payments.SRcreateorder, name='SRcreateorder'),
    # path('api/generateAwbSR', csrf_exempt(payments.generateAwbSR), name='generateAwbSR'),
    ###########  ADMIN DASHBOARD #########
    path("api/admin_login", views.admin_login, name="admin_login"),
    path(
        "api/admin_dashboard_analytics",
        views.admin_dashboard_analytics,
        name="admin_dashboard_analytics",
    ),
    path(
        "api/admin_dashboard_user",
        views.admin_dashboard_user,
        name="admin_dashboard_user",
    ),
    path("api/admin_seller_list", views.admin_seller_list, name="admin_seller_list"),
    path("api/admin_view_profile", views.admin_view_profile, name="admin_view_profile"),
    path(
        "api/admin_view_product_details",
        views.admin_view_product_details,
        name="admin_view_product_details",
    ),
    path(
        "api/admin_product_update",
        views.admin_product_update,
        name="admin_product_update",
    ),
    path(
        "api/admin_verify_product",
        views.admin_verify_product,
        name="admin_verify_product",
    ),
    path(
        "api/admin_reject_product",
        views.admin_reject_product,
        name="admin_reject_product",
    ),
    path(
        "api/admin_pending_rfqs_page",
        views.admin_pending_rfqs_page,
        name="admin_pending_rfqs_page",
    ),
    path(
        "api/admin_pending_rfq_approve",
        views.admin_pending_rfq_approve,
        name="admin_pending_rfq_approve",
    ),
    path(
        "api/admin_undo_approved_rfqs",
        views.admin_undo_approved_rfqs,
        name="admin_undo_approved_rfqs",
    ),
    path(
        "api/admin_pending_rfq_reject",
        views.admin_pending_rfq_reject,
        name="admin_pending_rfq_reject",
    ),
    #####################  ADMIN RAISE ISSUES   #########################
    path("api/admin_raise_issue", views.admin_raise_issue, name="admin_raise_issue"),
    path(
        "api/admin_current_requests",
        views.admin_current_requests,
        name="admin_current_requests",
    ),
    path(
        "api/admin_pending_requests",
        views.admin_pending_requests,
        name="admin_pending_requests",
    ),
    path(
        "api/admin_issues_history",
        views.admin_issues_history,
        name="admin_issues_history",
    ),
    path(
        "api/admin_approve_updated_fields",
        views.admin_approve_updated_fields,
        name="admin_approve_updated_fields",
    ),
    path(
        "api/admin_re_raise_issue",
        views.admin_re_raise_issue,
        name="admin_re_raise_issue",
    ),
    path(
        "api/admin_product_detailpage_issues",
        views.admin_product_detailpage_issues,
        name="admin_product_detailpage_issues",
    ),
    path(
        "api/test_product_search", views.test_product_search, name="test_product_search"
    ),
    path(
        "api/test_search_suggest", views.test_search_suggest, name="test_search_suggest"
    ),
    ########      Seller       #################
    path("api/file_upload", views.file_upload, name="file_upload"),
    path(
        "api/show_category_dropdown_addnewproduct",
        views.show_category_dropdown_addnewproduct,
        name="show_category_dropdown_addnewproduct",
    ),
    path(
        "api/show_ports_dropdown", views.show_ports_dropdown, name="show_ports_dropdown"
    ),
    path(
        "api/show_subcategory_dropdown_addnewproduct",
        views.show_subcategory_dropdown_addnewproduct,
        name="show_subcategory_dropdown_addnewproduct",
    ),
    path(
        "api/seller_add_update_ProductDB_object",
        views.seller_add_update_ProductDB_object,
        name="seller_add_update_ProductDB_object",
    ),
    path(
        "api/seller_add_update_ProductDetails",
        views.seller_add_update_ProductDetails,
        name="seller_add_update_ProductDetails",
    ),
    path(
        "api/seller_add_update_ProductImageDescription_object",
        views.seller_add_update_ProductImageDescription_object,
        name="seller_add_update_ProductImageDescription_object",
    ),
    path(
        "api/seller_add_update_ProductColorVariations_object",
        views.seller_add_update_ProductColorVariations_object,
        name="seller_add_update_ProductColorVariations_object",
    ),
    path(
        "api/seller_add_update_ProductExtraImages",
        views.seller_add_update_ProductExtraImages,
        name="seller_add_update_ProductExtraImages",
    ),
    path(
        "api/seller_add_update_ProductSizeVariations",
        views.seller_add_update_ProductSizeVariations,
        name="seller_add_update_ProductSizeVariations",
    ),
    path(
        "api/seller_add_update_ProductBulkPurchaseDetails",
        views.seller_add_update_ProductBulkPurchaseDetails,
        name="seller_add_update_ProductBulkPurchaseDetails",
    ),
    path(
        "api/seller_submit_draft_product_for_verification",
        views.seller_submit_draft_product_for_verification,
        name="seller_submit_draft_product_for_verification",
    ),
    path(
        "api/seller_get_products", views.seller_get_products, name="seller_get_products"
    ),
    path(
        "api/seller_get_product_alldetails",
        views.seller_get_product_alldetails,
        name="seller_get_product_alldetails",
    ),
    path(
        "api/seller_current_issues",
        views.seller_current_issues,
        name="seller_current_issues",
    ),
    path(
        "api/seller_issues_history",
        views.seller_issues_history,
        name="seller_issues_history",
    ),
    path(
        "api/seller_update_remarked_field",
        views.seller_update_remarked_field,
        name="seller_update_remarked_field",
    ),
    path(
        "api/seller_inventory_details",
        views.seller_inventory_details,
        name="seller_inventory_details",
    ),
    path(
        "api/seller_inventory_update",
        views.seller_inventory_update,
        name="seller_inventory_update",
    ),
    path(
        "api/seller_allproducts_review",
        views.seller_allproducts_review,
        name="seller_allproducts_review",
    ),
    path(
        "api/seller_product_detailed_review",
        views.seller_product_detailed_review,
        name="seller_product_detailed_review",
    ),
    path(
        "api/seller_notice_board", views.seller_notice_board, name="seller_notice_board"
    ),
    ################################      Seller Profile      #########################
    path(
        "api/seller_profile_view", views.seller_profile_view, name="seller_profile_view"
    ),
    path(
        "api/seller_profile_update",
        views.seller_profile_update,
        name="seller_profile_update",
    ),
    path(
        "api/seller_analytics_margins_screen_time",
        views.seller_analytics_margins_screen_time,
        name="seller_analytics_margins_screen_time",
    ),
    path(
        "api/seller_analytics_margins_sold_products",
        views.seller_analytics_margins_sold_products,
        name="seller_analytics_margins_sold_products",
    ),
    path(
        "api/seller_analytics_margins_searched_clicks",
        views.seller_analytics_margins_searched_clicks,
        name="seller_analytics_margins_searched_clicks",
    ),
    path(
        "api/seller_analytics_margins_other_clicks",
        views.seller_analytics_margins_other_clicks,
        name="seller_analytics_margins_other_clicks",
    ),
    path(
        "api/seller_analytics_margins_last_7days_searched_clicks",
        views.seller_analytics_margins_last_7days_searched_clicks,
        name="seller_analytics_margins_last_7days_searched_clicks",
    ),
    path(
        "api/seller_analytics_margins_last_7days_other_clicks",
        views.seller_analytics_margins_last_7days_other_clicks,
        name="seller_analytics_margins_last_7days_other_clicks",
    ),
    path(
        "api/seller_analytics_margins_wishlist",
        views.seller_analytics_margins_wishlist,
        name="seller_analytics_margins_wishlist",
    ),
    path(
        "api/seller_profile_view", views.seller_profile_view, name="seller_profile_view"
    ),
    path(
        "api/seller_profile_view", views.seller_profile_view, name="seller_profile_view"
    ),
    path(
        "api/seller_profile_view", views.seller_profile_view, name="seller_profile_view"
    ),
    ################################ Seller DASHBOARD  ############################
    path(
        "api/seller_dashboard_navbar",
        views.seller_dashboard_navbar,
        name="seller_dashboard_navbar",
    ),
    path(
        "api/seller_dashboard_show_rfqs",
        views.seller_dashboard_show_rfqs,
        name="seller_dashboard_show_rfqs",
    ),
    path(
        "api/seller_dashboard_upload_quotation",
        views.seller_dashboard_upload_quotation,
        name="seller_dashboard_upload_quotation",
    ),
    path(
        "api/seller_dashboard_active_buyers_daily",
        views.seller_dashboard_active_buyers_daily,
        name="seller_dashboard_active_buyers_daily",
    ),
    path(
        "api/seller_dashboard_visit_ratio_weekly",
        views.seller_dashboard_visit_ratio_weekly,
        name="seller_dashboard_visit_ratio_weekly",
    ),
    path(
        "api/seller_dashboard_user_traffic_monthly",
        views.seller_dashboard_user_traffic_monthly,
        name="seller_dashboard_user_traffic_monthly",
    ),
    path(
        "api/seller_dashboard_total_screen_time",
        views.seller_dashboard_total_screen_time,
        name="seller_dashboard_total_screen_time",
    ),
    path(
        "api/seller_dashboard_messages_today",
        views.seller_dashboard_messages_today,
        name="seller_dashboard_messages_today",
    ),
    path(
        "api/seller_dashboard_messages_week",
        views.seller_dashboard_messages_week,
        name="seller_dashboard_messages_week",
    ),
    path(
        "api/seller_dashboard_messages_month",
        views.seller_dashboard_messages_month,
        name="seller_dashboard_messages_month",
    ),
    path(
        "api/seller_dashboard_sales_acc_to_category",
        views.seller_dashboard_sales_acc_to_category,
        name="seller_dashboard_sales_acc_to_category",
    ),
    path(
        "api/seller_dashboard_customer_satisfaction",
        views.seller_dashboard_customer_satisfaction,
        name="seller_dashboard_customer_satisfaction",
    ),
    path(
        "api/seller_dashboard_supply_chain_overview",
        views.seller_dashboard_supply_chain_overview,
        name="seller_dashboard_supply_chain_overview",
    ),
    path(
        "api/seller_dashboard_summary",
        views.seller_dashboard_summary,
        name="seller_dashboard_summary",
    ),
    path(
        "api/seller_profile_view", views.seller_profile_view, name="seller_profile_view"
    ),
    ################################ Seller My Orders Section   #################################
    path("api/seller_all_orders", views.seller_all_orders, name="seller_all_orders"),
    path(
        "api/seller_exwork_pending_orders",
        views.seller_exwork_pending_orders,
        name="seller_exwork_pending_orders",
    ),
    path(
        "api/seller_unshipped_orders",
        views.seller_unshipped_orders,
        name="seller_unshipped_orders",
    ),
    path(
        "api/seller_shipped_orders",
        views.seller_shipped_orders,
        name="seller_shipped_orders",
    ),
    path(
        "api/seller_delivered_orders",
        views.seller_delivered_orders,
        name="seller_delivered_orders",
    ),
    path(
        "api/seller_cancelled_orders",
        views.seller_cancelled_orders,
        name="seller_cancelled_orders",
    ),
    path(
        "api/seller_schedule_pick_up_page",
        views.seller_schedule_pick_up_page,
        name="seller_schedule_pick_up_page",
    ),
    path(
        "api/seller_schedule_pick_up",
        views.seller_schedule_pick_up,
        name="seller_schedule_pick_up",
    ),
    ###############################   Home Page   ##########################################
    path(
        "api/homepage_single_category_products",
        views.homepage_single_category_products,
        name="homepage_single_category_products",
    ),
    path("api/homepage_news", views.homepage_news, name="homepage_news"),
    path(
        "api/detailed_homepage_news",
        views.detailed_homepage_news,
        name="detailed_homepage_news",
    ),
    path("api/homepage_add_rfq", views.homepage_add_rfq, name="homepage_add_rfq"),
    path("api/get_all_rfq", views.get_all_rfq, name="get_all_rfq"),
    #################################    WISHLIST      ######################
    path(
        "api/add_product_to_wishlist",
        views.add_product_to_wishlist,
        name="add_product_to_wishlist",
    ),
    path(
        "api/remove_product_from_wishlist",
        views.remove_product_from_wishlist,
        name="remove_product_from_wishlist",
    ),
    path(
        "api/get_product_from_wishlist",
        views.get_product_from_wishlist,
        name="get_product_from_wishlist",
    ),
    ###############################      Buyer Profile        ##########################
    path("api/buyer_profile_page", views.buyer_profile_page, name="buyer_profile_page"),
    path(
        "api/buyer_profile_update",
        views.buyer_profile_update,
        name="buyer_profile_update",
    ),
    path(
        "api/buyer_send_email_verification_email",
        views.buyer_send_email_verification_email,
        name="buyer_send_email_verification_email",
    ),
    path(
        "api/verify/<uidb64>/<new_email>/<token>",
        views.buyer_email_verify_update,
        name="verify",
    ),
    path(
        "api/buyer_phone_number_update",
        views.buyer_phone_number_update,
        name="buyer_phone_number_update",
    ),
    path(
        "api/buyer_submit_docket_number",
        views.buyer_submit_docket_number,
        name="buyer_submit_docket_number",
    ),
    path(
        "api/buyer_returned_products",
        views.buyer_returned_products_function,
        name="buyer_returned_products_function",
    ),
    path(
        "api/buyer_submit_return_request",
        views.buyer_submit_return_request,
        name="buyer_submit_return_request",
    ),
    ############################      Show Categorywise Products       ####################
    path(
        "api/category_specific_products",
        views.category_specific_products,
        name="category_specific_products",
    ),
    ############################      Product Detailed Page       ####################
    path(
        "api/product_details_page",
        views.product_details_page,
        name="product_details_page",
    ),
    path(
        "api/product_details_page_head_desc_details",
        views.product_details_page_head_desc_details,
        name="product_details_page_head_desc_details",
    ),
    path(
        "api/product_details_page_img_desc",
        views.product_details_page_img_desc,
        name="product_details_page_img_desc",
    ),
    # path('api/product_details_page_variants_data', views.product_details_page_variants_data, name="product_details_page_variants_data"),
    path(
        "api/product_details_page_review_section",
        views.product_details_page_review_section,
        name="product_details_page_review_section",
    ),
    path(
        "api/product_details_page_review_analysis",
        views.product_details_page_review_analysis,
        name="product_details_page_review_analysis",
    ),
    path(
        "api/product_details_page_countrywise_reviews_piechart",
        views.product_details_page_countrywise_reviews_piechart,
        name="product_details_page_countrywise_reviews_piechart",
    ),
    path(
        "api/product_page_screen_time_update",
        views.product_page_screen_time_update,
        name="product_page_screen_time_update",
    ),
    ############################           Trackor Page          ##############################
    path(
        "api/get_city_state_country_with_pincode",
        views.get_city_state_country_with_pincode,
        name="get_city_state_country_with_pincode",
    ),
    path(
        "api/get_coordinates_for_globe",
        views.get_coordinates_for_globe,
        name="get_coordinates_for_globe",
    ),
    ############################             MY ORDERS         ###############################
    path("api/click_on_buy_now", views.click_on_buy_now, name="click_on_buy_now"),
    ############################      notification buyer      ####################
    path("api/buyer_notification", views.buyer_notification, name="buyer_notification"),
    ##########################             Purchase Process      #########################
    path("api/buyer_all_orders", views.buyer_all_orders, name="buyer_all_orders"),
    path("api/tracker_page_data", views.tracker_page_data, name="tracker_page_data"),
    path("api/payment_page", views.payment_page, name="payment_page"),
    path("api/exwork_pay_later", views.exwork_pay_later, name="exwork_pay_later"),
    path("api/ddp_callbackrazor", razorpay.ddp_callbackrazor, name="ddp_callbackrazor"),
    #########################           Razorpay          ###################
    path(
        "api/ddp_click_on_pay_now",
        razorpay.ddp_click_on_pay_now,
        name="ddp_click_on_pay_now",
    ),
    path("api/ddp_callbackrazor", razorpay.ddp_callbackrazor, name="ddp_callbackrazor"),
    path(
        "api/create_exwork_order",
        razorpay.create_exwork_order,
        name="create_exwork_order",
    ),
    path(
        "api/exwork_click_on_pay_now",
        razorpay.exwork_click_on_pay_now,
        name="exwork_click_on_pay_now",
    ),
    path(
        "api/exwork_callbackrazor",
        razorpay.exwork_callbackrazor,
        name="exwork_callbackrazor",
    ),
    path("api/Payment_success", razorpay.Payment_success, name="Payment_success"),
    ##############################       APIs dedicated for APP only       #################
    #################   HomePage APIs    #######
    path(
        "api/category_names_images",
        views.category_names_images,
        name="category_names_images",
    ),
    path(
        "api/homepage_recently_viewed_products",
        views.homepage_recently_viewed_products,
        name="homepage_recently_viewed_products",
    ),
    path(
        "api/homepage_posters_brands",
        views.homepage_posters_brands,
        name="homepage_posters_brands",
    ),
    path("api/subcategories", views.subcategories, name="subcategories"),
    ############################################    CRON  JOBS    ##############################
    path(
        "api/hourly_views_update", views.hourly_views_update, name="hourly_views_update"
    ),
    # path('api/fire_send_otp', views.fire_send_otp, name="fire_send_otp"),
    # path('api/fire_verify_otp', views.fire_verify_otp, name="fire_verify_otp"),
    path("api/send_image", views.send_image, name="send_image"),
    # -----------------------------------------------------------------------------------------------------------------------
    # Contributed by Ashutosh Tiwari
    
    path("api/send-message", views.MsgToSupp, name="MsgToSupplier"),
    path("api/client-review", views.ClientReview, name="ClientReview"),
    path("api/primary_tags/", views.primary_tags, name="primary_tags"),
    path("api/primary_tags/sub_tags/", views.sub_tags, name="sub_tags"),
    # path("api/save_data/", views.save_data, name = "save_data"),
    path('api/reset-password-request', views.reset_password_request, name='reset_password_request'),
    path('api/reset-password/<str:uid>/<str:token>/', views.forgot_password, name='change_password'),
    path('api/get-top-clients/', views.gettopclients, name = "get-top-clients"),
    path('api/deals-of-the-day/',views.DealsOfTheDay, name = "Deals of the product"),
    path('api/warehouse-details', views.get_ware_house_details, name=" Get ware house deatils"),
    path('api/color-category', views.get_distinct_colors_by_category, name="get_distinct_colors_by_category"),
    
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

