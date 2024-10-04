"""
pcied_table_helper.py

This module provides helper functions for managing PCIE detach information tables in the PCIE daemon.
It includes functions to initialize state databases and retrieve PCIE detach information tables for different ASIC namespaces.
"""

from sonic_py_common import daemon_base, logger, multi_asic
from swsscommon import swsscommon

SYSLOG_IDENTIFIER = "pcied_table_helper"

helper_logger = logger.Logger(SYSLOG_IDENTIFIER)
PCIED_DETACHING_TABLE = 'PCIE_DETACH_INFO'

class PciedDetachTableHelper:
    def __init__(self):
        self.state_db = dict()
        self.pcied_detach_info_table = dict()
        # Fetch the namespaces in the platform to initialize state databases and PCIE detach info tables
        # for each ASIC. This ensures that each ASIC's state and detach information is managed separately.
        namespaces = multi_asic.get_front_end_namespaces()
        for namespace in namespaces:
            asic_id = multi_asic.get_asic_index_from_namespace(namespace)

            try:
                self.state_db[asic_id] = daemon_base.db_connect("STATE_DB", namespace)
                self.pcied_detach_info_table[asic_id] = swsscommon.Table(self.state_db[asic_id], PCIED_DETACHING_TABLE)
            except Exception as e:
                helper_logger.log_error(f"Failed to connect to STATE_DB for namespace {namespace}: {e}")

    def get_state_db(self):
        return self.state_db

    def get_pcied_detach_info_table(self):
        return self.pcied_detach_info_table
