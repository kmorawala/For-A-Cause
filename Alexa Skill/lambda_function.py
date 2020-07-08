# -*- coding: utf-8 -*-
"""Cause app."""

# python imports
from ask_sdk_model.interfaces.connections import SendRequestDirective
import random
import logging
import json

# imports from SDK
from ask_sdk_core.skill_builder import (SkillBuilder, CustomSkillBuilder)
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard  # for devices with a screen
from ask_sdk_model.ui import AskForPermissionsConsentCard
# this helps return the directive results Setup and Charge Directives
from ask_sdk_model.interfaces.connections import ConnectionsRequest

# imports from several utility functions
# data, utils, config, payload_builder, and directive_builder in a seperate file
from alexa import data, util, payload_builder, config, directive_builder

# DB query functions
from query_functions import *

# added for remembering attributes
import os
from ask_sdk_s3.adapter import S3Adapter
s3_adapter = S3Adapter(bucket_name=os.environ["S3_PERSISTENCE_BUCKET"])

# Session variables (only exist during one Alexa session)
sb = CustomSkillBuilder(persistence_adapter=s3_adapter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# global charity_name
# global charity_id

# Request Handler classes


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for skill launch or new search."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequestHandler")
        # global charity_name
        # global charity_id

        message = data.WELCOME_MESSAGE + " " + data.TODAYS_CHARITY_MESSAGE + \
            get_next_charity(self, handler_input)

        handler_input.response_builder.speak(message).ask(message)
        # logger.info(charity_id)
        # logger.info(charity_name)

        return handler_input.response_builder.response


def get_next_charity(self, handler_input):
    """Function used for going to the next charity in the database."""

    logger.info("In get_next_charity function")

    # Accessing persistance attributes for charity_id
    attr = handler_input.attributes_manager.persistent_attributes
    attributes_are_present = ("id" in attr)

    table_name = "Animals"
    # below global variables will be used in other classes/functions

    global charity_id

    # error checking to ensure charity_id is within a valid range
    if attributes_are_present:
        charity_id = attr['id']
        charity_id += 1
    else:
        charity_id = 1

    max_charity_id = get_item_count(table_name)
    if charity_id > max_charity_id:
        charity_id = 1

    message = get_charity_info(self, handler_input, charity_id, table_name)
    # DynamoDB query
    # charity_name, charity_mission = query_next_item(charity_id, table_name)
    # charity_name, charity_mission = query_next_item(2, "Animals")

    # message = charity_name + ". " + data.MISSION_MSG + charity_mission + " " + data.USER_OPTION
    # logger.info(message)

    # update and save persistent_attributes
    attr = {
        "id": charity_id
    }
    handler_input.attributes_manager.persistent_attributes = attr
    handler_input.attributes_manager.save_persistent_attributes()

    logger.info(charity_id)
    logger.info(charity_name)

    return message


def get_charity_info(self, handler_input, charity_id, table_name):
    """Function used for going to the next charity in the database."""
    logger.info("In get_charity_info function")

    global charity_name

    # DynamoDB query
    charity_name, charity_mission = query_next_item(charity_id, table_name)

    # charity_name, charity_mission = query_next_item(2, "Animals")
    message = charity_name + ". " + data.MISSION_MSG + \
        charity_mission + " " + data.USER_OPTION

    return message


class GetNextCharityIntentHandler(AbstractRequestHandler):
    """Handler for exploring the next charity."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("GetNextCharityIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetNextCharityIntentHandler")

        message = "Our next charity is " + \
            get_next_charity(self, handler_input)

        handler_input.response_builder.speak(message).ask(
            data.REPROMPT_SPEECH).set_card(SimpleCard(data.SKILL_NAME, message))

        return handler_input.response_builder.response


class GetCharityInfoIntentHandler(AbstractRequestHandler):
    """Handler for exploring the current charity."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("GetCharityInfoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetCharityInfoIntentHandler")
        # logger.info(charity_id)
        # logger.info(charity_name)

        table_name = "Animals"
        message = "Our charity is " + \
            get_charity_info(self, handler_input, charity_id, table_name)

        # message = "Our charity is " + get_charity_info(self, handler_input, charity_id, table_name)

        handler_input.response_builder.speak(message).ask(
            data.REPROMPT_SPEECH).set_card(SimpleCard(data.SKILL_NAME, message))

        return handler_input.response_builder.response


class MakeDonationIntentHandler(AbstractRequestHandler):
    """Handler for searching for a charity by name."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("MakeDonationIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In MakeDonationIntentHandler")
        logger.info(charity_id)
        logger.info(charity_name)

        # database query to get the total contribution made to the charity
        table_name = "Animals"
        total_contribution = get_total_contribution(charity_id, table_name)

        # access the user spoken slot value for the amount of contribution
        slots = handler_input.request_envelope.request.intent.slots
        amount_donated_list = slots["DonationAmount"].value
        global amount_donated
        amount_donated = int(amount_donated_list)
        total_contribution = total_contribution + int(amount_donated)

        # database query to update the total contribution
        update_total_contribution(
            charity_id, table_name, int(total_contribution))

        message = data.DONATION_MADE_SPEECH + charity_name + " for " + \
            str(amount_donated) + " dollars. Should I process your payment now?"

        handler_input.response_builder.speak(message).ask(
            data.REPROMPT_SPEECH).set_card(SimpleCard(data.SKILL_NAME, message))

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
    """Handler for Yes Intent. Used for confirmation only, when user agrees to use AmazonPay for their donation."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        return amazonPayCharge(self, handler_input, charity_name,  amount_donated)


def amazonPaySetup(self, handler_input, charity_name, amount_donated):
    """Customer has shown intent to purchase, call Setup to grab the customers shipping address detail """

    # Permission check
    handleMissingAmazonPayPermission(self, handler_input)

    permissions = handler_input.request_envelope.context.system.user.permissions
    amazonPayPermission = permissions.scopes['payments:autopay_consent']

    if amazonPayPermission.status == 'PermissionStatus.DENIED':
        handler_input.response_builder.speak("No permissions").ask(
            data.REPROMPT_SPEECH).set_card(SimpleCard(data.SKILL_NAME, data.DONATION_MADE_SPEECH))
        return handler_input.response_builder.response
        # return handlerInput.responseBuilder.speak( 'To make purchases in this skill, you need to enable Amazon Pay and turn on voice purchasing. To help, I sent a card to your Alexa app.' ).withAskForPermissionsConsentCard( [ 'payments:autopay_consent' ] ).getResponse();

    foo = handler_input.request_envelope.request.locale

    token = 'correlationToken'
    #setupPayload = payload_builder.createSetupPayload( handler_input.request_envelope.request.locale )
    #setupRequestDirective = directive_builder.createDirective( config.GLOBAL['directiveSetupName'], setupPayload, token )

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

# class JoseIntentHandler(AbstractRequestHandler):

#     """Handler for searching for a charity by name."""
#     def can_handle(self, handler_input):
#         # type: (HandlerInput) -> bool
#         return is_intent_name("JoseIntentHandler")(handler_input)

#     def handle(self, handler_input):
#         # type: (HandlerInput) -> Response
#         logger.info("In JoseIntentHandler")
#         logger.info(config.INIT['bucketName'])
#         #handler_input.response_builder.speak("Hello World").ask(
#         #    "Do you want to continue").set_card(SimpleCard(data.SKILL_NAME, data.DONATION_MADE_SPEECH))

#         #return handler_input.response_builder.response
#         return amazonPaySetup(self, handler_input, "Car")

# Customer has requested checkout and wants to be charged


def amazonPayCharge(self, handler_input, charity_name, amount_donated):

    # Permission check
    handleMissingAmazonPayPermission(self, handler_input)

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

    # If you have a valid billing agreement from a previous session, skip the Setup action and call the Charge action instead
    token = 'correlationToken'

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
                                'authorizationReferenceId': 'sdfwr3423fsxfsrq42',
                                'authorizationAmount': {
                                    '@type': 'Price',
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
                                'sellerOrderId': 'ABC-000-123232',
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
        handler_input.response_builder.speak("To make purchases in this skill, you need to enable Amazon Pay and turn on voice purchasing. To help, I sent a card to your Alexa app.").set_card(
            AskForPermissionsConsentCard(['payments:autopay_consent']))
        return handler_input.response_builder.response


class SetupConnectionsResponseHandler(AbstractRequestHandler):
    #"""This handles the Connections.Response event after a buy occurs."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("Connections.Response")(handler_input) and
                handler_input.request_envelope.request.name == "Setup")

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        connectionResponsePayload = handler_input.request_envelope.request.payload
        connectionResponseStatusCode = handler_input.request_envelope.request.status.code

        # If there are integration or runtime errors, do not charge the payment method
        if str(connectionResponseStatusCode) != '200':
            return logger.info("Error inside SetupConnectionsResponseHandler Status Code != 200")

        # Get the billingAgreementId and billingAgreementStatus from the Setup Connections.Response
        billingAgreementId = connectionResponsePayload['billingAgreementDetails']['billingAgreementId']
        billingAgreementStatus = connectionResponsePayload[
            'billingAgreementDetails']['billingAgreementStatus']

        # If billingAgreementStatus is valid, Charge the payment method
        if str(billingAgreementStatus) == 'OPEN':
            logger.info("OPENN!")

            # Save billingAgreementId attributes because directives will close the session
            session_attr = handler_input.attributes_manager.session_attributes
            session_attr["billingAgreementId"] = billingAgreementId
            session_attr["setup"] = True

            handler_input.response_builder.speak(
                "Your Donation will be made using amazon pay. Do you want to check out now?").set_should_end_session(False)
            return handler_input.response_builder.response

# You requested the Charge directive and are now receiving the Connections.Response


class ChargeConnectionsResponseHandler(AbstractRequestHandler):
    """This handles the Connections.Response event after a buy occurs."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("Connections.Response")(handler_input) and
                handler_input.request_envelope.request.name == "Charge")

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        connectionResponsePayload = handler_input.request_envelope.request.payload
        connectionResponseStatusCode = handler_input.request_envelope.request.status.code

        # If there are integration or runtime errors, do not charge the payment method
        # if str(connectionResponseStatusCode) != '200':
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
sb.add_request_handler(GetNextCharityIntentHandler())
sb.add_request_handler(GetCharityInfoIntentHandler())
sb.add_request_handler(MakeDonationIntentHandler())
sb.add_request_handler(YesIntentHandler())
# sb.add_request_handler(JoseIntentHandler())
sb.add_request_handler(SetupConnectionsResponseHandler())
sb.add_request_handler(ChargeConnectionsResponseHandler())
sb.add_request_handler(HelpIntentHandler())
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