import threading
import logging
from .elm import ELM, THREAD
import time
import sys
from cmd import Cmd
import rlcompleter

class python_ELM(Cmd):

    __hiden_methods = ('do_EOF',)
    rlc = rlcompleter.Completer().complete
    ps = '\033[01;32mCMD>\033[00m '

    def __init__(self, emulator):
        self.emulator = emulator
        self.prompt_active = True
        Cmd.prompt = self.ps
        Cmd.__init__(self)

    def print_topics(self, header, cmds, cmdlen, maxcol):
        if not cmds:
            return
        self.stdout.write(
        "Available commands include the following list (type help <topic>"
        "\nfor more information on each command). Besides, any Python"
        "\ncommand isaccepted. Autocompletion is fully allowed."
        "\n=============================================================="
        "==\n")
        self.columnize(cmds, maxcol-1)
        self.stdout.write("\n")

    def emptyline(self):
        return

    def do_EOF(self, arg):
        sys.exit(0)

    def get_names(self):
        return [n for n in dir(self.__class__) if n not in self.__hiden_methods]

    def do_quit(self, arg):
        'Quit the emulator'
        sys.exit(0)

    def do_delay(self, arg):
        "Delay each command of the seconds specified in the argument.\n"\
        "(Floating point number; default is 0.5 seconds.)"
        delay = 0.5 if len(arg) == 0 else float(arg.split()[0])
        if delay > 0:
            print("Delaying each command of %s seconds" % delay)
            self.emulator.delay = delay
        else:
            print("Delay removed")
            self.emulator.delay = 0

    def do_wait(self, arg):
        "Perform an immediate sleep of the seconds specified in the argument.\n"\
        "(Floating point number; default is 10 seconds.)"
        delay = 10 if len(arg) == 0 else float(arg.split()[0])
        print("Sleeping for %s seconds" % delay)
        time.sleep(delay)

    def do_prompt(self, arg):
        "Toggle prompt off/on."
        self.prompt_active = not self.prompt_active
        print("Prompt %s" % repr(self.prompt_active))
        Cmd.prompt = self.ps if self.prompt_active else ''

    def do_reset(self, arg):
        "Reset the emulator (counters and variables)"
        self.emulator.set_defaults()
        print("Reset done.")

    def do_counters(self, arg):
        "Print the number of each executed PID (upper case names), the values\n"\
        "associated to some 'AT' PIDs, the unknown requests, the emulator response\n"\
        "delay, the total number of executed commands and the current scenario."
        if self.emulator.counters:
            print("PID Counters:")
            for i in sorted(self.emulator.counters):
                print("  {:20s} = {}".format(i, self.emulator.counters[i]))
        else:
            print("No counters available.")
        print("  {:20s} = {}".format("delay", self.emulator.delay))
        print("  {:20s} = {}".format("scenario", self.emulator.scenario))

    def do_pause(self, arg):
        "Pause the execution."
        self.emulator.threadState = THREAD.PAUSED
        print("Backend emulator paused")

    def do_resume(self, arg):
        "Resume the execution after pausing; prints the used device."
        self.emulator.threadState = THREAD.ACTIVE
        print("Backend emulator resumed. Running on %s" % pts_name)

    scenarios = [
        'default',
        'test',
        'off',
        'car',
    ]

    def complete_scenario(self, text, line, start_index, end_index):
        if text:
            return [sc for sc in self.scenarios if sc.startswith(text)]
        else:
            return self.scenarios

    def do_scenario(self, arg):
        "Switch to the scenario specified in the argument; if the scenario is "\
        "missing or invalid, defaults to 'test'."
        self.emulator.scenario = 'test' if len(arg) == 0 else arg.split()[0]
        print("Emulator scenario switched to '%s'" % self.emulator.scenario)

    def do_off(self, arg):
        "Switch to 'engineoff' scenario"
        self.emulator.scenario='engineoff'
        print("Emulator scenario switched to '%s'" % self.emulator.scenario)

    def do_default(self, arg):
        "Reset to 'default' scenario"
        self.emulator.scenario='default'
        print("Emulator scenario reset to '%s'" % self.emulator.scenario)

    # completedefault and completenames manage autocompletion of Python
    # identifiers and namespaces
    def completedefault(self, text, line, begidx, endidx):
        return [self.rlc(text,x) for x in range(200)]

    def completenames(self, text, *ignored):
        dotext = 'do_'+text
        if not text:
            return [a[3:] for a in self.get_names() if a.startswith(dotext)]
        return [a[3:] for a in self.get_names() if a.startswith(dotext)
                ] + [self.rlc(text, x) for x in range(200)]

    # Execution of unrecognized commands
    def default(self, arg):
        try:
            print ( eval(arg) )
        except Exception:
            try:
                exec(arg)
            except Exception as e:
                print("Error executing command: %s" % e)


if __name__ == '__main__':
    try:
        emulator = ELM(None, None)
        with emulator as pts_name:
            while emulator.threadState == THREAD.STARTING:
                time.sleep(0.1)
            sys.stdout.flush()
            p_elm = python_ELM(emulator)
            p_elm.cmdloop('Welcome to the ELM327 OBD-II adapter emulator.\n'
                          'ELM327-emulator running on %s\n'
                          'Type help or ? to list commands.\n' % pts_name)
    except (KeyboardInterrupt, SystemExit):
        print('\n\nExiting.\n')
        sys.exit(0)
    sys.exit(1)