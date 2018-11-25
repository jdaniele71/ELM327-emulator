python-ELM
==========

A python simulator for the ELM327 OBD-II adapter. Built for testing [python-OBD](https://github.com/brendanwhitfield/python-OBD).

This simulator can process basic examples in [*python-OBD* documentation](https://python-obd.readthedocs.io/en/latest/) and reproduces a limited message flow
generated by a Toyota Auris Hybrid car, including some custom messages.

Run with:

```shell
python -m elm
```

Tested with Python 3.7. Python 2 is not supported.

The serial port to be used by the application interfacing the simulator is displayed in the first output line. E.g.,:

    Running on /dev/pts/1

Logging is controlled through `elm.yaml` (in the current directory by default). Its path can be set through the *ELM_LOG_CFG* environment variable.

A [dictionary](https://docs.python.org/3.7/tutorial/datastructures.html#dictionaries) is used to define commands and pids. The dictionary includes more sections (named scenarios):

- `'AT'`: supported AT commands
- `'default'`: supported default pids
- `'test'`: different values for some of the default pids
- any additional custom section can be used to define specific scenarios

Default settings include both the 'AT' and the 'default' scenarios.

The dictionary used to parse each ELM command is dynamically built as a union of three defined scenarios in the following order: 'default', 'AT', custom scenario (when applied).

Each subsequent scenario rededefine commands of the previousy ones. In principle, 'AT scenario is added to 'default' and, if a custom scenario is used, this is also added on top.

If `emulator.scenario` is set to a string different from *default*, the custom scenario set by the string is applied; any key defined in the custom scenario replaces the default settings ('AT' and 'default' scenarios).

Allowed keys to be used in the dictionary:

- `'Pid'`: short pid description
- `'Descr'`: shall be set to a string describing the pid
- `'Exec'`: command to be executed
- `'Log'`: logging.debug argument
- `'ResponseFooter'`: run a funtion and returns a footer to the response
- `'ResponseHeader'`: run a funtion and returns a header to the response
- `'Response'`: returned bytes 
- `'Action'`: can be set to 'skip' in order to skip the processing of the pid
- `'Header'`: not used

The simulator provides a trivial monitoring front-end, supporting command line strings and a backend thread executing the actual process.

At the prompt '*Enter command:*', the simulator accepts the following commands:

- `q` = quit
- `c` = print the number of executed commands
- `p` = pause
- `i` = toggle prompt off/on
- `r` = resume
- `s <n>` = delay the execution of the next command of <n> seconds
- `o` = switch to 'engineoff' scenario (`emulator.scenario='engineoff'`)
- `t` = switch to 'test' scenario (`emulator.scenario='test'`)
- `d` = reset to 'default' scenario (`emulator.scenario='default'`)
- `emulator.scenario='name of the new scenario'`
- any other Python command can be used to query/configure the backend thread

The dictionary can be used to build a workflow. The front-end can be controlled by an external piped automator.

