from functools import partial

from .group_commands import GroupCommands

from ..command import Command
from ..mode import Mode
from ..parsers.formula import Formula, MultiFormula
from ..parsers.mappings import FUEL_SYSTEM_STATUS, SECONDARY_AIR_STATUS, VEHICLE_STANDARDS, FUEL_TYPE_CODING
from ..parsers.pids import SupportedPIDS


M = Mode.REQUEST
C = partial(Command, M)

F = Formula
MF = MultiFormula
SP = SupportedPIDS

# https://en.wikipedia.org/wiki/OBD-II_PIDs#Service_01_-_Show_current_data

class Mode01(GroupCommands, registry_id=M):
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

    SUPPORTED_PIDS_A = C(0x00, 0x04, None, None, None, SP(0x01))
    """PIDs supported [$01 - $20]"""
    STATUS_DTC = C(0x01, 0x04, None, None, None)
    """Monitor status since DTCs cleared. (Includes MIL status, DTC count, tests)"""
    FREEZE_DTC = C(0x02, 0x02, None, None, None)
    """DTC that caused freeze frame storage."""
    FUEL_STATUS = C(0x03, 0x02, None, None, None, FUEL_SYSTEM_STATUS)
    """Fuel system status"""
    ENGINE_LOAD = C(0x04, 1, 0, 100, '%', F("100/255*A")) 
    """Calculated engine load"""
    ENGINE_COOLANT_TEMP = C(0x05, 1, -40, 215, "°C", F("A-40"))
    """Engine coolant temperature"""
    SHORT_FUEL_TRIM_BANK_1 = C(0x06, 1, -100, 99.2, '%', F("100/128*A-100"))
    """Short term fuel trim (STFT)—Bank 1"""
    LONG_FUEL_TRIM_BANK_1 = C(0x07, 1, -100, 99.2, '%', F("100/128*A-100"))
    """Long term fuel trim (LTFT)—Bank 1"""
    SHORT_FUEL_TRIM_BANK_2 = C(0x08, 1, -100, 99.2, '%', F("100/128*A-100"))
    """Short term fuel trim (STFT)—Bank 2"""
    LONG_FUEL_TRIM_BANK_2 = C(0x09, 1, -100, 99.2, '%', F("100/128*A-100"))
    """Long term fuel trim (LTFT)—Bank 2"""
    FUEL_PRESSURE = C(0x0A, 1, 0, 765, "kPa", F("3*A"))
    """Fuel pressure (gauge pressure)"""
    INTAKE_PRESSURE = C(0x0B, 1, 0, 255, "kPa", F('A'))
    """Intake manifold absolute pressure"""
    ENGINE_SPEED = C(0x0C, 2, 0, 16383.75, "rpm", F("(256*A+B)/4"))
    """Engine speed"""
    VEHICLE_SPEED = C(0x0D, 1, 0, 255, "km/h", F('A'))
    """Vehicle speed"""
    IGNITION_TIMING_ADVANCE = C(0x0E, 1, -64, 63.5, "° before TDC", F("A/2-64"))
    """Timing advance"""
    INTAKE_AIR_TEMP = C(0x0F, 1, -40, 215, "°C", F("A-40"))
    """Intake air temperature"""
    MAF_RATE = C(0x10, 2, 0, 655.35, "g/s", F("(256*A+B)/100"))
    """Mass air flow sensor (MAF) air flow rate"""
    THROTTLE_POSITION = C(0x11, 1, 0, 100, '%', F("100/255*A"))
    """Throttle position"""
    STATUS_SECONDARY_AIR = C(0x12, 1, None, None, None, SECONDARY_AIR_STATUS)
    """Commanded secondary air status"""
    OXYGEN_SENSORS_2_BANKS = C(0x13, 1, None, None, None)
    """Oxygen sensors present (in 2 banks)"""
    OXYGEN_SENSOR_1 = C(0x14, 2, [0, -100], [1.275, 99.2], ['V', '%'], MF("A/200", "100/128*B-100"))
    """Oxygen Sensor 1 A: Voltage B: Short term fuel trim"""
    OXYGEN_SENSOR_2 = C(0x15, 2, [0, -100], [1.275, 99.2], ['V', '%'], MF("A/200", "100/128*B-100"))
    """Oxygen Sensor 2 A: Voltage B: Short term fuel trim"""
    OXYGEN_SENSOR_3 = C(0x16, 2, [0, -100], [1.275, 99.2], ['V', '%'], MF("A/200", "100/128*B-100"))
    """Oxygen Sensor 3 A: Voltage B: Short term fuel trim"""
    OXYGEN_SENSOR_4 = C(0x17, 2, [0, -100], [1.275, 99.2], ['V', '%'], MF("A/200", "100/128*B-100"))
    """Oxygen Sensor 4 A: Voltage B: Short term fuel trim"""
    OXYGEN_SENSOR_5 = C(0x18, 2, [0, -100], [1.275, 99.2], ['V', '%'], MF("A/200", "100/128*B-100"))
    """Oxygen Sensor 5 A: Voltage B: Short term fuel trim"""
    OXYGEN_SENSOR_6 = C(0x19, 2, [0, -100], [1.275, 99.2], ['V', '%'], MF("A/200", "100/128*B-100"))
    """Oxygen Sensor 6 A: Voltage B: Short term fuel trim"""
    OXYGEN_SENSOR_7 = C(0x1A, 2, [0, -100], [1.275, 99.2], ['V', '%'], MF("A/200", "100/128*B-100"))
    """Oxygen Sensor 7 A: Voltage B: Short term fuel trim"""
    OXYGEN_SENSOR_8 = C(0x1B, 2, [0, -100], [1.275, 99.2], ['V', '%'], MF("A/200", "100/128*B-100"))
    """Oxygen Sensor 8 A: Voltage B: Short term fuel trim"""
    OBD_STANDARDS = C(0x1C, 1, 1, 250, None, VEHICLE_STANDARDS)       
    """OBD standards this vehicle conforms to"""
    OXYGEN_SENSORS_4_BANKS = C(0x1D, 1, None, None, None)
    """Oxygen sensors present (in 4 banks)"""
    STATUS_AUX_INPUT = C(0x1E, 1, None, None, None)
    """Auxiliary input status (e.g. Power Take Off)"""
    ENGINE_RUN_TIME = C(0x1F, 2, 0, 65535, 's', F("256*A+B"))
    """Run time since engine start"""

    SUPPORTED_PIDS_B = C(0x20, 4, None, None, None, SP(0x21)) 
    """PIDs supported [$21 - $40]"""
    MIL_DISTANCE = C(0x21, 2, 0, 65535, "km", F("256*A+B"))
    """Distance traveled with MIL on"""
    FUEL_RAIL_PRESSURE_VAC = C(0x22, 2, 0, 5177.265, "kPa", F("0.079*(256*A+B)"))
    """Fuel Rail Pressure (relative to manifold vacuum)"""
    FUEL_RAIL_GAUGE_PRESSURE = C(0x23, 2, 0, 655350, "kPa", F("10*(256*A+B)"))
    """Fuel Rail Gauge Pressure (diesel, or gasoline direct injection)"""
    OXYGEN_SENSOR_1_LAMBDA_VOLTAGE = C(0x24, 4, [0, 0], [2, 8], ["ratio", 'V'], MF("2/65536*(256*A+B)", "8/65536*(256*C+D)"))
    """O2 Sensor 1 Equiv. Ratio (Lambda) & Voltage"""
    OXYGEN_SENSOR_2_LAMBDA_VOLTAGE = C(0x25, 4, [0, 0], [2, 8], ["ratio", 'V'], MF("2/65536*(256*A+B)", "8/65536*(256*C+D)"))
    """O2 Sensor 2 Equiv. Ratio (Lambda) & Voltage"""
    OXYGEN_SENSOR_3_LAMBDA_VOLTAGE = C(0x26, 4, [0, 0], [2, 8], ["ratio", 'V'], MF("2/65536*(256*A+B)", "8/65536*(256*C+D)"))
    """O2 Sensor 3 Equiv. Ratio (Lambda) & Voltage"""
    OXYGEN_SENSOR_4_LAMBDA_VOLTAGE = C(0x27, 4, [0, 0], [2, 8], ["ratio", 'V'], MF("2/65536*(256*A+B)", "8/65536*(256*C+D)"))
    """O2 Sensor 4 Equiv. Ratio (Lambda) & Voltage"""
    OXYGEN_SENSOR_5_LAMBDA_VOLTAGE = C(0x28, 4, [0, 0], [2, 8], ["ratio", 'V'], MF("2/65536*(256*A+B)", "8/65536*(256*C+D)"))
    """O2 Sensor 5 Equiv. Ratio (Lambda) & Voltage"""
    OXYGEN_SENSOR_6_LAMBDA_VOLTAGE = C(0x29, 4, [0, 0], [2, 8], ["ratio", 'V'], MF("2/65536*(256*A+B)", "8/65536*(256*C+D)"))
    """O2 Sensor 6 Equiv. Ratio (Lambda) & Voltage"""
    OXYGEN_SENSOR_7_LAMBDA_VOLTAGE = C(0x2A, 4, [0, 0], [2, 8], ["ratio", 'V'], MF("2/65536*(256*A+B)", "8/65536*(256*C+D)"))
    """O2 Sensor 7 Equiv. Ratio (Lambda) & Voltage"""
    OXYGEN_SENSOR_8_LAMBDA_VOLTAGE = C(0x2B, 4, [0, 0], [2, 8], ["ratio", 'V'], MF("2/65536*(256*A+B)", "8/65536*(256*C+D)"))
    """O2 Sensor 8 Equiv. Ratio (Lambda) & Voltage"""
    EGR_PERC = C(0x2C, 1, 0, 100, '%', F("100/255*A"))
    """Percentage of EGR valve opening requested"""
    EGR_ERROR = C(0x2D, 1, -100, 99.2, '%', F("100/128*A-100"))
    """EGR Error"""
    COMMANDED_EVAP_PURGE = C(0x2E, 1, 0, 100, '%', F("100/255*A"))
    """Commanded evaporative purge"""
    FUEL_LEVEL = C(0x2F, 1, 0, 100, '%', F("100/255*A"))
    """Fuel Level Input"""
    CLEARED_DTC_WARM_UPS = C(0x30, 1, 0, 255, None, F('A'))
    """Warm-ups since codes cleared"""
    CLEARED_DTC_DISTANCE = C(0x31, 2, 0, 65535, "km", F("256*A+B"))
    """Distance traveled since codes cleared"""
    EVAP_PRESSURE = C(0x32, 2, -8192, 8191.75, "Pa")
    """Evap. System Vapor Pressure"""
    BAROMETRIC_PRESSURE = C(0x33, 1, 0, 255, "kPa", F('A'))
    """Absolute Barometric Pressure"""
    OXYGEN_SENSOR_1_LAMBDA_CURRENT = C(0x34, 4, [0, -128], [2, 128], ["ratio", "mA"], MF("2/65536*(256*A+B)", "(256*C+D)/256-128"))
    """O2 Sensor 1 Equiv. Ratio (Lambda) & Current"""
    OXYGEN_SENSOR_2_LAMBDA_CURRENT = C(0x35, 4, [0, -128], [2, 128], ["ratio", "mA"], MF("2/65536*(256*A+B)", "(256*C+D)/256-128"))
    """O2 Sensor 2 Equiv. Ratio (Lambda) & Current"""
    OXYGEN_SENSOR_3_LAMBDA_CURRENT = C(0x36, 4, [0, -128], [2, 128], ["ratio", "mA"], MF("2/65536*(256*A+B)", "(256*C+D)/256-128"))
    """O2 Sensor 3 Equiv. Ratio (Lambda) & Current"""
    OXYGEN_SENSOR_4_LAMBDA_CURRENT = C(0x37, 4, [0, -128], [2, 128], ["ratio", "mA"], MF("2/65536*(256*A+B)", "(256*C+D)/256-128"))
    """O2 Sensor 4 Equiv. Ratio (Lambda) & Current"""
    OXYGEN_SENSOR_5_LAMBDA_CURRENT = C(0x38, 4, [0, -128], [2, 128], ["ratio", "mA"], MF("2/65536*(256*A+B)", "(256*C+D)/256-128"))
    """O2 Sensor 5 Equiv. Ratio (Lambda) & Current"""
    OXYGEN_SENSOR_6_LAMBDA_CURRENT = C(0x39, 4, [0, -128], [2, 128], ["ratio", "mA"], MF("2/65536*(256*A+B)", "(256*C+D)/256-128"))
    """O2 Sensor 6 Equiv. Ratio (Lambda) & Current"""
    OXYGEN_SENSOR_7_LAMBDA_CURRENT = C(0x3A, 4, [0, -128], [2, 128], ["ratio", "mA"], MF("2/65536*(256*A+B)", "(256*C+D)/256-128"))
    """O2 Sensor 7 Equiv. Ratio (Lambda) & Current"""
    OXYGEN_SENSOR_8_LAMBDA_CURRENT = C(0x3B, 4, [0, -128], [2, 128], ["ratio", "mA"], MF("2/65536*(256*A+B)", "(256*C+D)/256-128"))
    """O2 Sensor 8 Equiv. Ratio (Lambda) & Current"""
    CATALYST_TEMP_BANK_1_SENSOR_1 = C(0x3C, 2, -40, 6513.5, "°C", F("(256*A+B)/10-40"))
    """Catalyst Temperature: Bank 1, Sensor 1"""
    CATALYST_TEMP_BANK_2_SENSOR_1 = C(0x3D, 2, -40, 6513.5, "°C", F("(256*A+B)/10-40"))
    """Catalyst Temperature: Bank 2, Sensor 1"""
    CATALYST_TEMP_BANK_1_SENSOR_2 = C(0x3E, 2, -40, 6513.5, "°C", F("(256*A+B)/10-40"))
    """Catalyst Temperature: Bank 1, Sensor 2"""
    CATALYST_TEMP_BANK_2_SENSOR_2 = C(0x3F, 2, -40, 6513.5, "°C", F("(256*A+B)/10-40"))
    """Catalyst Temperature: Bank 2, Sensor 2"""

    SUPPORTED_PIDS_C = C(0x40, 4, None, None, None, SP(0x41)) 
    """PIDs supported [$41 - $60]"""
    STATUS_DRIVE_CYCLE = C(0x41, 4, None, None, None)
    """Monitor status this drive cycle"""
    VEHICLE_VOLTAGE = C(0x42, 2, 0, 65.535, 'V', F("(256*A+B)/1000"))
    """Control module voltage"""
    ENGINE_LOAD_ABSOLUTE = C(0x43, 2, 0, 25700, '%', F("100/255*(256*A+B)"))
    """Absolute percentage calculated from air mass intake"""
    COMMANDED_AIR_FUEL_RATIO = C(0x44, 2, 0, 2, "ratio", F("2/65536*(256*A+B)"))
    """Commanded Air-Fuel Equivalence Ratio (lambda,λ)"""
    THROTTLE_POSITION_RELATIVE = C(0x45, 1, 0, 100, '%', F("100/255*A"))
    """Relative throttle position"""
    AMBIENT_AIR_TEMP = C(0x46, 1, -40, 215, "°C", F("A-40"))
    """Ambient air temperature"""
    THROTTLE_POSITION_B = C(0x47, 1, 0, 100, '%', F("100/255*A"))
    """Absolute throttle position B"""
    THROTTLE_POSITION_C = C(0x48, 1, 0, 100, '%', F("100/255*A"))
    """Absolute throttle position C"""
    ACCELERATOR_POSITION_D = C(0x49, 1, 0, 100, '%', F("100/255*A"))
    """Accelerator pedal position D"""
    ACCELERATOR_POSITION_E = C(0x4A, 1, 0, 100, '%', F("100/255*A"))
    """Accelerator pedal position E"""
    ACCELERATOR_POSITION_F = C(0x4B, 1, 0, 100, '%', F("100/255*A"))
    """Accelerator pedal position F"""
    THROTTLE_ACTUATOR = C(0x4C, 1, 0, 100, '%', F("100/255*A"))
    """Commanded throttle actuator"""
    MIL_RUN_TIME = C(0x4D, 2, 0, 65535, "min", F("256*A+B"))
    """Time run with MIL on"""
    CLEARED_DTC_SINCE = C(0x4E, 2, 0, 65535, "min", F("256*A+B"))
    """Time since trouble codes cleared"""
    MAX_FUEL_AIR_RATIO_O2_VOLT_CURR_PRESSURE = C(0x4F, 4, [0, 0, 0, 0], [255, 255, 255, 2550], ["ratio", 'V', "mA", "kPa"], MF('A', 'B', 'C', "D*10"))
    """Maximum value for Equiv Ratio, O2 Sensor V, O2 Sensor I, Intake Pressure"""
    MAF_MAX = C(0x50, 4, 0, 2550, "g/s", F("A*10"))
    """Maximum value for MAF rate"""
    FUEL_TYPE = C(0x51, 1, None, None, None, FUEL_TYPE_CODING)       
    """Fuel Type"""
    ETHANOL_PERC = C(0x52, 1, 0, 100, '%', F("100/255*A"))
    """Ethanol fuel %"""
    EVAP_PRESSURE_ABSOLUTE = C(0x53, 2, 0, 327.675, "kPa", F("(256*A+B)/200"))
    """Absolute Evap system Vapor Pressure"""
    EVAP_PRESSURE_ALT = C(0x54, 2, -32768, 32767, "Pa")
    """Evap system vapor pressure (alternate encoding)"""
    SHORT_OXYGEN_TRIM_BANK_1 = C(0x55, 2, -100, 99.2, '%', MF("100/128*A-100", "100/128*B-100"))
    """Short term secondary O2 sensor trim, A: bank 1, B: bank 3"""
    LONG_OXYGEN_TRIM_BANK_1 = C(0x56, 2, -100, 99.2, '%', MF("100/128*A-100", "100/128*B-100"))
    """Long term secondary O2 sensor trim, A: bank 1, B: bank 3"""
    SHORT_OXYGEN_TRIM_BANK_2 = C(0x57, 2, -100, 99.2, '%', MF("100/128*A-100", "100/128*B-100"))
    """Short term secondary O2 sensor trim, A: bank 2, B: bank 4"""
    LONG_OXYGEN_TRIM_BANK_2 = C(0x58, 2, -100, 99.2, '%', MF("100/128*A-100", "100/128*B-100"))
    """Long term secondary O2 sensor trim, A: bank 2, B: bank 4"""
    FUEL_RAIL_PRESSURE = C(0x59, 2, 0, 655350, "kPa", F("10*(256*A+B)"))
    """Fuel rail absolute pressure"""
    ACCELERATOR_POSITION_RELATIVE = C(0x5A, 1, 0, 100, '%', F("100/255*A"))
    """Relative accelerator pedal position"""
    HYBRID_BATTERY_REMAINING = C(0x5B, 1, 0, 100, '%', F("100/255*A"))
    """Hybrid battery pack remaining life"""
    ENGINE_OIL_TEMP = C(0x5C, 1, -40, 210, "°C", F("A-40"))
    """Engine oil temperature"""
    FUEL_INJECTION_TIMING = C(0x5D, 2, -210.0, 301.992, '°', F("(256*A+B)/128-210"))
    """Fuel injection timing"""
    ENGINE_FUEL_RATE = C(0x5E, 2, 0, 3212.75, "L/h", F("(256*A+B)/20"))
    """Engine fuel rate"""
    VEHICLE_EMISSION_STANDARDS = C(0x5F, 1, None, None, None)
    """Emission requirements to which vehicle is designed"""

    SUPPORTED_PIDS_D = C(0x60, 4, None, None, None, SP(0x61)) 
    """PIDs supported [$61 - $80]"""
    ENGINE_TORQUE_DEMAND = C(0x61, 1, -125, 130, '%', F("A-125"))
    """Driver's demand engine percent torque"""
    ENGINE_TORQUE_CURRENT = C(0x62, 1, -125, 130, '%', F("A-125"))
    """Actual engine percent torque"""
    ENGINE_TORQUE_REF = C(0x63, 2, 0, 65535, "N⋅m", F("256*A+B"))
    """Engine reference torque"""
    ENGINE_TORQUE_DATA = C(0x64, 5, -125, 130, '%', MF("A-125", "B-125", "C-125", "D-125", "E-125"))
    """Engine percent torque data"""
    AUX_INPUT_OUTPUT_SUPPORTED = C(0x65, 2, None, None, None)
    """Auxiliary input / output supported"""
    MAF_SENSOR = C(0x66, 5, 0, 2047.96875, "g/s") # MF("(256*B+C)/32", "(256*D+E)/32")
    """Mass air flow sensor"""
    ENGINE_COOLANT_TEMP_ALT = C(0x67, 3, -40, 215, "°C") # MF("B-40", "C-40")
    """Engine coolant temperature"""
    INTAKE_AIR_TEMP_ALT = C(0x68, 3, -40, 215, "°C") # MF("B-40", "C-40")
    """Intake air temperature sensor"""
    EGR_DATA = C(0x69, 7, None, None, None)
    """Actual EGR, Commanded EGR, and EGR Error"""
    DIESEL_INTAKE_AIR_FLOW = C(0x6A, 5, None, None, None)
    """Commanded Diesel intake air flow control and relative intake air flow position"""
    EGR_TEMP = C(0x6B, 5, None, None, None)
    """Exhaust gas recirculation temperature"""
    THROTTLE_ACTUATOR_ALT = C(0x6C, 5, None, None, None)
    """Commanded throttle actuator control and relative throttle position"""
    FUEL_PRESSURE_CONTROL = C(0x6D, 11, None, None, None)
    """Fuel pressure control system"""
    INJECTION_PRESSURE_CONTROL = C(0x6E, 9, None, None, None)
    """Injection pressure control system"""
    TURBO_PRESSURE = C(0x6F, 3, None, None, None)
    """Turbocharger compressor inlet pressure"""
    BOOST_PRESSURE_CONTROL = C(0x70, 10, None, None, None)
    """Boost pressure control"""
    VGT_CONTROL = C(0x71, 6, None, None, None)
    """Variable Geometry turbo (VGT) control"""
    WASTEGATE_CONTROL = C(0x72, 5, None, None, None)
    """Wastegate control"""
    EXHAUST_PRESSURE = C(0x73, 5, None, None, None)
    """Exhaust pressure"""
    TURBO_SPEED = C(0x74, 5, None, None, None)
    """Turbocharger RPM"""
    TURBO_TEMP = C(0x75, 7, None, None, None)
    """Turbocharger temperature"""
    TURBO_TEMP_ALT = C(0x76, 7, None, None, None)
    """Turbocharger temperature"""
    CHARGE_AIR_COOLER_TEMP = C(0x77, 5, None, None, None)
    """Charge air cooler temperature (CACT)"""
    EGT_BANK_1 = C(0x78, 9, None, None, None)
    """Exhaust Gas temperature (EGT) Bank 1"""
    EGT_BANK_2 = C(0x79, 9, None, None, None)
    """Exhaust Gas temperature (EGT) Bank 2"""
    DPF_PRESSURE_DIFF = C(0x7A, 7, None, None, None)
    """Diesel particulate filter (DPF) differential pressure"""
    DPF_PRESSURE = C(0x7B, 7, None, None, None)
    """Diesel particulate filter (DPF)"""
    DPF_TEMP = C(0x7C, 9, None, None, "°C", F("(256*A+B)/10-40"))
    """Diesel Particulate filter (DPF) temperature"""
    NOX_NTE_CONTROL_STATUS = C(0x7D, 1, None, None, None)
    """NOx NTE (Not-To-Exceed) control area status"""
    PM_NTE_CONTROL_STATUS = C(0x7E, 1, None, None, None)
    """PM NTE (Not-To-Exceed) control area status"""
    ENGINE_RUN_TIME_ALT = C(0x7F, 13, None, None, 's', F("B*(2**24)+C*(2**16)+D*(2**8)+E"))
    """Engine run time (Starting with MY 2010 the California Air Resources Board mandated that all diesel vehicles must supply total engine hours)"""

    SUPPORTED_PIDS_E = C(0x80, 4, None, None, None, SP(0x81)) 
    """PIDs supported [$81 - $A0]"""
    AECD_RUN_TIME = C(0x81, 41, None, None, None)
    """Engine run time for Auxiliary Emissions Control Device(AECD)"""
    AECD_RUN_TIME_AUX = C(0x82, 41, None, None, None)
    """Engine run time for Auxiliary Emissions Control Device(AECD)"""
    NOX_SENSOR = C(0x83, 9, None, None, None)
    """NOx sensor"""
    MANIFOLD_SURFACE_TEMP = C(0x84, 1, None, None, None)
    """Manifold surface temperature"""
    NOX_REAGENT_SYSTEM = C(0x85, 10, None, None, '%', F("100/255*F"))
    """NOx reagent system"""
    PM_SENSOR = C(0x86, 5, None, None, None)
    """Particulate matter (PM) sensor"""
    INTAKE_MAP = C(0x87, 5, None, None, None)
    """Intake manifold absolute pressure"""
    SCR_INDUCE_SYSTEM = C(0x88, 13, None, None, None)
    """SCR Induce System"""
    AECD_RUN_TIME_11_15 = C(0x89, 41, None, None, None)
    """Run Time for AECD #11-#15"""
    AECD_RUN_TIME_16_20 = C(0x8A, 41, None, None, None)
    """Run Time for AECD #16-#20"""
    DIESEL_AFTERTREATMENT = C(0x8B, 7, None, None, None)
    """Diesel Aftertreatment"""
    OXYGEN_SENSOR_WIDE_RANGE = C(0x8C, 17, None, None, None)
    """O2 Sensor (Wide Range)"""
    THROTTLE_POSITION_G = C(0x8D, 1, 0, 100, '%')
    """Throttle Position G"""
    ENGINE_FRICTION_TORQUE_PERC = C(0x8E, 1, -125, 130, '%', F("A-125"))
    """Engine Friction - Percent Torque"""
    PM_SENSOR_BANKS_1_2 = C(0x8F, 7, None, None, None)
    """PM Sensor Bank 1 & 2"""
    WWH_VEHICLE_INFORMATION = C(0x90, 3, None, None, 'h')
    """WWH-OBD Vehicle OBD System Information"""
    WWH_VEHICLE_INFORMATION_ALT = C(0x91, 5, None, None, 'h')
    """WWH-OBD Vehicle OBD System Information"""
    FUEL_SYSTEM_CONTROL = C(0x92, 2, None, None, None)
    """Fuel System Control"""
    WWH_VEHICLE_COUNTERS_SUPPORT = C(0x93, 3, None, None, 'h')
    """WWH-OBD Vehicle OBD Counters support"""
    NOX_WARNING = C(0x94, 12, None, None, None)
    """NOx Warning And Inducement System"""
    EGT = C(0x98, 9, None, None, None)
    """Exhaust Gas Temperature Sensor"""
    EGT_ALT = C(0x99, 9, None, None, None)
    """Exhaust Gas Temperature Sensor"""
    HYBRID_BATTERY_VOLTAGE = C(0x9A, 6, None, None, None)
    """Hybrid/EV Vehicle System Data, Battery, Voltage"""
    DIESEL_EXHAUST_FLUID_SENSOR = C(0x9B, 4, None, None, '%', F("100/255*D"))
    """Diesel Exhaust Fluid Sensor Data"""
    OXYGEN_SENSOR_DATA = C(0x9C, 17, None, None, None)
    """O2 Sensor Data"""
    ENGINE_MASS_FUEL_RATE = C(0x9D, 4, None, None, "g/s")
    """Engine Mass Fuel Rate"""
    ENGINE_EXHAUST_FLOW_RATE = C(0x9E, 2, None, None, "kg/h")
    """Engine Exhaust Flow Rate"""
    FUEL_USE_PERC = C(0x9F, 9, None, None, None)
    """Fuel System Percentage Use"""

    SUPPORTED_PIDS_F = C(0xA0, 4, None, None, None, SP(0xA1))
    """PIDs supported [$A1 - $C0]"""
    NOX_SENSOR_CORRECTED = C(0xA1, 9, None, None, "ppm")
    """NOx Sensor Corrected Data"""
    CYLINDER_FUEL_RATE = C(0xA2, 2, 0, 2047.96875, "mg/stroke", F("(256*A+B)/32"))
    """Cylinder Fuel Rate"""
    EVAP_SYSTEM_VAPOR_PRESSURE = C(0xA3, 9, None, None, "Pa")
    """Evap System Vapor Pressure"""
    TRANSMISSION_ACTUAL_GEAR = C(0xA4, 4, 0, 65.535, "ratio")
    """Transmission Actual Gear"""
    DIESEL_EXHAUST_FLUID_DOSING = C(0xA5, 4, 0, 127.5, '%')
    """Commanded Diesel Exhaust Fluid Dosing"""
    ODOMETER = C(0xA6, 4, 0, 429496729.5, "km", F("(A*(2**24)+B(2**16)+C*(2**8)+D)/10"))
    """Odometer (Starting with MY 2019 the California Air Resources Board mandated that all vehicles must supply odometer)"""
    NOX_CONCENTRATION_SENSORS_3_4 = C(0xA7, 4, None, None, None)
    """NOx Sensor Concentration Sensors 3 and 4"""
    NOX_CORRECTED_CONCENTRATION_SENSORS_3_4 = C(0xA8, 4, None, None, None)
    """NOx Sensor Corrected Concentration Sensors 3 and 4"""
    ABS_ENABLED = C(0xA9, 4, None, None, None)
    """ABS Disable Switch State"""

    SUPPORTED_PIDS_G = C(0xC0, 4, None, None, None, SP(0xC1))
    """PIDs supported [$C1 - $E0]"""
    FUEL_LEVEL_INPUT_A_B = C(0xC3, 2, 0, 25700, '%')
    """Fuel Level Input A/B"""
    EXHAUST_PARTICULATE_DIAG_TIME_COUNT = C(0xC4, 8, 0, 4294967295, "seconds/count")
    """Exhaust Particulate Control System Diagnostic Time/Count"""
    FUEL_PRESSURE_A_B = C(0xC5, 4, 0, 5177, "kPa")
    """Fuel Pressure A and B"""
    PARTICULATE_CONTROL_STATUS_COUNTERS = C(0xC6, 7, 0, 65535, 'h')
    """Byte 1 - Particulate control - driver inducement system status Byte 2,3 - Removal or block of the particulate aftertreatment system counter Byte 4,5 - Liquid regent injection system (e.g. fuel-borne catalyst) failure counter Byte 6,7 - Malfunction of Particulate control monitoring system counter"""
    DISTANCE_SINCE_REFLASH = C(0xC7, 2, 0, 65535, "km")
    """Distance Since Reflash or Module Replacement"""
    NOX_PCD_WARNING_LAMP_STATUS = C(0xC8, 1, None, None, "Bit")
    """NOx Control Diagnostic (NCD) and Particulate Control Diagnostic (PCD) Warning Lamp status"""