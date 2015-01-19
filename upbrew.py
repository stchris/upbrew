#!/usr/bin/env python

import subprocess

import rumps


APP_NAME = "upbrew"
MSG_NO_UPDATES = 'Already up-to-date.\n'
DEFAULT_TIMER_INTERVAL = 60 * 60


class BrewStatusBarApp(rumps.App):
    def __init__(self, name):
        super(BrewStatusBarApp, self).__init__(name)

    def check(self, always_notify=True):
        try:
            res = subprocess.check_output(["brew", "update"])
            notify = (res == MSG_NO_UPDATES and always_notify)
            if notify:
                rumps.notification(APP_NAME, "", res)
        except subprocess.CalledProcessError, e:
            rumps.notification(APP_NAME, "Error", e)

    @rumps.clicked("Check now")
    def check_now(self, _):
        self.title = "checking ..."
        self.check()
        self.title = APP_NAME

    @rumps.timer(DEFAULT_TIMER_INTERVAL)
    def timer(self, _):
        self.title = "checking ..."
        self.check(always_notify=False)
        self.title = APP_NAME


if __name__ == '__main__':
    BrewStatusBarApp(APP_NAME).run()
