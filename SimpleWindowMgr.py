import pygetwindow as gw

class SimpleWindowMgr():
    ################################# MIN
    def minimize_full_name(self, name):
        if (name is not None):
            window = self.get_window_full_name(name)
            if (window):
                window[0].minimize()
            else:
                print("Couldnt find the window " + name + " opened.")

    def minimize_startswith_name(self, prefix):
        if (prefix is not None):
            window = self.get_window_startswith_name(prefix)
            window[0].minimize()

    ################################# MAX
    def maximize_full_name(self, name):
        if (name is not None):
            window = self.get_window_full_name(name)
            if (window):
                window[0].maximize()
            else:
                print("Couldnt find the window " + name + " opened.")

    def maximize_startswith_name(self, prefix):
        if (prefix is not None):
            window = self.get_window_startswith_name(prefix)
            window[0].maximize()

    ################################# RESTORE
    def restore_full_name(self, name):
        if (name is not None):
            window = self.get_window_full_name(name)
            if (window):
                window[0].restore()
            else:
                print("Couldnt find the window " + name + " opened.")

    def restore_startswith_name(self, prefix):
        if (prefix is not None):
            window = self.get_window_startswith_name(prefix)
            window[0].restore()

    ################################# RESIZE
    def resize_full_name(self, name, x, y):
        if (name is not None):
            if (x > 0 and y > 0):
                window = self.get_window_startswith_name(name)
                window[0].resizeTo(x, y)

    def resize_startswith_name(self, prefix, x, y):
        if (prefix is not None):
            if (x > 0 and y > 0):
                window = self.get_window_startswith_name(prefix)
                window[0].resizeTo(x, y)

    ################################# MOVE
    def move_full_name(self, name, left, top):
        if (name is not None):
            window = self.get_window_startswith_name(name)
            window[0].moveTo(left, top)

    def move_startswith_name(self, prefix, left, top):
        if (prefix is not None):
            window = self.get_window_startswith_name(prefix)
            window[0].moveTo(left, top)

    ################################# UTILS
    def get_window_full_name(self, name):
        if (name is not None):
            window = gw.getWindowsWithTitle(name)
            return window

    def get_window_startswith_name(self, prefix):
        if (prefix is not None):
            windows = gw.getAllWindows()
            found_window = None
            for win in windows:
                if win.title.startswith(prefix):
                    found_window = win

            if found_window is None:
                print("Window starting with " + prefix + " does not exist")
                return
            target_window_title = found_window.title
            window = gw.getWindowsWithTitle(target_window_title)
            return window