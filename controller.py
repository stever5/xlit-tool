# controller.py
import wx
import logging
import os
from datetime import datetime
from typing import Optional
from model import XlitToolModel
from view import XlitToolView
from tmx_exporter import TMXExporter
from constants import UIStrings

logger = logging.getLogger(__name__)

class XlitToolController:
    def __init__(self) -> None:
        self._model = XlitToolModel()
        self._view = XlitToolView(self)
        self._tmx_exporter = TMXExporter()
        self._populate_transliteration_methods_in_view()
        self._bind_events()
        
        # Restore user's last selections after everything is set up
        self._view.restore_user_selections()

    def _populate_transliteration_methods_in_view(self) -> None:
        """Update the view's comboboxes with available languages and methods."""
        languages = self._model.get_languages()
        self._view.set_languages(languages)
        
        # Initially clear methods until a language is selected
        self._view.set_transliteration_methods([], self._model)

    def _bind_events(self) -> None:
        """Bind view events to controller handlers."""
        self._view.bind_language_combobox_change(self._handle_language_change)
        self._view.bind_combobox_change(self._handle_combobox_change)
        self._view.bind_tmx_button(self._handle_tmx)
        self._view.bind_clear_button(self._handle_clear)
        self._view.bind_transliterate_button(self._handle_transliteration)

    def _handle_language_change(self, event: wx.CommandEvent) -> None:
        """Handle changes in the language combobox."""
        try:
            selected_language = self._view.get_selected_language()
            
            if selected_language and selected_language != UIStrings.SELECT_LANGUAGE:
                # Get methods for the selected language
                methods = self._model.get_methods_by_language(selected_language)
                self._view.set_transliteration_methods(methods, self._model)
                
                # Reset match case checkbox since method hasn't been selected yet
                self._view.set_match_case_enabled(False)
            else:
                # Clear methods if no language selected
                self._view.set_transliteration_methods([], self._model)
                self._view.set_match_case_enabled(False)
                
        except (AttributeError, ValueError) as e:
            logger.error(f"Error handling language change: {e}")
            self._view.show_error_dialog("An error occurred while updating the interface.")
        except Exception as e:
            logger.error(f"Unexpected error handling language change: {e}")
            self._view.show_error_dialog("An unexpected error occurred while updating the interface.")

    def _handle_combobox_change(self, event: wx.CommandEvent) -> None:
        """Handle changes in the transliteration method combobox."""
        try:
            method_name = self._view.get_selected_method()
            enable_match_case = self._model.should_enable_match_case(method_name)
            self._view.set_match_case_enabled(enable_match_case)
        except (AttributeError, ValueError) as e:
            logger.error(f"Error handling combobox change: {e}")
            self._view.show_error_dialog("An error occurred while updating the interface.")
        except Exception as e:
            logger.error(f"Unexpected error handling combobox change: {e}")
            self._view.show_error_dialog("An unexpected error occurred while updating the interface.")

    def _handle_tmx(self, event: wx.CommandEvent) -> None:
        """Handle the 'Save to TMX' button click."""
        try:
            # Get current text and method
            source_text = self._view.get_input_text()
            target_text = self._view.get_output_text()
            method_name = self._view.get_selected_method()
            
            # Validate that we have content to export
            if not source_text or not source_text.strip():
                self._view.show_warning_dialog(
                    "Please enter some text to transliterate before exporting to TMX.",
                    "No Input Text"
                )
                return
                
            if not target_text or not target_text.strip():
                self._view.show_warning_dialog(
                    "Please transliterate the text first before exporting to TMX.",
                    "No Output Text"
                )
                return
            
            # Show file dialog to choose save location
            default_dir = self._view.config_manager.get_last_export_dir()
            with wx.FileDialog(
                self._view,
                UIStrings.TMX_SAVE_DIALOG_TITLE,
                defaultDir=default_dir,
                defaultFile=f"transliteration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tmx",
                wildcard=UIStrings.TMX_FILE_FILTER,
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
            ) as fileDialog:
                
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return  # User cancelled
                
                # Get the selected file path
                file_path = fileDialog.GetPath()
                
                # Save the directory for next time
                self._view.config_manager.set_last_export_dir(os.path.dirname(file_path))
                
                # Ensure .tmx extension
                if not file_path.lower().endswith('.tmx'):
                    file_path += '.tmx'
                
                # Export to TMX
                success, exported_path, error_message = self._tmx_exporter.export_transliteration(
                    source_text, target_text, method_name, os.path.dirname(file_path)
                )
                
                if success:
                    # Rename the exported file to user's chosen name if different
                    if exported_path != file_path:
                        try:
                            os.rename(exported_path, file_path)
                            exported_path = file_path
                        except OSError:
                            pass  # Keep original filename
                    
                    self._view.show_info_dialog(
                        f"TMX file exported successfully!\n\nSaved to: {exported_path}",
                        "Export Successful"
                    )
                    logger.info(f"TMX export successful: {exported_path}")
                else:
                    self._view.show_error_dialog(
                        f"Failed to export TMX file:\n{error_message}",
                        "Export Failed"
                    )
                    
        except (OSError, IOError) as e:
            logger.error(f"File system error during TMX export: {e}")
            self._view.show_error_dialog(
                "A file system error occurred while exporting to TMX. Please check the save location and permissions.",
                "Export Error"
            )
        except ValueError as e:
            logger.error(f"Invalid data during TMX export: {e}")
            self._view.show_error_dialog(
                "Invalid data detected during TMX export. Please check your input text.",
                "Export Error"
            )
        except Exception as e:
            logger.error(f"Unexpected error in TMX export handler: {e}")
            self._view.show_error_dialog(
                "An unexpected error occurred while exporting to TMX. Please try again.",
                "Export Error"
            )

    def _handle_clear(self, event: wx.CommandEvent) -> None:
        """Clear the input and output text fields."""
        try:
            self._view.clear_texts()
            logger.info("Text fields cleared successfully")
        except AttributeError as e:
            logger.error(f"Interface error clearing text fields: {e}")
            self._view.show_error_dialog("An interface error occurred while clearing the text fields.")
        except Exception as e:
            logger.error(f"Unexpected error clearing text fields: {e}")
            self._view.show_error_dialog("An unexpected error occurred while clearing the text fields.")

    def _handle_transliteration(self, event: wx.CommandEvent) -> None:
        """Perform transliteration based on the selected method and input text."""
        try:
            # Get input parameters
            method_name = self._view.get_selected_method()
            text = self._view.get_input_text()
            match_case = self._view.get_match_case() and self._view.is_match_case_enabled()

            # Perform transliteration with error handling
            success, result, error_message, warnings = self._model.transliterate(method_name, text, match_case)
            
            if success:
                self._view.set_output_text(result)
                logger.info(f"Transliteration completed successfully: {len(text)} -> {len(result)} characters")
                
                # Show warnings if any
                if warnings:
                    warning_msg = "Transliteration completed with the following warnings:\n\n" + "\n".join(f"• {w}" for w in warnings)
                    self._view.show_warning_dialog(warning_msg, "Transliteration Warnings")
            else:
                # Show user-friendly error message
                self._view.show_error_dialog(error_message, "Transliteration Error")
                # Clear output on error
                self._view.set_output_text("")
                
        except (AttributeError, ValueError) as e:
            logger.error(f"Interface or data error in transliteration handler: {e}")
            self._view.show_error_dialog(
                "An interface or data error occurred. Please check your input and try again.",
                "Transliteration Error"
            )
            self._view.set_output_text("")
        except Exception as e:
            logger.error(f"Unexpected error in transliteration handler: {e}")
            self._view.show_error_dialog(
                "An unexpected error occurred. Please try again or contact support if the problem persists.",
                "Unexpected Error"
            )
            self._view.set_output_text("")

