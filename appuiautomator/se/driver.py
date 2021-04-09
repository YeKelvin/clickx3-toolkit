#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : webdriver.py
# @Time    : 2020/10/14 12:24
# @Author  : Kelvin.Ye
import threading
import time

import cv2
import imageio
import numpy as np
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from appuiautomator.utils.log_util import get_logger

log = get_logger(__name__)


class Driver(WebDriver):
    def __init__(self, web_driver: WebDriver):
        # 直接把WebDriver的属性字典复制过来
        self.__dict__ = web_driver.__dict__

    @staticmethod
    def chrome(**kwargs):
        from appuiautomator.se.chromedriver import chrome_driver
        wd = chrome_driver(**kwargs)
        return Driver(wd)

    @staticmethod
    def firefox(**kwargs):
        from appuiautomator.se.geckodriver import firefox_driver
        wd = firefox_driver(**kwargs)
        return Driver(wd)

    def sleep(self, secs: float = 1):
        log.info(f'等待 {secs}s')
        time.sleep(secs)

    def clear_local_storage(self):
        log.info('清空localStorage')
        js = 'window.localStorage.clear();'
        self.execute_script(js)

    def window_scroll(self, width=None, height=None):
        """
        JavaScript API, Only support css positioning
        Setting width and height of window scroll bar.
        """
        if width is None:
            width = "0"
        if height is None:
            height = "0"
        js = f'window.scrollTo({str(width)},{str(height)});'
        self.execute_script(js)

    def get_title(self):
        js = 'return document.title;'
        return self.execute_script(js)

    def get_url(self):
        js = "return document.URL;"
        return self.execute_script(js)

    def accept_alert(self):
        self.switch_to.alert.accept()

    def dismiss_alert(self):
        self.switch_to.alert.dismiss()

    def alert_is_display(self):
        try:
            self.switch_to.alert
        except NoAlertPresentException:
            return False
        else:
            return True

    def get_alert_text(self):
        return self.switch_to.alert.text

    def move_by_offset(self, x, y):
        """Selenium API
        Moving the mouse to an offset from current mouse position.

        Args:
            x: X offset to move to, as a positive or negative integer.
            y: Y offset to move to, as a positive or negative integer.
        """
        ActionChains(self).move_by_offset(x, y).perform()

    def release(self):
        """Selenium API, Releasing a held mouse button on an element"""
        ActionChains(self).release().perform()


class Screenrecord:
    def __init__(self, driver: Driver):
        self._driver = driver
        self._running = False
        self._stop_event = threading.Event()
        self._done_event = threading.Event()
        self._filename = None
        self._fps = 20

    def __call__(self, *args, **kwargs):
        self._start(*args, **kwargs)
        return self

    def _iter_capture(self):
        while not self._stop_event.is_set():
            yield self._driver.get_screenshot_as_base64()

    def _resize_to(self, im, framesize):
        vh, vw = framesize
        h, w = im.shape[:2]
        frame = np.zeros((vh, vw, 3), dtype=np.uint8)  # create black background canvas
        sh = vh / h
        sw = vw / w
        if sh < sw:
            h, w = vh, int(sh * w)
        else:
            h, w = int(sw * h), vw
        left, top = (vw - w) // 2, (vh - h) // 2
        frame[top:top + h, left:left + w, :] = cv2.resize(im, dsize=(w, h))
        return frame

    def _pipe_resize(self, image_iter):
        firstim = next(image_iter)
        yield firstim
        vh, vw = firstim.shape[:2]
        for im in image_iter:
            if im.shape != firstim.shape:
                im = self._resize_to(im, (vh, vw))
            yield im

    def _pipe_convert(self, raw_iter):
        for raw in raw_iter:
            yield imageio.imread(raw)

    def _pipe_limit(self, raw_iter):
        findex = 0
        fstart = time.time()
        for raw in raw_iter:
            elapsed = time.time() - fstart
            fcount = int(elapsed * self._fps)
            for _ in range(fcount - findex):
                yield raw
            findex = fcount

    def _run(self):
        pipelines = [self._pipe_limit, self._pipe_convert, self._pipe_resize]
        _iter = self._iter_capture()
        for p in pipelines:
            _iter = p(_iter)

        with imageio.get_writer(self._filename, fps=self._fps) as wr:
            for im in _iter:
                wr.append_data(im)
        self._done_event.set()

    def _start(self, filename: str, fps: int = 20):
        if self._running:
            raise RuntimeError("screenrecord is already started")

        assert isinstance(fps, int)
        self._filename = filename
        self._fps = fps

        self._running = True
        th = threading.Thread(name="image2video", target=self._run)
        th.daemon = True
        th.start()

    def stop(self):
        if not self._running:
            raise RuntimeError("screenrecord is not started")
        self._stop_event.set()
        ret = self._done_event.wait(10.0)

        # reset
        self._stop_event.clear()
        self._done_event.clear()
        self._running = False
        return ret
