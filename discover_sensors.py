#!/usr/bin/env python3
import json
import os

SENSOR_DIR = '/sys/class/hwmon'


class Sensor():
    def __init__(self, device):
        """Initializes a sensor device.
        """
        self.device = os.path.realpath(device)

    def __repr__(self):
        """Return a string representation of this class.
        """
        return "{0}-{1}-{2}".format(
            self.name, self.connector, self.port_number)

    @property
    def connector(self):
        """Makes something of a guess for the connector.
        Connector is probably not the correct name, but I don't know what is.

        :return: the connector name (str)
        """
        connector = None
        if 'platform' in self.device:
            connector = 'isa'

        elif 'pci' in self.device:
            connector = 'pci'

        elif 'ATK' in self.device:
            connector = 'acpi'

        elif 'virtual' in self.device:
            connector = 'virtual'

        return connector

    @property
    def port_number(self):
        """For lack of a better word, this is the port_number.
        """
        dev_path = os.path.split(
            os.path.realpath(
                os.path.join(
                    self.device, 'device')))[1]

        number = ""
        if dev_path.count(':') > 0:
            dev_path = dev_path.split('.')[0]
            number = "".join(dev_path.split(':')[1:3])

        elif dev_path.count('.') > 0:
            number = dev_path.split('.')[1]
            number = hex(int(number)).replace('0x', '')

        if self.connector not in ['acpi', 'virtual']:
            number = number.zfill(4)

        else:
            number = 0

        return number

    @property
    def name(self):
        """Retrieves the device name.
        """
        try:
            with open(os.path.join(self.device, 'name'), 'r') as data:
                name = data.read().replace('\n', '')

        except FileNotFoundError:
            device = os.path.join(
                self.device, 'device', 'name')
            try:
                with open(device, 'r') as data:
                    name = data.read().replace('\n', '')

            except FileNotFoundError:
                name = 'ERROR'

        return name

    def label_sensor(self, item):
        """Retrieves the label of the sensor.
        """
        sensor = item.replace('_input', '')
        label_file = os.path.join(
            self.device,
            "{0}_label".format(sensor))
        try:
            with open(label_file, 'r') as data:
                label = data.read().replace('\n', '')

        except FileNotFoundError:
            label = self.name

        return sensor, label

    @property
    def sensors(self):
        """Retrieves all the info for the sensors.
        """
        sensors = []
        for item in os.listdir(self.device):
            if '_input' in item:
                sensor, label = self.label_sensor(item)
                sensors.append({
                    '{#DEVICE}': str(self),
                    '{#SHORTDEVICE}': self.name,
                    '{#SENSOR}': sensor,
                    '{#LABEL}': label
                })

        device = os.path.join(
            self.device, 'device')
        if os.path.isdir(device) is False:
            device = self.device

        for item in os.listdir(device):
            if '_input' in item:
                sensor, label = self.label_sensor(item)
                sensors.append({
                    '{#DEVICE}': str(self),
                    '{#SHORTDEVICE}': self.name,
                    '{#SENSOR}': sensor,
                    '{#LABEL}': label
                })

        return sensors


def hwmon():
    """Gathers all the hwmon devices from the system.
    """
    devices = [os.path.join(
        SENSOR_DIR, item) for item in os.listdir(SENSOR_DIR)]
    return devices


def main():
    devices = hwmon()
    sensors = []
    for device in devices:
        mon = Sensor(device)
        sensors.extend(mon.sensors)

    data = {'data': sensors}
    return json.dumps(data, sort_keys=True, indent=4)


if __name__ == '__main__':
    print(main())
