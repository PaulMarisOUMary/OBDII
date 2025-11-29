from functools import partial

from .group_commands import GroupCommands

from ..command import Command, Template
from ..mode import Mode


M = Mode.AT
C = partial(Command, M, expected_bytes=0x00, min_values=None, max_values=None, units=None)
t = Template

# ELM327.pdf (DSL) | AT Command Summary | Page 11 - 12

class ModeAT(GroupCommands, registry_id=M):
    """AT Commands"""

    # General Commands
    REPEAT = Command(Mode.NONE, '')
    """Repeat the last command"""
    BAUDRATE_DIVISOR = C(t("BRD {hh}"))
    """Try Baude Rate Divisor hh"""
    SET_BAUDRATE_TIMEOUT = C(t("BRT {hh}"))
    """Set Baud Rate Timeout"""
    TO_DEFAULT = C('D')
    """Set all to defaults"""
    ECHO_OFF = C("E0")
    """Echo off"""
    ECHO_ON = C("E1")
    """Echo on"""
    FORGET_EVENTS = C("FE")
    """Forget Events"""
    VERSION_ID = C('I')
    """Print the version ID"""
    LINEFEED_OFF = C("L0")
    """Linefeeds off"""
    LINEFEED_ON = C("L1")
    """Linefeeds on"""
    LOWPOWER = C("LP")
    """Go to Low Power mode"""
    MEMORY_OFF = C("M0")
    """Memory off"""
    MEMORY_ON = C("M0")
    """Memory on"""
    READ_STORED = C("RD")
    """Read the stored Data"""
    SAVE_DATA = C(t("SD {hh}"))
    """Save Data byte hh"""
    SOFT_RESET = C("WS")
    """Warm Start (quick software reset)"""
    RESET = C('Z')
    """Reset all"""
    DESCRIPTION = C("@1")
    """Display device description"""
    IDENTIFIER = C("@2")
    """Display device identifier"""
    STORE_ID = C(t("@3 {cccccccccccc}"))
    """Stores the @2 device identifier"""

    # Programmable Parameter Commands
    PROG_PARAM_OFF = C(t("PP {xx:str} OFF"))
    """Disable Prog Parameter xx"""
    PROG_PARAMS_OFF = C("PP FF OFF")
    """All Prog Parameters off"""
    PROG_PARAM_ON = C(t("PP {xx:str} ON"))
    """Enable Prog Parameter xx"""
    PROG_PARAMS_ON = C("PP FF ON")
    """All Prog Parameters on"""
    PROG_SET_PARAM = C(t("PP {xx:str} SV {yy:str}"))
    """For PP xx, Set the Value to yy"""
    PROG_SUMMARY = C("PPS")
    """Print a PP Summary"""

    # Voltage Reading Commands
    CALIBRATE_VOLTAGE = C(t("CV {dddd}"))
    """Calibrate the Voltage to dd.dd volts"""
    RESTORE_VOLTAGE = C("CV 0000")
    """Restore CV value to factory setting"""
    READ_VOLTAGE = C("RV")
    """Read the Voltage"""

    # Other
    IGN = C("IGN")
    """Read the IgnMon input level"""

    # OBD Command
    ALLOW_LONG = C("AL")
    """Allow Long (>7 bytes) messages"""
    ACTIVITY_MONITOR_COUNT = C("AMC")
    """Display Activity Monitor Count"""
    ACTIVITY_MONITOR_TIMEOUT = C(t("AMT {hh}"))
    """Set Activity Monitor Timeout to hh"""
    AUTO_RECEIVE = C("AR")
    """Automatically Receive"""
    ADAP_TIMING_OFF = C("AT0")
    """Adaptive Timing off"""
    ADAP_TIMING_1 = C("AT1")
    """Adaptive Timing Auto1"""
    ADAP_TIMING_2 = C("AT2")
    """Adaptive Timing Auto2"""
    BUFFER_DUMP = C("BD")
    """Perform a Buffer Dump"""
    BYPASS_INIT = C("BI")
    """Bypass the Initialization sequence"""
    DESC_PROTOCOL = C("DP")
    """Describe the current Protocol"""
    DESC_PROTOCOL_N = C("DPN")
    """Describe the Protocol by Number"""
    FILTER_TRANSMITTER_OFF = C("FT")
    """Filter Transmitter off"""
    FILTER_TRANSMITTER_ON = C(t("FT {hh}"))
    """Filter for Transmitter = hh"""
    HEADERS_OFF = C("H0")
    """Headers off"""
    HEADERS_ON = C("H1")
    """Headers on"""
    IS_PROTOCOL_ACTIVE = C("IA")
    """Is the Protocol active"""
    MONITOR_ALL = C("MA")
    """Monitor All"""
    MONITOR_RECEIVER = C(t("MR {hh}"))
    """Monitor for Receiver = hh"""
    MONITOR_TRANSMITTER = C(t("MT {hh}"))
    """Monitor for Transmitter = hh"""
    NORMAL_LENGTH = C("NL")
    """Normal Length messages"""
    PROTOCOL_CLOSE = C("PC")
    """Protocol Close"""
    RESPONSES_OFF = C("R0")
    """Responses off"""
    RESPONSES_ON = C("R1")
    """Responses on"""
    SET_RECEIVE_ADDR = C(t("RA {hh}"))
    """Set Receive Address to hh"""
    SPACES_OFF = C("S0")
    """Printing of Spaces off"""
    SPACES_ON = C("S1")
    """Printing of Spaces on"""
    SET_HEADER = C(t("SH {x}{y}{z}"))
    """Set Header to xyz"""
    SET_HEADER_LONG = C(t("SH {xx}{yy}{zz}"))
    """Set Header to xxyyzz"""
    SET_PROTOCOL = C(t("SP {h}"))
    """Set Protocol to h and save it"""
    SET_PROTOCOL_AUTO = C(t("SP A{h}"))
    """Set Protocol to Auto, h and save it"""
    PROTOCOL_ERASE = C("SP 00")
    """Erase stored protocol"""
    SET_RECEIVE_ADDR_ALT = C(t("SR {hh}"))
    """Set the receive address to hh"""
    STANDARD_SEARCH = C("SS")
    """Use Standard Search order (J1978)"""
    SET_TIMEOUT = C(t("ST {hh}"))
    """Set Timeout to hh x 4 msec"""
    SET_TESTER_ADDR = C(t("TA {hh}"))
    """Set Tester Address to hh"""
    TRY_PROTOCOL = C(t("TP {h}"))
    """Try Protocol h"""
    TRY_PROTOCOL_AUTO = C(t("TP A{h}"))
    """Try Protocol h with Auto search"""

    # J1850 Specific Commands (protocols 6 to C)
    IFR_OFF = C("IFR0")
    """IFRs off if not monitoring"""
    IFR_AUTO = C("IFR1")
    """IFRs Auto if not monitoring"""
    IFR_ON = C("IFR2")
    """IFRs on if not monitoring"""
    IFR_OFF_ALWAYS = C("IFR4")
    """IFRs off at all times"""
    IFR_AUTO_ALWAYS = C("IFR5")
    """IFRs auto at all times"""
    IFR_ON_ALWAYS = C("IFR6")
    """IFRs on at all times"""
    IFR_HEADER = C("IFR H")
    """IFR value from Header"""
    IFR_SOURCE = C("IFR S")
    """IFR value from Source"""

    # ISO Specific Commands (protocols 3 to 5)
    FAST_INIT = C("FI")
    """Perform a Fast Initiation"""
    SET_BAUDRATE_10400 = C("IB 10")
    """Set the ISO Baud rate to 10400"""
    SET_BAUDRATE_12500 = C("IB 12")
    """Set the ISO Baud rate to 12500"""
    SET_BAUDRATE_15625 = C("IB 15")
    """Set the ISO Baud rate to 15625"""
    SET_BAUDRATE_4800 = C("IB 48")
    """Set the ISO Baud rate to 4800"""
    SET_BAUDRATE_9600 = C("IB 96")
    """Set the ISO Baud rate to 9600"""
    SET_ISO_INIT_ADDR = C(t("IIA {hh}"))
    """Set ISO (slow) Init Address to hh"""
    KEY_WORDS = C("KW")
    """Display the Key Words"""
    KEY_WORD_OFF = C("KW0")
    """Key Word checking off"""
    KEY_WORD_ON = C("KW1")
    """Key Word checking on"""
    SLOW_INIT = C("SI")
    """Perform a Slow (5 baud) Initiation"""
    SET_WAKEUP = C(t("SW {hh}"))
    """Set Wakeup interval to hh x 20 msec"""
    SET_WAKEUP_STOP = C("SW 00")
    """Stop sending Wakeup messages"""
    # WAKEUP_MESSAGE = C(t("WM {xx xx xx xx xx xx}"))
    #"""Set the Wakeup Message"""
    
    # CAN Specific Commands
    CONFIRMATION_OFF = C("C0")
    """Send Confirmation off"""
    CONFIRMATION_ON = C("C1")
    """Send Confirmation on"""
    FORMAT_AUTO_OFF = C("CAF0")
    """Automatic Formatting off"""
    FORMAT_AUTO_ON = C("CAF1")
    """Automatic Formatting on"""
    CAN_EXT_ADDR_OFF = C("CEA")
    """Turn off CAN Extended Addressing"""
    CAN_EXT_ADDR = C(t("CEA {hh}"))
    """Use CAN Extended Address hh"""
    SET_CAN_EXT_ADDR_RX = C(t("CER {hh}"))
    """Set CAN Extended Rx address to hh"""
    SET_ID_FILTER = C(t("CF {hhh}"))
    """Set the ID Filter to hhh"""
    SET_ID_FILTER_LONG = C(t("CF {hhhhhhhh}"))
    """Set the ID Filter to hhhhhhhh"""
    FLOW_CONTROLS_OFF = C("CFC0")
    """Flow Controls off"""
    FLOW_CONTROLS_ON = C("CFC1")
    """Flow Controls on"""
    SET_ID_MASK = C(t("CM {hhh}"))
    """Set the ID Mask to hhh"""
    SET_ID_MASK_LONG = C(t("CM {hhhhhhhh}"))
    """Set the ID Mask to hhhhhhhh"""
    SET_CAN_PRIORITY = C(t("CP {hh}"))
    """Set CAN Priority to hh (29 bit)"""
    SET_CAN_ADDR = C(t("CRA {hhh}"))
    """Set CAN Receive Address to hhh"""
    SET_CAN_ADDR_LONG = C(t("CRA {hhhhhhhh}"))
    """Set CAN Receive Address to hhhhhhhh"""
    CAN_STATUS = C("CS")
    """Show the CAN Status counts"""
    SILENT_MONITORING_OFF = C("CSM0")
    """Silent Monitoring off"""
    SILENT_MONITORING_ON = C("CSM1")
    """Silent Monitoring on"""
    SET_TIMER_MULTIPLIER_1 = C("CTM1")
    """Set Timer Multiplier to 1"""
    SET_TIMER_MULTIPLIER_5 = C("CTM5")
    """Set Timer Multiplier to 5"""
    DLC_OFF = C("D0")
    """Display of the DLC off"""
    DLC_ON = C("D1")
    """Display of the DLC on"""
    SET_FLOW_CONTROL_MODE = C(t("FC SM {h}"))
    """Flow Control, Set the Mode to h"""
    SET_FLOW_CONTROL_HEADER = C(t("FC SH {hhh}"))
    """Flow Control, Set the Header to hhh"""
    SET_FLOW_CONTROL_HEADER_LONG = C(t("FC SH {hhhhhhhh}"))
    """Flow Control, Set the Header to hhhhhhhh"""
    # SET_FLOW_CONTROL_DATA = C(t("FC SD {xx xx xx xx xx}"))
    #"""Flow Control, Set Data to [...]"""
    PROTOCOL_B_BAUDRATE = C(t("PB {xx} {yy}"))
    """Protocol B options and baud rate"""
    RTR_MESSAGE = C("RTR")
    """Send an RTR message"""
    VARIABLE_DLC_OFF = C("V0")
    """Use of Variable DLC off"""
    VARIABLE_DLC_ON = C("V1")
    """Use of Variable DLC on"""
    
    # J1939 CAN Specific Commands
    MONITOR_DM1 = C("DM1")
    """Monitor for DM1 messages"""
    FORMAT_ELM = C("JE")
    """Use J1939 Elm data format"""
    FORMAT_HEADER_OFF = C("JHF0")
    """Header Formatting off"""
    FORMAT_HEADER_ON = C("JHF1")
    """Header Formatting on"""
    FORMAT_SAE = C("JS")
    """Use J1939 SAE data format"""
    J_SET_TIMER_MULTIPLIER_1 = C("JTM1")
    """Set timer multiplier to 1"""
    J_SET_TIMER_MULTIPLIER_5 = C("JTM5")
    """Set timer multiplier to 5"""
    MONITOR_PGN = C(t("MP {hhhh}"))
    """Monitor for PGN 0hhhh"""
    MONITOR_PGN_N = C(t("MP {hhhh} {n}"))
    """“ “ and get n messages"""
    MONITOR_PGN_LONG = C(t("MP {hhhhhh}"))
    """Monitor for PGN hhhhhh"""
    MONITOR_PGN_LONG_N = C(t("MP {hhhhhh} {n}"))
    """“ “ and get n messages"""