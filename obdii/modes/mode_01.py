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
        ALT = Alternative
        AUX = Auxiliary
        DTC = Diagnostic Trouble Code
        EGR = Exhaust Gas Recirculation
        EVAP = Evaporative System # Added
        MAF = Mass Air Flow
        MAX = Maximum
        MIL = Malfunction Indicator Lamp
        OBD = On-Board Diagnostics
        PERC = Percentage
        PID = Parameter ID
        TEMP = Temperature
        VAC = Vacuum
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
    # ENGINE_TORQUE_DEMAND = C(0x61, 0x01, "ENGINE_TORQUE_DEMAND", "Driver's demand engine percent torque", -125, 130, '%', F("A-125"))
    # ENGINE_TORQUE = C(0x62, 0x01, "ENGINE_TORQUE", "Actual engine percent torque", -125, 130, '%', F("A-125"))
    # ENGINE_TORQUE_REF = C(0x63, 0x02, "ENGINE_TORQUE_REF", "Engine reference torque", 0, 65535, "N⋅m", F("256*A+B"))
    # ENGINE_TORQUE_DATA = C(0x64, 0x05, "ENGINE_TORQUE_DATA", "Engine percent torque data", -125, 130, '%', MF("A-125", "B-125", "C-125", "D-125", "E-125"))
    # AUXILIARY_INPUT_OUTPUT_SUPPORTED = C(0x65, 0x02, "AUXILIARY_INPUT_OUTPUT_SUPPORTED", "Auxiliary input / output supported", None, None, None)
    # MAF_SENSOR = C(0x66, 0x05, "MAF_SENSOR", "Mass air flow sensor", 0, 2047.96875, "g/s")
    # ENGINE_COOLANT_TEMP = C(0x67, 0x03, "ENGINE_COOLANT_TEMP", "Engine coolant temperature", -40, 215, "°C")
    # INTAKE_AIR_TEMP_SENSOR = C(0x68, 0x03, "INTAKE_AIR_TEMP_SENSOR", "Intake air temperature sensor", -40, 215, "°C")
    # EGR_ACTUAL = C(0x69, 0x07, "ACTUAL_EGR", "Actual EGR", None, None, None)
# COMMANDED_DIESEL_INTAKE_AIR_FLOW_CONTROL_AND_RELATIVE_INTAKE_AIR_FLOW_POSITION = C(6A, 5, "Commanded Diesel intake air flow control and relative intake air flow position", "Commanded Diesel intake air flow control and relative intake air flow position", None, None, None)
# EXHAUST_GAS_RECIRCULATION_TEMPERATURE = C(6B, 5, "Exhaust gas recirculation temperature", "Exhaust gas recirculation temperature", None, None, None)
# COMMANDED_THROTTLE_ACTUATOR_CONTROL_AND_RELATIVE_THROTTLE_POSITION = C(6C, 5, "Commanded throttle actuator control and relative throttle position", "Commanded throttle actuator control and relative throttle position", None, None, None)
# FUEL_PRESSURE_CONTROL_SYSTEM = C(6D, 11, "Fuel pressure control system", "Fuel pressure control system", None, None, None)
# INJECTION_PRESSURE_CONTROL_SYSTEM = C(6E, 9, "Injection pressure control system", "Injection pressure control system", None, None, None)
# TURBOCHARGER_COMPRESSOR_INLET_PRESSURE = C(6F, 3, "Turbocharger compressor inlet pressure", "Turbocharger compressor inlet pressure", None, None, None)
# BOOST_PRESSURE_CONTROL = C(70, 10, "Boost pressure control", "Boost pressure control", None, None, None)
# VARIABLE_GEOMETRY_TURBO_(VGT)_CONTROL = C(71, 6, "Variable Geometry turbo (VGT) control", "Variable Geometry turbo (VGT) control", None, None, None)
# WASTEGATE_CONTROL = C(72, 5, "Wastegate control", "Wastegate control", None, None, None)
# EXHAUST_PRESSURE = C(73, 5, "Exhaust pressure", "Exhaust pressure", None, None, None)
# TURBOCHARGER_RPM = C(74, 5, "Turbocharger RPM", "Turbocharger RPM", None, None, None)
# TURBOCHARGER_TEMPERATURE = C(75, 7, "Turbocharger temperature", "Turbocharger temperature", None, None, None)
# TURBOCHARGER_TEMPERATURE = C(76, 7, "Turbocharger temperature", "Turbocharger temperature", None, None, None)
# CHARGE_AIR_COOLER_TEMPERATURE_(CACT) = C(77, 5, "Charge air cooler temperature (CACT)", "Charge air cooler temperature (CACT)", None, None, None)
# EXHAUST_GAS_TEMPERATURE_(EGT)_BANK_1 = C(78, 9, "Exhaust Gas temperature (EGT) Bank 1", "Exhaust Gas temperature (EGT) Bank 1", None, None, None)
# EXHAUST_GAS_TEMPERATURE_(EGT)_BANK_2 = C(79, 9, "Exhaust Gas temperature (EGT) Bank 2", "Exhaust Gas temperature (EGT) Bank 2", None, None, None)
# DIESEL_PARTICULATE_FILTER_(DPF)_DIFFERENTIAL_PRESSURE = C(7A, 7, "Diesel particulate filter (DPF) differential pressure", "Diesel particulate filter (DPF) differential pressure", None, None, None)
# DIESEL_PARTICULATE_FILTER_(DPF) = C(7B, 7, "Diesel particulate filter (DPF)", "Diesel particulate filter (DPF)", None, None, None)
# DIESEL_PARTICULATE_FILTER_(DPF)_TEMPERATURE = C(7C, 9, "Diesel Particulate filter (DPF) temperature", "Diesel Particulate filter (DPF) temperature", None, None, "°C")
# NOX_NTE_(NOT-TO-EXCEED)_CONTROL_AREA_STATUS = C(7D, 1, "NOx NTE (Not-To-Exceed) control area status", "NOx NTE (Not-To-Exceed) control area status", None, None, None)
# PM_NTE_(NOT-TO-EXCEED)_CONTROL_AREA_STATUS = C(7E, 1, "PM NTE (Not-To-Exceed) control area status", "PM NTE (Not-To-Exceed) control area status", None, None, None)
# ENGINE_RUN_TIME_[B] = C(7F, 13, "Engine run time [b]", "Engine run time [b]", None, None, "s")

# PIDS_E = C(80, 4, "PIDs supported [$81 - $A0]", "PIDs supported [$81 - $A0]", None, None, None)
# ENGINE_RUN_TIME_FOR_AUXILIARY_EMISSIONS_CONTROL_DEVICE(AECD) = C(81, 41, "Engine run time for Auxiliary Emissions Control Device(AECD)", "Engine run time for Auxiliary Emissions Control Device(AECD)", None, None, None)
# ENGINE_RUN_TIME_FOR_AUXILIARY_EMISSIONS_CONTROL_DEVICE(AECD) = C(82, 41, "Engine run time for Auxiliary Emissions Control Device(AECD)", "Engine run time for Auxiliary Emissions Control Device(AECD)", None, None, None)
# NOX_SENSOR = C(83, 9, "NOx sensor", "NOx sensor", None, None, None)
# MANIFOLD_SURFACE_TEMPERATURE = C(84, 1, "Manifold surface temperature", "Manifold surface temperature", None, None, None)
# NOX_REAGENT_SYSTEM = C(85, 10, "NOx reagent system", "NOx reagent system", None, None, '%')
# PARTICULATE_MATTER_(PM)_SENSOR = C(86, 5, "Particulate matter (PM) sensor", "Particulate matter (PM) sensor", None, None, None)
# INTAKE_MANIFOLD_ABSOLUTE_PRESSURE = C(87, 5, "Intake manifold absolute pressure", "Intake manifold absolute pressure", None, None, None)
# SCR_INDUCE_SYSTEM = C(88, 13, "SCR Induce System", "SCR Induce System", None, None, None)
# RUN_TIME_FOR_AECD_#11-#15 = C(89, 41, "Run Time for AECD #11-#15", "Run Time for AECD #11-#15", None, None, None)
# RUN_TIME_FOR_AECD_#16-#20 = C(8A, 41, "Run Time for AECD #16-#20", "Run Time for AECD #16-#20", None, None, None)
# DIESEL_AFTERTREATMENT = C(8B, 7, "Diesel Aftertreatment", "Diesel Aftertreatment", None, None, None)
# O2_SENSOR_(WIDE_RANGE) = C(8C, 17, "O2 Sensor (Wide Range)", "O2 Sensor (Wide Range)", None, None, None)
# THROTTLE_POSITION_G = C(8D, 1, "Throttle Position G", "Throttle Position G", 0, 100, '%')
# ENGINE_FRICTION_-_PERCENT_TORQUE = C(8E, 1, "Engine Friction - Percent Torque", "Engine Friction - Percent Torque", -125, 130, '%')
# PM_SENSOR_BANK_1_&_2 = C(8F, 7, "PM Sensor Bank 1 & 2", "PM Sensor Bank 1 & 2", None, None, None)
# WWH-OBD_VEHICLE_OBD_SYSTEM_INFORMATION = C(90, 3, "WWH-OBD Vehicle OBD System Information", "WWH-OBD Vehicle OBD System Information", None, None, "h")
# WWH-OBD_VEHICLE_OBD_SYSTEM_INFORMATION = C(91, 5, "WWH-OBD Vehicle OBD System Information", "WWH-OBD Vehicle OBD System Information", None, None, "h")
# FUEL_SYSTEM_CONTROL = C(92, 2, "Fuel System Control", "Fuel System Control", None, None, None)
# WWH-OBD_VEHICLE_OBD_COUNTERS_SUPPORT = C(93, 3, "WWH-OBD Vehicle OBD Counters support", "WWH-OBD Vehicle OBD Counters support", None, None, "h")
# NOX_WARNING_AND_INDUCEMENT_SYSTEM = C(94, 12, "NOx Warning And Inducement System", "NOx Warning And Inducement System", None, None, None)
# EXHAUST_GAS_TEMPERATURE_SENSOR = C(98, 9, "Exhaust Gas Temperature Sensor", "Exhaust Gas Temperature Sensor", None, None, None)
# EXHAUST_GAS_TEMPERATURE_SENSOR = C(99, 9, "Exhaust Gas Temperature Sensor", "Exhaust Gas Temperature Sensor", None, None, None)
# HYBRID/EV_VEHICLE_SYSTEM_DATA,_BATTERY,_VOLTAGE = C(9A, 6, "Hybrid/EV Vehicle System Data, Battery, Voltage", "Hybrid/EV Vehicle System Data, Battery, Voltage", None, None, None)
# DIESEL_EXHAUST_FLUID_SENSOR_DATA = C(9B, 4, "Diesel Exhaust Fluid Sensor Data", "Diesel Exhaust Fluid Sensor Data", None, None, '%')
# O2_SENSOR_DATA = C(9C, 17, "O2 Sensor Data", "O2 Sensor Data", None, None, None)
# ENGINE_FUEL_RATE = C(9D, 4, "Engine Fuel Rate", "Engine Fuel Rate", None, None, "g/s")
# ENGINE_EXHAUST_FLOW_RATE = C(9E, 2, "Engine Exhaust Flow Rate", "Engine Exhaust Flow Rate", None, None, "kg/h")
# FUEL_SYSTEM_PERCENTAGE_USE = C(9F, 9, "Fuel System Percentage Use", "Fuel System Percentage Use", None, None, None)

# PIDS_F = C(A0, 4, "PIDs supported [$A1 - $C0]", "PIDs supported [$A1 - $C0]", None, None, None)
# NOX_SENSOR_CORRECTED_DATA = C(A1, 9, "NOx Sensor Corrected Data", "NOx Sensor Corrected Data", None, None, "ppm")
# CYLINDER_FUEL_RATE = C(A2, 2, "Cylinder Fuel Rate", "Cylinder Fuel Rate", 0, 2047.96875, "mg/stroke")
# EVAP_SYSTEM_VAPOR_PRESSURE = C(A3, 9, "Evap System Vapor Pressure", "Evap System Vapor Pressure", None, None, "Pa")
# TRANSMISSION_ACTUAL_GEAR = C(A4, 4, "Transmission Actual Gear", "Transmission Actual Gear", 0, 65.535, "ratio")
# COMMANDED_DIESEL_EXHAUST_FLUID_DOSING = C(A5, 4, "Commanded Diesel Exhaust Fluid Dosing", "Commanded Diesel Exhaust Fluid Dosing", 0, 127.5, '%')
# ODOMETER_[C] = C(A6, 4, "Odometer [c]", "Odometer [c]", 0, 429496729.5, "km")
# NOX_SENSOR_CONCENTRATION_SENSORS_3_AND_4 = C(A7, 4, "NOx Sensor Concentration Sensors 3 and 4", "NOx Sensor Concentration Sensors 3 and 4", None, None, None)
# NOX_SENSOR_CORRECTED_CONCENTRATION_SENSORS_3_AND_4 = C(A8, 4, "NOx Sensor Corrected Concentration Sensors 3 and 4", "NOx Sensor Corrected Concentration Sensors 3 and 4", None, None, None)
# ABS_DISABLE_SWITCH_STATE = C(A9, 4, "ABS Disable Switch State", "ABS Disable Switch State", None, None, None)

# PIDS_G = C(C0, 4, "PIDs supported [$C1 - $E0]", "PIDs supported [$C1 - $E0]", None, None, None)
# FUEL_LEVEL_INPUT_A/B = C(C3, 2, "Fuel Level Input A/B", "Fuel Level Input A/B", 0, 25700, '%')
# EXHAUST_PARTICULATE_CONTROL_SYSTEM_DIAGNOSTIC_TIME/COUNT = C(C4, 8, "Exhaust Particulate Control System Diagnostic Time/Count", "Exhaust Particulate Control System Diagnostic Time/Count", 0, 4294967295, "seconds / Count")
# FUEL_PRESSURE_A_AND_B = C(C5, 4, "Fuel Pressure A and B", "Fuel Pressure A and B", 0, 5177, "kPa")
# BYTE_1_-_PARTICULATE_CONTROL_-_DRIVER_INDUCEMENT_SYSTEM_STATUS_BYTE_2,3_-_REMOVAL_OR_BLOCK_OF_THE_PARTICULATE_AFTERTREATMENT_SYSTEM_COUNTER_BYTE_4,5_-_LIQUID_REGENT_INJECTION_SYSTEM_(E.G._FUEL-BORNE_CATALYST)_FAILURE_COUNTER_BYTE_6,7_-_MALFUNCTION_OF_PARTICULATE_CONTROL_MONITORING_SYSTEM_COUNTER = C(C6, 7, "Byte 1 - Particulate control - driver inducement system status Byte 2,3 - Removal or block of the particulate aftertreatment system counter Byte 4,5 - Liquid regent injection system (e.g. fuel-borne catalyst) failure counter Byte 6,7 - Malfunction of Particulate control monitoring system counter", "Byte 1 - Particulate control - driver inducement system status Byte 2,3 - Removal or block of the particulate aftertreatment system counter Byte 4,5 - Liquid regent injection system (e.g. fuel-borne catalyst) failure counter Byte 6,7 - Malfunction of Particulate control monitoring system counter", 0, 65535, "h")
# DISTANCE_SINCE_REFLASH_OR_MODULE_REPLACEMENT = C(C7, 2, "Distance Since Reflash or Module Replacement", "Distance Since Reflash or Module Replacement", 0, 65535, "km")
# NOX_CONTROL_DIAGNOSTIC_(NCD)_AND_PARTICULATE_CONTROL_DIAGNOSTIC_(PCD)_WARNING_LAMP_STATUS = C(C8, 1, "NOx Control Diagnostic (NCD) and Particulate Control Diagnostic (PCD) Warning Lamp status", "NOx Control Diagnostic (NCD) and Particulate Control Diagnostic (PCD) Warning Lamp status", -, -, "Bit")
# DESCRIPTION = C(PID (hex), Data bytes returned, "Description", "Description", Min value, Max value, "Units")