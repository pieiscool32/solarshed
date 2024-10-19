import logging
import time
from prometheus_client import start_http_server, Gauge

from solarshed.controllers.renogy_rover import RenogyRover

logger = logging.getLogger(__name__)

SCRAPE_DELAY = 600

battery_percentage_gauge = Gauge('solarshed_battery_percentage', 'Battery %')
battery_voltage_gauge = Gauge('solarshed_battery_volts', 'Battery Voltage')
battery_temperature_gauge = Gauge('solarshed_battery_temperature_celsius', 'Battery Temperature')
battery_capacity_gauge = Gauge('solarshed_battery_amperes', 'Battery Amps')

controller_temperature_gauge = Gauge('solarshed_controller_temperature_celsius', 'Controller Temperature')
charging_state_gauge = Gauge('solarshed_controller_charging_state', 'Controller Charging State')

load_voltage_gauge = Gauge('solarshed_load_volts', 'Load Voltage')
load_current_gauge = Gauge('solarshed_load_amperes', 'Load Current')
load_power_gauge = Gauge('solarshed_load_power_watts', 'Load Power')

solar_voltage_gauge = Gauge('solarshed_solar_volts', 'Solar Voltage')
solar_current_gauge = Gauge('solarshed_solar_amperes', 'Solar Current')
solar_power_gauge = Gauge('solarshed_solar_watts', 'Solar Power')

solar_charge_amp_hours_gauge = Gauge('solarshed_charge_amp_hours', 'Charge Amp Hours Today')
solar_discharge_amp_hours_gauge = Gauge('solarshed_discharge_amp_hours', 'Discharge Amp Hours Today')
solar_power_generated_gauge = Gauge('solarshed_power_generated', 'Power Generation Today')

# Start up the server to expose the metrics.
start_http_server(5000)

while True:
    try:
        controller = RenogyRover('/dev/ttyUSB0', 1)

        battery_percentage_gauge.set(controller.battery_percentage())
        battery_voltage_gauge.set(controller.battery_voltage())
        battery_temperature_gauge.set(controller.battery_temperature())
        battery_capacity_gauge.set(controller.battery_capacity())

        controller_temperature_gauge.set(controller.controller_temperature())
        charging_state_gauge.set(controller.charging_status())

        load_voltage_gauge.set(controller.load_voltage())
        load_current_gauge.set(controller.load_current())
        load_power_gauge.set(controller.load_power())

        solar_voltage_gauge.set(controller.solar_voltage())
        solar_current_gauge.set(controller.solar_current())
        solar_power_gauge.set(controller.solar_power())

        solar_charge_amp_hours_gauge.set(controller.charging_amp_hours_today())
        solar_discharge_amp_hours_gauge.set(controller.discharging_amp_hours_today())
        solar_power_generated_gauge.set(controller.power_generation_today())

        time.sleep(SCRAPE_DELAY)
    except:
        logger.exception('problem updating gauges')
