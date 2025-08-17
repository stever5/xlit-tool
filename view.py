from config_manager import ConfigManager
import wx
import os
import logging
from typing import List, Dict, Optional, Any
from wx.adv import AboutDialogInfo, AboutBox
from constants import UIStrings, AppConfig

logger = logging.getLogger(__name__)

class XlitToolView(wx.Frame):
    def __init__(self, controller: Any) -> None:
        self.config_manager = ConfigManager()
        
        # Use saved window size or default
        window_size = self.config_manager.get_window_size()
        super().__init__(None, title=UIStrings.WINDOW_TITLE, size=window_size)
        
        # Use saved window position if available
        window_pos = self.config_manager.get_window_position()
        if window_pos:
            self.SetPosition(window_pos)
        
        self.controller = controller
        self.current_font_size = self.config_manager.get_font_size()
        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        self.method_mapping = {}  # Maps display names to full method names
        
        # Bind close event to save window state
        self.Bind(wx.EVT_CLOSE, self.on_close)
        
        self.init_ui()

    def init_ui(self) -> None:
        self.create_menubar()
        self.main_panel = wx.Panel(self)
        self.setup_main_sizer()
        self.apply_font_size(self.current_font_size)

    def setup_main_sizer(self) -> None:
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.create_method_section(self.main_panel), 
            proportion=0, flag=wx.EXPAND|wx.ALL, border=AppConfig.BORDER_SIZE)
        main_sizer.Add(self.create_text_section(self.main_panel), 
            proportion=1, flag=wx.EXPAND|wx.ALL, border=AppConfig.BORDER_SIZE)
        self.main_panel.SetSizer(main_sizer)

    def set_font_recursive(self, container: wx.Window, new_font: wx.Font) -> None:
        """Recursively apply new font to all components within a container."""
        for child in container.GetChildren():
            child.SetFont(new_font)
            if hasattr(child, 'GetChildren') and child.GetChildren():
                self.set_font_recursive(child, new_font)
            if isinstance(child, wx.Button):
                child.SetInitialSize(child.GetBestSize())

    def apply_font_size(self, font_size: int) -> None:
        new_font = wx.Font(font_size, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.set_font_recursive(self, new_font)
        menubar = self.GetMenuBar()
        for i in range(menubar.GetMenuCount()):
            menu = menubar.GetMenu(i)
            for item in menu.GetMenuItems():
                item.SetFont(new_font)
        self.Layout()
        self.main_panel.GetSizer().Layout()

    def on_font_size(self, event: wx.CommandEvent) -> None:
        font_size = int(event.GetEventObject().GetLabel(event.GetId())[:-2])
        self.apply_font_size(font_size)
        self.config_manager.write_font_size(font_size)

    def create_menubar(self) -> None:
        menubar = wx.MenuBar()
        about_menu = wx.Menu()
        about_menu.Append(wx.ID_ABOUT, 'About', 
            'Information about this program')
        menubar.Append(about_menu, '&About')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.on_about, id=wx.ID_ABOUT)

        # Create a Settings menu with font size options
        settings_menu = wx.Menu()
        font_sizes = [10, 12, 14, 16, 18]
        font_size_submenu = self.create_font_size_submenu(font_sizes)

        settings_menu.AppendSubMenu(font_size_submenu, 'Font size')
        menubar.Append(settings_menu, '&Settings')

        self.SetMenuBar(menubar)

    def create_font_size_submenu(self, sizes: List[int]) -> wx.Menu:
        font_size_submenu = wx.Menu()
        for size in sizes:
            item_id = wx.NewIdRef()
            font_size_submenu.Append(item_id, f"{size}px", 
                f"Set font size to {size}px", kind=wx.ITEM_RADIO)
            if size == self.current_font_size:
                font_size_submenu.Check(item_id, True)
            # Bind font size event here
            self.Bind(wx.EVT_MENU, self.on_font_size, item_id)

        return font_size_submenu

    def create_method_section(self, parent: wx.Window) -> wx.StaticBoxSizer:
        """Create the transliteration method section with language and method dropdown menus."""
        staticbox = wx.StaticBox(parent, label=UIStrings.SELECT_LANGUAGE_METHOD_SECTION)
        
        # Language selection
        language_label = wx.StaticText(parent, label=UIStrings.LANGUAGE_LABEL)
        self.language_combo = wx.Choice(parent, size=(AppConfig.LANGUAGE_COMBO_WIDTH, -1))
        
        # Method selection
        method_label = wx.StaticText(parent, label=UIStrings.METHOD_LABEL)
        self.combo = wx.Choice(parent, size=(AppConfig.METHOD_COMBO_WIDTH, -1))
        self.combo.Enable(False)  # Disabled until language is selected

        self.checkbox = wx.CheckBox(parent, label=UIStrings.MATCH_ALL_CAPS)
        self.checkbox.Enable(False)

        # Layout: Language and Method dropdowns in top row, checkbox below
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Top row with language and method selection
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(language_label, proportion=0, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=AppConfig.SMALL_BORDER)
        hbox1.Add(self.language_combo, proportion=0, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=AppConfig.SMALL_BORDER)
        hbox1.Add(method_label, proportion=0, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=AppConfig.SMALL_BORDER)
        hbox1.Add(self.combo, proportion=0, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=AppConfig.SMALL_BORDER)
        
        # Bottom row with checkbox
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(self.checkbox, proportion=0, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=AppConfig.SMALL_BORDER)
        
        vbox.Add(hbox1, proportion=0, flag=wx.EXPAND)
        vbox.Add(hbox2, proportion=0, flag=wx.EXPAND)

        sizer = wx.StaticBoxSizer(staticbox, wx.VERTICAL)
        sizer.Add(vbox, proportion=1, flag=wx.EXPAND|wx.ALL, border=AppConfig.BORDER_SIZE)
        return sizer

    def create_text_section(self, parent: wx.Window) -> wx.StaticBoxSizer:
        """Create the text section with input/output TextCtrls and buttons."""
        staticbox = wx.StaticBox(parent, -1, label=UIStrings.ENTER_TEXT_SECTION)

        sizer = wx.StaticBoxSizer(staticbox, wx.VERTICAL)
        grid = wx.GridBagSizer(hgap=3, vgap=0)
        sizer.Add(grid, 1, flag=wx.EXPAND|wx.ALL)

        text_ctrl_label = wx.StaticText(parent, label=UIStrings.ENTER_PASTE_TEXT)
        grid.Add(text_ctrl_label, pos=(0,0), 
            flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=AppConfig.SMALL_BORDER)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        grid.Add(hbox2, pos=(0,1), flag=wx.EXPAND|wx.ALL|wx.ALIGN_RIGHT, 
            border=AppConfig.SMALL_BORDER)

        self.tmx_button = wx.Button(parent, label=UIStrings.SAVE_LINES_TMX)
        self.clear_button = wx.Button(parent, label=UIStrings.CLEAR)
        self.transliterate_button = wx.Button(parent, label=UIStrings.TRANSLITERATE)

        hbox2.Add(self.tmx_button, proportion=0, flag=wx.RIGHT, border=AppConfig.SMALL_BORDER)
        hbox2.Add(self.clear_button, proportion=0, flag=wx.RIGHT, border=AppConfig.SMALL_BORDER)
        hbox2.Add(self.transliterate_button, proportion=0, flag=wx.RIGHT)

        self.text1 = wx.TextCtrl(parent, size=(AppConfig.TEXT_CTRL_WIDTH, AppConfig.TEXT_CTRL_HEIGHT), style=wx.TE_MULTILINE)
        self.text2 = wx.TextCtrl(parent, size=(AppConfig.TEXT_CTRL_WIDTH, AppConfig.TEXT_CTRL_HEIGHT), style=wx.TE_MULTILINE)

        grid.Add(self.text1, pos=(1,0), flag=wx.EXPAND|wx.ALL, border=AppConfig.SMALL_BORDER)
        grid.Add(self.text2, pos=(1,1), flag=wx.EXPAND|wx.ALL, border=AppConfig.SMALL_BORDER)
        grid.AddGrowableRow(1, 0)
        grid.AddGrowableCol(0, 1)
        grid.AddGrowableCol(1, 1)

        return sizer

    def on_about(self, event: wx.CommandEvent) -> None:
        """Display an About dialog with program information."""
        info = wx.adv.AboutDialogInfo()
        info.SetName(UIStrings.APP_NAME)
        info.SetVersion(UIStrings.APP_VERSION)
        info.SetDescription(UIStrings.APP_DESCRIPTION)
        info.SetLicense(UIStrings.APP_LICENSE)
        info.AddDeveloper(UIStrings.APP_DEVELOPER)

        # Load and set the icon for the About dialog (if it exists)
        icon_path = os.path.join(self.app_dir, "xlit-tool.png")
        if os.path.exists(icon_path):
            try:
                icon = wx.Icon(icon_path, wx.BITMAP_TYPE_PNG)
                info.SetIcon(icon)
            except (OSError, IOError, wx.wxAssertionError) as e:
                # If icon fails to load, continue without it
                logger.debug(f"Failed to load icon for About dialog: {e}")
                pass

        wx.adv.AboutBox(info)

    def on_close(self, event: wx.CloseEvent) -> None:
        """Handle window close event to save state."""
        # Save window size and position
        self.config_manager.set_window_size(self.GetSize())
        self.config_manager.set_window_position(self.GetPosition())
        
        # Save current selections
        if hasattr(self, 'language_combo'):
            selected_language = self.get_selected_language()
            if selected_language and selected_language != UIStrings.SELECT_LANGUAGE:
                self.config_manager.set_last_selected_language(selected_language)
        
        if hasattr(self, 'combo'):
            selected_method = self.get_selected_method()
            if selected_method:
                self.config_manager.set_last_selected_method(selected_method)
        
        # Continue with normal close
        event.Skip()

    def restore_user_selections(self) -> None:
        """Restore the user's last selections."""
        # Restore language selection
        last_language = self.config_manager.get_last_selected_language()
        if last_language:
            for i in range(self.language_combo.GetCount()):
                if self.language_combo.GetString(i) == last_language:
                    self.language_combo.SetSelection(i)
                    # Trigger language change to populate methods
                    if hasattr(self, 'controller'):
                        event = wx.CommandEvent(wx.wxEVT_COMMAND_CHOICE_SELECTED)
                        event.SetEventObject(self.language_combo)
                        self.controller._handle_language_change(event)
                    break
        
        # If we have a language selected and methods are available, restore method selection
        if last_language and hasattr(self, 'method_mapping'):
            last_method = self.config_manager.get_last_selected_method()
            if last_method:
                # Find the display name for this method
                for display_name, full_name in self.method_mapping.items():
                    if full_name == last_method:
                        for i in range(self.combo.GetCount()):
                            if self.combo.GetString(i) == display_name:
                                self.combo.SetSelection(i)
                                # Trigger method change to update UI state
                                if hasattr(self, 'controller'):
                                    event = wx.CommandEvent(wx.wxEVT_COMMAND_CHOICE_SELECTED)
                                    event.SetEventObject(self.combo)
                                    self.controller._handle_combobox_change(event)
                                break
                        break

    def set_languages(self, languages: List[str]) -> None:
        """Set the available languages in the language combobox."""
        self.language_combo.Clear()
        for language in languages:
            self.language_combo.Append(language)
        
        # Set the first item ("Select language") as the default selection
        if len(languages) > 0:
            self.language_combo.SetSelection(0)

    def set_transliteration_methods(self, methods: List[str], model: Optional[Any] = None) -> None:
        """Set the available transliteration methods in the method choice."""
        self.combo.Clear()
        self.method_mapping = {}  # Clear previous mapping
        
        for method in methods:
            if model:
                display_name = model.get_method_display_name(method)
            else:
                display_name = method
            self.combo.Append(display_name)
            self.method_mapping[display_name] = method
        
        # Enable the method combo if methods are available
        self.combo.Enable(len(methods) > 0)
        if len(methods) > 0:
            self.combo.SetSelection(0)
        

    def set_match_case_enabled(self, enabled: bool) -> None:
        """Enable or disable the match case checkbox."""
        self.checkbox.Enable(enabled)

    def get_input_text(self) -> str:
        """Retrieve the content of the input text field."""
        return self.text1.GetValue()

    def get_output_text(self) -> str:
        """Retrieve the content of the output text field."""
        return self.text2.GetValue()

    def get_match_case(self) -> bool:
        """Return the value (True/False) of the 'Match ALL CAPS' checkbox."""
        return self.checkbox.GetValue()

    def get_selected_language(self) -> str:
        """Return the current language from the language Choice."""
        return self.language_combo.GetStringSelection()

    def get_selected_method(self) -> str:
        """Return the current transliteration method from the Choice."""
        display_name = self.combo.GetStringSelection()
        return self.method_mapping.get(display_name, display_name)

    def set_output_text(self, text: str) -> None:
        """Set the text of the output TextCtrl (text2)."""
        self.text2.SetValue(text)

    def is_match_case_enabled(self) -> bool:
        """Check if the match case checkbox is enabled."""
        return self.checkbox.IsEnabled()

    def bind_language_combobox_change(self, handler):
        """Bind an event handler to the language choice change event."""
        self.Bind(wx.EVT_CHOICE, handler, self.language_combo)

    def bind_combobox_change(self, handler):
        """Bind an event handler to the method choice change event."""
        self.Bind(wx.EVT_CHOICE, handler, self.combo)

    def bind_tmx_button(self, handler):
        """Bind an event handler to the 'Save lines to TMX' button click."""
        self.Bind(wx.EVT_BUTTON, handler, self.tmx_button)

    def bind_clear_button(self, handler):
        """Bind an event handler to the 'Clear' button click."""
        self.Bind(wx.EVT_BUTTON, handler, self.clear_button)

    def bind_transliterate_button(self, handler):
        """Bind an event handler to the 'Transliterate' button click."""
        self.Bind(wx.EVT_BUTTON, handler, self.transliterate_button)

    def clear_texts(self):
        """Clear both input and output text fields."""
        self.text1.SetValue("")
        self.text2.SetValue("")

    def show_error_dialog(self, error_message, title="Error"):
        """Display an error dialog to the user."""
        wx.MessageBox(error_message, title, wx.OK | wx.ICON_ERROR)

    def show_warning_dialog(self, warning_message, title="Warning"):
        """Display a warning dialog to the user."""
        wx.MessageBox(warning_message, title, wx.OK | wx.ICON_WARNING)

    def show_info_dialog(self, info_message, title="Information"):
        """Display an information dialog to the user."""
        wx.MessageBox(info_message, title, wx.OK | wx.ICON_INFORMATION)

