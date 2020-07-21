#
#    To run this skill, the minimum values you need configure are in INIT: bucketName, sandboxCustomerEmailId, and sellerId
#
#    A detailed list of attribute descriptions can be found here:
#    https://developer.amazon.com/docs/amazon-pay/amazon-pay-apis-for-alexa.html
#


# You must specify these values to run this skill
INIT = {
    'bucketName':                         'your-bucket',               # Required; Used for skill state management
    'sandboxCustomerEmailId':             'youremail@email.com',                       # Required*; If sandboxMode equals true;
    'sellerId':                           'ENTERSELLERID',                             # Required; Amazon Pay seller ID
}

# These attributes are used globally across US, EU, and JP
GLOBAL = {
    'paymentAction':                      'AuthorizeAndCapture',                      # Required; 'Authorize' or 'AuthorizeAndCapture'
    'sandboxMode':                        'true',                                     # Required*; Must be true for sandbox testing; Must be false to submit to certification & production
    'version':                            '2',                                        # Required;
    'payloadSetupType':                   'SetupAmazonPayRequest',                    # Required;
    'payloadChargeType':                  'ChargeAmazonPayRequest',                   # Required;
    'directiveType':                      'Connections.SendRequest',                  # Required;
    'directiveSetupName':                 'Setup',                                    # Required;
    'directiveChargeName':                'Charge',                                   # Required;
    'needAmazonShippingAddress':          'true',                                     # Optional; Must be boolean
    'transactionTimeout':                 0,                                          # Optional; The default and recommended value for Alexa transactions is 0
}

# These attributes will change based on your region ( US, EU, or JP )
REGIONAL = {
    'en-US': {
        'countryOfEstablishment':         'US',                                       # Required;
        'currencyCode':                   'USD',                                      # Required;
        'ledgerCurrency':                 'USD',                                      # Required;
        'checkoutLanguage':               'en_US',                                    # Optional; US must be en_US
        'customInformation':              '',                                         # Optional; Max 1024 chars
        'sellerAuthorizationNote':        'Billing Agreement Seller Note',            # Optional; Max 255 chars; In sandbox mode you can pass simulation strings. See utilities.js
        'sellerNote':                     'Thanks for donating with For A Cause',     # Optional; Max 1024 chars, visible on confirmation mails to buyers
        'sellerStoreName':                'For A Cause',                              # Optional; Documentation calls this out as storeName not sellerStoreName
        'softDescriptor':                 'For A Cause',                              # Optional; Max 16 chars; This value is visible on customers credit card statements
    }
}

#
#    The following strings DO NOT interact with Amazon Pay, they are here to augment the skill
#    Order Summary, Order Confirmation, Cancel and Refund Custom Intents are required for certification:
#    https://developer.amazon.com/docs/amazon-pay/certify-skill-with-amazon-pay.html
#

# CARD INFORMATION
storeURL                         = 'www.for-a-cause.net/'
logoURL                          = 'https://github.com/kmorawala/For-A-Cause/blob/master/Images/icon_108_A2Z.png'   # Required; your store url

# LAUNCH INTENT
#launchRequestWelcomeTitle        = 'Welcome to '+ REGIONAL[ 'en-US' ].sellerStoreName +'. '
#launchRequestWelcomeResponse     = launchRequestWelcomeTitle +'We have everything you need for the perfect shave.'
launchRequestQuestionResponse    = 'Are you interested in a starter kit, or refills?'

# NO INTENT
noIntentResponse                 = 'Okay. Do you want to order something else?'

# CART SUMMARY
cartSummaryCheckout              = ' Do you want to check out now?';
cartSummarySubscription          = ' Every 2 months, you’ll be charged 10 dollars for your refill.';
#cartSummaryResponse              = 'Your total for the '+ REGIONAL[ 'en-US' ].sellerStoreName +' donation is 10 dollars.<break time=".5s"/>'

# CANCEL & REFUND CONTACT DETAILS
storePhoneNumber                 = '1-234-567-8910'
storeEmail                       = 'help@for-a-cause.net'
storeEmailPhonetic               = 'help at for a cause dot net'

# REFUND INTENT - REQUIRED
refundOrderTitle                 = 'Refund Order Details'
#refundOrderIntentResponse        = 'To request a refund, email '+ storeEmailPhonetic +', or call us. I sent contact information to your Alexa app.'
refundOrderCardResponse          = 'Not completely happy with your order? We are here to help.\n To request a refund, contact us at '+ storePhoneNumber +' or email '+ storeEmail +'.'

# CANCEL INTENT - REQUIRED
cancelOrderTitle                 = 'Cancel Order Details'
#cancelOrderIntentResponse        = 'To request a cancellation, email '+ storeEmailPhonetic +', or call us. I sent contact information to your Alexa app.'
cancelOrderCardResponse          = 'Want to change or cancel your order? We are here to help.\n Contact us at '+ storePhoneNumber +' or email '+ storeEmail +'.'

# ORDER CONFIRMATION - REQUIRED
confirmationTitle                = 'Order Confirmation Details'
confirmationPlaceOrder           = 'Your order has been placed.'
#confirmationThanks               = 'Thanks for shaving with '+ REGIONAL[ 'en-US' ].sellerStoreName +'.'
#confirmationIntentResponse       = REGIONAL[ 'en-US' ].sellerStoreName + ' will email you when your order ships. Thanks for shaving with '+ REGIONAL[ 'en-US' ].sellerStoreName +'.'
confirmationItems                = 'Products: 1 {productType}'
confirmationTotal                = 'Total amount: ${productPrice}'
confirmationTracking             = 'Tracking number: 99999999999.'
#confirmationCardResponse         = confirmationPlaceOrder + '\n' + confirmationItems   + '\n' + confirmationTotal   + '\n' + confirmationThanks  + '\n' + storeURL

# ORDER TRACKER INTENT
orderTrackerTitle                = 'Order Status'
orderTrackerIntentResponse       = 'Your order shipped via Amazon, and delivery is estimated for this Friday. Check your order email for the tracking number.'
orderTrackerCardResponse         = 'Your order #99999 was shipped via Amazon and is estimated to arrive on Friday.\n You can check the status at any time using tracking number 99999999999.';

# HELP INTENT
helpCommandsIntentResponse       = 'To check order status, say where is my order. To cancel an order, say cancel order. To ask for a refund, say refund.'

# FALLBACK INTENT
#fallbackHelpMessage              = 'Hmm, I\'m not sure about that. ' + helpCommandsIntentResponse

# EXITSKILL INTENT
exitSkillResponse                = 'OK, bye for now'


#
#    The following strings are used to output errors to test the skill
#

# ERROR RESPONSE STRINGS
scope                            = 'payments:autopay_consent'    # Required; Used request permissions for Amazon Pay
enablePermission                 = 'To make purchases in this skill, you need to enable Amazon Pay and turn on voice purchasing. To help, I sent a card to your Alexa app.'
errorMessage                     = 'Merchant error occurred. '
errorUnknown                     = 'Unknown error occurred. '
errorStatusCode                  = 'Status code: '
errorStatusMessage               = ' Status message: '
errorPayloadMessage              = ' Payload message: '
errorBillingAgreement            = 'Billing agreement state is '
errorBillingAgreementMessage 	 = '. Reach out to the user to resolve this issue.'
authorizationDeclineMessage 	 = 'Your order was not placed and you have not been charged.'
debug                            = 'debug'


