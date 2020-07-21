#
#    Builds and returns directives that contain either a Setup or Charge payload
#    https://developer.amazon.com/docs/amazon-pay/integrate-skill-with-amazon-pay-v2.html#workflow1
#
from alexa import config
#const config = require( 'config' );

def createDirective( name, payload, token ): 
    directive = {
        'type':       config.GLOBAL['directiveType'],
        'name':       name,
        'payload':    payload,
        'token':      token      
    };

    return directive;
