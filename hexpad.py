import streamlit as st
import io

SAMPLE_TEXT = "1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+{}|:\"<>?QWERTYUIOPASDFGHJKLZXCVBNM"

def format_hex_line(offset, hex_bytes, ascii_chars, bytes_per_line=16):
    """Format a line in hexdump style with spacing every 4 bytes"""
    # Format offset as decimal (0, 16, 32, etc.)
    offset_str = f"{offset}"

    # Calculate how many actual bytes we have
    actual_bytes = len(hex_bytes) // 2
    
    # Format hex bytes with spaces and extra space every 4 bytes
    hex_parts = []
    for i in range(0, len(hex_bytes), 2):
        if i + 1 < len(hex_bytes):
            hex_parts.append(hex_bytes[i:i+2])
        else:
            hex_parts.append(hex_bytes[i] + " ")

    # Pad with empty spaces for missing bytes to maintain alignment
    for i in range(actual_bytes, bytes_per_line):
        hex_parts.append("  ")  # Two spaces for missing byte

    # Add extra spacing every 4 bytes (every 4 hex pairs)
    formatted_hex = []
    for i, hex_pair in enumerate(hex_parts):
        formatted_hex.append(hex_pair)
        if (i + 1) % 4 == 0 and i + 1 < len(hex_parts):
            formatted_hex.append(" ")  # Extra space every 4 bytes
    
    # Join with spaces and calculate proper padding width
    hex_section = " ".join(formatted_hex)
    
    # Format ASCII section - ALWAYS pad to bytes_per_line width so it never shifts
    ascii_section = "|" + ascii_chars.ljust(bytes_per_line) + "|"
    
    return f"{offset_str:<6}  {hex_section}  {ascii_section}"

def char_to_printable(byte_val):
    """Convert byte to printable ASCII character"""
    if 32 <= byte_val <= 126:  # Printable ASCII range
        return chr(byte_val)
    else:
        return "."

def ebcdic_char_to_printable(byte_val):
    """Convert EBCDIC byte to its actual character representation"""
    # EBCDIC to ASCII mapping for cp037
    ebcdic_to_ascii = {
        0xF0: '0', 0xF1: '1', 0xF2: '2', 0xF3: '3', 0xF4: '4', 
        0xF5: '5', 0xF6: '6', 0xF7: '7', 0xF8: '8', 0xF9: '9',
        0xC1: 'A', 0xC2: 'B', 0xC3: 'C', 0xC4: 'D', 0xC5: 'E', 
        0xC6: 'F', 0xC7: 'G', 0xC8: 'H', 0xC9: 'I', 0xD1: 'J',
        0xD2: 'K', 0xD3: 'L', 0xD4: 'M', 0xD5: 'N', 0xD6: 'O',
        0xD7: 'P', 0xD8: 'Q', 0xD9: 'R', 0xE2: 'S', 0xE3: 'T',
        0xE4: 'U', 0xE5: 'V', 0xE6: 'W', 0xE7: 'X', 0xE8: 'Y',
        0xE9: 'Z', 0x81: 'a', 0x82: 'b', 0x83: 'c', 0x84: 'd',
        0x85: 'e', 0x86: 'f', 0x87: 'g', 0x88: 'h', 0x89: 'i',
        0x91: 'j', 0x92: 'k', 0x93: 'l', 0x94: 'm', 0x95: 'n',
        0x96: 'o', 0x97: 'p', 0x98: 'q', 0x99: 'r', 0xA2: 's',
        0xA3: 't', 0xA4: 'u', 0xA5: 'v', 0xA6: 'w', 0xA7: 'x',
        0xA8: 'y', 0xA9: 'z', 0x40: ' ', 0x4B: '.', 0x4C: '<',
        0x4D: '(', 0x4E: '+', 0x4F: '|', 0x50: '&', 0x5A: '!',
        0x5B: '$', 0x5C: '*', 0x5D: ')', 0x5E: ';', 0x60: '-',
        0x61: '/', 0x6B: ',', 0x6C: '%', 0x6D: '_', 0x6E: '>',
        0x6F: '?', 0x79: '`', 0x7A: ':', 0x7B: '#', 0x7C: '@',
        0x7D: "'", 0x7E: '=', 0x7F: '"', 0xA1: '~', 0x90: '^',
        0xBD: '[', 0xBF: ']', 0xC0: '{', 0xD0: '}', 0xE0: '\\',
        0x6A: '|'
    }
    return ebcdic_to_ascii.get(byte_val, '.')

def text_to_hexdump(text, encoding='utf-8', bytes_per_line=16):
    """Convert text to hexdump format"""
    # Map encoding names
    encoding_map = {
        'cp037 (ebcdic)': 'cp037',
        'utf-8': 'utf-8',
        'ascii': 'ascii',
        'cp1252 (windows)': 'cp1252',
        'iso-8859-1 (latin-1)': 'iso-8859-1'
    }
    
    try:
        enc = encoding_map.get(encoding.lower(), encoding.lower())
        byte_data = text.encode(enc)
    except UnicodeEncodeError:
        enc = encoding_map.get(encoding.lower(), encoding.lower())
        byte_data = text.encode(enc, errors='replace')
    
    lines = []
    offset = 0
    
    for i in range(0, len(byte_data), bytes_per_line):
        chunk = byte_data[i:i + bytes_per_line]
        
        # Convert to hex string
        hex_bytes = ''.join(f'{b:02x}' for b in chunk)
        
        # Convert to ASCII representation - use EBCDIC mapping if EBCDIC encoding
        if encoding.lower().startswith('cp037') or 'ebcdic' in encoding.lower():
            ascii_chars = ''.join(ebcdic_char_to_printable(b) for b in chunk)
        else:
            ascii_chars = ''.join(char_to_printable(b) for b in chunk)
        
        # Format the line
        line = format_hex_line(offset, hex_bytes, ascii_chars, bytes_per_line)
        lines.append(line)
        
        offset += len(chunk)
    
    return '\n'.join(lines)

def hex_to_text(hex_input, encoding='utf-8'):
    """Convert hex string to text"""
    # Map encoding names
    encoding_map = {
        'cp037 (ebcdic)': 'cp037',
        'utf-8': 'utf-8',
        'ascii': 'ascii',
        'cp1252 (windows)': 'cp1252',
        'iso-8859-1 (latin-1)': 'iso-8859-1'
    }
    
    try:
        # Clean hex input
        hex_clean = ''.join(hex_input.split())
        hex_clean = ''.join(c for c in hex_clean if c in '0123456789abcdefABCDEF')
        
        if len(hex_clean) % 2 != 0:
            return "Error: Hex string must have even number of characters"
        
        # Convert to bytes
        byte_data = bytes.fromhex(hex_clean)
        
        # Convert to text
        enc = encoding_map.get(encoding.lower(), encoding.lower())
        return byte_data.decode(enc)
            
    except Exception as e:
        return f"Error: {str(e)}"

def parse_hexdump(hexdump_text):
    """Parse hexdump output back to original text"""
    lines = hexdump_text.strip().split('\n')
    hex_data = ""
    
    for line in lines:
        if not line.strip():
            continue
            
        # Extract hex part (skip offset, take hex section before ASCII)
        parts = line.split('|')
        if len(parts) >= 2:
            hex_part = parts[0].split('  ', 1)
            if len(hex_part) >= 2:
                hex_section = hex_part[1].strip()
                # Remove spaces from hex section
                hex_data += hex_section.replace(' ', '')
    
    return hex_data

def main():
    st.set_page_config(page_title="Hexpad Utility", layout="wide")
    
    st.markdown("""
    <style>
    /* Global styling */
    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 30px;
        font-size: 2.8rem;
        font-weight: 700;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Section headers with animated gradients */
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 12px;
        margin: 25px 0 15px 0;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Enhanced hexdump output with gradient border */
    .hexdump-output {
        font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', 'Source Code Pro', 'Courier New', monospace;
        font-size: 13px;
        line-height: 1.6;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #e8f4fd;
        border: 2px solid transparent;
        background-clip: padding-box;
        border-radius: 12px;
        padding: 25px;
        white-space: pre;
        overflow-x: auto;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
        position: relative;
    }
    
    .hexdump-output::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
        border-radius: 12px;
        z-index: -1;
    }
    
    /* Metrics container with gradient background */
    .metrics-container {
        display: flex;
        justify-content: space-around;
        margin: 20px 0;
        gap: 15px;
        padding: 10px;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(240, 147, 251, 0.1));
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Enhanced metric boxes */
    .metric-box {
        text-align: center;
        padding: 15px 20px;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.7));
        border-radius: 12px;
        min-width: 120px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .metric-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    }
    
    .metric-box strong {
        color: #667eea;
        font-size: 1.2rem;
        font-weight: 700;
    }
    
    /* Monospace font for input text areas with gradient border */
    .stTextArea textarea {
        font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', 'Source Code Pro', 'Courier New', monospace !important;
        font-size: 14px !important;
        line-height: 1.4 !important;
        border: 2px solid transparent !important;
        background: linear-gradient(white, white) padding-box, linear-gradient(135deg, #667eea, #764ba2) border-box !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3) !important;
        transform: scale(1.01) !important;
    }
    
    /* Enhanced sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(102, 126, 234, 0.05), rgba(240, 147, 251, 0.05));
    }
    
    /* Button styling enhancements */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        transition: all 0.3s ease !important;
        color: white !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
    }
    
    /* Sidebar buttons */
    .stButton > button:not([kind="primary"]) {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(240, 147, 251, 0.1)) !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 8px !important;
        color: #667eea !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:not([kind="primary"]):hover {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(240, 147, 251, 0.2)) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* Clear button special styling */
    .stButton > button:has-text("🗑️ Clear All") {
        background: linear-gradient(135deg, #ff6b6b, #ee5a52) !important;
        color: white !important;
        border: none !important;
    }
    
    .stButton > button:has-text("🗑️ Clear All"):hover {
        background: linear-gradient(135deg, #ee5a52, #ff6b6b) !important;
    }
    
    /* Download button styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #51cf66, #40c057) !important;
        border: none !important;
        border-radius: 8px !important;
        color: white !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #40c057, #51cf66) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(64, 192, 87, 0.3) !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(240, 147, 251, 0.1));
        border-radius: 8px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        color: #667eea;
        font-weight: 600;
        transition: all 0.3s ease;
        min-width: 200px;
        text-align: center;
        padding: 8px 16px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Footer enhancements */
    .footer-tip {
        text-align: center;
        padding: 15px;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(240, 147, 251, 0.05));
        border-radius: 10px;
        border: 1px solid rgba(102, 126, 234, 0.1);
        margin-top: 20px;
        color: #667eea;
        font-style: italic;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.7));
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 8px;
    }
    
    /* Animation for page load */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .main {
        animation: fadeInUp 0.6s ease-out;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-title">🔧 Hexpad Utility</h1>', unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        encoding = st.selectbox(
            "Character Encoding",
            ["CP037 (EBCDIC)", "UTF-8", "ASCII", "CP1252 (Windows)", "ISO-8859-1 (Latin-1)"],
            help="Choose the character encoding for conversion"
        )
        
        bytes_per_line = st.selectbox(
            "Bytes per line",
            [8, 16, 32],
            index=1,
            help="Number of bytes to display per line"
        )
        
        # Sample data button
        if st.button("📝 Load Sample", use_container_width=True):
            # Generate sample hex based on current encoding
            encoding_map = {
                'cp037 (ebcdic)': 'cp037',
                'utf-8': 'utf-8',
                'ascii': 'ascii',
                'cp1252 (windows)': 'cp1252',
                'iso-8859-1 (latin-1)': 'iso-8859-1'
            }
            try:
                enc = encoding_map.get(encoding.lower(), encoding.lower())
                sample_bytes = SAMPLE_TEXT.encode(enc)
                sample_hex = ''.join(f'{b:02x}' for b in sample_bytes)
            except:
                sample_bytes = SAMPLE_TEXT.encode('utf-8', errors='replace')
                sample_hex = ''.join(f'{b:02x}' for b in sample_bytes)
            
            st.session_state["input_text"] = SAMPLE_TEXT
            st.session_state["hex_input"] = sample_hex
        
        # Clear button
        if st.button("🗑️ Clear All", use_container_width=True, help="Clear all input and output areas"):
            # Clear session state for both tabs by setting to empty strings
            st.session_state["input_text"] = ""
            st.session_state["hex_input"] = ""
            st.rerun()
        
        st.markdown("### 📖 Format Info")
        st.markdown("""
        **Hexdump Format:**
        ```
        offset   xx xx xx xx xx xx xx xx  |xxxxxxxx|
        ```
        - `offset`: decimal offset (0, 16, 32, ...)
        - `xx xx`: hex bytes with spaces
        - `|xxxxxxxx|`: ASCII representation
        """)
    
    # Main tabs
    tab1, tab2 = st.tabs(["📝 Text → Hexdump Conversion", "🔄 Hex → Text Conversion"])
    
    with tab1:
        st.markdown('<div class="section-header">📝 Text to Hexdump Conversion</div>', unsafe_allow_html=True)
        
        input_text = st.text_area(
            "Input Text",
            height=200,
            key="input_text",
            placeholder="Enter text to convert to hexdump format...",
            help="Enter any text to see its hexdump representation"
        )
        
        # Convert button
        convert_button = st.button("🔍 Generate Hexdump", type="primary", use_container_width=True)
        
        if convert_button and input_text:
            # Show metrics
            try:
                encoding_map = {
                    'cp037 (ebcdic)': 'cp037',
                    'utf-8': 'utf-8',
                    'ascii': 'ascii',
                    'cp1252 (windows)': 'cp1252',
                    'iso-8859-1 (latin-1)': 'iso-8859-1'
                }
                enc = encoding_map.get(encoding.lower(), encoding.lower())
                byte_count = len(input_text.encode(enc))
            except:
                byte_count = len(input_text.encode('utf-8', errors='replace'))
            
            st.markdown(f"""
            <div class="metrics-container">
                <div class="metric-box">
                    <strong>{byte_count}</strong><br>Bytes
                </div>
                <div class="metric-box">
                    <strong>{encoding}</strong><br>Encoding
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Generate hexdump
            hexdump_output = text_to_hexdump(input_text, encoding.lower(), bytes_per_line)
            
            st.markdown("#### 🔍 Hexdump Output")
            st.markdown(f'<div class="hexdump-output">{hexdump_output}</div>', unsafe_allow_html=True)
            
            # Download button
            st.download_button(
                "📥 Download Hexdump",
                hexdump_output,
                file_name=f"hexdump_{encoding.lower()}.txt",
                mime="text/plain"
            )
    
    with tab2:
        st.markdown('<div class="section-header">🔄 Hex to Text Conversion</div>', unsafe_allow_html=True)
        
        hex_input = st.text_area(
            "Hex Input",
            height=150,
            key="hex_input",
            placeholder="Enter hex bytes (e.g., 48656c6c6f20576f726c64 or 48 65 6c 6c 6f)...",
            help="Enter hex bytes separated by spaces or as continuous string"
        )
        
        # Convert button
        convert_button2 = st.button("🔄 Convert to Text", type="primary", use_container_width=True)
        
        if convert_button2 and hex_input.strip():
            result = hex_to_text(hex_input, encoding.lower())
            
            if result.startswith("Error:"):
                st.error(result)
            else:
                # Show metrics for the converted result
                try:
                    encoding_map = {
                        'cp037 (ebcdic)': 'cp037',
                        'utf-8': 'utf-8',
                        'ascii': 'ascii',
                        'cp1252 (windows)': 'cp1252',
                        'iso-8859-1 (latin-1)': 'iso-8859-1'
                    }
                    enc = encoding_map.get(encoding.lower(), encoding.lower())
                    byte_count = len(result.encode(enc))
                except:
                    byte_count = len(result.encode('utf-8', errors='replace'))
                
                st.markdown(f"""
                <div class="metrics-container">
                    <div class="metric-box">
                        <strong>{byte_count}</strong><br>Bytes
                    </div>
                    <div class="metric-box">
                        <strong>{encoding}</strong><br>Encoding
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Show hexdump of result for verification
                hexdump_verification = text_to_hexdump(result, encoding.lower(), bytes_per_line)
                
                st.markdown("#### ✅ Converted Text as Hexdump")
                st.markdown(f'<div class="hexdump-output">{hexdump_verification}</div>', unsafe_allow_html=True)
                
                # Download button
                st.download_button(
                    "📥 Download Text",
                    result,
                    file_name=f"converted_text_{encoding.lower()}.txt",
                    mime="text/plain"
                )
    
    # Footer
    st.markdown("---")
    st.markdown('<div class="footer-tip">💡 <strong>Tip:</strong> This tool mimics the Linux <code>hexdump -C</code> command functionality with enhanced visual styling.</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
