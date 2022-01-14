## About RunTracker
RunTracker was designed for a specific use case - to track progress on the route from Wilmington, NC to Buffalo, NY. However, the goal is to make RunTracker an app that can accomodate any reasonable start and end point.

The RunTracker directory structure is as follows:
- RunTracker (root directory)
    - cfg
        - configuration files
    - docs
        - documentation
    - utils
        - utility and helper functions
    - runtracker
        - scripts to execute
    - setup.py

RunTracker is designed to be run from the command line and takes 3 parameters(2 required, 1 optional):
- **end_date:** API data retreival end date. Defaults to current date. Start date is calculated in setup and set to 7 days prior to end date.
- **environment:** used to specify testing or production execution mode. Main difference is the table new data is inserted into. Default choices are "dev" and "prod"
- **push (optional):** tells the script whether the resulting plot is to be pushed to the Plotly hosting service. Passing the string "push" to this argument will set the setup.py variable `push` to `True`. If no value is passed to this argument, it is set by default to `False`. When set to `False`, the plot will not be pushed to a host, but will display locally upon execution.
