#!/usr/bin/env python

"""
upbrew - homebrew update notifier

LICENSE: MIT
"""

import subprocess

import rumps


# status bar message in normal state
APP_NAME = "upbrew"
# status bar message when updates are available
APP_NAME_WITH_UPDATES = "upbrew*"
# status bar message while checking for updates
LOADING_MSG = "checking ..."
# message we expect from homebrew when no updates are available
MSG_NO_UPDATES = 'Already up-to-date.\n'
# message to show in the menu when no new updates are available
MENU_NO_UPDATES = 'No new updates'
# how often, in seconds, we check for updates
DEFAULT_TIMER_INTERVAL = 60 * 60


class BrewStatusBarApp(rumps.App):
    def __init__(self, name):
        super(BrewStatusBarApp, self).__init__(name)
        # store the last output of `brew update` if it's not MSG_NO_UPDATES
        self.last_output = None
        # build the menu
        self.menu_check = rumps.MenuItem('Check now')
        self.menu_updates = rumps.MenuItem(MENU_NO_UPDATES)
        self.menu = [
            self.menu_check,
            self.menu_updates
        ]

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
            if res != MSG_NO_UPDATES:
                # new updates => store and display
                self.last_output = res
                self.menu_updates.title = self.last_output
            else:
                # no new updates => reset menu to default
                self.last_output = None
                self.menu_updates.title = MENU_NO_UPDATES
            notify = (res == MSG_NO_UPDATES and always_notify)
            if notify:
                rumps.notification(APP_NAME, "", res)
        except subprocess.CalledProcessError, e:
            rumps.notification(APP_NAME, "Error", e)

    @rumps.clicked("Check now")
    def check_now(self, _):
        """ manual check handler """
        self.title = LOADING_MSG
        self.check()
        self.title = APP_NAME_WITH_UPDATES if self.last_output else APP_NAME

    @rumps.timer(DEFAULT_TIMER_INTERVAL)
    def timer(self, _):
        """ timed check handler """
        self.title = LOADING_MSG
        self.check(always_notify=False)
        self.title = APP_NAME_WITH_UPDATES if self.last_output else APP_NAME


if __name__ == '__main__':
    BrewStatusBarApp(APP_NAME).run()
