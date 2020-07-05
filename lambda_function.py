# -*- coding: utf-8 -*-
"""Cause app."""

from ask_sdk_model.interfaces.connections import SendRequestDirective
import random
import logging
import json
# import os
# import boto3
from query_functions import query_next_item, get_item_count
# from query_functions import
from ask_sdk_core.skill_builder import (SkillBuilder, CustomSkillBuilder)
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard  # for devices with a screen
# data, utils, config, payload_builder, and directive_builder in a seperate file
from alexa import data, util, payload_builder, config, directive_builder
from ask_sdk_model.ui import AskForPermissionsConsentCard
# from ask_sdk_model.interfaces.amazonpay.model
# added for remembering attributes
import os
from ask_sdk_s3.adapter import S3Adapter
s3_adapter = S3Adapter(bucket_name=os.environ["S3_PERSISTENCE_BUCKET"])
# from ask_sdk_s3.adapter import S3Adapter #Importing S3Adapter if needed

# Create a skill builder
sb = CustomSkillBuilder(persistence_adapter=s3_adapter)
# sb = SkillBuilder()

# Create a logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Request Handler classes


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for skill launch or new search."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequestHandler")

        # storing persistance attributes and checking for id attributes
        attr = handler_input.attributes_manager.persistent_attributes
        attributes_are_present = ("id" in attr)

        # error checking
        if attributes_are_present:
            charity_id = attr['id']
        else:
            charity_id = 1

        max_charity_id = get_item_count("Animals")

        if charity_id > max_charity_id:
            charity_id = 1

        # DynamoDB query
        charity_name, charity_mission = query_next_item(charity_id, "Animals")
        # charity_name, charity_mission = query_next_item(2, "Animals")

        # checking if the item count function is working
        # item_count =
        # + "Item counts are " + item_count

        message = data.WELCOME_TEST_MESSAGE + \
            str(charity_id) + " " + charity_name + ". " + \
            "It's mission is " + charity_mission
        handler_input.response_builder.speak(message).ask(
            data.HELP_MESSAGE)

        # Increment the charity_id
        charity_id += 1

        # update and save persistent_attributes
        attr = {
            "id": charity_id
        }
        handler_input.attributes_manager.persistent_attributes = attr
        handler_input.attributes_manager.save_persistent_attributes()

        return handler_input.response_builder.response


class GetCharityInfoIntentHandler(AbstractRequestHandler):
    """Handler for providing charity information."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("GetCharityInfoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetCharityInfoHandler")

        charity_info = "info about the charity goes here"

        handler_input.response_builder.speak(charity_info).ask(
            data.REPROMPT_SPEECH).set_card(SimpleCard(data.SKILL_NAME, charity_info))

        return handler_input.response_builder.response


class SearchACharityIntentHandler(AbstractRequestHandler):
    """Handler for searching for a charity."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("SearchACharityIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SearchACharityIntentHandler")

        handler_input.response_builder.speak(data.SEARCH_A_CHARITY_SPEECH).ask(
            data.REPROMPT_SPEECH).set_card(SimpleCard(data.SKILL_NAME, data.SEARCH_A_CHARITY_SPEECH))

        return handler_input.response_builder.response


class SearchACharityByNameIntentHandler(AbstractRequestHandler):
    """Handler for searching for a charity by name."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("SearchACharityByNameIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SearchACharityByNameIntentHandler")

        handler_input.response_builder.speak(data.ASK_CHARITY_NAME_SPEECH).ask(
            data.REPROMPT_SPEECH).set_card(SimpleCard(data.SKILL_NAME, data.ASK_CHARITY_NAME_SPEECH))

        return handler_input.response_builder.response


class SearchACharityByCategoryIntentHandler(AbstractRequestHandler):
    """Handler for searching for a charity by name."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("SearchACharityByCategoryIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SearchACharityByCategoryIntentHandler")

        handler_input.response_builder.speak(data.ASK_CHARITY_CATEGORY_SPEECH).ask(
            data.REPROMPT_SPEECH).set_card(SimpleCard(data.SKILL_NAME, data.ASK_CHARITY_CATEGORY_SPEECH))

        return handler_input.response_builder.response


class GetDonationInfoIntentHandler(AbstractRequestHandler):
    """Handler for searching for a charity by name."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("GetDonationInfoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetDonationInfoIntentHandler")

        handler_input.response_builder.speak(data.DONATION_MADE_SPEECH).ask(
            data.REPROMPT_SPEECH).set_card(SimpleCard(data.SKILL_NAME, data.DONATION_MADE_SPEECH))

        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        handler_input.response_builder.speak(data.HELP_MESSAGE).ask(
            data.REPROMPT_SPEECH).set_card(SimpleCard(data.SKILL_NAME, data.HELP_MESSAGE))

        return handler_input.response_builder.response


class YesIntentHandler(AbstractRequestHandler):
    """Handler for Yes Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In YesIntentHandler")

        #handler_input.response_builder.speak("Right on!")

        # return handler_input.response_builder.response
        return JoseIntentHandler.amazonPayCharge(self, handler_input)


class JoseIntentHandler(AbstractRequestHandler):

    """Handler for searching for a charity by name."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("JoseIntentHandler")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In JoseIntentHandler")
        logger.info(config.INIT['bucketName'])
        # handler_input.response_builder.speak("Hello World").ask(
        #    "Do you want to continue").set_card(SimpleCard(data.SKILL_NAME, data.DONATION_MADE_SPEECH))

        # return handler_input.response_builder.response
        return JoseIntentHandler.amazonPaySetup(self, handler_input, "Car")

    # Customer has shown intent to purchase, call Setup to grab the customers shipping address detail
    def amazonPaySetup(self, handler_input, productType):

        # update and save persistent_attributes

        logger.info('handler_input')
        # logger.info(handler_input.attributes_manager)

        # Save session attributes because skill connection directives will close the session
        #session_attr = handler_input.attributes_manager.session_attributes
        # logger.info(session_attr)
        #session_attr["productType"] = productType
        #attributesManager = handler_input
        # print(attributesManager)
        #attributes = attributesManager.persistent_attributes
        #attributes.productType = productType
        # attributesManager.setSessionAttributes(attributes)

        # Permission check
        JoseIntentHandler.handleMissingAmazonPayPermission(self, handler_input)
        logger.info("after permission check in setup ")

        permissions = handler_input.request_envelope.context.system.user.permissions
        amazonPayPermission = permissions.scopes['payments:autopay_consent']

        logger.info(permissions)
        logger.info("amazonPayPermission")
        logger.info(amazonPayPermission)

        if amazonPayPermission.status == 'PermissionStatus.DENIED':
            logger.info("Inside amazonPayPermission IF Statement")
            handler_input.response_builder.speak("No permissions").ask(
                data.REPROMPT_SPEECH).set_card(SimpleCard(data.SKILL_NAME, data.DONATION_MADE_SPEECH))
            return handler_input.response_builder.response
            # return handlerInput.responseBuilder.speak( 'To make purchases in this skill, you need to enable Amazon Pay and turn on voice purchasing. To help, I sent a card to your Alexa app.' ).withAskForPermissionsConsentCard( [ 'payments:autopay_consent' ] ).getResponse();
        logger.info("After if amazonPayPermission.status == PermissionStatus")

        foo = handler_input.request_envelope.request.locale

        # If you have a valid billing agreement from a previous session, skip the Setup action and call the Charge action instead
        token = 'correlationToken'
        # If you do not have a billing agreement, set the Setup payload and send the request directive
        setupPayload = payload_builder.createSetupPayload(
            handler_input.request_envelope.request.locale)
        logger.info(setupPayload)
        setupRequestDirective = directive_builder.createDirective(
            config.GLOBAL['directiveSetupName'], setupPayload, token)
        logger.info(setupRequestDirective)

        # handler_input.response_builder.speak("Setting Up Payment").ask(
        #    data.REPROMPT_SPEECH).set_card(SimpleCard(data.SKILL_NAME, data.DONATION_MADE_SPEECH))

        # handler_input.response_builder.add_directive(setupRequestDirective).ask(
        #    data.REPROMPT_SPEECH).set_card(SimpleCard(data.SKILL_NAME, data.DONATION_MADE_SPEECH))

        return handler_input.response_builder.add_directive(
            SendRequestDirective(
                name="Setup",
                payload={
                    '@type': 'SetupAmazonPayRequest',
                    '@version': '2',
                                'sellerId': 'A2G5K08S7KTD5R',
                                'countryOfEstablishment': 'US',
                                'ledgerCurrency': 'USD',
                                'checkoutLanguage': 'en-US',
                                'sandboxCustomerEmailId': 'cordovaorlando.jc+sandbox@gmail.com',
                                'sandboxMode': True,
                                'needAmazonShippingAddress': True,
                                'billingAgreementAttributes': {
                                    '@type': 'BillingAgreementAttributes',
                                    '@version': '2',
                                    'sellerNote': 'Thanks for shaving with No Nicks',
                                    'platformId': None,
                                    'sellerBillingAgreementAttributes': {
                                        '@type': 'SellerBillingAgreementAttributes',
                                        '@version': '2',
                                        'sellerBillingAgreementId': 'BA12345',
                                        'storeName': 'No Nicks',
                                        'customInformation': ''
                                    }
                                }
                },
                token="correlationToken")
        ).response
        # return handler_input.response_builder.response
        # return handler_input.response_builder.addDirective( setupRequestDirective ).withShouldEndSession( true ).response

    # Customer has requested checkout and wants to be charged
    def amazonPayCharge(self, handler_input):

        # Permission check
        JoseIntentHandler.handleMissingAmazonPayPermission(self, handler_input)

        permissions = handler_input.request_envelope.context.system.user.permissions
        amazonPayPermission = permissions.scopes['payments:autopay_consent']

        logger.info("In amazonPayCharge")
        logger.info(amazonPayPermission.status)

        if amazonPayPermission.status == 'PermissionStatus.DENIED':
            logger.info("Inside amazonPayPermission IF Statement")
            handler_input.response_builder.speak("No permissions").ask(
                data.REPROMPT_SPEECH).set_card(SimpleCard(data.SKILL_NAME, data.DONATION_MADE_SPEECH))
            return handler_input.response_builder.response
            # return handlerInput.responseBuilder.speak( 'To make purchases in this skill, you need to enable Amazon Pay and turn on voice purchasing. To help, I sent a card to your Alexa app.' ).withAskForPermissionsConsentCard( [ 'payments:autopay_consent' ] ).getResponse();

        #foo = handler_input.request_envelope.request.locale

        # If you have a valid billing agreement from a previous session, skip the Setup action and call the Charge action instead
        token = 'correlationToken'
        # If you do not have a billing agreement, set the Setup payload and send the request directive
        #setupPayload = payload_builder.createSetupPayload( handler_input.request_envelope.request.locale )
        # logger.info(setupPayload)
        #setupRequestDirective = directive_builder.createDirective( config.GLOBAL['directiveSetupName'], setupPayload, token )
        # logger.info(setupRequestDirective)

        # handler_input.response_builder.speak("Setting Up Payment").ask(
        #    data.REPROMPT_SPEECH).set_card(SimpleCard(data.SKILL_NAME, data.DONATION_MADE_SPEECH))

        # handler_input.response_builder.add_directive(setupRequestDirective).ask(
        #    data.REPROMPT_SPEECH).set_card(SimpleCard(data.SKILL_NAME, data.DONATION_MADE_SPEECH))

        return handler_input.response_builder.add_directive(
            SendRequestDirective(
                name="Charge",
                payload={
                    '@type': 'ChargeAmazonPayRequest',
                    '@version': '2',
                                'sellerId': 'A2G5K08S7KTD5R',
                                'billingAgreementId': 'C01-1108076-6653603',
                                'paymentAction': 'AuthorizeAndCapture',
                                'authorizeAttributes': {
                                    '@type': 'AuthorizeAttributes',
                                    '@version': '2',
                                    'authorizationReferenceId': 'sdfwr3423fsxfsrq43',
                                    'authorizationAmount': {
                                        '@type': 'AuthorizeAttributes',
                                        '@version': '2',
                                        'amount': '9',
                                        'currencyCode': 'USD'
                                    },
                                    'transactionTimeout': 0,
                                    'sellerAuthorizationNote': 'Billing Agreement Seller Note',
                                    'softDescriptor': 'No Nicks'
                                },
                    'sellerOrderAttributes': {
                                    '@type': 'SellerOrderAttributes',
                                    '@version': '2',
                                    'sellerOrderId': 'ABC-000-123234',
                                    'storeName': 'No Nicks',
                                    'customInformation': '',
                                    'sellerNote': 'Thanks for shaving with No Nicks'
                                }

                },
                token="correlationToken")
        ).response

    def handleMissingAmazonPayPermission(self, handler_input):
        logger.info("In handleMissingAmazonPayPermission")
        permissions = handler_input.request_envelope.context.system.user.permissions
        amazonPayPermission = permissions.scopes['payments:autopay_consent']
        logger.info(str(amazonPayPermission.status))
        if str(amazonPayPermission.status) == 'PermissionStatus.DENIED':
            logger.info("Inside DENIED")
            handler_input.response_builder.speak("To make purchases in this skill, you need to enable Amazon Pay and turn on voice purchasing. To help, I sent a card to your Alexa app.").set_card(
                AskForPermissionsConsentCard(['payments:autopay_consent']))
            return handler_input.response_builder.response

            # handler_input.response_builder.speak("Declined").ask(
            # data.REPROMPT_SPEECH).set_card(SimpleCard(data.SKILL_NAME, data.DONATION_MADE_SPEECH))
            # return handler_input.response_builder.response
            # return handlerInput.responseBuilder
            #                .speak( 'To make purchases in this skill, you need to enable Amazon Pay and turn on voice purchasing. To help, I sent a card to your Alexa app.' )
            #                .withAskForPermissionsConsentCard( [ 'payments:autopay_consent' ] )
            #                .getResponse();


class SetupConnectionsResponseHandler(AbstractRequestHandler):
    #"""This handles the Connections.Response event after a buy occurs."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        logger.info("In SetupConnectionsResponseHandler 1")
        return (is_request_type("Connections.Response")(handler_input) and
                handler_input.request_envelope.request.name == "Setup")

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SetupConnectionsResponseHandler 2")

        #connectionResponsePayload = handler_input.request_envelope.request.payload
        #connectionResponseStatusCode = handler_input.request_envelope.request.status.code

        # If there are integration or runtime errors, do not charge the payment method
        # if connectionResponseStatusCode != 200:
        #    logger.info("Error inside SetupConnectionsResponseHandler Status Code != 200")
        # return error.handleErrors( handlerInput )
        # logger.info(connectionResponsePayload)
        # logger.info(connectionResponseStatusCode)

        # Permission check
        JoseIntentHandler.handleMissingAmazonPayPermission(self, handler_input)

        # Get the billingAgreementId and billingAgreementStatus from the Setup Connections.Response
        billingAgreementId = 'BA12345'
        billingAgreementStatus = 'OPEN'

        # logger.info(billingAgreementStatus)

        # if ( billingAgreementStatus === 'OPEN' ):
        logger.info("HEYY!")
        # logger.info(handler_input.attributes_manager.session_attributes["productType"])

        handler_input.response_builder.speak(
            "Your Donation will be made using amazon pay. Do you want to check out now?").set_should_end_session(False)

        return handler_input.response_builder.response

# You requested the Charge directive and are now receiving the Connections.Response


class ChargeConnectionsResponseHandler(AbstractRequestHandler):
    #"""This handles the Connections.Response event after a buy occurs."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        logger.info("In ChargeConnectionsResponseHandler 1")
        return (is_request_type("Connections.Response")(handler_input) and
                handler_input.request_envelope.request.name == "Charge")

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ChargeConnectionsResponseHandler 2")

        connectionResponsePayload = handler_input.request_envelope.request.payload
        connectionResponseStatusCode = handler_input.request_envelope.request.status.code

        # If there are integration or runtime errors, do not charge the payment method
        # if connectionResponseStatusCode != 200:
        #    logger.info("Error inside SetupConnectionsResponseHandler Status Code != 200")
        # return error.handleErrors( handlerInput )
        logger.info(connectionResponsePayload)
        logger.info(connectionResponseStatusCode)

        # Permission check
        JoseIntentHandler.handleMissingAmazonPayPermission(self, handler_input)

        # Get the billingAgreementId and billingAgreementStatus from the Setup Connections.Response
        #billingAgreementId = 'BA12345'
        #billingAgreementStatus = 'OPEN'

        # logger.info(billingAgreementStatus)

        # if ( billingAgreementStatus === 'OPEN' ):
        # logger.info("HEYY!")
        # logger.info(handler_input.attributes_manager.session_attributes["productType"])

        handler_input.response_builder.speak(
            "Thank you for your donation. The order has been placed.").set_should_end_session(True)

        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        handler_input.response_builder.speak(data.GOODBYE_ANSWER).set_card(
            SimpleCard(data.SKILL_NAME, data.GOODBYE_ANSWER))

        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.

    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        handler_input.response_builder.speak(data.FALLBACK_MESSAGE).ask(
            data.REPROMPT_SPEECH).set_card(SimpleCard(data.SKILL_NAME, data.FALLBACK_MESSAGE))

        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)
        handler_input.response_builder.speak(FALLBACK_ANSWER).ask(
            HELP_REPROMPT)

        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""

    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""

    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Register intent handlers
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetCharityInfoIntentHandler())
sb.add_request_handler(SearchACharityIntentHandler())
sb.add_request_handler(SearchACharityByNameIntentHandler())
sb.add_request_handler(SearchACharityByCategoryIntentHandler())
sb.add_request_handler(GetDonationInfoIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(JoseIntentHandler())
sb.add_request_handler(SetupConnectionsResponseHandler())
sb.add_request_handler(ChargeConnectionsResponseHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# Register request and response interceptors
# sb.add_global_request_interceptor(LocalizationInterceptor())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
