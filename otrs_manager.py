# ============================================================================#
# title           :OTRSManager.py
# description     :This Module contain all OTRS operations functionality
# author          :myasul@siemplify.co
# date            :10-05-2019
# python_version  :2.7
# ============================================================================#

# ============================= IMPORTS ===================================== #
import requests
import base64
import urllib
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# ============================== CONSTS ===================================== #
OTRS_DEFAULT_ROUTE = {
    'mapping_create_ticket': 'TicketCreate',
    'mapping_update_ticket': 'TicketUpdate',
    'mapping_get_ticket': 'TicketGet',
    'mapping_search_ticket': 'TicketSearch',
}
OTRS_ROUTE_MAPPING_GET_TICKET = 'mapping_get_ticket'
OTRS_ROUTE_MAPPING_SEARCH_TICKET = 'mapping_search_ticket'
OTRS_STATETYPE_IDS = [1, 2]
OTRS_CREATE_TIME = 'Ticket Create Time in Minutes'
OTRS_TITLE_SEARCH = 'Title Search'
OTRS_DEVICE_URL = 'Device URL'
OTRS_REST_ENDPOINT = "otrs/nph-genericinterface.pl/Webservice"
OTRS_SERVICE = "Service Name"
USERNAME = 'Username'
PASSWORD = 'Password'
# ============================= CLASSES ===================================== #


class OTRSManagerError(Exception):
    """
    General Exception for OTRS Manager
    """
    pass


class OTRSManager(object):
    def __init__(self, username, password, parameters):
        """
        Test connectivity with OTRS
        """
        self.username = username
        self.password = password
        self.parameters = parameters
        self.session = requests.Session()
        url = self.prepare_url(OTRS_ROUTE_MAPPING_GET_TICKET, ticket_id='1')

        response = self.session.get(url)

        self.validate_response(response, "Unable to connect")

    def prepare_url(self, mapping, ticket_id=None):
        if mapping in self.parameters:
            action_route_uri = self.parameters.get(mapping)
        else:
            action_route_uri = OTRS_DEFAULT_ROUTE.get(mapping)

        if ticket_id and mapping == OTRS_ROUTE_MAPPING_GET_TICKET:
            return self._prepare_get_ticket_url(
                action_route_uri, ticket_id
            )
        elif mapping == OTRS_ROUTE_MAPPING_SEARCH_TICKET:
            return self._prepare_search_ticket_url(action_route_uri)
        else:
            raise OTRSManagerError('Invalid mapping.')

    def _prepare_get_ticket_url(self, action_route_uri, ticket_id):
        username = self._build_parameter_string(
            "UserLogin",
            self.parameters.get(USERNAME)
        )

        password = self._build_parameter_string(
            "Password",
            self.parameters.get(PASSWORD)
        )

        return '{device_url}/{endpoint}/{service}/{action_uri}/'\
            '/{ticket_id}?{username}{password}'\
            '&AllArticles=1&Attachments=>1&GetAttachmentContents=>1'.format(
                device=self.parameters.get(OTRS_DEVICE_URL),
                endpoint=OTRS_REST_ENDPOINT,
                service=self.parameters.get(OTRS_SERVICE),
                action_uri=action_route_uri,
                ticket_id=ticket_id,
                username=username,
                password=password
            )

    def _prepare_search_ticket_url(self, action_route_uri):
        username = self._build_parameter_string(
            "UserLogin",
            self.parameters.get(USERNAME)
        )

        password = self._build_parameter_string(
            "Password",
            self.parameters.get(PASSWORD)
        )

        # Tickets created within the specified time are the
        # only ones that will be polled.
        ticket_create_time = self._build_parameter_string(
            "TicketCreateTimeNewerMinutes",
            self.parameters.get(OTRS_CREATE_TIME)
        )

        # State IDs
        state_type_ids = self._build_parameter_string(
            "StateTypeIDs", OTRS_STATETYPE_IDS)

        # Title substring search
        title_string = self.parameters.get(OTRS_TITLE_SEARCH)
        title_search = ""
        if title_string:
            title_list = []
            for title in title_string.split(","):
                title_list.append(urllib.quote("%{}%".format(title.strip())))
            title_search = self._build_parameter_string("Title", title_list)
            # TODO :: To be continued

        return '{device}/{endpoint}/{service}/{action_uri}' \
            '?{username}{password}{ticket_create_time}' \
            '{state_type_ids}{title_search}'.format(
                device=self.parameters.get(OTRS_DEVICE_URL),
                endpoint=OTRS_REST_ENDPOINT,
                service=self.parameters.get(OTRS_SERVICE),
                action_uri=action_route_uri,
                username=username,
                password=password,
                ticket_create_time=ticket_create_time,
                state_type_ids=state_type_ids,
                title_search=title_search
            )

    def _build_parameter_string(self, param_key, param_value):
        if isinstance(param_value, list) and \
                len(param_value) > 0:
            param_list = []
            for value in param_value:
                param_list.append("&{}={}".format(param_key, value))
            return "".join(param_list)
        elif param_value and \
                (isinstance(param_value, str) or
                    isinstance(param_value, int)):
            return "&{}={}".format(param_key, param_value)
        else:
            return ""

    @staticmethod
    def validate_response(res, error_msg="An error occured"):
        try:
            res.raise_for_status()
        except requests.HTTPError as error:
            raise OTRSManagerError(
                "{error_msg}: {error} {text}".format(
                    error_msg=error_msg,
                    error=error,
                    text=error.response.content
                )
            )
