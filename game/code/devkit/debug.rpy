init -999 python:
    ## Should we enable the use of developer tools? This should be
    ## set to False before the game is released, so the user can't
    ## cheat using developer tools.
    config.developer = True
    # config.debug = False

    DEBUG = True # General debugging.
    DEBUG_LOG = True # Logging general. Crash if devlog is used and this is False.
    DEBUG_PROFILING = False # Loading time of various game elements.
    DEBUG_INTERACTIONS = False

    DEBUG_CHARS = False
    def char_debug(msg, mode="warning"):
        if DEBUG_CHARS:
            func = getattr(devlog, mode)
            func("|CHAR DEBUG| {}".format(msg))

    # Qeust/Events
    DEBUG_QE = False # Debug Quests and Events
    def qe_debug(msg, mode="info"):
        if DEBUG_QE:
            func = getattr(devlog, mode)
            func("|CHAR DEBUG| {}".format(msg))

    # SimPy:
    DEBUG_SIMPY = False
    DEBUG_SIMPY_ND_BUILDING_REPORT = DSNBR = False
    def simpy_debug(msg):
        if DEBUG_SIMPY:
            devlog.info("|SIMPY DEBUG| {}".format(msg))

    DEBUG_ND = False
    def nd_debug(msg, mode="info"):
        if DEBUG_ND:
            func = getattr(devlog, mode)
            func("|ND DEBUG| {}".format(msg))

    # Item systems:
    DEBUG_AUTO_ITEM = False
    def aeq_debug(msg):
        if DEBUG_AUTO_ITEM:
            devlog.info("|AEQ DEBUG| {}".format(msg))

    # Battle Engine:
    DEBUG_BE = True
    def be_debug(msg):
        if DEBUG_BE:
            devlog.info("|BE DEBUG| {}".format(msg))

    # Simulated exploration:
    DEBUG_SE = False

label debug_callstack:
    return
