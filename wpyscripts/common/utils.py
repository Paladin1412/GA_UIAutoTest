# -*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

import traceback
import time
import threading
import logging
import wpyscripts.manager as manager

logger = logging.getLogger("wetest")


def screensnap_thread(report, stop, times, interval):
    logger.info("time_snap Start")
    for i in range(times):
        if stop.is_set():
            logger.debug("end")
            return
        try:
            logger.debug("auto screen shot")
            report.screenshot()
            stop.wait(interval)
        except:
            stack = traceback.format_exc()
            logger.warn(stack)


class time_snap(object):
    def __init__(self, interval=10, times=30):
        self.times = times
        self.interval = interval
        self.report = manager.get_reporter()
        self.snap_thread=None

    def __call__(self, fn):
        def wrapped(*args, **kwargs):
            stop=threading.Event()
            try:
                self.snap_thread=threading.Thread(target=screensnap_thread, args=(self.report, stop, self.times, self.interval))
                self.snap_thread.start()
                fn(*args, **kwargs)
            except:
                stack = traceback.format_exc()
                logger.warn(stack)
            finally:
                stop.set()

        return wrapped

