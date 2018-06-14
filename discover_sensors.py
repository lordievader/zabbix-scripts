#!/usr/bin/env python3
import json
import os

SENSOR_DIR = '/sys/class/hwmon'


class Sensor():
    def __init__(self, device):
        self.device = device

    def label_sensor(self, item):
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
    def name(self):
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

    @property
    def sensors(self):
        sensors = []
        for item in os.listdir(self.device):
            if '_input' in item:
                sensor, label = self.label_sensor(item)
                sensors.append({
                    '{#DEVICE}': self.name,
                    '{#SENSOR}': sensor,
                    '{#LABEL}': label
                })

        device = os.path.join(
            self.device, 'device')
        for item in os.listdir(device):
            if '_input' in item:
                sensor, label = self.label_sensor(item)
                sensors.append({
                    '{#DEVICE}': self.name,
                    '{#SENSOR}': sensor,
                    '{#LABEL}': label
                })

        return sensors


def hwmon():
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
    print(json.dumps(data, sort_keys=True, indent=4))


if __name__ == '__main__':
    main()
