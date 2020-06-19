# -*- coding: utf-8 -*-
"""Cause app."""

import random
import logging
import json
# import os
# import boto3
from query_functions import query_next_item
from ask_sdk_core.skill_builder import (SkillBuilder, CustomSkillBuilder)
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard  # for devices with a screen
from alexa import data, util  # data and utils in a seperate file
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
        charity_id = 1
        #charity_name = "Charity Name Holder"
        #charity_mission = "Charity Mission Holder"

        # storing persistance attributes and checking for id attributes
        attr = handler_input.attributes_manager.persistent_attributes
        attributes_are_present = ("id" in attr)

        # error checking
        if attributes_are_present:
            charity_id = attr['id']
        else:
            charity_id = 1

        # DynamoDB query
        charity_name, charity_mission = query_next_item(charity_id, "Animals")

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
