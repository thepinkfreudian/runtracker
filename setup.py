import sys
from datetime import datetime
import utils.utils as utils

start_date = sys.argv[1]
end_date = sys.argv[2]
environment = sys.argv[3]

## testing
# start_date = '1/6/2022'
# end_date = '1/11/2022'
# environment = 'dev'


push = False
if len(sys.argv) > 4:
    if sys.argv[4] == 'push':
        push = True
    else:
        error_message = "Invalid argument '" + str(sys.argv[4]) + "' passed to sys.argv[4]."
        utils.exit_on_error(error_message)

valid_start_date = utils.validate_input_date(start_date)
valid_end_date = utils.validate_input_date(end_date)
valid_environment = utils.validate_environment(environment)

if not valid_start_date or not valid_end_date:
    error_message = "Invalid date format. Use 'm/d/yyyy'."
    utils.exit_on_error(error_message)

if not valid_environment:
    error_message = "Invalid environment '" + str(environment) + "' passed to sys.argv[3]."
    utils.exit_on_error(error_message)

config_file = '../cfg/config.json'
config = utils.get_session_config(config_file)

