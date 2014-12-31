#!/usr/bin/env python2

"""Youtubedlg module responsible for the options window.

Attributes:
    AUDIO_QUALITY (list): Contains audio qualities. See parsers AUDIO_QUALITY
        attribute for available values.
        
    AUDIO_FORMATS (list): Contains audio formats. 
        See optionsmanager.OptionsManager 'audio_format' option for available
        values.
        
    FORMATS (list): Contains video formats. This list contains all the 
        available video formats without the 'default' and 'none' options.
        See parsers VIDEO_FORMATS attribute for available values.

    SUBS_LANG (list): Contains subtitles languages. See parsers SUBS_LANG
        attribute for available values.
        
    FILESIZES (list): Contains filesize units. See parsers FILESIZE_UNITS
        attribute for available values.
        
Note:
    For every item inside the attributes of this module (except AUDIO_FORMATS)
    there must be a valid key on the corresponding attribute of the parsers
    module. For example to add a new video format you need to specify the 
    video format {'name': 'key'} on the parsers module and then add the 'name'
    of the video format on the FORMATS attribute to be visible on the GUI.
        
"""

from os import name

import wx

from .logmanager import LogGUI
from .version import __version__


from .info import (
    __descriptionfull__,
    __licensefull__,
    __projecturl__,
    __appname__,
    __author__
)

AUDIO_QUALITY = ['high', 'mid', 'low']

AUDIO_FORMATS = [
    "mp3",
    "wav",
    "aac",
    "m4a",
    "vorbis"
]

FORMATS = [
    "3gp [176x144]",
    "3gp [320x240]",
    "flv [400x240]",
    "flv [640x360]",
    "flv [854x480]",
    "webm [640x360]",
    "webm [854x480]",
    "webm [1280x720]",
    "webm [1920x1080]",
    "mp4 [640x360]",
    "mp4 [1280x720]",
    "mp4 [1920x1080]",
    "mp4 [4096x3072]",
    "mp4 144p (DASH)",
    "mp4 240p (DASH)",
    "mp4 360p (DASH)",
    "mp4 480p (DASH)",
    "mp4 720p (DASH)",
    "mp4 1080p (DASH)",
    "mp4 1440p (DASH)",
    "mp4 2160p (DASH)",
    "webm 240p (DASH)",
    "webm 360p (DASH)",
    "webm 480p (DASH)",
    "webm 720p (DASH)",
    "webm 1080p (DASH)",
    "webm 1440p (DASH)",
    "webm 2160p (DASH)",
    "mp4 360p (3D)",
    "mp4 480p (3D)",
    "mp4 720p (3D)",
    "mp4 1080p (3D)",
    "webm 360p (3D)",
    "webm 480p (3D)",
    "webm 720p (3D)",
    "m4a 48k (DASH AUDIO)",
    "m4a 128k (DASH AUDIO)",
    "m4a 256k (DASH AUDIO)",
    "webm 48k (DASH AUDIO)",
    "webm 256k (DASH AUDIO)"
]

SUBS_LANG = [
    "English",
    "Greek",
    "Portuguese",
    "French",
    "Italian",
    "Russian",
    "Spanish",
    "German"
]

FILESIZES = [
    'Bytes',
    'Kilobytes',
    'Megabytes',
    'Gigabytes',
    'Terabytes',
    'Petabytes',
    'Exabytes',
    'Zettabytes',
    'Yottabytes'
]


class OptionsFrame(wx.Frame):

    """Youtubedlg options frame class.

    Attributes:
        FRAME_SIZE (tuple): Frame size (width, height).
        FRAME_TITLE (string): Options window title.
        
        *_TAB (string): Constant string with the name of each tab.
    
    Args:
        parent (mainframe.MainFrame): Parent class.
    
    """
    
    FRAME_SIZE = (640, 270)

    FRAME_TITLE = "Options"

    GENERAL_TAB = "General"
    VIDEO_TAB = "Video"
    AUDIO_TAB = "Audio"
    PLAYLIST_TAB = "Playlist"
    OUTPUT_TAB = "Output"
    SUBTITLES_TAB = "Subtitles"
    FILESYS_TAB = "Filesystem"
    SHUTDOWN_TAB = "Shutdown"
    AUTH_TAB = "Authentication"
    CONNECTION_TAB = "Connection"
    LOG_TAB = "Log"
    CMD_TAB = "Commands"

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title=self.FRAME_TITLE, size=self.FRAME_SIZE)
        self.opt_manager = parent.opt_manager
        self.log_manager = parent.log_manager
        self.app_icon = parent.app_icon

        if self.app_icon is not None:
            self.SetIcon(self.app_icon)

        # Create GUI
        panel = wx.Panel(self)
        notebook = wx.Notebook(panel)

        # Create Tabs
        tab_args = (self, notebook)
        
        self.tabs = (
            (GeneralTab(*tab_args), self.GENERAL_TAB),
            (VideoTab(*tab_args), self.VIDEO_TAB),
            (AudioTab(*tab_args), self.AUDIO_TAB),
            (PlaylistTab(*tab_args), self.PLAYLIST_TAB),
            (OutputTab(*tab_args), self.OUTPUT_TAB),
            (SubtitlesTab(*tab_args), self.SUBTITLES_TAB),
            (FilesystemTab(*tab_args), self.FILESYS_TAB),
            (ShutdownTab(*tab_args), self.SHUTDOWN_TAB),
            (AuthenticationTab(*tab_args), self.AUTH_TAB),
            (ConnectionTab(*tab_args), self.CONNECTION_TAB),
            (LogTab(*tab_args), self.LOG_TAB),
            (CMDTab(*tab_args), self.CMD_TAB)
        )

        # Add tabs on notebook
        for tab, label in self.tabs:
            notebook.AddPage(tab, label)

        sizer = wx.BoxSizer()
        sizer.Add(notebook, 1, wx.EXPAND)
        panel.SetSizer(sizer)

        self.Bind(wx.EVT_CLOSE, self._on_close)

        self.load_all_options()

    def _on_close(self, event):
        """Event handler for wx.EVT_CLOSE event.
        
        This method is used to save the options and hide the options window.
        
        Args:
            event (wx.Event): Event item.
        
        """
        self.save_all_options()
        self.Hide()

    def reset(self):
        """Resets the default options. """
        self.opt_manager.load_default()
        self.load_all_options()

    def load_all_options(self):
        """Load options for each tab. """
        for tab, _ in self.tabs:
            tab.load_options()

    def save_all_options(self):
        """Save options of each tab. """
        for tab, _ in self.tabs:
            tab.save_options()


class TabPanel(wx.Panel):

    """Main tab class from which each tab inherits.
    
    Contains methods to create widgets, load options etc..
    
    Attributes:
        Each of this attributes is the Default one. In order to use a
        different size you must overwrite the corresponding attribute
        on the child object.
    
        CHECKBOX_SIZE (tuple): wx.Checkbox size (width, height). On Windows
            we change the height value in order to look the same with Linux.
    
        BUTTONS_SIZE (tuple): wx.Button size (width, height)
    
        TEXTCTRL_SIZE (tuple): wx.TextCtrl size (width, height)
        
        SPINCTRL_SIZE (tuple): wx.SpinCtrl size (width, height)
        
        SIZE_* (int): Constant size number.
        
    Args:
        parent (OptionsFrame): The parent of all tabs.
        notebook (wx.Notebook): The container for each tab.
    
    """

    CHECKBOX_SIZE = (-1, -1)
    if name == 'nt':
        CHECKBOX_SIZE = (-1, 25)

    BUTTONS_SIZE = (-1, -1)
    TEXTCTRL_SIZE = (-1, -1)
    SPINCTRL_SIZE = (70, 20)

    SIZE_80 = 80
    SIZE_50 = 50
    SIZE_40 = 40
    SIZE_30 = 30
    SIZE_20 = 20
    SIZE_15 = 15
    SIZE_10 = 10
    SIZE_5 = 5

    def __init__(self, parent, notebook):
        wx.Panel.__init__(self, notebook)
        self.opt_manager = parent.opt_manager
        self.log_manager = parent.log_manager
        self.app_icon = parent.app_icon
        
        self.reset_handler = parent.reset
        
    def create_button(self, label, event_handler=None):
        """Creates and returns an wx.Button.
        
        Args:
            label (string): wx.Button label.
            
            event_handler (function): Can be any function with one parameter
                the event item.
            
        Note:
            In order to change the button size you need to overwrite the 
            BUTTONS_SIZE attribute on the current class.
        
        """
        button = wx.Button(self, label=label, size=self.BUTTONS_SIZE)

        if event_handler is not None:
            button.Bind(wx.EVT_BUTTON, event_handler)

        return button

    def create_checkbox(self, label, event_handler=None):
        """Creates and returns an wx.CheckBox.
        
        Args:
            label (string): wx.CheckBox label.
            
            event_handler (function): Can be any function with one parameter
                the event item.
                
        Note:
            In order to change the checkbox size you need to overwrite the
            CHECKBOX_SIZE attribute on the current class.
        
        """
        checkbox = wx.CheckBox(self, label=label, size=self.CHECKBOX_SIZE)

        if event_handler is not None:
            checkbox.Bind(wx.EVT_CHECKBOX, event_handler)

        return checkbox

    def create_textctrl(self, style=None):
        """Creates and returns an wx.TextCtrl.
        
        Args:
            style (long): Can be any valid wx.TextCtrl style.
                
        Note:
            In order to change the textctrl size you need to overwrite the
            TEXTCTRL_SIZE attribute on the current class.
        
        """
        if style is None:
            textctrl = wx.TextCtrl(self, size=self.TEXTCTRL_SIZE)
        else:
            textctrl = wx.TextCtrl(self, size=self.TEXTCTRL_SIZE, style=style)

        return textctrl

    def create_combobox(self, choices, size=(-1, -1), event_handler=None):
        """Creates and returns an wx.ComboBox.
        
        Args:
            choices (list): List of strings that contains the choices for the
                wx.ComboBox widget.
                
            size (tuple): wx.ComboBox size (width, height).
            
            event_handler (function): Can be any function with one parameter
                the event item.
        
        """
        combobox = wx.ComboBox(self, choices=choices, size=size)

        if event_handler is not None:
            combobox.Bind(wx.EVT_COMBOBOX, event_handler)

        return combobox

    def create_dirdialog(self, label):
        """Creates and returns an wx.DirDialog.

        Args:
            label (string): wx.DirDialog widget title.s
        
        """
        dlg = wx.DirDialog(self, label)
        return dlg
        
    def create_radiobutton(self, label, event_handler=None, style=None):
        """Creates and returns an wx.RadioButton.
        
        Args:
            label (string): wx.RadioButton label.
            
            event_handler (function): Can be any function with one parameter
                the event item.
        
            style (long): Can be any valid wx.RadioButton style.
        
        """
        if style is None:
            radiobutton = wx.RadioButton(self, label=label)
        else:
            radiobutton = wx.RadioButton(self, label=label, style=style)

        if event_handler is not None:
            radiobutton.Bind(wx.EVT_RADIOBUTTON, event_handler)

        return radiobutton

    def create_spinctrl(self, spin_range=(0, 999)):
        """Creates and returns an wx.SpinCtrl.
        
        Args:
            spin_range (tuple): wx.SpinCtrl range (min, max).
            
        Note:
            In order to change the size of the spinctrl widget you need
            to overwrite the SPINCTRL_SIZE attribute on the current class.
        
        """
        spinctrl = wx.SpinCtrl(self, size=self.SPINCTRL_SIZE)
        spinctrl.SetRange(*spin_range)

        return spinctrl

    def create_statictext(self, label):
        """Creates and returns an wx.StaticText.
        
        Args:
            label (string): wx.StaticText label.
        
        """
        statictext = wx.StaticText(self, label=label)
        return statictext

    def create_popup(self, text, title, style):
        """Creates an wx.MessageBox.
        
        Args:
            text (string): wx.MessageBox message.
            
            title (string): wx.MessageBox title.
            
            style (long): Can be any valid wx.MessageBox style.
        
        """
        wx.MessageBox(text, title, style)

    def _set_sizer(self):
        """Sets the sizer for the current panel.
        
        You need to overwrite this method on the child class in order
        to set the panels sizers.
        
        """
        pass

    def _disable_items(self):
        """Disables widgets.
        
        If you want any widgets to be disabled by default you specify
        them in this method.
        
        """
        pass
    
    def load_options(self):
        """Load options from the optionsmanager.OptionsManager object
        to the current tab.
        
        """
        pass
    
    def save_options(self):
        """Save options of the current tab back to
        optionsmanager.OptionsManager object.
        
        """
        pass
    

class LogTab(TabPanel):

    """Options frame log tab.

    Attributes:
        Constant strings for the widgets.
    
    """
    
    ENABLE_LABEL = "Enable Log"
    WRITE_LABEL = "Write Time"
    CLEAR_LABEL = "Clear Log"
    VIEW_LABEL = "View Log"
    PATH_LABEL = "Path: {0}"
    LOGSIZE_LABEL = "Log Size: {0} Bytes"
    RESTART_LABEL = "Restart"
    RESTART_MSG = "Please restart {0}"

    def __init__(self, *args, **kwargs):
        super(LogTab, self).__init__(*args, **kwargs)

        self.enable_checkbox = self.create_checkbox(self.ENABLE_LABEL, self._on_enable)
        self.time_checkbox = self.create_checkbox(self.WRITE_LABEL, self._on_time)
        self.clear_button = self.create_button(self.CLEAR_LABEL, self._on_clear)
        self.view_button = self.create_button(self.VIEW_LABEL, self._on_view)

        self.log_path = self.create_statictext(self.PATH_LABEL.format(self._get_logpath()))
        self.log_size = self.create_statictext(self.LOGSIZE_LABEL.format(self._get_logsize()))

        self._set_sizer()
        self._disable_items()

    def _set_sizer(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.AddSpacer(self.SIZE_20)
        main_sizer.Add(self.enable_checkbox, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(self.SIZE_5)
        main_sizer.Add(self.time_checkbox, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(self.SIZE_15)

        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_sizer.Add(self.clear_button)
        buttons_sizer.AddSpacer(self.SIZE_20)
        buttons_sizer.Add(self.view_button)

        main_sizer.Add(buttons_sizer, flag=wx.ALIGN_CENTER_HORIZONTAL)

        main_sizer.AddSpacer(self.SIZE_20)
        main_sizer.Add(self.log_path, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(self.SIZE_10)
        main_sizer.Add(self.log_size, flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.SetSizer(main_sizer)

    def _disable_items(self):
        if self.log_manager is None:
            self.time_checkbox.Disable()
            self.clear_button.Disable()
            self.view_button.Disable()
            self.log_path.Hide()
            self.log_size.Hide()

    def _get_logpath(self):
        """Returns the path to the log file. """
        if self.log_manager is None:
            return ''
        return self.log_manager.log_file

    def _get_logsize(self):
        """Returns the size (Bytes) of the log file. """
        if self.log_manager is None:
            return 0
        return self.log_manager.log_size()

    def _set_logsize(self):
        """Updates the self.log_size widget with the current log file size ."""
        self.log_size.SetLabel(self.LOGSIZE_LABEL.format(self._get_logsize()))
        
    def _on_time(self, event):
        """Event handler for self.time_checkbox. """
        self.log_manager.add_time = self.time_checkbox.GetValue()

    def _on_enable(self, event):
        """Event handler for self.enable_checkbox. """
        self.create_popup(self.RESTART_MSG.format(__appname__),
                          self.RESTART_LABEL,
                          wx.OK | wx.ICON_INFORMATION)

    def _on_clear(self, event):
        """Event handler for self.clear_button. """
        self.log_manager.clear()
        self.log_size.SetLabel(self.LOGSIZE_LABEL.format(self._get_logsize()))

    def _on_view(self, event):
        """Event handler for self.view_button. """
        logger_gui = LogGUI(self)
        logger_gui.Show()
        logger_gui.load(self.log_manager.log_file)

    def load_options(self):
        self.enable_checkbox.SetValue(self.opt_manager.options['enable_log'])
        self.time_checkbox.SetValue(self.opt_manager.options['log_time'])
        self._set_logsize()

    def save_options(self):
        self.opt_manager.options['enable_log'] = self.enable_checkbox.GetValue()
        self.opt_manager.options['log_time'] = self.time_checkbox.GetValue()


class ShutdownTab(TabPanel):

    """Options frame shutdown tab.

    Attributes:
        TEXTCTRL_SIZE (tuple): Overwrites the TEXTCTRL_SIZE attribute of
            the TabPanel class.
            
        *_LABEL (string): Constant string label for the widgets.
    
    """
    
    TEXTCTRL_SIZE = (250, 25)

    SHUTDOWN_LABEL = "Shutdown when finished"
    SUDO_LABEL = "SUDO password"

    def __init__(self, *args, **kwargs):
        super(ShutdownTab, self).__init__(*args, **kwargs)

        self.shutdown_checkbox = self.create_checkbox(self.SHUTDOWN_LABEL, self._on_shutdown_check)
        self.sudo_text = self.create_statictext(self.SUDO_LABEL)
        self.sudo_box = self.create_textctrl(wx.TE_PASSWORD)

        self._set_sizer()
        self._disable_items()

    def _disable_items(self):
        if name == 'nt':
            self.sudo_text.Hide()
            self.sudo_box.Hide()

    def _set_sizer(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.AddSpacer(self.SIZE_40)
        main_sizer.Add(self.shutdown_checkbox, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(self.SIZE_20)
        main_sizer.Add(self.sudo_text, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(self.SIZE_5)
        main_sizer.Add(self.sudo_box, flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.SetSizer(main_sizer)

    def _on_shutdown_check(self, event):
        """Event handler for self.shutdown_checkbox. """
        self.sudo_box.Enable(self.shutdown_checkbox.GetValue())

    def load_options(self):
        self.shutdown_checkbox.SetValue(self.opt_manager.options['shutdown'])
        self.sudo_box.SetValue(self.opt_manager.options['sudo_password'])
        self._on_shutdown_check(None)

    def save_options(self):
        self.opt_manager.options['shutdown'] = self.shutdown_checkbox.GetValue()
        self.opt_manager.options['sudo_password'] = self.sudo_box.GetValue()


class PlaylistTab(TabPanel):

    """Options frame playlist tab.

    Attributes:
        *_LABEL (string): Constant string label for the widgets.
    
    """
    
    START_LABEL = "Playlist Start"
    STOP_LABEL = "Playlist Stop"
    MAX_LABEL = "Max Downloads"

    def __init__(self, *args, **kwargs):
        super(PlaylistTab, self).__init__(*args, **kwargs)

        self.start_spinctrl = self.create_spinctrl((1, 999))
        self.stop_spinctrl = self.create_spinctrl()
        self.max_spinctrl = self.create_spinctrl()

        self.start_text = self.create_statictext(self.START_LABEL)
        self.stop_text = self.create_statictext(self.STOP_LABEL)
        self.max_text = self.create_statictext(self.MAX_LABEL)

        self._set_sizer()

    def _set_sizer(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.AddSpacer(self.SIZE_20)
        main_sizer.Add(self.start_text, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(self.SIZE_5)
        main_sizer.Add(self.start_spinctrl, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(self.SIZE_15)
        main_sizer.Add(self.stop_text, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(self.SIZE_5)
        main_sizer.Add(self.stop_spinctrl, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(self.SIZE_15)
        main_sizer.Add(self.max_text, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(self.SIZE_5)
        main_sizer.Add(self.max_spinctrl, flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.SetSizer(main_sizer)

    def load_options(self):
        self.start_spinctrl.SetValue(self.opt_manager.options['playlist_start'])
        self.stop_spinctrl.SetValue(self.opt_manager.options['playlist_end'])
        self.max_spinctrl.SetValue(self.opt_manager.options['max_downloads'])

    def save_options(self):
        self.opt_manager.options['playlist_start'] = self.start_spinctrl.GetValue()
        self.opt_manager.options['playlist_end'] = self.stop_spinctrl.GetValue()
        self.opt_manager.options['max_downloads'] = self.max_spinctrl.GetValue()


class ConnectionTab(TabPanel):

    """Options frame connection tab.

    Attributes:
        SPINCTRL_SIZE (tuple): Overwrites the SPINCTRL_SIZE attribute of
            the TabPanel class.
    
        *_LABEL (string): Constant string label for widgets.
    
    """
    
    SPINCTRL_SIZE = (60, -1)

    RETRIES_LABEL = "Retries"
    USERAGENT_LABEL = "User Agent"
    REF_LABEL = "Referer"
    PROXY_LABEL = "Proxy"

    def __init__(self, *args, **kwargs):
        super(ConnectionTab, self).__init__(*args, **kwargs)

        self.retries_spinctrl = self.create_spinctrl((1, 999))
        self.useragent_box = self.create_textctrl()
        self.referer_box = self.create_textctrl()
        self.proxy_box = self.create_textctrl()

        self.retries_text = self.create_statictext(self.RETRIES_LABEL)
        self.useragent_text = self.create_statictext(self.USERAGENT_LABEL)
        self.referer_text = self.create_statictext(self.REF_LABEL)
        self.proxy_text = self.create_statictext(self.PROXY_LABEL)

        self._set_sizer()

    def _set_sizer(self):
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        vertical_sizer = wx.BoxSizer(wx.VERTICAL)

        vertical_sizer.AddSpacer(self.SIZE_10)

        retries_sizer = wx.BoxSizer(wx.HORIZONTAL)
        retries_sizer.Add(self.retries_text)
        retries_sizer.AddSpacer(self.SIZE_5)
        retries_sizer.Add(self.retries_spinctrl)
        vertical_sizer.Add(retries_sizer)

        vertical_sizer.AddSpacer(self.SIZE_10)
        vertical_sizer.Add(self.useragent_text)
        vertical_sizer.AddSpacer(self.SIZE_5)
        vertical_sizer.Add(self.useragent_box, flag=wx.EXPAND)
        vertical_sizer.AddSpacer(self.SIZE_10)
        vertical_sizer.Add(self.referer_text)
        vertical_sizer.AddSpacer(self.SIZE_5)
        vertical_sizer.Add(self.referer_box, flag=wx.EXPAND)
        vertical_sizer.AddSpacer(self.SIZE_10)
        vertical_sizer.Add(self.proxy_text)
        vertical_sizer.AddSpacer(self.SIZE_5)
        vertical_sizer.Add(self.proxy_box, flag=wx.EXPAND)

        main_sizer.AddSpacer(self.SIZE_10)
        main_sizer.Add(vertical_sizer, 1, flag=wx.RIGHT, border=self.SIZE_40)

        self.SetSizer(main_sizer)

    def load_options(self):
        self.proxy_box.SetValue(self.opt_manager.options['proxy'])
        self.referer_box.SetValue(self.opt_manager.options['referer'])
        self.retries_spinctrl.SetValue(self.opt_manager.options['retries'])
        self.useragent_box.SetValue(self.opt_manager.options['user_agent'])

    def save_options(self):
        self.opt_manager.options['proxy'] = self.proxy_box.GetValue()
        self.opt_manager.options['referer'] = self.referer_box.GetValue()
        self.opt_manager.options['retries'] = self.retries_spinctrl.GetValue()
        self.opt_manager.options['user_agent'] = self.useragent_box.GetValue()


class AuthenticationTab(TabPanel):

    """Options frame authentication tab.

    Attributes:
        TEXTCTRL_SIZE (tuple): Overwrites the TEXTCTRL_SIZE attribute of the 
            TabPanel class.
            
        *_LABEL (string): Constant string label for the widgets.
    
    """
    
    TEXTCTRL_SIZE = (250, 25)

    USERNAME_LABEL = "Username"
    PASSWORD_LABEL = "Password"
    VIDEOPASS_LABEL = "Video Password (vimeo, smotri)"

    def __init__(self, *args, **kwargs):
        super(AuthenticationTab, self).__init__(*args, **kwargs)

        self.username_box = self.create_textctrl()
        self.password_box = self.create_textctrl(wx.TE_PASSWORD)
        self.videopass_box = self.create_textctrl(wx.TE_PASSWORD)

        self.username_text = self.create_statictext(self.USERNAME_LABEL)
        self.password_text = self.create_statictext(self.PASSWORD_LABEL)
        self.videopass_text = self.create_statictext(self.VIDEOPASS_LABEL)

        self._set_sizer()

    def _set_sizer(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.AddSpacer(self.SIZE_15)
        main_sizer.Add(self.username_text, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(self.SIZE_5)
        main_sizer.Add(self.username_box, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(self.SIZE_15)
        main_sizer.Add(self.password_text, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(self.SIZE_5)
        main_sizer.Add(self.password_box, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(self.SIZE_15)
        main_sizer.Add(self.videopass_text, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(self.SIZE_5)
        main_sizer.Add(self.videopass_box, flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.SetSizer(main_sizer)

    def load_options(self):
        self.username_box.SetValue(self.opt_manager.options['username'])
        self.password_box.SetValue(self.opt_manager.options['password'])
        self.videopass_box.SetValue(self.opt_manager.options['video_password'])

    def save_options(self):
        self.opt_manager.options['username'] = self.username_box.GetValue()
        self.opt_manager.options['password'] = self.password_box.GetValue()
        self.opt_manager.options['video_password'] = self.videopass_box.GetValue()


class AudioTab(TabPanel):

    """Options frame audio tab.

    Attributes:
        *_LABEL (string): Constant string label for the widgets.
    
    """

    TO_AUDIO_LABEL = "Convert to Audio"
    KEEP_VIDEO_LABEL = "Keep Video"
    AUDIO_FORMAT_LABEL = "Audio Format"
    AUDIO_QUALITY_LABEL = "Audio Quality"

    def __init__(self, *args, **kwargs):
        super(AudioTab, self).__init__(*args, **kwargs)

        self.to_audio_checkbox = self.create_checkbox(self.TO_AUDIO_LABEL, self._on_audio_check)
        self.keep_video_checkbox = self.create_checkbox(self.KEEP_VIDEO_LABEL)
        self.audioformat_combo = self.create_combobox(AUDIO_FORMATS, (160, 30))
        self.audioquality_combo = self.create_combobox(AUDIO_QUALITY, (80, 25))

        self.audioformat_text = self.create_statictext(self.AUDIO_FORMAT_LABEL)
        self.audioquality_text = self.create_statictext(self.AUDIO_QUALITY_LABEL)

        self._set_sizer()

    def _set_sizer(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.AddSpacer(self.SIZE_15)
        main_sizer.Add(self.to_audio_checkbox, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(self.SIZE_5)
        main_sizer.Add(self.keep_video_checkbox, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(self.SIZE_10)
        main_sizer.Add(self.audioformat_text, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(self.SIZE_5)
        main_sizer.Add(self.audioformat_combo, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(self.SIZE_10)
        main_sizer.Add(self.audioquality_text, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(self.SIZE_5)
        main_sizer.Add(self.audioquality_combo, flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.SetSizer(main_sizer)

    def _on_audio_check(self, event):
        """Event handler for self.to_audio_checkbox. """
        self.audioformat_combo.Enable(self.to_audio_checkbox.GetValue())
        self.audioquality_combo.Enable(self.to_audio_checkbox.GetValue())

    def load_options(self):
        self.to_audio_checkbox.SetValue(self.opt_manager.options['to_audio'])
        self.keep_video_checkbox.SetValue(self.opt_manager.options['keep_video'])
        self.audioformat_combo.SetValue(self.opt_manager.options['audio_format'])
        self.audioquality_combo.SetValue(self.opt_manager.options['audio_quality'])
        self._on_audio_check(None)

    def save_options(self):
        self.opt_manager.options['to_audio'] = self.to_audio_checkbox.GetValue()
        self.opt_manager.options['keep_video'] = self.keep_video_checkbox.GetValue()
        self.opt_manager.options['audio_format'] = self.audioformat_combo.GetValue()
        self.opt_manager.options['audio_quality'] = self.audioquality_combo.GetValue()


class VideoTab(TabPanel):

    """Options frame video tab.

    Attributes:
        VIDEO_FORMATS (list): List that contains all the video formats
            plus the 'default' one.
            
        SECOND_VIDEO_FORMATS (list): List that contains all the video formats
            plus the 'none' one.
            
        COMBOBOX_SIZE (tuple): Overwrites the COMBOBOX_SIZE attribute of the
            TabPanel class.
            
        *_LABEL (string): Constant string label for the widgets.
    
    """
    
    VIDEO_FORMATS = ["default"] + FORMATS
    SECOND_VIDEO_FORMATS = ["none"] + FORMATS
    
    COMBOBOX_SIZE = (200, 30)

    VIDEO_FORMAT_LABEL = "Video Format"
    SEC_VIDEOFORMAT_LABEL = "Mix Format"

    def __init__(self, *args, **kwargs):
        super(VideoTab, self).__init__(*args, **kwargs)

        self.videoformat_combo = self.create_combobox(self.VIDEO_FORMATS,
                                                      self.COMBOBOX_SIZE,
                                                      self._on_videoformat)
        self.sec_videoformat_combo = self.create_combobox(self.SECOND_VIDEO_FORMATS,
                                                          self.COMBOBOX_SIZE)

        self.videoformat_text = self.create_statictext(self.VIDEO_FORMAT_LABEL)
        self.sec_videoformat_text = self.create_statictext(self.SEC_VIDEOFORMAT_LABEL)

        self._set_sizer()

    def _set_sizer(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.AddSpacer(self.SIZE_30)
        main_sizer.Add(self.videoformat_text, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(self.SIZE_5)
        main_sizer.Add(self.videoformat_combo, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(self.SIZE_10)
        main_sizer.Add(self.sec_videoformat_text, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(self.SIZE_5)
        main_sizer.Add(self.sec_videoformat_combo, flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.SetSizer(main_sizer)

    def _on_videoformat(self, event):
        """Event handler for self.videoformat_combo. """
        condition = (self.videoformat_combo.GetValue() != 'default')
        self.sec_videoformat_combo.Enable(condition)

    def load_options(self):
        self.videoformat_combo.SetValue(self.opt_manager.options['video_format'])
        self.sec_videoformat_combo.SetValue(self.opt_manager.options['second_video_format'])
        self._on_videoformat(None)

    def save_options(self):
        self.opt_manager.options['video_format'] = self.videoformat_combo.GetValue()
        self.opt_manager.options['second_video_format'] = self.sec_videoformat_combo.GetValue()


class OutputTab(TabPanel):

    """Options frame output tab.

    Attributes:
        TEXTCTRL_SIZE (tuple): Overwrites the TEXTCTRL_SIZE attribute of
            the TabPanel class.
            
        * (string): Constant string label for the widgets.
        
    """
    
    TEXTCTRL_SIZE = (300, 20)

    RESTRICT_LABEL = "Restrict filenames (ASCII)"
    ID_AS_NAME = "ID as Name"
    TITLE_AS_NAME = "Title as Name"
    CUST_TITLE = "Custom Template (youtube-dl)"

    def __init__(self, *args, **kwargs):
        super(OutputTab, self).__init__(*args, **kwargs)

        self.res_names_checkbox = self.create_checkbox(self.RESTRICT_LABEL)
        self.id_rbtn = self.create_radiobutton(self.ID_AS_NAME, self._on_pick, wx.RB_GROUP)
        self.title_rbtn = self.create_radiobutton(self.TITLE_AS_NAME, self._on_pick)
        self.custom_rbtn = self.create_radiobutton(self.CUST_TITLE, self._on_pick)
        self.title_template = self.create_textctrl()

        self._set_sizer()

    def _set_sizer(self):
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        vertical_sizer = wx.BoxSizer(wx.VERTICAL)

        vertical_sizer.AddSpacer(self.SIZE_15)
        vertical_sizer.Add(self.res_names_checkbox)
        vertical_sizer.AddSpacer(self.SIZE_5)
        vertical_sizer.Add(self.id_rbtn)
        vertical_sizer.AddSpacer(self.SIZE_5)
        vertical_sizer.Add(self.title_rbtn)
        vertical_sizer.AddSpacer(self.SIZE_5)
        vertical_sizer.Add(self.custom_rbtn)
        vertical_sizer.AddSpacer(self.SIZE_10)
        vertical_sizer.Add(self.title_template)

        main_sizer.Add(vertical_sizer, flag=wx.LEFT, border=self.SIZE_5)

        self.SetSizer(main_sizer)

    def _on_pick(self, event):
        """Event handler for the radiobuttons. """
        self.title_template.Enable(self.custom_rbtn.GetValue())

    def _get_output_format(self):
        """Returns output_format string type base on the radiobuttons.
        
        See optionsmanager.OptionsManager 'output_format' option for more
        informations.
        
        """
        if self.id_rbtn.GetValue():
            return 'id'
        elif self.title_rbtn.GetValue():
            return 'title'
        elif self.custom_rbtn.GetValue():
            return 'custom'

    def _set_output_format(self, output_format):
        """Enables the corresponding radiobutton base on the output_format. """
        if output_format == 'id':
            self.id_rbtn.SetValue(True)
        elif output_format == 'title':
            self.title_rbtn.SetValue(True)
        elif output_format == 'custom':
            self.custom_rbtn.SetValue(True)

    def load_options(self):
        self._set_output_format(self.opt_manager.options['output_format'])
        self.title_template.SetValue(self.opt_manager.options['output_template'])
        self.res_names_checkbox.SetValue(self.opt_manager.options['restrict_filenames'])
        self._on_pick(None)

    def save_options(self):
        self.opt_manager.options['output_format'] = self._get_output_format()
        self.opt_manager.options['output_template'] = self.title_template.GetValue()
        self.opt_manager.options['restrict_filenames'] = self.res_names_checkbox.GetValue()


class FilesystemTab(TabPanel):

    """Options frame filesystem tab.

    Attributes:
        *_LABEL (string): Constant string label for the widgets.
    
    """
    
    IGN_ERR_LABEL = "Ignore Errors"
    OPEN_DIR_LABEL = "Open destination folder"
    WRT_INFO_LABEL = "Write info to (.json) file"
    WRT_DESC_LABEL = "Write description to file"
    WRT_THMB_LABEL = "Write thumbnail to disk"
    FILESIZE_LABEL = "Filesize"
    MIN_LABEL = "Min"
    MAX_LABEL = "Max"
    
    def __init__(self, *args, **kwargs):
        super(FilesystemTab, self).__init__(*args, **kwargs)

        self.ign_err_checkbox = self.create_checkbox(self.IGN_ERR_LABEL)
        self.open_dir_checkbox = self.create_checkbox(self.OPEN_DIR_LABEL)
        self.write_info_checkbox = self.create_checkbox(self.WRT_INFO_LABEL)
        self.write_desc_checkbox = self.create_checkbox(self.WRT_DESC_LABEL)
        self.write_thumbnail_checkbox = self.create_checkbox(self.WRT_THMB_LABEL)
        
        self.min_filesize_spinner = self.create_spinctrl((0, 1024))
        self.max_filesize_spinner = self.create_spinctrl((0, 1024))
        self.min_filesize_combo = self.create_combobox(FILESIZES)
        self.max_filesize_combo = self.create_combobox(FILESIZES)
        self.min_text = self.create_statictext(self.MIN_LABEL)
        self.max_text = self.create_statictext(self.MAX_LABEL)

        self._set_sizer()

    def _set_sizer(self):    
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        main_sizer.Add(self._set_left_sizer(), 1, wx.LEFT, border=self.SIZE_5)
        main_sizer.Add(self._set_right_sizer(), 1, wx.EXPAND)

        self.SetSizer(main_sizer)

    def _set_left_sizer(self):
        """Sets and returns the left BoxSizer. """
        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.AddSpacer(self.SIZE_15)
        sizer.Add(self.ign_err_checkbox)
        sizer.AddSpacer(self.SIZE_5)
        sizer.Add(self.open_dir_checkbox)
        sizer.AddSpacer(self.SIZE_5)
        sizer.Add(self.write_desc_checkbox)
        sizer.AddSpacer(self.SIZE_5)
        sizer.Add(self.write_thumbnail_checkbox)
        sizer.AddSpacer(self.SIZE_5)
        sizer.Add(self.write_info_checkbox)

        return sizer

    def _set_right_sizer(self):
        """Sets and returns the right BoxSizer. """
        static_box = wx.StaticBox(self, label=self.FILESIZE_LABEL)

        sizer = wx.StaticBoxSizer(static_box, wx.VERTICAL)

        sizer.AddSpacer(self.SIZE_20)

        sizer.Add(self.min_text, flag=wx.ALIGN_CENTER_HORIZONTAL)
            
        sizer.AddSpacer(self.SIZE_5)
            
        hor_sizer = wx.BoxSizer(wx.HORIZONTAL)
        hor_sizer.Add(self.min_filesize_spinner)
        hor_sizer.AddSpacer(self.SIZE_10)
        hor_sizer.Add(self.min_filesize_combo)

        sizer.Add(hor_sizer, flag=wx.ALIGN_CENTER_HORIZONTAL)

        sizer.AddSpacer(self.SIZE_10)

        sizer.Add(self.max_text, flag=wx.ALIGN_CENTER_HORIZONTAL)
        
        sizer.AddSpacer(self.SIZE_5)
        
        hor_sizer = wx.BoxSizer(wx.HORIZONTAL)
        hor_sizer.Add(self.max_filesize_spinner)
        hor_sizer.AddSpacer(self.SIZE_10)
        hor_sizer.Add(self.max_filesize_combo)

        sizer.Add(hor_sizer, flag=wx.ALIGN_CENTER_HORIZONTAL)

        return sizer

    def load_options(self):
        self.open_dir_checkbox.SetValue(self.opt_manager.options['open_dl_dir'])
        self.write_info_checkbox.SetValue(self.opt_manager.options['write_info'])
        self.ign_err_checkbox.SetValue(self.opt_manager.options['ignore_errors'])
        self.write_desc_checkbox.SetValue(self.opt_manager.options['write_description'])
        self.write_thumbnail_checkbox.SetValue(self.opt_manager.options['write_thumbnail'])
        self.min_filesize_spinner.SetValue(self.opt_manager.options['min_filesize'])
        self.max_filesize_spinner.SetValue(self.opt_manager.options['max_filesize'])
        self.min_filesize_combo.SetValue(self.opt_manager.options['min_filesize_unit'])
        self.max_filesize_combo.SetValue(self.opt_manager.options['max_filesize_unit'])
        
    def save_options(self):
        self.opt_manager.options['write_thumbnail'] = self.write_thumbnail_checkbox.GetValue()
        self.opt_manager.options['write_description'] = self.write_desc_checkbox.GetValue()
        self.opt_manager.options['ignore_errors'] = self.ign_err_checkbox.GetValue()
        self.opt_manager.options['write_info'] = self.write_info_checkbox.GetValue()
        self.opt_manager.options['open_dl_dir'] = self.open_dir_checkbox.GetValue()
        self.opt_manager.options['min_filesize'] = self.min_filesize_spinner.GetValue()
        self.opt_manager.options['max_filesize'] = self.max_filesize_spinner.GetValue()
        self.opt_manager.options['min_filesize_unit'] = self.min_filesize_combo.GetValue()
        self.opt_manager.options['max_filesize_unit'] = self.max_filesize_combo.GetValue()

class SubtitlesTab(TabPanel):

    """Options frame subtitles tab.

    Attributes:
        *_LABEL (string): Constant string label for the widgets.
    
    """
    
    DL_SUBS_LABEL = "Download subtitle file by language"
    DL_ALL_SUBS_LABEL = "Download all available subtitles"
    DL_AUTO_SUBS_LABEL = "Download automatic subtitle file (YOUTUBE ONLY)"
    EMBED_SUBS_LABEL = "Embed subtitles in the video (only for mp4 videos)"
    SUBS_LANG_LABEL = "Subtitles Language"

    def __init__(self, *args, **kwargs):
        super(SubtitlesTab, self).__init__(*args, **kwargs)

        self.write_subs_checkbox = self.create_checkbox(self.DL_SUBS_LABEL, self._on_subs_pick)
        self.write_all_subs_checkbox = self.create_checkbox(self.DL_ALL_SUBS_LABEL, self._on_subs_pick)
        self.write_auto_subs_checkbox = self.create_checkbox(self.DL_AUTO_SUBS_LABEL, self._on_subs_pick)
        self.embed_subs_checkbox = self.create_checkbox(self.EMBED_SUBS_LABEL)
        self.subs_lang_combo = self.create_combobox(SUBS_LANG, (140, 30))

        self.subs_lang_text = self.create_statictext(self.SUBS_LANG_LABEL)
        
        self._set_sizer()
        self._disable_items()
        
    def _disable_items(self):
        self.embed_subs_checkbox.Disable()
        self.subs_lang_combo.Disable()

    def _set_sizer(self):
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        vertical_sizer = wx.BoxSizer(wx.VERTICAL)

        vertical_sizer.AddSpacer(self.SIZE_15)
        vertical_sizer.Add(self.write_subs_checkbox)
        vertical_sizer.AddSpacer(self.SIZE_5)
        vertical_sizer.Add(self.write_all_subs_checkbox)
        vertical_sizer.AddSpacer(self.SIZE_5)
        vertical_sizer.Add(self.write_auto_subs_checkbox)
        vertical_sizer.AddSpacer(self.SIZE_5)
        vertical_sizer.Add(self.embed_subs_checkbox)
        vertical_sizer.AddSpacer(self.SIZE_10)
        vertical_sizer.Add(self.subs_lang_text, flag=wx.LEFT, border=self.SIZE_5)
        vertical_sizer.AddSpacer(self.SIZE_5)
        vertical_sizer.Add(self.subs_lang_combo, flag=wx.LEFT, border=self.SIZE_10)
        
        main_sizer.Add(vertical_sizer, flag=wx.LEFT, border=self.SIZE_5)

        self.SetSizer(main_sizer)

    def _on_subs_pick(self, event):
        """Event handler for the write_subs checkboxes. """
        if self.write_subs_checkbox.GetValue():
            self.write_all_subs_checkbox.Disable()
            self.write_auto_subs_checkbox.Disable()
            self.embed_subs_checkbox.Enable()
            self.subs_lang_combo.Enable()
        elif self.write_all_subs_checkbox.GetValue():
            self.write_subs_checkbox.Disable()
            self.write_auto_subs_checkbox.Disable()
        elif self.write_auto_subs_checkbox.GetValue():
            self.write_subs_checkbox.Disable()
            self.write_all_subs_checkbox.Disable()
            self.embed_subs_checkbox.Enable()
        else:
            self.embed_subs_checkbox.Disable()
            self.embed_subs_checkbox.SetValue(False)
            self.subs_lang_combo.Disable()
            self.write_subs_checkbox.Enable()
            self.write_all_subs_checkbox.Enable()
            self.write_auto_subs_checkbox.Enable()

    def load_options(self):
        self.subs_lang_combo.SetValue(self.opt_manager.options['subs_lang'])
        self.write_subs_checkbox.SetValue(self.opt_manager.options['write_subs'])
        self.embed_subs_checkbox.SetValue(self.opt_manager.options['embed_subs'])
        self.write_all_subs_checkbox.SetValue(self.opt_manager.options['write_all_subs'])
        self.write_auto_subs_checkbox.SetValue(self.opt_manager.options['write_auto_subs'])
        self._on_subs_pick(None)

    def save_options(self):
        self.opt_manager.options['subs_lang'] = self.subs_lang_combo.GetValue()
        self.opt_manager.options['write_subs'] = self.write_subs_checkbox.GetValue()
        self.opt_manager.options['embed_subs'] = self.embed_subs_checkbox.GetValue()
        self.opt_manager.options['write_all_subs'] = self.write_all_subs_checkbox.GetValue()
        self.opt_manager.options['write_auto_subs'] = self.write_auto_subs_checkbox.GetValue()


class GeneralTab(TabPanel):

    """Options frame general tab.

    Attributes:
        BUTTONS_SIZE (tuple): Overwrites the BUTTONS_SIZE attribute of the 
            TabPanel class.
            
        *_LABEL (string): Constant string label for the widgets.
    
    """
    
    BUTTONS_SIZE = (110, 40)

    ABOUT_LABEL = "About"
    OPEN_LABEL = "Open"
    RESET_LABEL = "Reset Options"
    SAVEPATH_LABEL = "Save Path"
    SETTINGS_DIR_LABEL = "Settings File: {0}"
    PICK_DIR_LABEL = "Choose Directory"
    
    def __init__(self, *args, **kwargs):
        super(GeneralTab, self).__init__(*args, **kwargs)

        self.savepath_box = self.create_textctrl()
        self.about_button = self.create_button(self.ABOUT_LABEL, self._on_about)
        self.open_button = self.create_button(self.OPEN_LABEL, self._on_open)
        self.reset_button = self.create_button(self.RESET_LABEL, self._on_reset)

        self.savepath_text = self.create_statictext(self.SAVEPATH_LABEL)
        
        cfg_file = self.SETTINGS_DIR_LABEL.format(self.opt_manager.settings_file)
        self.cfg_file_dir = self.create_statictext(cfg_file)
        
        self._set_sizer()
        
    def _set_sizer(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.AddSpacer(self.SIZE_20)
        main_sizer.Add(self.savepath_text, flag=wx.ALIGN_CENTER_HORIZONTAL)
        
        main_sizer.AddSpacer(self.SIZE_10)
        savepath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        savepath_sizer.Add(self.savepath_box, 1, wx.LEFT | wx.RIGHT, self.SIZE_80)
        main_sizer.Add(savepath_sizer, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND)
        
        main_sizer.AddSpacer(self.SIZE_20)
        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_sizer.Add(self.about_button)
        buttons_sizer.Add(self.open_button, flag=wx.LEFT | wx.RIGHT, border=self.SIZE_50)
        buttons_sizer.Add(self.reset_button)
        main_sizer.Add(buttons_sizer, flag=wx.ALIGN_CENTER_HORIZONTAL)
        
        main_sizer.AddSpacer(self.SIZE_30)
        main_sizer.Add(self.cfg_file_dir, flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.SetSizer(main_sizer)

    def _on_reset(self, event):
        """Event handler of the self.reset_button. """
        self.reset_handler()

    def _on_open(self, event):
        """Event handler of the self.open_button. """
        dlg = self.create_dirdialog(self.PICK_DIR_LABEL)
        
        if dlg.ShowModal() == wx.ID_OK:
            self.savepath_box.SetValue(dlg.GetPath())

        dlg.Destroy()

    def _on_about(self, event):
        """Event handler of the self.about_button. """
        info = wx.AboutDialogInfo()

        if self.app_icon is not None:
            info.SetIcon(self.app_icon)

        info.SetName(__appname__)
        info.SetVersion(__version__)
        info.SetDescription(__descriptionfull__)
        info.SetWebSite(__projecturl__)
        info.SetLicense(__licensefull__)
        info.AddDeveloper(__author__)

        wx.AboutBox(info)

    def load_options(self):
        self.savepath_box.SetValue(self.opt_manager.options['save_path'])

    def save_options(self):
        self.opt_manager.options['save_path'] = self.savepath_box.GetValue()


class CMDTab(TabPanel):

    """Options frame command tab.

    Attributes:
        CMD_LABEL (string): Constant string label for the widgets.
    
    """
    
    CMD_LABEL = "Command line arguments (e.g. --help)"

    def __init__(self, *args, **kwargs):
        super(CMDTab, self).__init__(*args, **kwargs)

        self.cmd_args_box = self.create_textctrl()
        self.cmd_args_text = self.create_statictext(self.CMD_LABEL)
        
        self._set_sizer()
        
    def _set_sizer(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.AddSpacer(self.SIZE_50)
        main_sizer.Add(self.cmd_args_text, flag=wx.ALIGN_CENTER_HORIZONTAL)

        main_sizer.AddSpacer(self.SIZE_10)
        cmdbox_sizer = wx.BoxSizer(wx.HORIZONTAL)
        cmdbox_sizer.Add(self.cmd_args_box, 1, wx.LEFT | wx.RIGHT, border=self.SIZE_80)
        main_sizer.Add(cmdbox_sizer, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND)

        self.SetSizer(main_sizer)

    def load_options(self):
        self.cmd_args_box.SetValue(self.opt_manager.options['cmd_args'])

    def save_options(self):
        self.opt_manager.options['cmd_args'] = self.cmd_args_box.GetValue()