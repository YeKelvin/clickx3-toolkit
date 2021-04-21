#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : devices_manager.py
# @Time    : 2019/10/15 14:46
# @Author  : Kelvin.Ye
from queue import Queue
from typing import Dict, List

from adbutils import AdbDevice, adb

from clickx3.utils.design_patterns import Singleton
from clickx3.utils.log_util import get_logger

log = get_logger(__name__)


class AndroidDevicesManager(Singleton):
    def __init__(self):
        # 设备列表
        self.__unused_devices = adb.device_list()  #type: List[AdbDevice]
        # 设备总数
        self.__devices_total = len(self.__unused_devices)  # type: int
        # 空闲设备队列
        self.__unused_queue = self.__init_queue()  # type: Queue
        # 已使用的设备
        self.__used_devices = {}  # type: Dict[str, AdbDevice]

    def get_device(self) -> str:
        """获取空闲设备的设备号

        Returns: device serial

        """
        device = self.__unused_queue.get()
        serial = device.serial
        self.__used_devices[serial] = device
        log.info(f'获取空闲Android设备的设备号:[ {serial} ]')
        return serial

    def release_device(self, serial: str) -> None:
        """释放设备
        """
        log.info(f'释放Android设备:[ {serial} ]')
        device = self.__used_devices.pop(serial)
        self.__unused_queue.put(device)

    def __init_queue(self):
        """初始化设备队列
        """
        unused_queue = Queue(self.__devices_total)
        for adb_device in self.__unused_devices:
            unused_queue.put(adb_device)
        return unused_queue


class DevicesManager:
    @staticmethod
    def android():
        return AndroidDevicesManager()

    @staticmethod
    def ios(self):
        ...


if __name__ == '__main__':
    from tidevice import Device, Usbmux
    from pprint import pprint

    u = Usbmux()

    # List devices
    devices = u.device_list()
    pprint(devices)

    buid = u.read_system_BUID()
    print("BUID:", buid)

    d = Device()
    dev_pkey = d.get_value("DevicePublicKey", no_session=True)
    print("DevicePublicKey:", dev_pkey)

    wifi_address = d.get_value("WiFiAddress", no_session=True)
    print("WiFi Address:", wifi_address)

    with d.create_inner_connection() as s:
        ret = s.send_recv_packet({
            "Request": "GetValue",
            "Label": "example",
        })
        pprint(ret['Value'])
