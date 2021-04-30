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
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from clickx3.utils.log_util import get_logger

log = get_logger(__name__)


class Driver(WebDriver):

    def __init__(self, web_driver: WebDriver):
        # 直接把WebDriver的属性字典复制过来
        self.__dict__ = web_driver.__dict__
        self.wait_until = DriverWait(self)

    @staticmethod
    def chrome(**kwargs):
        from clickx3.se.support.chromedriver import chrome_driver
        wd = chrome_driver(**kwargs)
        return Driver(wd)

    @staticmethod
    def firefox(**kwargs):
        from clickx3.se.support.geckodriver import firefox_driver
        wd = firefox_driver(**kwargs)
        return Driver(wd)

    @staticmethod
    def edge(**kwargs):
        from clickx3.se.support.msedgedriver import edge_driver
        wd = edge_driver(**kwargs)
        return Driver(wd)

    def get(self, url):
        log.info(f'打开地址，url:[ {url} ]')
        super().get(url)

    def refresh(self):
        log.info('刷新页面')
        super().refresh()

    def sleep(self, secs: float = 1):
        log.info(f'等待 {secs}s')
        time.sleep(secs)

    def clear_cookies(self):
        log.info('清空cookies')
        self.delete_all_cookies()

    def clear_local_storage(self):
        log.info('清空localStorage')
        js = 'localStorage.clear();'
        self.execute_script(js)

    def clear_session_storage(self):
        log.info('清空sessionStorage')
        js = 'sessionStorage.clear();'
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

    def click_exists(self, by, value, visible=True, timeout=2):
        try:
            log.info(f'如果元素存在且可见时点击元素，timeout:[ {timeout}s ]')
            element = self._retry_find_element(by, value, visible=visible, timeout=timeout)
            element.click()
        except NoSuchElementException:
            log.info(f'元素不存在或不可见，无需点击，By:[ {by} ] value:[ {value} ]')

    def tap_exists(self, by, value, visible=True, timeout=2):
        try:
            log.info(f'如果元素存在且可见时点击元素，timeout:[ {timeout}s ]')
            element = self._retry_find_element(by, value, visible=visible, timeout=timeout)
            element.tap()
        except NoSuchElementException:
            log.info(f'元素不存在或不可见，无需点击，By:[ {by} ] value:[ {value} ]')

    def _retry_find_element(self, by, value, **kwargs):
        from clickx3.se.element import Element

        visible = kwargs.pop('visible', False)
        delay = kwargs.pop('delay', 0.5)
        timeout = kwargs.pop('timeout', 10)
        interval = kwargs.pop('interval', 0.5)

        # 计算重试次数
        retry_count = int(float(timeout) / float(interval))
        # 延迟查找元素
        if delay:
            time.sleep(delay)

        # 重试次数小于1时，不重试，找不到直接抛异常
        if retry_count < 1:
            web_element = self.find_element(by, value)
            element = Element(driver=self, web_element=web_element)
            if visible:
                element.wait_until.visibility()
            return element

        # 重试查找元素，元素存在时返回，找不到时重试直到timeout后抛出异常
        for i in range(retry_count):
            try:
                if i > 0:
                    time.sleep(interval)
                web_element = self.find_element(by, value)
                element = Element(driver=self, web_element=web_element)
                if visible:
                    element.wait_until.visibility()
                return element
            except NoSuchElementException:
                if i == (retry_count - 1):
                    raise
                continue


class DriverWait:

    def __init__(self, driver):
        self.driver = driver

    def url_contains(self, url, timeout=5, errmsg=''):
        """等待url包含指定的字符串（区分大小写）

        Returns:
            匹配返回true，不匹配返回false
        """
        log.info(f'等待url跳转并包含:[ {url} ]')
        try:
            return WebDriverWait(self.driver, timeout).until(EC.url_contains(url), message=errmsg)
        except TimeoutException:
            log.error(f'等待超时，当前url:[ {self.driver.current_url} ]')
            raise

    def url_matches(self, pattern, timeout=5, errmsg=''):
        """等待url正则匹配指定的字符串

        Returns:
            匹配返回true，不匹配返回false
        """
        log.info(f'等待url跳转并正则匹配:[ {pattern} ]')
        try:
            return WebDriverWait(self.driver, timeout).until(EC.url_matches(pattern), message=errmsg)
        except TimeoutException:
            log.error(f'等待超时，当前url:[ {self.driver.current_url} ]')
            raise

    def url_to_be(self, url, timeout=5, errmsg=''):
        """等待url完全等于指定的字符串

        Returns:
            匹配返回true，不匹配返回false
        """
        log.info(f'等待url跳转并完全等于:[ {url} ]')
        try:
            return WebDriverWait(self.driver, timeout).until(EC.url_to_be(url), message=errmsg)
        except TimeoutException:
            log.error(f'等待超时，当前url:[ {self.driver.current_url} ]')
            raise

    def url_changes(self, url, timeout=5, errmsg=''):
        """等待url匹配指定的字符串（不完全匹配）

        Returns:
            匹配返回true，不匹配返回false
        """
        log.info(f'等待url跳转并不完全匹配:[ {url} ]')
        try:
            return WebDriverWait(self.driver, timeout).until(EC.url_changes(url), message=errmsg)
        except TimeoutException:
            log.error(f'等待超时，当前url:[ {self.driver.current_url} ]')
            raise


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
