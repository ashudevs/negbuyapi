import json
import requests
from rest_framework.decorators import api_view
from negbuy import settings
from .models import *
from rest_framework.response import Response
from datetime import datetime as dt

dhl_api_key = settings.DHL_API_KEY

@api_view(['POST','GET'])
def trackShipment(request):
    trackingNumber = request.data['trackingNumber']
    url = "https://api-eu.dhl.com/track/shipments"

    querystring = {
        "trackingNumber": trackingNumber
        }

    headers = {
        'Accept': 'application/json',
        'DHL-API-Key': dhl_api_key
        }

    response = requests.request('GET',url, headers=headers, params=querystring)

    json_data = json.loads(response.text)
    return Response(json_data)


@api_view(['POST','GET'])
def shipmentrates(request):

    url = "https://api-mock.dhl.com/mydhlapi/rates"

    querystring = {
        "accountNumber":"123456789",
        "originCountryCode":"CZ",
        "originCityName":"Prague",
        "originPostalCode":"14800",
        "destinationCountryCode":"CZ",
        "destinationCityName":"Prague",
        "originPostalCode":"14800",
        "weight":"5",
        "length":"15",
        "width":"10",
        "height":"5",
        "plannedShippingDate":"2020-02-26",
        "isCustomsDeclarable":"false",
        "unitOfMeasurement":"metric"
    }

    headers = {
        "Accept": "application/json",
        "Message-Reference": "d0e7832e-5c98-11ea-bc55-0242ac13",
        "Message-Reference-Date": "Wed, 21 Oct 2015 07:28:00 GMT",
        "Authorization": "Basic ZGVtby1rZXk6ZGVtby1zZWNyZXQ="
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    json_data = json.loads(response.text)
    return Response(json_data)



@api_view(['POST'])
def createShipment(request):
    # user_id = request.headers['User-id']
    # product_id = request.data['product_id']
    date = dt.now()
    # # today = date.today() ### for production
    # usr = userDB.objects.get(user_id=user_id)
    # prods = product.objects.get(id=product_id)
    # product_seller = prods.username.username
    # seller = userDB.objects.get(username=product_seller)
    # seller_city = seller.city
    # seller_country = seller.country
    

    url = "https://api-mock.dhl.com/mydhlapi/shipments"

    payload = {
        "plannedShippingDateAndTime": "2019-08-04T14:00:31GMT+01:00",
        "pickup": {
            "isRequested": False,
            "closeTime": "18:00",
            "location": "reception",
            "specialInstructions": [
                {
                    "value": "please ring door bell",
                    "typeCode": "TBD"
                }
            ],
            "pickupDetails": {
                "postalAddress": {
                    "postalCode": "14800",
                    "cityName": "Prague",
                    "countryCode": "CZ",
                    "provinceCode": "CZ",
                    "addressLine1": "V Parku 2308/10",
                    "addressLine2": "addres2",
                    "addressLine3": "addres3",
                    "countyName": "Central Bohemia",
                    "provinceName": "Central Bohemia",
                    "countryName": "Czech Republic"
                },
                "contactInformation": {
				"email": "that@before.de",
				"phone": "+1123456789",
				"mobilePhone": "+60112345678",
				"companyName": "Company Name",
				"fullName": "John Brew"
			},
                "registrationNumbers": [
                    {
                        "typeCode": "VAT",
                        "number": "CZ123456789",
                        "issuerCountryCode": "CZ"
                    }
                ],
                "bankDetails": [
                    {
                        "name": "Russian Bank Name",
                        "settlementLocalCurrency": "RUB",
                        "settlementForeignCurrency": "USD"
                    }
                ],
                "typeCode": "business"
            },
            "pickupRequestorDetails": {
                "postalAddress": {
                    "postalCode": "14800",
                    "cityName": "Prague",
                    "countryCode": "CZ",
                    "provinceCode": "CZ",
                    "addressLine1": "V Parku 2308/10",
                    "addressLine2": "addres2",
                    "addressLine3": "addres3",
                    "countyName": "Central Bohemia",
                    "provinceName": "Central Bohemia",
                    "countryName": "Czech Republic"
                },
                "contactInformation": {
                    "email": "that@before.de",
                    "phone": "+1123456789",
                    "mobilePhone": "+60112345678",
                    "companyName": "Company Name",
                    "fullName": "John Brew"
                },
                "registrationNumbers": [
                    {
                        "typeCode": "VAT",
                        "number": "CZ123456789",
                        "issuerCountryCode": "CZ"
                    }
                ],
                "bankDetails": [
                    {
                        "name": "Russian Bank Name",
                        "settlementLocalCurrency": "RUB",
                        "settlementForeignCurrency": "USD"
                    }
                ],
                "typeCode": "business"
            }
        },
        "productCode": "D",
        "localProductCode": "D",
        "getRateEstimates": False,
        "accounts": [
            {
                "typeCode": "shipper",
                "number": "123456789"
            }
        ],
        "valueAddedServices": [
            {
                "serviceCode": "II",
                "value": 100,
                "currency": "GBP",
                "method": "cash",
                "dangerousGoods": [
                    {
                        "contentId": "908",
                        "dryIceTotalNetWeight": 12,
                        "unCode": "UN-7843268473"
                    }
                ]
            }
        ],
        "outputImageProperties": {
            "printerDPI": 300,
            "customerBarcodes": [
                {
                    "content": "barcode content",
                    "textBelowBarcode": "text below barcode",
                    "symbologyCode": "93"
                }
            ],
            "customerLogos": [
                {
                    "fileFormat": "PNG",
                    "content": "base64 encoded image"
                }
            ],
            "encodingFormat": "pdf",
            "imageOptions": [
                {
                    "typeCode": "label",
                    "templateName": "ECOM26_84_001",
                    "isRequested": True,
                    "hideAccountNumber": False,
                    "numberOfCopies": 1,
                    "invoiceType": "commercial",
                    "languageCode": "eng",
                    "languageCountryCode": "br",
                    "encodingFormat": "png",
                    "renderDHLLogo": False,
                    "fitLabelsToA4": False,
                    "labelFreeText": "string",
                    "labelCustomerDataText": "string"
                }
            ],
            "splitTransportAndWaybillDocLabels": True,
            "allDocumentsInOneImage": True,
            "splitDocumentsByPages": True,
            "splitInvoiceAndReceipt": True,
            "receiptAndLabelsInOneImage": True
        },
        "customerReferences": [
            {
                "value": "Customer reference",
                "typeCode": "CU"
            }
        ],
        "identifiers": [
            {
                "typeCode": "shipmentId",
                "value": "1234567890",
                "dataIdentifier": "00"
            }
        ],
        "customerDetails": {
            "shipperDetails": {
                "postalAddress": {
                    "postalCode": "14800",
                    "cityName": "Prague",
                    "countryCode": "CZ",
                    "provinceCode": "CZ",
                    "addressLine1": "V Parku 2308/10",
                    "addressLine2": "addres2",
                    "addressLine3": "addres3",
                    "countyName": "Central Bohemia",
                    "provinceName": "Central Bohemia",
                    "countryName": "Czech Republic"
                },
                "contactInformation": {
                    "email": "that@before.de",
                    "phone": "+1123456789",
                    "mobilePhone": "+60112345678",
                    "companyName": "Company Name",
                    "fullName": "John Brew"
                },
                "registrationNumbers": [
                    {
                        "typeCode": "VAT",
                        "number": "CZ123456789",
                        "issuerCountryCode": "CZ"
                    }
                ],
                "bankDetails": [
                    {
                        "name": "Russian Bank Name",
                        "settlementLocalCurrency": "RUB",
                        "settlementForeignCurrency": "USD"
                    }
                ],
                "typeCode": "business"
            },
            "receiverDetails": {
                "postalAddress": {
                    "postalCode": "14800",
                    "cityName": "Prague",
                    "countryCode": "CZ",
                    "provinceCode": "CZ",
                    "addressLine1": "V Parku 2308/10",
                    "addressLine2": "addres2",
                    "addressLine3": "addres3",
                    "countyName": "Central Bohemia",
                    "provinceName": "Central Bohemia",
                    "countryName": "Czech Republic"
                },
                "contactInformation": {
                    "email": "that@before.de",
                    "phone": "+1123456789",
                    "mobilePhone": "+60112345678",
                    "companyName": "Company Name",
                    "fullName": "John Brew"
                },
                "registrationNumbers": [
                    {
                        "typeCode": "VAT",
                        "number": "CZ123456789",
                        "issuerCountryCode": "CZ"
                    }
                ],
                "bankDetails": [
                    {
                        "name": "Russian Bank Name",
                        "settlementLocalCurrency": "RUB",
                        "settlementForeignCurrency": "USD"
                    }
                ],
                "typeCode": "business"
            },
            "buyerDetails": {
                "postalAddress": {
                    "postalCode": "14800",
                    "cityName": "Prague",
                    "countryCode": "CZ",
                    "provinceCode": "CZ",
                    "addressLine1": "V Parku 2308/10",
                    "addressLine2": "addres2",
                    "addressLine3": "addres3",
                    "countyName": "Central Bohemia",
                    "provinceName": "Central Bohemia",
                    "countryName": "Czech Republic"
                },
                "contactInformation": {
                    "email": "buyer@domain.com",
                    "phone": "+44123456789",
                    "mobilePhone": "+42123456789",
                    "companyName": "Customer Company Name",
                    "fullName": "Mark Companer"
                },
                "registrationNumbers": [
                    {
                        "typeCode": "VAT",
                        "number": "CZ123456789",
                        "issuerCountryCode": "CZ"
                    }
                ],
                "bankDetails": [
                    {
                        "name": "Russian Bank Name",
                        "settlementLocalCurrency": "RUB",
                        "settlementForeignCurrency": "USD"
                    }
                ],
                "typeCode": "business"
            },
            "importerDetails": {
                "postalAddress": {
                    "postalCode": "14800",
                    "cityName": "Prague",
                    "countryCode": "CZ",
                    "provinceCode": "CZ",
                    "addressLine1": "V Parku 2308/10",
                    "addressLine2": "addres2",
                    "addressLine3": "addres3",
                    "countyName": "Central Bohemia",
                    "provinceName": "Central Bohemia",
                    "countryName": "Czech Republic"
                },
                "contactInformation": {
                    "email": "that@before.de",
                    "phone": "+1123456789",
                    "mobilePhone": "+60112345678",
                    "companyName": "Company Name",
                    "fullName": "John Brew"
                },
                "registrationNumbers": [
                    {
                        "typeCode": "VAT",
                        "number": "CZ123456789",
                        "issuerCountryCode": "CZ"
                    }
                ],
                "bankDetails": [
                    {
                        "name": "Russian Bank Name",
                        "settlementLocalCurrency": "RUB",
                        "settlementForeignCurrency": "USD"
                    }
                ],
                "typeCode": "business"
            },
            "exporterDetails": {
                "postalAddress": {
                    "postalCode": "14800",
                    "cityName": "Prague",
                    "countryCode": "CZ",
                    "provinceCode": "CZ",
                    "addressLine1": "V Parku 2308/10",
                    "addressLine2": "addres2",
                    "addressLine3": "addres3",
                    "countyName": "Central Bohemia",
                    "provinceName": "Central Bohemia",
                    "countryName": "Czech Republic"
                },
                "contactInformation": {
                    "email": "that@before.de",
                    "phone": "+1123456789",
                    "mobilePhone": "+60112345678",
                    "companyName": "Company Name",
                    "fullName": "John Brew"
                },
                "registrationNumbers": [
                    {
                        "typeCode": "VAT",
                        "number": "CZ123456789",
                        "issuerCountryCode":"CZ"
                    }
                ],
                "bankDetails": [
                    {
                        "name": "Russian Bank Name",
                        "settlementLocalCurrency": "RUB",
                        "settlementForeignCurrency": "USD"
                    }
                ],
                "typeCode": "business"
            },
            "sellerDetails": {
                "postalAddress": {
                    "postalCode": "14800",
                    "cityName": "Prague",
                    "countryCode": "CZ",
                    "provinceCode": "CZ",
                    "addressLine1": "V Parku 2308/10",
                    "addressLine2": "addres2",
                    "addressLine3": "addres3",
                    "countyName": "Central Bohemia",
                    "provinceName": "Central Bohemia",
                    "countryName": "Czech Republic"
                },
                "contactInformation": {
                    "email": "that@before.de",
                    "phone": "+1123456789",
                    "mobilePhone": "+60112345678",
                    "companyName": "Company Name",
                    "fullName": "John Brew"
                },
                "registrationNumbers": [
                    {
                        "typeCode": "VAT",
                        "number": "CZ123456789",
                        "issuerCountryCode": "CZ"
                    }
                ],
                "bankDetails": [
                    {
                        "name": "Russian Bank Name",
                        "settlementLocalCurrency": "RUB",
                        "settlementForeignCurrency": "USD"
                    }
                ],
                "typeCode": "business"
            },
            "payerDetails": {
                "postalAddress": {
                    "postalCode": "14800",
                    "cityName": "Prague",
                    "countryCode": "CZ",
                    "provinceCode": "CZ",
                    "addressLine1": "V Parku 2308/10",
                    "addressLine2": "addres2",
                    "addressLine3": "addres3",
                    "countyName": "Central Bohemia",
                    "provinceName": "Central Bohemia",
                    "countryName": "Czech Republic"
                },
                "contactInformation": {
                    "email": "that@before.de",
                    "phone": "+1123456789",
                    "mobilePhone": "+60112345678",
                    "companyName": "Company Name",
                    "fullName": "John Brew"
                },
                "registrationNumbers": [
                    {
                        "typeCode": "VAT",
                        "number": "CZ123456789",
                        "issuerCountryCode": "CZ"
                    }
                ],
                "bankDetails": [
                    {
                        "name": "Russian Bank Name",
                        "settlementLocalCurrency": "RUB",
                        "settlementForeignCurrency": "USD"
                    }
                ],
                "typeCode": "business"
            }
        },
        "content": {
            "packages": [
                {
                    "typeCode": "2BP",
                    "weight": 22.501,
                    "dimensions": {
                        "length": 15.001,
                        "width": 15.001,
                        "height": 40.001
                    },
                    "customerReferences": [
                        {
                            "value": "Customer reference",
                            "typeCode": "CU"
                        }
                    ],
                    "identifiers": [
                        {
                            "typeCode": "shipmentId",
                            "value": "1234567890",
                            "dataIdentifier": "00"
                        }
                    ],
                    "description": "Piece content description",
                    "labelBarcodes": [
                        {
                            "position": "left",
                            "symbologyCode": "93",
                            "content": "string",
                            "textBelowBarcode": "text below left barcode"
                        }
                    ],
                    "labelText": [
                        {
                            "position": "left",
                            "caption": "text caption",
                            "value": "text value"
                        }
                    ],
                    "labelDescription": "bespoke label description"
                }
            ],
            "isCustomsDeclarable": True,
            "declaredValue": 150,
            "declaredValueCurrency": "CZK",
            "exportDeclaration": {
                "lineItems": [
                    {
                        "number": 1,
                        "description": "line item description",
                        "price": 150,
                        "quantity": {
                            "value": 1,
                            "unitOfMeasurement": "BOX"
                        },
                        "commodityCodes": [
                            {
                                "typeCode": "outbound",
                                "value": "HS1234567890"
                            }
                        ],
                        "exportReasonType": "permanent",
                        "manufacturerCountry": "CZ",
                        "exportControlClassificationNumber": "US123456789",
                        "weight": {
                            "netValue": 10,
                            "grossValue": 10
                        },
                        "isTaxesPaid": True,
                        "additionalInformation": ["string"],
                        "customerReferences": [
                            {
                                "typeCode": "AFE",
                                "value": "custref123"
                            }
                        ],
                        "customsDocuments": [
                            {
                                "typeCode": "972",
                                "value": "custdoc456"
                            }
                        ]
                    }
                ],
                "invoice": {
                    "number": "12345-ABC",
                    "date": "2020-03-18",
                    "signatureName": "Brewer",
                    "signatureTitle": "Mr.",
                    "signatureImage": "Base64 encoded image",
                    "instructions": ["string"],
                    "customerDataTextEntries": ["string"],
                    "totalNetWeight": 999999999999,
                    "totalGrossWeight": 999999999999,
                    "customerReferences": [
                        {
                            "typeCode": "CU",
                            "value": "custref112"
                        }
                    ],
                    "termsOfPayment": "100 days"
                },
                "remarks": [{"value": "declaration remark"}],
                "additionalCharges": [
                    {
                        "value": 10,
                        "caption": "fee",
                        "typeCode": "freight"
                    }
                ],
                "destinationPortName": "port details",
                "placeOfIncoterm": "port of departure or destination details",
                "payerVATNumber": "12345ED",
                "recipientReference": "recipient reference",
                "exporter": {
                    "id": "123",
                    "code": "EXPCZ"
                },
                "packageMarks": "marks",
                "declarationNotes": [{"value": "up to three declaration notes"}],
                "exportReference": "export reference",
                "exportReason": "export reason",
                "exportReasonType": "permanent",
                "licenses": [
                    {
                        "typeCode": "export",
                        "value": "license"
                    }
                ],
                "shipmentType": "personal",
                "customsDocuments": [
                    {
                        "typeCode": "972",
                        "value": "custdoc445"
                    }
                ]
            },
            "description": "shipment description",
            "USFilingTypeValue": "12345",
            "incoterm": "DAP",
            "unitOfMeasurement": "metric"
        },
        "documentImages": [
            {
                "typeCode": "INV",
                "imageFormat": "PDF",
                "content": "base64 encoded image"
            }
        ],
        "onDemandDelivery": {
            "deliveryOption": "servicepoint",
            "location": "front door",
            "specialInstructions": "ringe twice",
            "gateCode": "1234",
            "whereToLeave": "concierge",
            "neighbourName": "Mr.Dan",
            "neighbourHouseNumber": "777",
            "authorizerName": "Newman",
            "servicePointId": "SPL123",
            "requestedDeliveryDate": "2020-04-20"
        },
        "requestOndemandDeliveryURL": False,
        "shipmentNotification": [
            {
                "typeCode": "email",
                "receiverId": "receiver@email.com",
                "languageCode": "eng",
                "languageCountryCode": "UK",
                "bespokeMessage": "message to be included in the notification"
            }
        ],
        "prepaidCharges": [
            {
                "typeCode": "freight",
                "currency": "CZK",
                "value": 200,
                "method": "cash"
            }
        ],
        "getTransliteratedResponse": False,
        "estimatedDeliveryDate": {
            "isRequested": False,
            "typeCode": "QDDC"
        },
        "getAdditionalInformation": [
            {
                "typeCode": "pickupDetails",
                "isRequested": True
            }
        ],
        "parentShipment": {
            "productCode": "s",
            "packagesCount": 1
        }
    }
    headers = {
        "Accept": "application/json",
        "Message-Reference": "d0e7832e-5c98-11ea-bc55-0242ac13",
        "Message-Reference-Date": str(date),
        "Authorization": "Basic ZGVtby1rZXk6ZGVtby1zZWNyZXQ="
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    json_data = json.loads(response.text)
    return Response(json_data)

@api_view(['POST','GET'])
def addressValidation(request):

    url = "https://api-mock.dhl.com/mydhlapi/address-validate"

    querystring = {
        "type":"pickup",
        "countryCode":"CZ",
        "postalCode":"14800"
        }

    headers = {
        "Accept": "application/json",
        "Message-Reference": "d0e7832e-5c98-11ea-bc55-0242ac13",
        "Message-Reference-Date": "Wed, 21 Oct 2015 07:28:00 GMT",
        "Authorization": "Basic ZGVtby1rZXk6ZGVtby1zZWNyZXQ="
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    json_data = json.loads(response.text)
    return Response(json_data)

