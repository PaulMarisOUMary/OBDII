from functools import partial

from ..basetypes import BaseMode, Command, Mode

M = Mode.AT
C = partial(Command, M, min_values=None, max_values=None, units=None)

# ELM327.pdf | AT Command Summary | Page 8 - 9

class ModeAT(BaseMode):
    """AT Commands"""

    # General Commands
    REPEAT = Command(Mode.NONE, '', 0x00, "REPEAT", "Repeat the last command")
    BAUDRATE_DIVISOR = C("BRD {hh}", 0x00, "BAUDRATE_DIVISOR", "Try Baude Rate Divisor hh", command_args={"hh": int})
    SET_BAUDRATE_TIMEOUT = C("BRT {hh}", 0x00, "SET_BAUDRATE_TIMEOUT", "Set Baud Rate Timeout", command_args={"hh": int})
    TO_DEFAULT = C('D', 0x00, "TO_DEFAULT", "Set all to defaults")
    ECHO_OFF = C("E0", 0x00, "ECHO_OFF", "Echo off")
    ECHO_ON = C("E1", 0x00, "ECHO_ON", "Echo on")
    FORGET_EVENTS = C("FE", 0x00, "FORGET_EVENTS", "Forget Events")
    VERSION_ID = C('I', 0x00, "VERSION_ID", "Print the version ID")
    LINEFEED_OFF = C("L0", 0x00, "LINEFEED_OFF", "Linefeeds off")
    LINEFEED_ON = C("L1", 0x00, "LINEFEED_ON", "Linefeeds on")
    LOWPOWER = C("LP", 0x00, "LOWPOWER", "Go to Low Power mode")
    MEMORY_OFF = C("M0", 0x00, "MEMORY_OFF", "Memory off")
    MEMORY_ON = C("M0", 0x00, "MEMORY_ON", "Memory on")
    READ_STORED = C("RD", 0x00, "READ_STORED", "Read the stored Data")
    SAVE_DATA = C("SD {hh}", 0x00, "SAVE_DATA", "Save Data byte hh", command_args={"hh": int})
    SOFT_RESET = C("WS", 0x00, "SOFT_RESET", "Warm Start (quick software reset)")
    RESET = C('Z', 0x00, "RESET", "Reset all")
    DESCRIPTION = C("@1", 0x00, "DESCRIPTION", "Display device description")
    IDENTIFIER = C("@2", 0x00, "IDENTIFIER", "Display device identifier")
    STORE_ID = C("@3 {cccccccccccc}", 0x00, "STORE_ID", "Stores the @2 device identifier", command_args={"cccccccccccc": int})

    # Programmable Parameter Commands
    PROG_PARAM_OFF = C("PP {xx} OFF", 0x00, "PROG_PARAM_OFF", "Disable Prog Parameter xx", command_args={"xx": str})
    PROG_PARAMS_OFF = C("PP FF OFF", 0x00, "PROG_PARAMS_OFF", "All Prog Parameters off")
    PROG_PARAM_ON = C("PP {xx} ON", 0x00, "PROG_PARAM_ON", "Enable Prog Parameter xx", command_args={"xx": str})
    PROG_PARAMS_ON = C("PP FF ON", 0x00, "PROG_PARAMS_ON", "All Prog Parameters on")
    PROG_SET_PARAM = C("PP {xx} SV {yy}", 0x00, "PROG_SET_PARAM", "For PP xx, Set the Value to yy", command_args={"xx": str, "yy": str})
    PROG_SUMMARY = C("PPS", 0x00, "PROG_SUMMARY", "Print a PP Summary")

    # Voltage Reading Commands
    CALIBRATE_VOLTAGE = C("CV {dddd}", 0x00, "CALIBRATE_VOLTAGE", "Calibrate the Voltage to dd.dd volts", command_args={"dddd": int})
    RESTORE_VOLTAGE = C("CV 0000", 0x00, "RESTORE_VOLTAGE", "Restore CV value to factory setting")
    READ_VOLTAGE = C("RV", 0x00, "READ_VOLTAGE", "Read the Voltage")

    # Other
    IGN = C("IGN", 0x00, "IGN", "read the IgnMon input level")

    # OBD Command
    ALLOW_LONG = C("AL", 0x00, "ALLOW_LONG", "Allow Long (>7 bytes) messages")
    AUTO_RECEIVE = C("AR", 0x00, "AUTO_RECEIVE", "Automatically Receive")
    ADAP_TIMING_OFF = C("AT0", 0x00, "ADAP_TIMING_OFF", "Adaptive Timing off")
    ADAP_TIMING_1 = C("AT1", 0x00, "ADAP_TIMING_1", "Adaptive Timing Auto1")
    ADAP_TIMING_2 = C("AT2", 0x00, "ADAP_TIMING_2", "Adaptive Timing Auto2")
    BUFFER_DUMP = C("BD", 0x00, "BUFFER_DUMP", "Perform a Buffer Dump")
    BYPASS_INIT = C("BI", 0x00, "BYPASS_INIT", "Bypass the Initialization sequence")
    DESC_PROTOCOL = C("DP", 0x00, "DESC_PROTOCOL", "Describe the current Protocol")
    DESC_PROTOCOL_N = C("DPN", 0x00, "DESC_PROTOCOL_N", "Describe the Protocol by Number")
    HEADERS_OFF = C("H0", 0x00, "HEADERS_OFF", "Headers off")
    HEADERS_ON = C("H1", 0x00, "HEADERS_ON", "Headers on")
    MONITOR_ALL = C("MA", 0x00, "MONITOR_ALL", "Monitor All")
    MONITOR_RECEIVER = C("MR {hh}", 0x00, "MONITOR_RECEIVER", "Monitor for Receiver = hh", command_args={"hh": int})
    MONITOR_TRANSMITTER = C("MT {hh}", 0x00, "MONITOR_TRANSMITTER", "Monitor for Transmitter = hh", command_args={"hh": int})
    NORMAL_LENGTH = C("NL", 0x00, "NORMAL_LENGTH", "Normal Length messages")
    PROTOCOL_CLOSE = C("PC", 0x00, "PROTOCOL_CLOSE", "Protocol Close")
    RESPONSES_OFF = C("R0", 0x00, "RESPONSES_OFF", "Responses off")
    RESPONSES_ON = C("R1", 0x00, "RESPONSES_ON", "Responses on")
    SET_RECEIVE_ADDR = C("RA {hh}", 0x00, "SET_RECEIVE_ADDR", "Set Receive Address to hh", command_args={"hh": int})
    SPACES_OFF = C("S0", 0x00, "SPACES_OFF", "Printing of Spaces off")
    SPACES_ON = C("S1", 0x00, "SPACES_ON", "Printing of Spaces on")
    SET_HEADER = C("SH {x}{y}{z}", 0x00, "SET_HEADER", "Set Header to xyz", command_args={'x': str, 'y': str, 'z': str})
    SET_HEADER_LONG = C("SH {xx}{yy}{zz}", 0x00, "SET_HEADER_LONG", "Set Header to xxyyzz", command_args={"xx": str, "yy": str, "zz": str})
    SET_PROTOCOL = C("SP {h}", 0x00, "SET_PROTOCOL", "Set Protocol to h and save it", command_args={"h": int})
    SET_PROTOCOL_AUTO = C("SP A{h}", 0x00, "SET_PROTOCOL_AUTO", "Set Protocol to Auto, h and save it", command_args={"h": int})
    SET_RECEIVE_ADDR_ALT = C("SR {hh}", 0x00, "SET_RECEIVE_ADDR_ALT", "Set the receive address to hh", command_args={"hh": int})
    STANDARD_SEARCH = C("SS", 0x00, "STANDARD_SEARCH", "Use Standard Search order (J1978)")
    SET_TIMEOUT = C("ST {hh}", 0x00, "SET_TIMEOUT", "Set Timeout to hh x 4 msec", command_args={"hh": int})
    SET_TESTER_ADDR = C("TA {hh}", 0x00, "SET_TESTER_ADDR", "Set Tester Address to hh", command_args={"hh": int})
    TRY_PROTOCOL = C("TP {h}", 0x00, "TRY_PROTOCOL", "Try Protocol h", command_args={"h": int})
    TRY_PROTOCOL_AUTO = C("TP A{h}", 0x00, "TRY_PROTOCOL_AUTO", "Try Protocol h with Auto search", command_args={"h": int})

    # ISO Specific Commands
    FAST_INIT = C("FI", 0x00, "FAST_INIT", "Perform a Fast Initiation")
    SET_BAUDRATE_10400 = C("IB 10", 0x00, "SET_BAUDRATE_10400", "Set the ISO Baud rate to 10400")
    SET_BAUDRATE_4800 = C("IB 48", 0x00, "SET_BAUDRATE_4800", "Set the ISO Baud rate to 4800")
    SET_BAUDRATE_9600 = C("IB 96", 0x00, "SET_BAUDRATE_9600", "Set the ISO Baud rate to 9600")
    SET_ISO_INIT_ADDR = C("IIA {hh}", 0x00, "SET_ISO_INIT_ADDR", "Set ISO (slow) Init Address to hh", command_args={"hh": int})
    KEY_WORDS = C("KW", 0x00, "KEY_WORDS", "Display the Key Words")
    KEY_WORD_OFF = C("KW0", 0x00, "KEY_WORD_OFF", "Key Word checking off")
    KEY_WORD_ON = C("KW1", 0x00, "KEY_WORD_ON", "Key Word checking on")
    SLOW_INIT = C("SI", 0x00, "SLOW_INIT", "Perform a Slow (5 baud) Initiation")
    SET_WAKEUP = C("SW {hh}", 0x00, "SET_WAKEUP", "Set Wakeup interval to hh x 20 msec", command_args={"hh": int})
    # WAKEUP_MESSAGE = C("", 0x00, "WAKEUP_MESSAGE", "Set the Wakeup Message")

    # J1850 Specific Commands
    IFR_OFF = C("IFR0", 0x00, "IFR_OFF", "IFRs off")
    IFR_AUTO = C("IFR1", 0x00, "IFR_AUTO", "IFRs Auto")
    IFR_ON = C("IFR2", 0x00, "IFR_ON", "IFRs on")
    IFR_HEADER = C("IFR H", 0x00, "IFR_HEADER", "IFR value from Header")
    IFR_SOURCE = C("IFR S", 0x00, "IFR_SOURCE", "IFR value from Source")
    
    # CAN Specific Commands
    CAN_EXT_ADDR_OFF = C("CEA", 0x00, "CAN_EXT_ADDR_OFF", "Turn off CAN Extended Addressing")
    CAN_EXT_ADDR = C("CEA {hh}", 0x00, "CAN_EXT_ADDR", "Use CAN Extended Address hh", command_args={"hh": int})
    FORMAT_AUTO_OFF = C("CAF0", 0x00, "FORMAT_AUTO_OFF", "Automatic Formatting off")
    FORMAT_AUTO_ON = C("CAF0", 0x00, "FORMAT_AUTO_ON", "Automatic Formatting on")
    SET_ID_FILTER = C("CF {hhh}", 0x00, "SET_ID_FILTER", "Set the ID Filter to hhh", command_args={"hhh": int})
    SET_ID_FILTER_LONG = C("CF {hhhhhhhh}", 0x00, "SET_ID_FILTER_LONG", "Set the ID Filter to hhhhhhhh", command_args={"hhhhhhhh": int})
    FLOW_CONTROLS_OFF = C("CFC0", 0x00, "FLOW_CONTROLS_OFF", "Flow Controls off")
    FLOW_CONTROLS_ON = C("CFC1", 0x00, "FLOW_CONTROLS_ON", "Flow Controls on")
    SET_ID_MASK = C("CM {hhh}", 0x00, "SET_ID_MASK", "Set the ID Mask to hhh", command_args={"hhh": int})
    SET_ID_MASK_LONG = C("CM {hhhhhhhh}", 0x00, "SET_ID_MASK_LONG", "Set the ID Mask to hhhhhhhh", command_args={"hhhhhhhh": int})
    SET_CAN_PRIORITY = C("CP {hh}", 0x00, "SET_CAN_PRIORITY", "Set CAN Priority to hh (29 bit)", command_args={"hh": int})
    SET_CAN_ADDR = C("CRA {hhh}", 0x00, "SET_CAN_ADDR", "Set CAN Receive Address to hhh", command_args={"hhh": int})
    SET_CAN_ADDR_LONG = C("CRA {hhhhhhhh}", 0x00, "SET_CAN_ADDR_LONG", "Set CAN Receive Address to hhhhhhhh", command_args={"hhhhhhhh": int})
    CAN_STATUS = C("CS", 0x00, "CAN_STATUS", "Show the CAN Status counts")
    DLC_OFF = C("D0", 0x00, "DLC_OFF", "Display of the DLC off")
    DLC_ON = C("D1", 0x00, "DLC_ON", "Display of the DLC on")
    SET_FLOW_CONTROL_MODE = C("FC SM {h}", 0x00, "SET_FLOW_CONTROL_MODE", "Flow Control, Set the Mode to h", command_args={"h": int})
    SET_FLOW_CONTROL_HEADER = C("FC SH {hhh}", 0x00, "SET_FLOW_CONTROL_HEADER", "Flow Control, Set the Header to hhh", command_args={"hhh": int})
    SET_FLOW_CONTROL_HEADER_LONG = C("FC SH {hhhhhhhh}", 0x00, "SET_FLOW_CONTROL_HEADER_LONG", "Flow Control, Set the Header to hhhhhhhh", command_args={"hhhhhhhh": int})
    # SET_FLOW_CONTROL_DATA = C("", 0x00, "SET_FLOW_CONTROL_DATA", "Flow Control, Set Data to [...]")
    PROTOCOL_B_BAUDRATE = C("PB {xx} {yy}", 0x00, "PROTOCOL_B_BAUDRATE", "Protocol B options and baud rate", command_args={"xx": str, "yy": str})
    RTR_MESSAGE = C("RTR", 0x00, "RTR_MESSAGE", "Send an RTR message")
    VARIABLE_DLC_OFF = C("V0", 0x00, "VARIABLE_DLC_OFF", "Use of Variable DLC off")
    VARIABLE_DLC_ON = C("V1", 0x00, "VARIABLE_DLC_ON", "Use of Variable DLC on")
    
    # J1939 CAN Specific Commands
    MONITOR_DM1 = C("DM1", 0x00, "MONITOR_DM1", "Monitor for DM1 messages")
    FORMAT_ELM = C("JE", 0x00, "FORMAT_ELM", "Use J1939 Elm data format")
    FORMAT_SAE = C("JS", 0x00, "FORMAT_SAE", "Use J1939 SAE data format")
    MONITOR_PGN = C("MP {hhhh}", 0x00, "MONITOR_PGN", "Monitor for PGN 0hhhh", command_args={"hhhh": int})
    MONITOR_PGN_LONG = C("MP {hhhhhh}", 0x00, "MONITOR_PGN_LONG", "Monitor for PGN hhhhhh", command_args={"hhhhhh": int})