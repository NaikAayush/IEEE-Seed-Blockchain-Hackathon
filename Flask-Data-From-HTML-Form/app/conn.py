from borneo import NoSQLHandle, NoSQLHandleConfig, Regions
from borneo.iam import SignatureProvider

#
# Required information:
#

# the region to which the application will connect
region = Regions.AP_MUMBAI_1

# if using a specified credentials file
credentials_file = "~/.oci/config"

#
# Create an AuthorizationProvider
#
at_provider = SignatureProvider(config_file=credentials_file)

#
# create a configuration object
#
config = NoSQLHandleConfig(region, at_provider)

#
# create a handle from the configuration object
#
handle = NoSQLHandle(config)
