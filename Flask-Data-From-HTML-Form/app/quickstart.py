#
# Copyright (c) 2018, 2020 Oracle and/or its affiliates.  All rights reserved.
#
# Licensed under the Universal Permissive License v 1.0 as shown at
#  https://oss.oracle.com/licenses/upl/
#

#
# This is a simple quickstart to demonstrate use of the Python driver for
# the Oracle NoSQL Database. It can be used to run against the Oracle NoSQL
# Database Cloud Service, against the Cloud Simulator, or against an
# on-premise Oracle NoSQL database.
#
# Usage:
#   python quickstart.py <cloud | cloudsim | kvstore>
#
# Use cloud for the Cloud Service
# Use cloudsim for the Cloud Simulator
# Use kvstore for the on-premise database
#
# This example is not intended to be an exhaustive overview of the API,
# which has a number of additional operations.
#
# Requirements:
#  1. Python 2.7 or 3.5+
#  2. Python dependencies (install using pip or other mechanism):
#   o requests
#   o oci (only if running against the Cloud Service)
#  3. If running against the Cloud Simulator, it can be downloaded from
#  here:
#   http://www.oracle.com/technetwork/topics/cloud/downloads/index.html
#  It requires Java
#  4. If running against the Oracle NoSQL Database Cloud Service an account
#  must be used.
#

import sys

from borneo import (
    AuthorizationProvider, DeleteRequest, GetRequest,
    IllegalArgumentException, NoSQLHandle, NoSQLHandleConfig, PutRequest,
    QueryRequest, Regions, TableLimits, TableRequest)
from borneo.iam import SignatureProvider
from borneo.kv import StoreAccessTokenProvider


#
# EDIT: these values based on desired region and/or endpoint for a local
# server
#
cloud_region = Regions.AP_MUMBAI_1
cloudsim_endpoint = 'localhost:8080'
kvstore_endpoint = 'localhost:80'
cloudsim_id = 'cloudsim'  # a fake user id/namespace for the Cloud Simulator

# Cloud Service Only
#
# EDIT: set these variables to the credentials to use if you are not using
# a configuration file in ~/.oci/config
# Use of these credentials vs a file is determined by a value of tenancy
# other than None.
#
tenancy = None  # tenancy'd OCID (string)
user = None  # user's OCID (string)
private_key = 'path-to-private-key-or-private-key-content'
fingerprint = 'fingerprint for uploaded public key'
# pass phrase (string) for private key, or None if not set
pass_phrase = None


class CloudsimAuthorizationProvider(AuthorizationProvider):
    """
    Cloud Simulator Only.

    This class is used as an AuthorizationProvider when using the Cloud
    Simulator, which has no security configuration. It accepts a string
    tenant_id that is used as a simple namespace for tables.
    """

    def __init__(self, tenant_id):
        super(CloudsimAuthorizationProvider, self).__init__()
        self._tenant_id = tenant_id

    def close(self):
        pass

    def get_authorization_string(self, request=None):
        return 'Bearer ' + self._tenant_id


def get_handle(nosql_env):
    """
    Returns a NoSQLHandle based on the requested environment. The
    differences among the supported environments are encapsulated in this
    method.
    """
    if nosql_env == 'cloud':
        endpoint = cloud_region
        #
        # Get credentials using SignatureProvider. SignatureProvider has
        # several ways to accept credentials. See the documentation:
        #  https://nosql-python-sdk.readthedocs.io/en/stable/api/borneo.iam.SignatureProvider.html
        #
        if tenancy is not None:
            print('Using directly provided credentials')
            #
            # Credentials are provided directly
            #
            provider = SignatureProvider(tenant_id=tenancy,
                                         user_id=user,
                                         fingerprint=fingerprint,
                                         private_key=private_key,
                                         pass_phrase=pass_phrase)
        else:
            #
            # Credentials will come from a file.
            #
            # By default the file is ~/.oci/config. A config_file = <path>
            # argument can be passed to specify a different file.
            #
            print('Using credentials and DEFAULT profile from ' +
                  '~/.oci/config')
            provider = SignatureProvider()
    elif nosql_env == 'cloudsim':
        print('Using cloud simulator endpoint ' + cloudsim_endpoint)
        endpoint = cloudsim_endpoint
        provider = CloudsimAuthorizationProvider(cloudsim_id)

    elif nosql_env == 'kvstore':
        print('Using on-premise endpoint ' + kvstore_endpoint)
        endpoint = kvstore_endpoint
        provider = StoreAccessTokenProvider()

    else:
        raise IllegalArgumentException('Unknown environment: ' + nosql_env)

    return NoSQLHandle(NoSQLHandleConfig(endpoint, provider))


def main():

    table_name = 'PythonQuickstart'

    if len(sys.argv) != 2:
        print('Usage: python quickstart.py <cloud | cloudsim | kvstore>')
        raise SystemExit

    nosql_env = sys.argv[1:][0]
    print('Using environment: ' + str(nosql_env))

    handle = None
    try:

        #
        # Create a handle
        #
        handle = get_handle(nosql_env)

        #
        # Create a table
        #
        statement = (
            'Create table if not exists {} (id integer, sid integer, ' +
            'name string, primary key(shard(sid), id))').format(table_name)
        request = TableRequest().set_statement(statement).set_table_limits(
            TableLimits(30, 10, 1))
        handle.do_table_request(request, 50000, 3000)
        print('After create table')

        #
        # Put a few rows
        #
        request = PutRequest().set_table_name(table_name)
        for i in range(10):
            value = {'id': i, 'sid': 0, 'name': 'myname' + str(i)}
            request.set_value(value)
            handle.put(request)
        print('After put of 10 rows')

        #
        # Get the row
        #
        request = GetRequest().set_key({'id': 1, 'sid': 0}).set_table_name(
            table_name)
        result = handle.get(request)
        print('After get: ' + str(result))

        #
        # Query, using a range
        #
        statement = (
            'select * from ' + table_name + ' where id > 2 and id < 8')
        request = QueryRequest().set_statement(statement)
        print('Query results for: ' + statement)
        #
        # If the :py:meth:`borneo.QueryRequest.is_done` returns False, there
        # may be more results, so queries should generally be run in a loop.
        # It is possible for single request to return no results but the
        # query still not done, indicating that the query loop should
        # continue.
        #
        while True:
            result = handle.query(request)
            for r in result.get_results():
                print('\t' + str(r))
            if request.is_done():
                break

        #
        # Delete the row
        #
        request = DeleteRequest().set_table_name(table_name).set_key(
            {'id': 1, 'sid': 0})
        result = handle.delete(request)
        print('After delete: ' + str(result))

        #
        # Get again to show deletion
        #
        request = GetRequest().set_key({'id': 1, 'sid': 0}).set_table_name(
            table_name)
        result = handle.get(request)
        print('After get (should be None): ' + str(result))

        #
        # Drop the table
        #
        request = TableRequest().set_statement(
            'drop table if exists {} '.format(table_name))
        result = handle.table_request(request)

        #
        # Table drop can take time, depending on the state of the system.
        # If this wait fails the table will still probably been dropped
        #
        result.wait_for_completion(handle, 40000, 2000)
        print('After drop table')

        print('Quickstart is complete')
    except Exception as e:
        print(e)
    finally:
        # If the handle isn't closed Python will not exit properly
        if handle is not None:
            handle.close()


if __name__ == '__main__':
    main()
