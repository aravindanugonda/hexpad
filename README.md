# HexPad - Text Analyzer & Hex Inspector

A powerful Streamlit-based web application for analyzing text and viewing its hexadecimal representation. Perfect for debugging text encoding issues, inspecting special characters, and understanding data at the byte level.

## 🚀 Features

- **Text Analysis**: Visualize text with special character representation
- **Hex Inspection**: View hexadecimal representation of text in both ASCII and EBCDIC encoding
- **Character Ruler**: Precise position tracking with configurable line lengths
- **Special Character Visualization**:
  - `·` for spaces
  - `→` for tabs  
  - `¶` for newlines
  - `↴` for carriage returns
  - Unicode symbols for control characters
- **Export Functionality**: Download analysis reports as text files
- **Responsive Design**: Clean, professional interface with real-time metrics

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

3. **Basic Workflow**:
   - Enter or paste text in the input area
   - Configure line length and encoding mode in the sidebar
   - Click "🔍 Analyze Text" to see results
   - Use the ruler for precise character positioning
   - Download analysis reports for offline review

## 🎯 Use Cases

- **Text Encoding Debugging**: Identify encoding issues and special characters
- **Data Analysis**: Inspect binary data representation in text form
- **File Format Analysis**: Understanding file headers and structured data
- **Legacy System Integration**: Working with EBCDIC-encoded mainframe data
- **Educational Tool**: Learning about character encoding and hex representation

## 🔧 Configuration Options

- **Line Length**: Adjustable from 40 to 500 characters (default: 140)
- **Encoding Mode**: ASCII or EBCDIC support
- **Export Formats**: Plain text analysis reports

## 📝 Sample Data

The application includes sample data with common characters for quick testing:
```
1234567890-=qwertyuiop[]\asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+{}|:"<>?QWERTYUIOPASDFGHJKLZXCVBNM
```

## 🎨 Interface Features

- **Professional Styling**: Modern, clean interface with gradient headers
- **Responsive Layout**: Optimized for both desktop and mobile viewing
- **Real-time Metrics**: Live character and line counts
- **Sticky Ruler**: Always-visible position reference
- **Scrollable Output**: Efficient handling of large text analysis

## 🔍 Analysis Output

The tool provides comprehensive analysis including:

1. **Character Position Ruler**: 1-based positioning with visual markers
2. **Processed Text**: Special characters replaced with visible symbols
3. **Hex Representation**: Upper and lower nibbles displayed separately
4. **Line-by-line Breakdown**: Detailed analysis for each line of input

## 📊 Export Features

- **Comprehensive Reports**: Complete analysis with metadata
- **Formatted Output**: Structured text files with clear sections
- **Custom Filenames**: Automatic naming based on encoding mode
- **Legend Included**: Symbol explanations in every export

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🚀 Deployment

For deployment on Streamlit Cloud or other platforms:

1. Ensure `requirements.txt` includes all dependencies
2. The main application file is `hexpad.py`
3. No additional configuration files needed

---

**Happy Analyzing!** 🔍✨
