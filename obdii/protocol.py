from enum import Enum


class Protocol(Enum):
    UNKNOWN = -1
    """Unknown protocol"""

    AUTO = 0x00
    """Automatically determine the protocol"""
    SAE_J1850_PWM = 0x01
    """SAE J1850 PWM (41.6 kbaud)"""
    SAE_J1850_VPW = 0x02
    """SAE J1850 VPW (10.4 kbaud)"""
    ISO_9141_2 = 0x03
    """ISO 9141-2 (5 baud init, 10.4 kbaud)"""
    ISO_14230_4_KWP = 0x04
    """ISO 14230-4 KWP (5 baud init, 10.4 kbaud)"""
    ISO_14230_4_KWP_FAST = 0x05
    """ISO 14230-4 KWP (fast init, 10.4 kbaud)"""
    ISO_15765_4_CAN = 0x06
    """ISO 15765-4 CAN (11 bit ID, 500 kbaud)"""
    ISO_15765_4_CAN_B = 0x07
    """ISO 15765-4 CAN (29 bit ID, 500 kbaud)"""
    ISO_15765_4_CAN_C = 0x08
    """ISO 15765-4 CAN (11 bit ID, 250 kbaud)"""
    ISO_15765_4_CAN_D = 0x09
    """ISO 15765-4 CAN (29 bit ID, 250 kbaud)"""
    SAE_J1939_CAN = 0x0A
    """SAE J1939 CAN (29 bit ID, 250* kbaud), default settings (user adjustable)"""
    USER1_CAN = 0x0B
    """USER1 CAN (11* bit ID, 125* kbaud), default settings (user adjustable)"""
    USER2_CAN = 0x0C
    """USER2 CAN (11* bit ID, 50* kbaud), default settings (user adjustable)"""