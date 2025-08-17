"""
TMX (Translation Memory eXchange) export functionality.
TMX is a standard format for exchanging translation memories between different tools.
"""

import os
import xml.etree.ElementTree as ET
from datetime import datetime
import logging
from method_registry import get_method_registry

logger = logging.getLogger(__name__)

class TMXExporter:
    """Handle TMX file creation and export."""
    
    def __init__(self):
        self.tmx_version = "1.4"
        self.creation_tool = "Transliterator"
        self.creation_tool_version = "0.1"
        
        # Get language mapping from registry
        self.registry = get_method_registry()
    
    def create_tmx_document(self, source_text, target_text, source_lang=None, target_lang="en", method_name=""):
        """
        Create a TMX document with the given source and target text.
        
        Args:
            source_text (str): Original text
            target_text (str): Transliterated text
            source_lang (str): Source language code (auto-detected or specified)
            target_lang (str): Target language code
            method_name (str): Name of transliteration method used
            
        Returns:
            ET.Element: Root element of TMX document
        """
        # Infer source language from method name if not provided
        if source_lang is None:
            source_lang = self.registry.get_language_code(method_name)
        
        # Create root TMX element
        tmx = ET.Element("tmx")
        tmx.set("version", self.tmx_version)
        
        # Create header
        header = ET.SubElement(tmx, "header")
        header.set("creationtool", self.creation_tool)
        header.set("creationtoolversion", self.creation_tool_version)
        header.set("datatype", "PlainText")
        header.set("segtype", "sentence")
        header.set("adminlang", "en")
        header.set("srclang", source_lang)
        header.set("o-tmf", self.creation_tool)
        header.set("creationdate", datetime.now().strftime("%Y%m%dT%H%M%SZ"))
        
        # Add notes about the transliteration method
        if method_name:
            note = ET.SubElement(header, "note")
            note.text = f"Transliteration method: {method_name}"
        
        # Create body
        body = ET.SubElement(tmx, "body")
        
        # Split text into lines for individual translation units
        source_lines = source_text.strip().split('\n')
        target_lines = target_text.strip().split('\n')
        
        # Ensure we have the same number of lines
        max_lines = max(len(source_lines), len(target_lines))
        source_lines.extend([''] * (max_lines - len(source_lines)))
        target_lines.extend([''] * (max_lines - len(target_lines)))
        
        # Create translation units
        for i, (src_line, tgt_line) in enumerate(zip(source_lines, target_lines)):
            if src_line.strip() or tgt_line.strip():  # Only add non-empty lines
                tu = ET.SubElement(body, "tu")
                tu.set("tuid", f"tu_{i+1}")
                
                # Source translation unit variant
                tuv_src = ET.SubElement(tu, "tuv")
                tuv_src.set("xml:lang", source_lang)
                seg_src = ET.SubElement(tuv_src, "seg")
                seg_src.text = src_line.strip()
                
                # Target translation unit variant
                tuv_tgt = ET.SubElement(tu, "tuv")
                tuv_tgt.set("xml:lang", target_lang)
                seg_tgt = ET.SubElement(tuv_tgt, "seg")
                seg_tgt.text = tgt_line.strip()
        
        return tmx
    
    def _indent_xml(self, elem, level=0):
        """Indent XML for pretty printing (fallback for older Python versions)."""
        indent = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = indent + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = indent
            for child in elem:
                self._indent_xml(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = indent
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = indent
    
    def export_to_file(self, tmx_root, file_path):
        """
        Export TMX document to file.
        
        Args:
            tmx_root (ET.Element): TMX root element
            file_path (str): Path to save the TMX file
            
        Returns:
            tuple: (success: bool, error_message: str)
        """
        try:
            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Create ElementTree and write to file
            tree = ET.ElementTree(tmx_root)
            
            # Pretty print (try modern method first, fallback for older Python)
            try:
                ET.indent(tree, space="  ", level=0)  # Python 3.9+
            except AttributeError:
                # Fallback for older Python versions
                self._indent_xml(tmx_root)
            
            # Write XML declaration and TMX content
            with open(file_path, 'wb') as f:
                f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
                f.write(b'<!DOCTYPE tmx SYSTEM "tmx14.dtd">\n')
                tree.write(f, encoding='utf-8', xml_declaration=False)
            
            logger.info(f"TMX file exported successfully to: {file_path}")
            return True, ""
            
        except PermissionError:
            error_msg = f"Permission denied: Cannot write to {file_path}"
            logger.error(error_msg)
            return False, error_msg
        except OSError as e:
            error_msg = f"File system error: {e}"
            logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Unexpected error during TMX export: {e}"
            logger.error(error_msg)
            return False, error_msg
    
    def export_transliteration(self, source_text, target_text, method_name="", output_dir=None):
        """
        Complete TMX export process for transliteration data.
        
        Args:
            source_text (str): Original text
            target_text (str): Transliterated text
            method_name (str): Transliteration method name
            output_dir (str): Output directory (defaults to user's Documents)
            
        Returns:
            tuple: (success: bool, file_path: str, error_message: str)
        """
        try:
            # Validate inputs
            if not source_text or not source_text.strip():
                return False, "", "Source text is empty"
            if not target_text or not target_text.strip():
                return False, "", "Target text is empty"
            
            # Determine output directory
            if not output_dir:
                output_dir = os.path.expanduser("~/Documents")
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_method_name = "".join(c for c in method_name if c.isalnum() or c in (' ', '_', '-')).strip()
            safe_method_name = safe_method_name.replace(' ', '_')
            filename = f"transliteration_{safe_method_name}_{timestamp}.tmx"
            file_path = os.path.join(output_dir, filename)
            
            # Create TMX document
            tmx_root = self.create_tmx_document(source_text, target_text, method_name=method_name)
            
            # Export to file
            success, error = self.export_to_file(tmx_root, file_path)
            
            if success:
                return True, file_path, ""
            else:
                return False, "", error
                
        except Exception as e:
            error_msg = f"Error during TMX export process: {e}"
            logger.error(error_msg)
            return False, "", error_msg