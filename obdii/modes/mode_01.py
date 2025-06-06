from functools import partial

from .group_commands import GroupCommands

from ..command import Command
from ..mode import Mode
from ..parsers.formula import Formula, MultiFormula
from ..parsers.pids import SupportedPIDS


M = Mode.REQUEST
C = partial(Command, M)

F = Formula
MF = MultiFormula
SP = SupportedPIDS

# https://en.wikipedia.org/wiki/OBD-II_PIDs#Service_01_-_Show_current_data

class Mode01(GroupCommands):
    """Request Commands - OBD Mode 01 PIDs

    Abbreviations:
        ABS = Anti-lock Braking System
        AECD = Auxiliary Emission Control Device
        ALT = Alternative
        AUX = Auxiliary
        DIAG = Diagnostic
        DPF = Diesel Particulate Filter
        DTC = Diagnostic Trouble Code
        EGR = Exhaust Gas Recirculation
        EGT = Exhaust Gas Temperature
        EVAP = Evaporative System
        MAF = Mass Air Flow
        MAX = Maximum
        MIL = Malfunction Indicator Lamp
        NTE = Not-To-Exceed
        OBD = On-Board Diagnostics
        PERC = Percentage
        PID = Parameter ID
        SCR = Selective Catalytic Reduction
        TEMP = Temperature
        TURBO = Turbocharger
        VAC = Vacuum
        VGT = Variable Geometry Turbocharger
        WWH = World-Wide Harmonized
    """

    SUPPORTED_PIDS_A = C(0x00, 0x04, "SUPPORTED_PIDS_A", "PIDs supported [$01 - $20]", None, None, None, SP(0x01))
    STATUS_DTC = C(0x01, 0x04, "STATUS_DTC", "Monitor status since DTCs cleared. (Includes MIL status, DTC count, tests)", None, None, None)
    FREEZE_DTC = C(0x02, 0x02, "FREEZE_DTC", "DTC that caused freeze frame storage.", None, None, None)
    FUEL_STATUS = C(0x03, 0x02, "FUEL_STATUS", "Fuel system status", None, None, None)
    ENGINE_LOAD = C(0x04, 0x01, "ENGINE_LOAD", "Calculated engine load", 0, 100, '%', F("100/255*A"))
    ENGINE_COOLANT_TEMP = C(0x05, 0x01, "ENGINE_COOLANT_TEMP", "Engine coolant temperature", -40, 215, "°C", F("A-40"))
    SHORT_FUEL_TRIM_BANK_1 = C(0x06, 0x01, "SHORT_FUEL_TRIM_BANK_1", "Short term fuel trim (STFT)—Bank 1", -100, 99.2, '%', F("100/128*A-100"))
    LONG_FUEL_TRIM_BANK_1 = C(0x07, 0x01, "LONG_FUEL_TRIM_BANK_1", "Long term fuel trim (LTFT)—Bank 1", -100, 99.2, '%', F("100/128*A-100"))
    SHORT_FUEL_TRIM_BANK_2 = C(0x08, 0x01, "SHORT_FUEL_TRIM_BANK_2", "Short term fuel trim (STFT)—Bank 2", -100, 99.2, '%', F("100/128*A-100"))
    LONG_FUEL_TRIM_BANK_2 = C(0x09, 0x01, "LONG_FUEL_TRIM_BANK_2", "Long term fuel trim (LTFT)—Bank 2", -100, 99.2, '%', F("100/128*A-100"))
    FUEL_PRESSURE = C(0x0A, 0x01, "FUEL_PRESSURE", "Fuel pressure (gauge pressure)", 0, 765, "kPa", F("3*A"))
    INTAKE_PRESSURE = C(0x0B, 0x01, "INTAKE_PRESSURE", "Intake manifold absolute pressure", 0, 255, "kPa", F('A'))
    ENGINE_SPEED = C(0x0C, 0x02, "ENGINE_SPEED", "Engine speed", 0, 16383.75, "rpm", F("(256*A+B)/4"))
    VEHICLE_SPEED = C(0x0D, 0x01, "VEHICLE_SPEED", "Vehicle speed", 0, 255, "km/h", F('A'))
    IGNITION_TIMING_ADVANCE = C(0x0E, 0x01, "IGNITION_TIMING_ADVANCE", "Timing advance", -64, 63.5, "° before TDC", F("A/2-64"))
    INTAKE_AIR_TEMP = C(0x0F, 0x01, "INTAKE_AIR_TEMP", "Intake air temperature", -40, 215, "°C", F("A-40"))
    MAF_RATE = C(0x10, 0x02, "MAF_RATE", "Mass air flow sensor (MAF) air flow rate", 0, 655.35, "g/s", F("(256*A+B)/100")) 
    THROTTLE_POSITION = C(0x11, 0x01, "THROTTLE_POSITION", "Throttle position", 0, 100, '%', F("100/255*A"))
    STATUS_SECONDARY_AIR = C(0x12, 0x01, "STATUS_SECONDARY_AIR", "Commanded secondary air status", None, None, None) 
    OXYGEN_SENSORS_2_BANKS = C(0x13, 0x01, "OXYGEN_SENSORS_2_BANKS", "Oxygen sensors present (in 2 banks)", None, None, None) 
    OXYGEN_SENSOR_1 = C(0x14, 0x02, "OXYGEN_SENSOR_1", "Oxygen Sensor 1 A: Voltage B: Short term fuel trim", [0, -100], [1.275, 99.2], ['V', '%'], MF("A/200", "100/128*B-100"))
    OXYGEN_SENSOR_2 = C(0x15, 0x02, "OXYGEN_SENSOR_2", "Oxygen Sensor 2 A: Voltage B: Short term fuel trim", [0, -100], [1.275, 99.2], ['V', '%'], MF("A/200", "100/128*B-100"))
    OXYGEN_SENSOR_3 = C(0x16, 0x02, "OXYGEN_SENSOR_3", "Oxygen Sensor 3 A: Voltage B: Short term fuel trim", [0, -100], [1.275, 99.2], ['V', '%'], MF("A/200", "100/128*B-100"))
    OXYGEN_SENSOR_4 = C(0x17, 0x02, "OXYGEN_SENSOR_4", "Oxygen Sensor 4 A: Voltage B: Short term fuel trim", [0, -100], [1.275, 99.2], ['V', '%'], MF("A/200", "100/128*B-100"))
    OXYGEN_SENSOR_5 = C(0x18, 0x02, "OXYGEN_SENSOR_5", "Oxygen Sensor 5 A: Voltage B: Short term fuel trim", [0, -100], [1.275, 99.2], ['V', '%'], MF("A/200", "100/128*B-100"))
    OXYGEN_SENSOR_6 = C(0x19, 0x02, "OXYGEN_SENSOR_6", "Oxygen Sensor 6 A: Voltage B: Short term fuel trim", [0, -100], [1.275, 99.2], ['V', '%'], MF("A/200", "100/128*B-100"))
    OXYGEN_SENSOR_7 = C(0x1A, 0x02, "OXYGEN_SENSOR_7", "Oxygen Sensor 7 A: Voltage B: Short term fuel trim", [0, -100], [1.275, 99.2], ['V', '%'], MF("A/200", "100/128*B-100"))
    OXYGEN_SENSOR_8 = C(0x1B, 0x02, "OXYGEN_SENSOR_8", "Oxygen Sensor 8 A: Voltage B: Short term fuel trim", [0, -100], [1.275, 99.2], ['V', '%'], MF("A/200", "100/128*B-100"))
    OBD_STANDARDS = C(0x1C, 0x01, "OBD_STANDARDS", "OBD standards this vehicle conforms to", 1, 250, None)
    OXYGEN_SENSORS_4_BANKS = C(0x1D, 0x01, "OXYGEN_SENSORS_4_BANKS", "Oxygen sensors present (in 4 banks)", None, None, None) 
    STATUS_AUX_INPUT = C(0x1E, 0x01, "STATUS_AUX_INPUT", "Auxiliary input status (e.g. Power Take Off)", None, None, None)
    ENGINE_RUN_TIME = C(0x1F, 0x02, "ENGINE_RUN_TIME", "Run time since engine start", 0, 65535, 's', F("256*A+B"))

    SUPPORTED_PIDS_B = C(0x20, 0x04, "SUPPORTED_PIDS_B", "PIDs supported [$21 - $40]", None, None, None, SP(0x21))
    MIL_DISTANCE = C(0x21, 0x02, "MIL_DISTANCE", "Distance traveled with MIL on", 0, 65535, "km", F("256*A+B"))
    FUEL_RAIL_PRESSURE_VAC = C(0x22, 0x02, "FUEL_RAIL_PRESSURE_VAC", "Fuel Rail Pressure (relative to manifold vacuum)", 0, 5177.265, "kPa", F("0.079*(256*A+B)"))
    FUEL_RAIL_GAUGE_PRESSURE = C(0x23, 0x02, "FUEL_RAIL_GAUGE_PRESSURE", "Fuel Rail Gauge Pressure (diesel, or gasoline direct injection)", 0, 655350, "kPa", F("10*(256*A+B)"))
    OXYGEN_SENSOR_1_LAMBDA_VOLTAGE = C(0x24, 0x04, "OXYGEN_SENSOR_1_LAMBDA_VOLTAGE", "O2 Sensor 1 Equiv. Ratio (Lambda) & Voltage", [0, 0], [2, 8], ["ratio", 'V'], MF("2/65536*(256*A+B)", "8/65536*(256*C+D)"))
    OXYGEN_SENSOR_2_LAMBDA_VOLTAGE = C(0x25, 0x04, "OXYGEN_SENSOR_2_LAMBDA_VOLTAGE", "O2 Sensor 2 Equiv. Ratio (Lambda) & Voltage", [0, 0], [2, 8], ["ratio", 'V'], MF("2/65536*(256*A+B)", "8/65536*(256*C+D)"))
    OXYGEN_SENSOR_3_LAMBDA_VOLTAGE = C(0x26, 0x04, "OXYGEN_SENSOR_3_LAMBDA_VOLTAGE", "O2 Sensor 3 Equiv. Ratio (Lambda) & Voltage", [0, 0], [2, 8], ["ratio", 'V'], MF("2/65536*(256*A+B)", "8/65536*(256*C+D)"))
    OXYGEN_SENSOR_4_LAMBDA_VOLTAGE = C(0x27, 0x04, "OXYGEN_SENSOR_4_LAMBDA_VOLTAGE", "O2 Sensor 4 Equiv. Ratio (Lambda) & Voltage", [0, 0], [2, 8], ["ratio", 'V'], MF("2/65536*(256*A+B)", "8/65536*(256*C+D)"))
    OXYGEN_SENSOR_5_LAMBDA_VOLTAGE = C(0x28, 0x04, "OXYGEN_SENSOR_5_LAMBDA_VOLTAGE", "O2 Sensor 5 Equiv. Ratio (Lambda) & Voltage", [0, 0], [2, 8], ["ratio", 'V'], MF("2/65536*(256*A+B)", "8/65536*(256*C+D)"))
    OXYGEN_SENSOR_6_LAMBDA_VOLTAGE = C(0x29, 0x04, "OXYGEN_SENSOR_6_LAMBDA_VOLTAGE", "O2 Sensor 6 Equiv. Ratio (Lambda) & Voltage", [0, 0], [2, 8], ["ratio", 'V'], MF("2/65536*(256*A+B)", "8/65536*(256*C+D)"))
    OXYGEN_SENSOR_7_LAMBDA_VOLTAGE = C(0x2A, 0x04, "OXYGEN_SENSOR_7_LAMBDA_VOLTAGE", "O2 Sensor 7 Equiv. Ratio (Lambda) & Voltage", [0, 0], [2, 8], ["ratio", 'V'], MF("2/65536*(256*A+B)", "8/65536*(256*C+D)"))
    OXYGEN_SENSOR_8_LAMBDA_VOLTAGE = C(0x2B, 0x04, "OXYGEN_SENSOR_8_LAMBDA_VOLTAGE", "O2 Sensor 8 Equiv. Ratio (Lambda) & Voltage", [0, 0], [2, 8], ["ratio", 'V'], MF("2/65536*(256*A+B)", "8/65536*(256*C+D)"))
    EGR_PERC = C(0x2C, 0x01, "EGR_PERC", "Percentage of EGR valve opening requested", 0, 100, '%', F("100/255*A"))
    EGR_ERROR = C(0x2D, 0x01, "EGR_ERROR", "EGR Error", -100, 99.2, '%', F("100/128*A-100"))
    COMMANDED_EVAP_PURGE = C(0x2E, 0x01, "COMMANDED_EVAP_PURGE", "Commanded evaporative purge", 0, 100, '%', F("100/255*A")) 
    FUEL_LEVEL = C(0x2F, 0x01, "FUEL_LEVEL", "Fuel Level Input", 0, 100, '%', F("100/255*A")) 
    CLEARED_DTC_WARM_UPS = C(0x30, 0x01, "CLEARED_DTC_WARM_UPS", "Warm-ups since codes cleared", 0, 255, None, F('A'))
    CLEARED_DTC_DISTANCE = C(0x31, 0x02, "CLEARED_DTC_DISTANCE", "Distance traveled since codes cleared", 0, 65535, "km", F("256*A+B"))
    EVAP_PRESSURE = C(0x32, 0x02, "EVAP_PRESSURE", "Evap. System Vapor Pressure", -8192, 8191.75, "Pa")
    BAROMETRIC_PRESSURE = C(0x33, 0x01, "BAROMETRIC_PRESSURE", "Absolute Barometric Pressure", 0, 255, "kPa", F('A'))
    OXYGEN_SENSOR_1_LAMBDA_CURRENT = C(0x34, 0x04, "OXYGEN_SENSOR_1_LAMBDA_CURRENT", "O2 Sensor 1 Equiv. Ratio (Lambda) & Current", [0, -128], [2, 128], ["ratio", "mA"], MF("2/65536*(256*A+B)", "(256*C+D)/256-128"))
    OXYGEN_SENSOR_2_LAMBDA_CURRENT = C(0x35, 0x04, "OXYGEN_SENSOR_2_LAMBDA_CURRENT", "O2 Sensor 2 Equiv. Ratio (Lambda) & Current", [0, -128], [2, 128], ["ratio", "mA"], MF("2/65536*(256*A+B)", "(256*C+D)/256-128"))
    OXYGEN_SENSOR_3_LAMBDA_CURRENT = C(0x36, 0x04, "OXYGEN_SENSOR_3_LAMBDA_CURRENT", "O2 Sensor 3 Equiv. Ratio (Lambda) & Current", [0, -128], [2, 128], ["ratio", "mA"], MF("2/65536*(256*A+B)", "(256*C+D)/256-128"))
    OXYGEN_SENSOR_4_LAMBDA_CURRENT = C(0x37, 0x04, "OXYGEN_SENSOR_4_LAMBDA_CURRENT", "O2 Sensor 4 Equiv. Ratio (Lambda) & Current", [0, -128], [2, 128], ["ratio", "mA"], MF("2/65536*(256*A+B)", "(256*C+D)/256-128"))
    OXYGEN_SENSOR_5_LAMBDA_CURRENT = C(0x38, 0x04, "OXYGEN_SENSOR_5_LAMBDA_CURRENT", "O2 Sensor 5 Equiv. Ratio (Lambda) & Current", [0, -128], [2, 128], ["ratio", "mA"], MF("2/65536*(256*A+B)", "(256*C+D)/256-128"))
    OXYGEN_SENSOR_6_LAMBDA_CURRENT = C(0x39, 0x04, "OXYGEN_SENSOR_6_LAMBDA_CURRENT", "O2 Sensor 6 Equiv. Ratio (Lambda) & Current", [0, -128], [2, 128], ["ratio", "mA"], MF("2/65536*(256*A+B)", "(256*C+D)/256-128"))
    OXYGEN_SENSOR_7_LAMBDA_CURRENT = C(0x3A, 0x04, "OXYGEN_SENSOR_7_LAMBDA_CURRENT", "O2 Sensor 7 Equiv. Ratio (Lambda) & Current", [0, -128], [2, 128], ["ratio", "mA"], MF("2/65536*(256*A+B)", "(256*C+D)/256-128"))
    OXYGEN_SENSOR_8_LAMBDA_CURRENT = C(0x3B, 0x04, "OXYGEN_SENSOR_8_LAMBDA_CURRENT", "O2 Sensor 8 Equiv. Ratio (Lambda) & Current", [0, -128], [2, 128], ["ratio", "mA"], MF("2/65536*(256*A+B)", "(256*C+D)/256-128"))
    CATALYST_TEMP_BANK_1_SENSOR_1 = C(0x3C, 0x02, "CATALYST_TEMP_BANK_1_SENSOR_1", "Catalyst Temperature: Bank 1, Sensor 1", -40, 6513.5, "°C", F("(256*A+B)/10-40"))
    CATALYST_TEMP_BANK_2_SENSOR_1 = C(0x3D, 0x02, "CATALYST_TEMP_BANK_2_SENSOR_1", "Catalyst Temperature: Bank 2, Sensor 1", -40, 6513.5, "°C", F("(256*A+B)/10-40"))
    CATALYST_TEMP_BANK_1_SENSOR_2 = C(0x3E, 0x02, "CATALYST_TEMP_BANK_1_SENSOR_2", "Catalyst Temperature: Bank 1, Sensor 2", -40, 6513.5, "°C", F("(256*A+B)/10-40"))
    CATALYST_TEMP_BANK_2_SENSOR_2 = C(0x3F, 0x02, "CATALYST_TEMP_BANK_2_SENSOR_2", "Catalyst Temperature: Bank 2, Sensor 2", -40, 6513.5, "°C", F("(256*A+B)/10-40"))

    SUPPORTED_PIDS_C = C(0x40, 0x04, "SUPPORTED_PIDS_C", "PIDs supported [$41 - $60]", None, None, None, SP(0x41))
    STATUS_DRIVE_CYCLE = C(0x41, 0x04, "STATUS_DRIVE_CYCLE", "Monitor status this drive cycle", None, None, None)
    VEHICLE_VOLTAGE = C(0x42, 0x02, "VEHICLE_VOLTAGE", "Control module voltage", 0, 65.535, 'V', F("(256*A+B)/1000"))
    ENGINE_LOAD_ABSOLUTE = C(0x43, 0x02, "ENGINE_LOAD_ABSOLUTE", "Absolute percentage calculated from air mass intake", 0, 25700, '%', F("100/255*(256*A+B)"))
    COMMANDED_AIR_FUEL_RATIO = C(0x44, 0x02, "COMMANDED_AIR_FUEL_RATIO", "Commanded Air-Fuel Equivalence Ratio (lambda,λ)", 0, 2, "ratio", F("2/65536*(256*A+B)")) 
    THROTTLE_POSITION_RELATIVE = C(0x45, 0x01, "THROTTLE_POSITION_RELATIVE", "Relative throttle position", 0, 100, '%', F("100/255*A"))
    AMBIENT_AIR_TEMP = C(0x46, 0x01, "AMBIENT_AIR_TEMP", "Ambient air temperature", -40, 215, "°C", F("A-40"))
    THROTTLE_POSITION_B = C(0x47, 0x01, "THROTTLE_POSITION_B", "Absolute throttle position B", 0, 100, '%', F("100/255*A"))
    THROTTLE_POSITION_C = C(0x48, 0x01, "THROTTLE_POSITION_C", "Absolute throttle position C", 0, 100, '%', F("100/255*A"))
    ACCELERATOR_POSITION_D = C(0x49, 0x01, "ACCELERATOR_POSITION_D", "Accelerator pedal position D", 0, 100, '%', F("100/255*A"))
    ACCELERATOR_POSITION_E = C(0x4A, 0x01, "ACCELERATOR_POSITION_E", "Accelerator pedal position E", 0, 100, '%', F("100/255*A"))
    ACCELERATOR_POSITION_F = C(0x4B, 0x01, "ACCELERATOR_POSITION_F", "Accelerator pedal position F", 0, 100, '%', F("100/255*A"))
    THROTTLE_ACTUATOR = C(0x4C, 0x01, "THROTTLE_ACTUATOR", "Commanded throttle actuator", 0, 100, '%', F("100/255*A"))
    MIL_RUN_TIME = C(0x4D, 0x02, "MIL_RUN_TIME", "Time run with MIL on", 0, 65535, "min", F("256*A+B"))
    CLEARED_DTC_SINCE = C(0x4E, 0x02, "CLEARED_DTC_SINCE", "Time since trouble codes cleared", 0, 65535, "min", F("256*A+B"))
    MAX_FUEL_AIR_RATIO_O2_VOLT_CURR_PRESSURE = C(0x4F, 0x04, "MAX_FUEL_AIR_RATIO_O2_VOLT_CURR_PRESSURE", "Maximum value for Equiv Ratio, O2 Sensor V, O2 Sensor I, Intake Pressure", [0, 0, 0, 0], [255, 255, 255, 2550], ["ratio", 'V', "mA", "kPa"], MF('A', 'B', 'C', 'D*10'))
    MAF_MAX = C(0x50, 0x04, "MAF_MAX", "Maximum value for MAF rate", 0, 2550, "g/s", F("A*10"))
    FUEL_TYPE = C(0x51, 0x01, "FUEL_TYPE", "Fuel Type", None, None, None)
    ETHANOL_PERC = C(0x52, 0x01, "ETHANOL_PERC", "Ethanol fuel %", 0, 100, '%', F("100/255*A"))
    EVAP_PRESSURE_ABSOLUTE = C(0x53, 0x02, "EVAP_PRESSURE_ABSOLUTE", "Absolute Evap system Vapor Pressure", 0, 327.675, "kPa", F("(256*A+B)/200")) 
    EVAP_PRESSURE_ALT = C(0x54, 0x02, "EVAP_PRESSURE_ALT", "Evap system vapor pressure (alternate encoding)", -32768, 32767, "Pa")
    SHORT_OXYGEN_TRIM_BANK_1 = C(0x55, 0x02, "SHORT_OXYGEN_TRIM_BANK_1", "Short term secondary O2 sensor trim, A: bank 1, B: bank 3", -100, 99.2, '%', MF("100/128*A-100", "100/128*B-100"))
    LONG_OXYGEN_TRIM_BANK_1 = C(0x56, 0x02, "LONG_OXYGEN_TRIM_BANK_1", "Long term secondary O2 sensor trim, A: bank 1, B: bank 3", -100, 99.2, '%', MF("100/128*A-100", "100/128*B-100"))
    SHORT_OXYGEN_TRIM_BANK_2 = C(0x57, 0x02, "SHORT_OXYGEN_TRIM_BANK_2", "Short term secondary O2 sensor trim, A: bank 2, B: bank 4", -100, 99.2, '%', MF("100/128*A-100", "100/128*B-100"))
    LONG_OXYGEN_TRIM_BANK_2 = C(0x58, 0x02, "LONG_OXYGEN_TRIM_BANK_2", "Long term secondary O2 sensor trim, A: bank 2, B: bank 4", -100, 99.2, '%', MF("100/128*A-100", "100/128*B-100"))
    FUEL_RAIL_PRESSURE = C(0x59, 0x02, "FUEL_RAIL_PRESSURE", "Fuel rail absolute pressure", 0, 655350, "kPa", F("10*(256*A+B)"))
    ACCELERATOR_POSITION_RELATIVE = C(0x5A, 0x01, "ACCELERATOR_POSITION_RELATIVE", "Relative accelerator pedal position", 0, 100, '%', F("100/255*A"))
    HYBRID_BATTERY_REMAINING = C(0x5B, 0x01, "HYBRID_BATTERY_REMAINING", "Hybrid battery pack remaining life", 0, 100, '%', F("100/255*A"))
    ENGINE_OIL_TEMP = C(0x5C, 0x01, "ENGINE_OIL_TEMP", "Engine oil temperature", -40, 210, "°C", F("A-40"))
    FUEL_INJECTION_TIMING = C(0x5D, 0x02, "FUEL_INJECTION_TIMING", "Fuel injection timing", -210.00, 301.992, "°", F("(256*A+B)/128-210"))
    ENGINE_FUEL_RATE = C(0x5E, 0x02, "ENGINE_FUEL_RATE", "Engine fuel rate", 0, 3212.75, "L/h", F("(256*A+B)/20"))
    VEHICLE_EMISSION_STANDARDS = C(0x5F, 0x01, "VEHICLE_EMISSION_STANDARDS", "Emission requirements to which vehicle is designed", None, None, None) 

    SUPPORTED_PIDS_D = C(0x60, 0x04, "SUPPORTED_PIDS_D", "PIDs supported [$61 - $80]", None, None, None, SP(0x61))
    ENGINE_TORQUE_DEMAND = C(0x61, 0x01, "ENGINE_TORQUE_DEMAND", "Driver's demand engine percent torque", -125, 130, '%', F("A-125"))
    ENGINE_TORQUE_CURRENT = C(0x62, 0x01, "ENGINE_TORQUE_CURRENT", "Actual engine percent torque", -125, 130, '%', F("A-125"))
    ENGINE_TORQUE_REF = C(0x63, 0x02, "ENGINE_TORQUE_REF", "Engine reference torque", 0, 65535, "N⋅m", F("256*A+B"))
    ENGINE_TORQUE_DATA = C(0x64, 0x05, "ENGINE_TORQUE_DATA", "Engine percent torque data", -125, 130, '%', MF("A-125", "B-125", "C-125", "D-125", "E-125"))
    AUX_INPUT_OUTPUT_SUPPORTED = C(0x65, 0x02, "AUX_INPUT_OUTPUT_SUPPORTED", "Auxiliary input / output supported", None, None, None)
    MAF_SENSOR = C(0x66, 0x05, "MAF_SENSOR", "Mass air flow sensor", 0, 2047.96875, "g/s") # MF("(256*B+C)/32", "(256*D+E)/32")
    ENGINE_COOLANT_TEMP_ALT = C(0x67, 0x03, "ENGINE_COOLANT_TEMP_ALT", "Engine coolant temperature", -40, 215, "°C") # MF("B-40", "C-40")
    INTAKE_AIR_TEMP_ALT = C(0x68, 0x03, "INTAKE_AIR_TEMP_ALT", "Intake air temperature sensor", -40, 215, "°C") # MF("B-40", "C-40")
    EGR_DATA = C(0x69, 0x07, "EGR_DATA", "Actual EGR, Commanded EGR, and EGR Error", None, None, None)
    DIESEL_INTAKE_AIR_FLOW = C(0x6A, 0x05, "DIESEL_INTAKE_AIR_FLOW", "Commanded Diesel intake air flow control and relative intake air flow position", None, None, None)
    EGR_TEMP = C(0x6B, 0x05, "EGR_TEMP", "Exhaust gas recirculation temperature", None, None, None)
    THROTTLE_ACTUATOR_ALT = C(0x6C, 0x05, "THROTTLE_ACTUATOR_ALT", "Commanded throttle actuator control and relative throttle position", None, None, None)
    FUEL_PRESSURE_CONTROL = C(0x6D, 0x0B, "FUEL_PRESSURE_CONTROL", "Fuel pressure control system", None, None, None)
    INJECTION_PRESSURE_CONTROL = C(0x6E, 0x09, "INJECTION_PRESSURE_CONTROL", "Injection pressure control system", None, None, None)
    TURBO_PRESSURE = C(0x6F, 0x03, "TURBO_PRESSURE", "Turbocharger compressor inlet pressure", None, None, None)
    BOOST_PRESSURE_CONTROL = C(0x70, 0x0A, "BOOST_PRESSURE_CONTROL", "Boost pressure control", None, None, None)
    VGT_CONTROL = C(0x71, 0x06, "VGT_CONTROL", "Variable Geometry turbo (VGT) control", None, None, None)
    WASTEGATE_CONTROL = C(0x72, 0x05, "WASTEGATE_CONTROL", "Wastegate control", None, None, None)
    EXHAUST_PRESSURE = C(0x73, 0x05, "EXHAUST_PRESSURE", "Exhaust pressure", None, None, None)
    TURBO_SPEED = C(0x74, 0x05, "TURBO_SPEED", "Turbocharger RPM", None, None, None)
    TURBO_TEMP = C(0x75, 0x07, "TURBO_TEMP", "Turbocharger temperature", None, None, None)
    TURBO_TEMP_ALT = C(0x76, 0x07, "TURBO_TEMP_ALT", "Turbocharger temperature", None, None, None)
    CHARGE_AIR_COOLER_TEMP = C(0x77, 0x05, "CHARGE_AIR_COOLER_TEMP", "Charge air cooler temperature (CACT)", None, None, None)
    EGT_BANK_1 = C(0x78, 0x09, "EGT_BANK_1", "Exhaust Gas temperature (EGT) Bank 1", None, None, None)
    EGT_BANK_2 = C(0x79, 0x09, "EGT_BANK_2", "Exhaust Gas temperature (EGT) Bank 2", None, None, None)
    DPF_PRESSURE_DIFF = C(0x7A, 0x07, "DPF_PRESSURE_DIFF", "Diesel particulate filter (DPF) differential pressure", None, None, None)
    DPF_PRESSURE = C(0x7B, 0x07, "DPF_PRESSURE", "Diesel particulate filter (DPF)", None, None, None)
    DPF_TEMP = C(0x7C, 0x09, "DPF_TEMP", "Diesel Particulate filter (DPF) temperature", None, None, "°C", F("(256*A+B)/10-40"))
    NOX_NTE_CONTROL_STATUS = C(0x7D, 0x01, "NOX_NTE_CONTROL_STATUS", "NOx NTE (Not-To-Exceed) control area status", None, None, None)
    PM_NTE_CONTROL_STATUS = C(0x7E, 0x01, "PM_NTE_CONTROL_STATUS", "PM NTE (Not-To-Exceed) control area status", None, None, None)
    ENGINE_RUN_TIME_ALT = C(0x7F, 0x0D, "ENGINE_RUN_TIME_ALT", "Engine run time (Starting with MY 2010 the California Air Resources Board mandated that all diesel vehicles must supply total engine hours)", None, None, 's', F("B*(2**24)+C*(2**16)+D*(2**8)+E"))

    SUPPORTED_PIDS_E = C(0x80, 0x04, "SUPPORTED_PIDS_E", "PIDs supported [$81 - $A0]", None, None, None, SP(0x81))
    AECD_RUN_TIME = C(0x81, 0x29, "AECD_RUN_TIME", "Engine run time for Auxiliary Emissions Control Device(AECD)", None, None, None)
    AECD_RUN_TIME_AUX = C(0x82, 0x29, "AECD_RUN_TIME_AUX", "Engine run time for Auxiliary Emissions Control Device(AECD)", None, None, None)
    NOX_SENSOR = C(0x83, 0x09, "NOX_SENSOR", "NOx sensor", None, None, None)
    MANIFOLD_SURFACE_TEMP = C(0x84, 0x01, "MANIFOLD_SURFACE_TEMP", "Manifold surface temperature", None, None, None)
    NOX_REAGENT_SYSTEM = C(0x85, 0x0A, "NOX_REAGENT_SYSTEM", "NOx reagent system", None, None, '%', F("100/255*F"))
    PM_SENSOR = C(0x86, 0x05, "PM_SENSOR", "Particulate matter (PM) sensor", None, None, None)
    INTAKE_MAP = C(0x87, 0x05, "INTAKE_MAP", "Intake manifold absolute pressure", None, None, None)
    SCR_INDUCE_SYSTEM = C(0x88, 0x0D, "SCR_INDUCE_SYSTEM", "SCR Induce System", None, None, None)
    AECD_RUN_TIME_11_15 = C(0x89, 0x29, "AECD_RUN_TIME_11_15", "Run Time for AECD #11-#15", None, None, None)
    AECD_RUN_TIME_16_20 = C(0x8A, 0x29, "AECD_RUN_TIME_16_20", "Run Time for AECD #16-#20", None, None, None)
    DIESEL_AFTERTREATMENT = C(0x8B, 0x07, "DIESEL_AFTERTREATMENT", "Diesel Aftertreatment", None, None, None)
    OXYGEN_SENSOR_WIDE_RANGE = C(0x8C, 0x11, "OXYGEN_SENSOR_WIDE_RANGE", "O2 Sensor (Wide Range)", None, None, None)
    THROTTLE_POSITION_G = C(0x8D, 0x01, "THROTTLE_POSITION_G", "Throttle Position G", 0, 100, '%')
    ENGINE_FRICTION_TORQUE_PERC = C(0x8E, 0x01, "ENGINE_FRICTION_TORQUE_PERC", "Engine Friction - Percent Torque", -125, 130, '%', F("A-125"))
    PM_SENSOR_BANKS_1_2 = C(0x8F, 0x07, "PM_SENSOR_BANKS_1_2", "PM Sensor Bank 1 & 2", None, None, None)
    WWH_VEHICLE_INFORMATION = C(0x90, 0x03, "WWH_VEHICLE_INFORMATION", "WWH-OBD Vehicle OBD System Information", None, None, 'h')
    WWH_VEHICLE_INFORMATION_ALT = C(0x91, 0x05, "WWH_VEHICLE_INFORMATION_ALT", "WWH-OBD Vehicle OBD System Information", None, None, 'h')
    FUEL_SYSTEM_CONTROL = C(0x92, 0x02, "FUEL_SYSTEM_CONTROL", "Fuel System Control", None, None, None)
    WWH_VEHICLE_COUNTERS_SUPPORT = C(0x93, 0x03, "WWH_VEHICLE_COUNTERS_SUPPORT", "WWH-OBD Vehicle OBD Counters support", None, None, 'h')
    NOX_WARNING = C(0x94, 0x0C, "NOX_WARNING", "NOx Warning And Inducement System", None, None, None)
    EGT = C(0x98, 0x09, "EGT", "Exhaust Gas Temperature Sensor", None, None, None)
    EGT_ALT = C(0x99, 0x09, "EGT_ALT", "Exhaust Gas Temperature Sensor", None, None, None)
    HYBRID_BATTERY_VOLTAGE = C(0x9A, 0x06, "HYBRID_BATTERY_VOLTAGE", "Hybrid/EV Vehicle System Data, Battery, Voltage", None, None, None)
    DIESEL_EXHAUST_FLUID_SENSOR = C(0x9B, 0x04, "DIESEL_EXHAUST_FLUID_SENSOR", "Diesel Exhaust Fluid Sensor Data", None, None, '%', F("100/255*D"))
    OXYGEN_SENSOR_DATA = C(0x9C, 0x11, "OXYGEN_SENSOR_DATA", "O2 Sensor Data", None, None, None)
    ENGINE_MASS_FUEL_RATE = C(0x9D, 0x04, "ENGINE_MASS_FUEL_RATE", "Engine Mass Fuel Rate", None, None, "g/s")
    ENGINE_EXHAUST_FLOW_RATE = C(0x9E, 0x02, "ENGINE_EXHAUST_FLOW_RATE", "Engine Exhaust Flow Rate", None, None, "kg/h")
    FUEL_USE_PERC = C(0x9F, 0x09, "FUEL_USE_PERC", "Fuel System Percentage Use", None, None, None)

    SUPPORTED_PIDS_F = C(0xA0, 0x04, "SUPPORTED_PIDS_F", "PIDs supported [$A1 - $C0]", None, None, None, SP(0xA1))
    NOX_SENSOR_CORRECTED = C(0xA1, 0x09, "NOX_SENSOR_CORRECTED", "NOx Sensor Corrected Data", None, None, "ppm")
    CYLINDER_FUEL_RATE = C(0xA2, 0x02, "CYLINDER_FUEL_RATE", "Cylinder Fuel Rate", 0, 2047.96875, "mg/stroke", F("(256*A+B)/32"))
    EVAP_SYSTEM_VAPOR_PRESSURE = C(0xA3, 0x09, "EVAP_SYSTEM_VAPOR_PRESSURE", "Evap System Vapor Pressure", None, None, "Pa")
    TRANSMISSION_ACTUAL_GEAR = C(0xA4, 0x04, "TRANSMISSION_ACTUAL_GEAR", "Transmission Actual Gear", 0, 65.535, "ratio") # F("(256*C+D)/1000")
    DIESEL_EXHAUST_FLUID_DOSING = C(0xA5, 0x04, "DIESEL_EXHAUST_FLUID_DOSING", "Commanded Diesel Exhaust Fluid Dosing", 0, 127.5, '%') # F("B/2")
    ODOMETER = C(0xA6, 0x04, "ODOMETER", "Odometer (Starting with MY 2019 the California Air Resources Board mandated that all vehicles must supply odometer)", 0, 429_496_729.5, "km", F("(A*(2**24)+B(2**16)+C*(2**8)+D)/10"))
    NOX_CONCENTRATION_SENSORS_3_4 = C(0xA7, 0x04, "NOX_CONCENTRATION_SENSORS_3_4", "NOx Sensor Concentration Sensors 3 and 4", None, None, None)
    NOX_CORRECTED_CONCENTRATION_SENSORS_3_4 = C(0xA8, 0x04, "NOX_CORRECTED_CONCENTRATION_SENSORS_3_4", "NOx Sensor Corrected Concentration Sensors 3 and 4", None, None, None)
    ABS_ENABLED = C(0xA9, 0x04, "ABS_ENABLED", "ABS Disable Switch State", None, None, None)

    SUPPORTED_PIDS_G = C(0xC0, 0x04, "SUPPORTED_PIDS_G", "PIDs supported [$C1 - $E0]", None, None, None, SP(0xC1))
    FUEL_LEVEL_INPUT_A_B = C(0xC3, 0x02, "FUEL_LEVEL_INPUT_A_B", "Fuel Level Input A/B", 0, 25700, '%')
    EXHAUST_PARTICULATE_DIAG_TIME_COUNT = C(0xC4, 0x08, "EXHAUST_PARTICULATE_DIAG_TIME_COUNT", "Exhaust Particulate Control System Diagnostic Time/Count", 0, 4_294_967_295, "seconds/count")
    FUEL_PRESSURE_A_B = C(0xC5, 0x04, "FUEL_PRESSURE_A_B", "Fuel Pressure A and B", 0, 5177, "kPa")
    PARTICULATE_CONTROL_STATUS_COUNTERS = C(0xC6, 0x07, "PARTICULATE_CONTROL_STATUS_COUNTERS", "Byte 1 - Particulate control - driver inducement system status Byte 2,3 - Removal or block of the particulate aftertreatment system counter Byte 4,5 - Liquid regent injection system (e.g. fuel-borne catalyst) failure counter Byte 6,7 - Malfunction of Particulate control monitoring system counter", 0, 65535, 'h')
    DISTANCE_SINCE_REFLASH = C(0xC7, 0x02, "DISTANCE_SINCE_REFLASH", "Distance Since Reflash or Module Replacement", 0, 65535, "km")
    NOX_PCD_WARNING_LAMP_STATUS = C(0xC8, 0x01, "NOX_PCD_WARNING_LAMP_STATUS", "NOx Control Diagnostic (NCD) and Particulate Control Diagnostic (PCD) Warning Lamp status", None, None, "Bit")