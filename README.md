# HexPad - Hexdump Utility

A powerful Streamlit-based web application that mimics the Linux `hexdump -C` command functionality with enhanced visual styling. Perfect for converting text to hexdump format and vice versa, with support for multiple character encodings.

## 🚀 Features

- **Text to Hexdump Conversion**: Convert any text to hexdump format with proper offset, hex bytes, and ASCII representation
- **Hex to Text Conversion**: Convert hex strings back to readable text
- **Multiple Encoding Support**: 
  - CP037 (EBCDIC) - IBM mainframe encoding
  - UTF-8 - Universal character encoding
  - ASCII - Basic ASCII encoding
  - CP1252 (Windows) - Windows character encoding
  - ISO-8859-1 (Latin-1) - Western European encoding
- **Configurable Display**: Choose 8, 16, or 32 bytes per line
- **Professional Hexdump Format**: Mimics Linux `hexdump -C` with decimal offsets and ASCII sidebar
- **Visual Enhancements**: Modern UI with gradient styling and animations
- **Export Functionality**: Download hexdump outputs and converted text files
- **Sample Data**: Built-in test data for quick experimentation

## 📋 Requirements

- Python 3.7+
- Streamlit

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/aravindanugonda/hexpad.git
   cd hexpad
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

1. Start the application:
   ```bash
   streamlit run hexpad.py
   ```

2. Open your browser and navigate to `http://localhost:8501`

3. **Text to Hexdump Workflow**:
   - Switch to the "📝 Text → Hexdump Conversion" tab
   - Enter or paste text in the input area
   - Configure encoding and bytes per line in the sidebar
   - Click "🔍 Generate Hexdump" to see the hexdump output
   - Download the hexdump file for offline use

4. **Hex to Text Workflow**:
   - Switch to the "🔄 Hex → Text Conversion" tab
   - Enter hex bytes (with or without spaces)
   - Choose the appropriate encoding in the sidebar
   - Click "🔄 Convert to Text" to see the converted text
   - Download the converted text file

## 🎯 Use Cases

- **Binary Data Analysis**: Inspect file contents and binary data structures
- **Text Encoding Debugging**: Understand how text appears in different encodings
- **Legacy System Integration**: Work with EBCDIC data from mainframe systems
- **File Format Analysis**: Examine file headers and binary formats
- **Educational Tool**: Learn about hexadecimal representation and character encodings
- **Data Recovery**: Convert hex dumps back to readable text

## 🔧 Configuration Options

- **Character Encoding**: Choose from CP037 (EBCDIC), UTF-8, ASCII, CP1252 (Windows), or ISO-8859-1 (Latin-1)
- **Bytes per Line**: Display 8, 16, or 32 bytes per line (default: 16)
- **Sample Data**: Load built-in test data for quick experimentation
- **Clear Function**: Reset all input and output areas

## 📝 Hexdump Format

The application produces hexdump output in the standard format:
```
offset   xx xx xx xx xx xx xx xx  |xxxxxxxx|
0        48 65 6c 6c 6f 20 57 6f  |Hello Wo|
8        72 6c 64 21              |rld!    |
```

- **offset**: Decimal byte offset (0, 16, 32, ...)
- **xx xx**: Hexadecimal bytes with spaces every 4 bytes
- **|xxxxxxxx|**: ASCII representation with non-printable characters as dots

## 🎨 Interface Features

- **Modern UI Design**: Gradient styling with professional color schemes
- **Responsive Layout**: Optimized for desktop and mobile viewing
- **Tabbed Interface**: Separate tabs for text-to-hex and hex-to-text conversion
- **Real-time Metrics**: Live byte counts and encoding information
- **Animated Elements**: Smooth transitions and hover effects
- **Monospace Fonts**: Proper display of hexdump output with fixed-width fonts

## 🔍 Output Features

**Text to Hexdump Conversion:**
1. **Hexdump Display**: Linux `hexdump -C` compatible format
2. **Byte Metrics**: Real-time byte count and encoding information
3. **Download Option**: Export hexdump as text file

**Hex to Text Conversion:**
1. **Text Output**: Converted readable text
2. **Verification Hexdump**: Shows hexdump of converted text for verification
3. **Error Handling**: Clear error messages for invalid hex input
4. **Download Option**: Export converted text as file

## 📊 Export Features

- **Hexdump Files**: Save hexdump output with encoding-specific filenames
- **Text Files**: Export converted text with proper encoding
- **Automatic Naming**: Files named with encoding information
- **Multiple Formats**: Support for various character encodings

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🚀 Deployment

For deployment on Streamlit Cloud or other platforms:

1. Ensure `requirements.txt` includes all dependencies (streamlit)
2. The main application file is `hexpad.py`
3. No additional configuration files needed
4. Set Python version to 3.7+ for compatibility

## 💡 Technical Details

- **EBCDIC Support**: Full CP037 character mapping for mainframe compatibility
- **Unicode Handling**: Proper UTF-8 encoding with error handling
- **Memory Efficient**: Processes large text inputs without performance issues
- **Cross-Platform**: Works on Windows, macOS, and Linux

---

**Happy Hex Dumping!** 🔍✨
