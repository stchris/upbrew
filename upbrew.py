#!/usr/bin/env python

"""
upbrew - homebrew update notifier

LICENSE: MIT
"""

import subprocess

import rumps


# status bar message in normal state
APP_NAME = "upbrew"
# message we expect from homebrew when no updates are available
MSG_NO_UPDATES = 'Already up-to-date.\n'
# how often, in seconds, we check for updates
DEFAULT_TIMER_INTERVAL = 60 * 60


class BrewStatusBarApp(rumps.App):
    def __init__(self, name):
        super(BrewStatusBarApp, self).__init__(name)

    def check(self, always_notify=True):
        """
        Check for updates by calling `brew update` and expecting anything else
        than MSG_NO_UPDATES if updates are available. Then notify if
        appropriate.

        :param always_notify: if False will only notify if there are updates
        or on errors
        """
        try:
            res = subprocess.check_output(["brew", "update"])
            notify = (res == MSG_NO_UPDATES and always_notify)
            if notify:
                rumps.notification(APP_NAME, "", res)
        except subprocess.CalledProcessError, e:
            rumps.notification(APP_NAME, "Error", e)

    @rumps.clicked("Check now")
    def check_now(self, _):
        """ manual check handler """
        self.title = "checking ..."
        self.check()
        self.title = APP_NAME

    @rumps.timer(DEFAULT_TIMER_INTERVAL)
    def timer(self, _):
        """ timed check handler """
        self.title = "checking ..."
        self.check(always_notify=False)
        self.title = APP_NAME


if __name__ == '__main__':
    BrewStatusBarApp(APP_NAME).run()
