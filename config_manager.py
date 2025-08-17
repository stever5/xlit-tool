import wx
import os
from typing import Optional, Tuple
from constants import AppConfig

class ConfigManager:
    """Enhanced configuration manager with improved functionality."""
    
    def __init__(self, config_name: str = AppConfig.CONFIG_APP_NAME):
        self.config = wx.Config(config_name)

    def get_font_size(self, default_size: int = AppConfig.DEFAULT_FONT_SIZE) -> int:
        """Retrieve the font size from the config."""
        return self.config.ReadInt(AppConfig.CONFIG_FONT_SIZE_KEY, default_size)

    def set_font_size(self, font_size: int) -> None:
        """Save the font size to the config."""
        self.config.WriteInt(AppConfig.CONFIG_FONT_SIZE_KEY, font_size)
        self.config.Flush()  # Ensure it's written immediately

    def get_last_export_dir(self, default_dir: Optional[str] = None) -> str:
        """Get the last directory used for TMX export."""
        if default_dir is None:
            default_dir = os.path.expanduser(AppConfig.DEFAULT_TMX_DIR)
        return self.config.Read(AppConfig.CONFIG_LAST_EXPORT_DIR_KEY, default_dir)

    def set_last_export_dir(self, directory: str) -> None:
        """Save the last directory used for TMX export."""
        self.config.Write(AppConfig.CONFIG_LAST_EXPORT_DIR_KEY, directory)
        self.config.Flush()

    def get_window_size(self, default_size: Tuple[int, int] = AppConfig.WINDOW_SIZE) -> Tuple[int, int]:
        """Get saved window size or default."""
        width = self.config.ReadInt('WindowWidth', default_size[0])
        height = self.config.ReadInt('WindowHeight', default_size[1])
        return (width, height)

    def set_window_size(self, size: Tuple[int, int]) -> None:
        """Save window size."""
        self.config.WriteInt('WindowWidth', size[0])
        self.config.WriteInt('WindowHeight', size[1])
        self.config.Flush()

    def get_window_position(self, default_pos: Optional[Tuple[int, int]] = None) -> Optional[Tuple[int, int]]:
        """Get saved window position."""
        if default_pos is None:
            return None
        x = self.config.ReadInt('WindowX', default_pos[0])
        y = self.config.ReadInt('WindowY', default_pos[1])
        return (x, y)

    def set_window_position(self, position: Tuple[int, int]) -> None:
        """Save window position."""
        self.config.WriteInt('WindowX', position[0])
        self.config.WriteInt('WindowY', position[1])
        self.config.Flush()

    def get_last_selected_language(self, default: str = "") -> str:
        """Get the last selected language."""
        return self.config.Read('LastSelectedLanguage', default)

    def set_last_selected_language(self, language: str) -> None:
        """Save the last selected language."""
        self.config.Write('LastSelectedLanguage', language)
        self.config.Flush()

    def get_last_selected_method(self, default: str = "") -> str:
        """Get the last selected transliteration method."""
        return self.config.Read('LastSelectedMethod', default)

    def set_last_selected_method(self, method: str) -> None:
        """Save the last selected transliteration method."""
        self.config.Write('LastSelectedMethod', method)
        self.config.Flush()

    # Legacy methods for backward compatibility
    def read_font_size(self, default_size=AppConfig.DEFAULT_FONT_SIZE):
        """Legacy method - use get_font_size instead."""
        return self.get_font_size(default_size)

    def write_font_size(self, font_size):
        """Legacy method - use set_font_size instead."""
        self.set_font_size(font_size)

