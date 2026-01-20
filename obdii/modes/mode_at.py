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

    # AT Command Descriptions | Page 12 - 30

    # General Commands
    REPEAT = Command(Mode.NONE, '')
    """Repeat the last AT or OBD command performed"""
    SET_BAUDRATE_DIVISOR = C(t("BRD {hh}"))
    """Try to set the RS232 baud rate divisor where the rate in kbps is 4000 divided by hh, with automatic fallback on failure"""
    SET_BAUDRATE_TIMEOUT = C(t("BRT {hh}"))
    """Set the baud rate handshake timeout, where the delay is hh multiplied by 5.0ms (00 selects the maximum timeout)"""
    RESET_DEFAULTS = C('D')
    """Restore all settings, including protocol, headers, filters, masks and timers to their factory default values"""
    ECHO_OFF = C("E0")
    """Disable echoing of characters received on the RS232 port back to the host computer"""
    ECHO_ON = C("E1")
    """Enable echoing of characters received on the RS232 port back to the host computer"""
    FORGET_EVENTS = C("FE")
    """Clear internal event flags, such as fatal CAN errors or low voltage resets, that may block protocol searches"""
    VERSION_ID = C('I')
    """Display the device identification string and firmware version"""
    LINEFEED_OFF = C("L0")
    """Disable sending of a linefeed character after each carriage return"""
    LINEFEED_ON = C("L1")
    """Enable sending of a linefeed character after each carriage return"""
    LOWPOWER = C("LP")
    """Enter low power standby mode, reducing power consumption until awakened by activity or reset"""
    MEMORY_OFF = C("M0")
    """Disable the automatic saving of the last valid OBD protocol used"""
    MEMORY_ON = C("M1")
    """Enable the automatic saving of the last valid OBD protocol used to non-volatile memory"""
    READ_STORED = C("RD")
    """Retrieve the single byte of data previously stored in the non-volatile memory"""
    SAVE_DATA = C(t("SD {hh}"))
    """Store a single byte of data hh in non-volatile memory that will persist through power cycles"""
    RESET_SOFT = C("WS")
    """Perform a software reset restoring defaults while preserving baud rate settings"""
    RESET = C('Z')
    """Performs a complete hardware reset, restoring all settings and the default baud rate"""
    DESCRIPTION = C("@1")
    """Display the device description string of the ELM327"""
    DEVICE_ID = C("@2")
    """Display the stored 12-character device identifier previously programmed with @3, return an error if none is found"""
    STORE_DEVICE_ID = C(t("@3 {cccccccccccc}"))
    """Permanently store a 12-character device identifier in memory that cannot be altered once set"""

    # Programmable Parameter Commands
    PROG_PARAM_OFF = C(t("PP {hh} OFF"))
    """Disable the specified hh Programmable Parameter, reverting it to its factory default"""
    PROG_PARAMS_OFF = C("PP FF OFF")
    """Disable all Programmable Parameters and reverts them to factory defaults"""
    PROG_PARAM_ON = C(t("PP {hh} ON"))
    """Enable the specified hh Programmable Parameter, allowing its assigned value to override the factory default"""
    PROG_PARAMS_ON = C("PP FF ON")
    """Enable all Programmable Parameters at the same time"""
    PROG_SET_PARAM = C(t("PP {hh} SV {yy}"))
    """Assign the value yy to Programmable Parameter hh, the value takes effect only after the parameter is enabled with PP hh ON"""
    PROG_SUMMARY = C("PPS")
    """Display a summary of all Programmable Parameters, showing their values and whether they are enabled"""

    # Voltage Reading Commands
    CALIBRATE_VOLTAGE = C(t("CV {dddd}"))
    """Calibrate the ELM327 voltage reading to a specific reference value, where dddd represents dd.dd volts"""
    RESTORE_VOLTAGE = C("CV 0000")
    """Restore the ELM327 voltage calibration to the original factory setting"""
    READ_VOLTAGE = C("RV")
    """Read the current input voltage at pin 2 and converts it to a decimal string"""

    # Other
    IGNITION_LEVEL = C("IGN")
    """Read and report the logic level of the ignition monitor input at pin 15 (IgnMon), return ON for high and OFF for low"""

    # OBD Command
    LONG_MESSAGES_ON = C("AL")
    """Allow sending 8 byte messages and receiving unlimited length messages, bypassing the standard 7 byte limit"""
    ACTIVITY_MONITOR_COUNT = C("AMC")
    """Display the internal counter representing the time since OBD activity was last detected"""
    ACTIVITY_MONITOR_TIMEOUT = C(t("AMT {hh}"))
    """Set the Activity Monitor timeout period to hh before low power mode is triggered"""
    AUTO_RECEIVE = C("AR")
    """Automatically set the ELM327 to receive responses from the correct vehicle address based on the current message headers"""
    ADAP_TIMING_OFF = C("AT0")
    """Disable Adaptive Timing, forcing the timeout to always match the AT ST setting"""
    ADAP_TIMING_AUTO = C("AT1")
    """Enable Adaptive Timing (default), automatically adjusts timeouts based on vehicle response times"""
    ADAP_TIMING_AGGRESSIVE = C("AT2")
    """Enable a more aggressive version of Adaptive Timing, adjusting timeouts more quickly for slow-response vehicles"""
    BUFFER_DUMP = C("BD")
    """Dump the content of the 12 byte OBD message buffer, showing the length byte followed by the stored messages"""
    BYPASS_INIT = C("BI")
    """Activate the current OBD protocol by bypassing the protocol initialization or handshaking sequence"""
    DESC_PROTOCOL = C("DP")
    """Display a text description of the current active OBD protocol, indicating 'AUTO' if automatic detection is enabled"""
    DESC_PROTOCOL_N = C("DPN")
    """Display the number of the current active OBD protocol, prefixed with a 'A' if automatic detection is enabled"""
    FILTER_TRANSMITTER_OFF = C("FT")
    """Disable any active message filter for received OBD messages"""
    FILTER_TRANSMITTER_ON = C(t("FT {hh}"))
    """Enable filtering to only accept messages where the transmitter address matches hh"""
    HEADERS_OFF = C("H0")
    """Disable the display of header bytes in responses"""
    HEADERS_ON = C("H1")
    """Enable the display of header bytes, showing full message details including check digits and PCI bytes"""
    IS_PROTOCOL_ACTIVE = C("IA")
    """Return whether the ELM327 considers the current protocol to be active (connected), returning Y for yes or N for no"""
    MONITOR_ALL = C("MA")
    """Continuously monitor and display all messages on the OBD bus without responding, until interrupted via RS232 input"""
    MONITOR_RECEIVER = C(t("MR {hh}"))
    """Monitor the bus and display only messages sent to the specified receiver address hh, until interrupted via RS232 input"""
    MONITOR_TRANSMITTER = C(t("MT {hh}"))
    """Monitor the bus and display only messages sent by the specified transmitter address hh, until interrupted via RS232 input"""
    LONG_MESSAGES_OFF = C("NL")
    """Restrict message length to the standard OBD limit of 7 bytes (reverse AT AL)"""
    PROTOCOL_CLOSE = C("PC")
    """Forcibly stop and deactivate the current protocol"""
    RESPONSES_OFF = C("R0")
    """Disable automatic reception of vehicle responses, allowing commands to be sent blindly"""
    RESPONSES_ON = C("R1")
    """Enable automatic reception and display of vehicle responses (default)"""
    SET_RECEIVE_ADDR = C(t("RA {hh}"))
    """Set the receive address to hh, disabling auto receive and accepting only messages addressed to hh"""
    SPACES_OFF = C("S0")
    """Disable space characters insertion in responses"""
    SPACES_ON = C("S1")
    """Enable space characters insertion between hex bytes in responses for better readability"""
    SET_HEADER_11 = C(t("SH {x}{y}{z}"))
    """Set a 3 digit 11 bit CAN identifier (header), leading zeros are added automatically"""
    SET_HEADER = C(t("SH {xx}{yy}{zz}"))
    """Set a 3 byte message header"""
    SET_HEADER_29 = C(t("SH {ww}{xx}{yy}{zz}"))
    """Set a CAN 29 bit message header using 4 bytes"""
    SET_PROTOCOL = C(t("SP {h}"))
    """Set the protocol to h and saves it as the new default in EEPROM, if set to 0, select automatic protocol detection"""
    SET_PROTOCOL_AUTO = C(t("SP A{h}"))
    """Set the protocol to h while enabling automatic detection on failure"""
    PROTOCOL_ERASE = C("SP 00")
    """Set the protocol to automatic detection and clear the stored protocol from EEPROM"""
    SET_RECEIVE_ADDR_ALT = C(t("SR {hh}"))
    """Set the receive address to hh, disabling auto receive and accepting only messages addressed to hh (identical to AT RA)"""
    STANDARD_SEARCH = C("SS")
    """Use the SAE J1978 standard protocol search sequence for initiating connections"""
    SET_TIMEOUT = C(t("ST {hh}"))
    """Set response timeout to hh * 4ms"""
    SET_TESTER_ADDR = C(t("TA {hh}"))
    """Temporarily set the tester (scan tool) address to hh, overriding the default PP 06 value"""
    TRY_PROTOCOL = C(t("TP {h}"))
    """Attempts to use protocol h without saving it to EEPROM"""
    TRY_PROTOCOL_AUTO = C(t("TP A{h}"))
    """Attempts to use protocol h without saving it to EEPROM while enabling automatic detection on failure"""

    # J1850 Specific Commands (protocols 6 to C)
    IFR_OFF = C("IFR0")
    """Disable all In-Frame Responses while not monitoring"""
    IFR_AUTO = C("IFR1")
    """Send In-Frame Responses if the message is correct and the 'K' bit allows it while not monitoring (default)"""
    IFR_ON = C("IFR2")
    """Always send In-Frame Responses regardless of message errors while not monitoring"""
    IFR_OFF_ALWAYS = C("IFR4")
    """Disable all In-Frame Responses, even during monitoring"""
    IFR_AUTO_ALWAYS = C("IFR5")
    """Send In-Frame Responses if the message is correct and the 'K' bit allows it"""
    IFR_ON_ALWAYS = C("IFR6")
    """Always send In-Frame Responses regardless of message errors or monitoring state"""
    IFR_HEADER = C("IFR H")
    """Use the header's source byte for the In-Frame Response (default)"""
    IFR_SOURCE = C("IFR S")
    """Use the source (tester) address for the In-Frame Response instead of the value in the header"""

    # ISO Specific Commands (protocols 3 to 5)
    FAST_INIT = C("FI")
    """Performs a fast initiation sequence for ISO 14230-4 KWP, requires protocol 5 to be active"""
    SET_BAUDRATE_10400 = C("IB 10")
    """Sets the ISO 9141-2 and ISO 14230-4 baud rate to the default of 10400"""
    SET_BAUDRATE_12500 = C("IB 12")
    """Sets the ISO 9141-2 and ISO 14230-4 baud rate to 12500"""
    SET_BAUDRATE_15625 = C("IB 15")
    """Sets the ISO 9141-2 and ISO 14230-4 baud rate to 15625"""
    SET_BAUDRATE_4800 = C("IB 48")
    """Sets the ISO 9141-2 and ISO 14230-4 baud rate to 4800"""
    SET_BAUDRATE_9600 = C("IB 96")
    """Sets the ISO 9141-2 and ISO 14230-4 baud rate to 9600"""
    SET_ISO_INIT_ADDR = C(t("IIA {hh}"))
    """Sets the destination address for the ISO 9141-2 or ISO 14230-4 slow (5 baud) initiation sequence, default is $33"""
    KEY_WORDS = C("KW")
    """Display the two key word bytes received from the ECU during the initiation sequence"""
    KEY_WORD_OFF = C("KW0")
    """Disable key word checking, allowing initiation to proceed even if key word values are non-standard"""
    KEY_WORD_ON = C("KW1")
    """Enable standard key word checking during initiation sequences (default)"""
    SLOW_INIT = C("SI")
    """Perform a slow initiation sequence for ISO 9141-2 or ISO 14230-4 KWP (5 baud), requires protocol 3 or 4 to be active"""
    SET_WAKEUP = C(t("SW {hh}"))
    """Set the periodic wakeup messages interval to hh * 20 ms, keeps the ECU connection active, only supported for protocols 3, 4, and 5"""
    SET_WAKEUP_STOP = C("SW 00")
    """Stop sending periodic wakeup messages"""
    WAKEUP_MESSAGE = C(t("WM {xxxxxxxxxxxx}"))
    """Override the default periodic wakeup message, accepts 1 to 6 bytes"""
    
    # CAN Specific Commands
    CONFIRMATION_OFF = C("C0")
    """Disable confirmation of CAN message transmission errors, return to the prompt state a little quicker, requires an ELM327 >= 2.3"""
    CONFIRMATION_ON = C("C1")
    """Enable confirmation of CAN message transmission errors, requires an ELM327 >= 2.3"""
    FORMAT_AUTO_OFF = C("CAF0")
    """Disable CAN automatic formatting, requiring all CAN data bytes to be provided and displayed exactly as sent and received"""
    FORMAT_AUTO_ON = C("CAF1")
    """Enable CAN automatic formatting, automatically handling PCI bytes, padding, and simplifying CAN send and receive data"""
    CAN_EXT_ADDR_OFF = C("CEA")
    """Turn off CAN extended addressing and restores default receive address"""
    CAN_EXT_ADDR = C(t("CEA {hh}"))
    """Enable CAN extended addressing by inserting the hh value as the first data byte of all CAN messages that you send"""
    SET_CAN_EXT_ADDR_RX = C(t("CER {hh}"))
    """Set CAN extended receive address to hh"""
    SET_ID_FILTER = C(t("CF {hhh}"))
    """Set the CAN ID filter to hhh for 11bit identifiers, allowing only matching CAN messages to be received"""
    SET_ID_FILTER_LONG = C(t("CF {hhhhhhhh}"))
    """Set the CAN ID filter to hhhhhhhh for 29bit identifiers, allowing only matching CAN messages to be received"""
    FLOW_CONTROL_OFF = C("CFC0")
    """Disable automatic sending of CAN Flow Control and J1939 CTS messages"""
    FLOW_CONTROL_ON = C("CFC1")
    """Enable automatic sending of CAN Flow Control and J1939 CTS messages"""
    SET_ID_MASK = C(t("CM {hhh}"))
    """Set the 11bit CAN ID Mask to hhh where 1 signifies a required bit match, and 0 ignored"""
    SET_ID_MASK_LONG = C(t("CM {hhhhhhhh}"))
    """Set the 29bit CAN ID Mask to hhh where 1 signifies a required bit match, and 0 ignored"""
    SET_CAN_PRIORITY = C(t("CP {hh}"))
    """Set the 5 most significant bits of a 29bit CAN ID to hh for message priority, default is 18hex"""
    RESET_CAN_ADDR = C(t("CRA"))
    """Reset the CAN receive address filters to their default values"""
    SET_CAN_ADDR = C(t("CRA {hhh}"))
    """Set the CAN receive address to hhh, adjusting mask and filter to accept only matching 11bit IDs"""
    SET_CAN_ADDR_LONG = C(t("CRA {hhhhhhhh}"))
    """Set the CAN receive address to hhhhhhhh, adjusting mask and filter to accept only matching 29bit IDs"""
    CAN_STATUS = C("CS")
    """Display CAN transmit and receive error counts, with ELM327 >= 2.2 also show the current frequency of the signal at the CAN input"""
    SILENT_MONITORING_OFF = C("CSM0")
    """Disable CAN silent monitoring, allowing the ELM327 to send ACKs and interact with the bus"""
    SILENT_MONITORING_ON = C("CSM1")
    """Enable CAN silent monitoring, preventing the ELM327 from sending ACKs or altering bus traffic"""
    SET_TIMER_MULTIPLIER_1 = C("CTM1")
    """Set the timeout multiplier to 1 for all CAN protocols (default)"""
    SET_TIMER_MULTIPLIER_5 = C("CTM5")
    """Set the timeout multiplier to 5 for all CAN protocols"""
    DLC_OFF = C("D0")
    """Disable display of the CAN Data Length Code"""
    DLC_ON = C("D1")
    """Enable display of the CAN Data Length Code"""
    SET_FLOW_CONTROL_MODE = C(t("FC SM {h}"))
    """Set the Flow Control response mode to h, 0 = fully automatic, 1 = user defined, 2 = user defined data"""
    SET_FLOW_CONTROL_HEADER = C(t("FC SH {hhh}"))
    """Set the Flow Control CAN header to hhh for 11bit IDs"""
    SET_FLOW_CONTROL_HEADER_LONG = C(t("FC SH {hhhhhhhh}"))
    """Set the Flow Control CAN header to hhhhhhhh for 29bit IDs"""
    SET_FLOW_CONTROL_DATA = C(t("FC SD {xxxxxxxxxx}"))
    """Set 1-5 bytes for CAN Flow Control messages, used only in Flow Control modes 1 or 2"""
    PROTOCOL_B_BAUDRATE = C(t("PB {xx} {yy}"))
    """Set Protocol B parameters xx and yy, overriding PP 2C and PP 2D values for the next initialization without changing stored programmable parameters"""
    RTR_MESSAGE = C("RTR")
    """Send a Remote Transmission Request message which contains no data bytes"""
    VARIABLE_DLC_OFF = C("V0")
    """Disable the forcing of variable data lengths for CAN messages (default)"""
    VARIABLE_DLC_ON = C("V1")
    """Forces the current CAN protocol to use variable data length messages"""
    
    # J1939 CAN Specific Commands
    MONITOR_DM1 = C("DM1")
    """Continuously monitors for J1939 Diagnostic Mode 1 (DM1) messages, including support for multi-segment transport protocols"""
    FORMAT_ELM = C("JE")
    """Enable J1939 ELM data format, automatically reversing byte order for PGN requests"""
    FORMAT_HEADER_OFF = C("JHF0")
    """Disable J1939 header formatting, displaying the ID information as four separate bytes"""
    FORMAT_HEADER_ON = C("JHF1")
    """Enable J1939 header formatting, isolating priority bits and grouping PGN information (default)"""
    FORMAT_SAE = C("JS")
    """Enable J1939 SAE data format, sending bytes in standard SAE (little-endian) order without reversal"""
    J_SET_TIMER_MULTIPLIER_1 = C("JTM1")
    """Sets the J1939 ST timer multiplier to 1"""
    J_SET_TIMER_MULTIPLIER_5 = C("JTM5")
    """Sets the J1939 ST timer multiplier to 5"""
    MONITOR_PGN = C(t("MP {hhhh}"))
    """Monitor for J1939 PGN hhhh"""
    MONITOR_PGN_N = C(t("MP {hhhh} {n}"))
    """Monitor for J1939 PGN hhhh, fetching n messages before stopping"""
    MONITOR_PGN_LONG = C(t("MP {hhhhhh}"))
    """Monitor for J1939 PGN hhhhhh"""
    MONITOR_PGN_LONG_N = C(t("MP {hhhhhh} {n}"))
    """Monitor for J1939 PGN hhhhhh, fetching n messages before stopping"""