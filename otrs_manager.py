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
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# ============================== CONSTS ===================================== #
OTRS_DEFAULT_ROUTE = {
    'mapping_create_ticket': '/TicketCreate',
    'mapping_update_ticket': '/TicketUpdate',
    'mapping_get_ticket': '/TicketGet',
    'mapping_search_ticket': '/TicketSearch',
}
OTRS_ROUTE_MAPPING_GET_TICKET = 'mapping_get_ticket'
OTRS_ROUTE_MAPPING_SEARCH_TICKET = 'mapping_search_ticket'
OTRS_STATETYPE_IDS = [1, 2]
OTRS_CREATE_TIME = 'Ticket Create Time in Minutes'
OTRS_TITLE_SEARCH = 'Title Search'
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

    def _prepare_get_ticket_url(self, action_route_uri, ticket_id):
        pass

    def _prepare_search_ticket_url(self, action_route_uri):
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
        if title_string:
            title_list = [x.strip() for x in title_string.split(",")]
            # TODO :: To be continued

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
