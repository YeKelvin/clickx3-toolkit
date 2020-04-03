#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : devices_manager.py
# @Time    : 2019/10/15 14:46
# @Author  : Kelvin.Ye
from queue import Queue

from adbutils import adb, AdbDevice

from appuiautomator.utils.design_patterns import Singleton


class DevicesManager:
    pass


class AndroidDevicesManager(Singleton):
    def __init__(self):
        # 设备列表
        self.__unused_list: [AdbDevice] = adb.device_list()
        # 设备总数
        self.__devices_total_number: int = len(self.__unused_list)
        # 空闲设备队列
        self.__unused_queue: Queue = self.__init_queue()
        # 已使用的设备
        self.__used_devices: {str: AdbDevice} = {}

    def get_device(self) -> str:
        """获取空闲设备的设备号
        @:return serial
        """
        device = self.__unused_queue.get()
        serial = device.serial
        self.__used_devices[serial] = device
        return serial

    def release_device(self, serial: str) -> None:
        """释放设备
        """
        device = self.__used_devices.pop(serial)
        self.__unused_queue.put(device)

    def __init_queue(self):
        """初始化设备队列
        """
        unused_queue = Queue(self.__devices_total_number)
        for adb_device in self.__unused_list:
            unused_queue.put(adb_device)
        return unused_queue
