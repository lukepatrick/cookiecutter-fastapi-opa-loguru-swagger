
# Logging
In the api, there should never be a `print` statement. All information that is necessary for debugging and checking operations should be logged with an appropriate level. 
## Std library
[loguru](https://github.com/Delgan/loguru) - This is the logging library that should be used throughout

## What not to log?
1. full passwords - Never, ever, ever log full passwords. It is acceptable to log the last few characters of the password for debugging purposes, but this should be done with extreme caution.

## What level should I choose when I log?

**Debug** - log at this level about anything that happens in the program. This is mostly used during debugging, and I’d advocate trimming down the number of debug statement before entering the production stage, so that only the most meaningful entries are left, and can be activated during troubleshooting.

**Info** - log at this level all actions that are user-driven, or system specific (ie regularly scheduled operations…)

**Warning** - log at this level all events that could potentially become an error. For instance if one database call took more than a predefined time, or if an in-memory cache is near capacity. This will allow proper automated alerting, and during troubleshooting will allow to better understand how the system was behaving before the failure.

**ERROR** - log every error condition at this level. That can be API calls that return errors or internal error conditions.

**FATAL** - too bad, it’s doomsday. Use this very scarcely, this shouldn’t happen a lot in a real program. Usually logging at this level signifies the end of the program. For instance, if a network daemon can’t bind a network socket, log at this level and exit is the only sensible thing to do.