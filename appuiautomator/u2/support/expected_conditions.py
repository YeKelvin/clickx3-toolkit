c#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : expected_conditions.py
# @Time    : 2021/4/15 13:06
# @Author  : Kelvin.Ye

# Not yet implemented


class invisibility_of_element_located(object):
    """ An Expectation for checking that an element is either invisible or not
    present on the DOM.

    locator used to find the element
    """
    def __init__(self, locator):
        self.target = locator

    def __call__(self, driver):
        try:
            target = self.target
            if not isinstance(target, WebElement):
                target = _find_element(driver, target)
            return _element_if_visible(target, False)
        except (NoSuchElementException, StaleElementReferenceException):
            # In the case of NoSuchElement, returns true because the element is
            # not present in DOM. The try block checks if the element is present
            # but is invisible.
            # In the case of StaleElementReference, returns true because stale
            # element reference implies that element is no longer visible.
            return True
