# ============================================================================#
# title           :OTRSConnector.py
# description     :This Module contain all OTRS connector functionality
# author          :myasul@siemplify.co
# date            :10-05-2019
# python_version  :2.7
# ============================================================================#

# ============================= IMPORTS ===================================== #
import sys
import SiemplifyUtils
from SiemplifyConnectors import SiemplifyConnectorExecution
from SiemplifyConnectorDataModel import CaseInfo

# ============================== CONSTS ===================================== #
PRODUCT = VENDOR = 'OTRS'
OTRS_SCRIPT_NAME = 'OTRS Connector'
OTRS_DEVICE_URL = 'device_url'
USERNAME = 'username'
PASSWORD = 'Password'
OTRS_SERVICE = 'Service Name'
OTRS_ROUTE_MAPPING_SEARCH_TICKET = 'mapping_search_ticket'
OTRS_MAX_TICKET = 'Max Tickets Per Cycle'
TIMEZONE = 'Server Timezone'

# ============================= CLASSES ===================================== #


class OTRSConnectorException(Exception):
    """
    OTRS Connector Exception
    """
    pass


class OTRSConnector(object):
    def __init__(self, connector_scope, otrs_manager, max_tickets_per_cycle):
        self.connector_scope = connector_scope
        self.logger = connector_scope.LOGGER
        self.otrs_manager = otrs_manager
        self.max_tickets_per_cycle = max_tickets_per_cycle

    def validate_timestamp(self, last_run_timestamp, offset):
        """
        """
        pass


def main():
    """
    Main execution - OTRS Connector
    """
    connector_scope = SiemplifyConnectorExecution()
    connector_scope.script_name = OTRS_SCRIPT_NAME
    output_variables = {}
    log_items = []

    connector_scope.LOGGER.info("========== Starting Connector ===========")
    try:
        connector_scope.LOGGER.info('Connecting to OTRS')
        username = connector_scope.parameters.get(OTRS_USERNAME)
        password = connector_scope.parameters.get(OTRS_PASSWORD)
        max_tickets_per_cycle = int(
            connector_scope.parameters.get(OTRS_MAX_TICKET))
        timezone = connector_scope.parameters.get(TIMEZONE)

        otrs_manager = OTRSManager(username, password)

    except Exception as e:
        connector_scope.LOGGER.scope(e.message)
        connector_scope.LOGGER.exception(e)
        raise OTRSConnectorException('Unexpected error: {}'.format(e))


def test():
    pass


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == 'True':
        print 'Main execution started'
        main()
    else:
        print 'Test execution started'
        test()
