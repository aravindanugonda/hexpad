import streamlit as st
import codecs

DEFAULT_TEXT = r"""1234567890-=qwertyuiop[]\asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+{}|:\"<>?QWERTYUIOPASDFGHJKLZXCVBNM"""

def replace_non_printable(text):
    replaced = []
    for char in text:
        if char == '\t':
            replaced.append('→')   # Tab
        elif char == ' ':
            replaced.append('·')   # Space
        elif char == '\n':
            replaced.append('¶\n') # Newline
        elif char == '\r':
            replaced.append('↴')   # Carriage return
        elif ord(char) < 32:        # Control characters
            replaced.append(chr(0x2400 + ord(char)))
        else:
            replaced.append(char)
    return ''.join(replaced)

def generate_ruler(line_length):
    numbers_line = [' '] * line_length
    ruler_line = ['·'] * line_length
    
    # Create ruler with different markers for different positions
    for pos in range(line_length):
        col_num = pos + 1  # 1-based position
        if col_num % 10 == 0:
            ruler_line[pos] = '|'  # Every 10th position
        elif col_num % 5 == 0:
            ruler_line[pos] = '+'  # Every 5th position
        else:
            ruler_line[pos] = '·'  # Regular positions
    
    # Place position numbers at 1-based intervals (1, 11, 21, 31, etc.)
    for pos in range(1, line_length + 1, 10):
        position_number = pos
        num_str = str(position_number)
        
        # Convert to 0-based index for ruler array
        ruler_pos = pos - 1
        
        # Place number right-aligned at the marker position
        start = max(0, ruler_pos - len(num_str) + 1)
        for i, c in enumerate(num_str):
            write_pos = start + i
            if 0 <= write_pos < line_length:
                numbers_line[write_pos] = c
    
    return ''.join(numbers_line), ''.join(ruler_line)

def generate_html_ruler(line_length):
    """Generate HTML-formatted ruler with colored markers for better visualization"""
    numbers_line = []
    ruler_line = []
    
    # Generate number line
    numbers_str = [' '] * line_length
    for pos in range(1, line_length + 1, 10):
        num_str = str(pos)
        ruler_pos = pos - 1
        start = max(0, ruler_pos - len(num_str) + 1)
        for i, c in enumerate(num_str):
            write_pos = start + i
            if 0 <= write_pos < line_length:
                numbers_str[write_pos] = c
    
    # Create colored number line
    for i, char in enumerate(numbers_str):
        col_num = i + 1
        if char != ' ':
            numbers_line.append(f'<span class="ruler-number-marker">{char}</span>')
        elif col_num % 10 == 0:
            numbers_line.append('<span class="ruler-10th"> </span>')
        elif col_num % 5 == 0:
            numbers_line.append('<span class="ruler-5th"> </span>')
        else:
            numbers_line.append('<span class="ruler-regular"> </span>')
    
    # Create colored ruler line
    for pos in range(line_length):
        col_num = pos + 1
        if col_num % 10 == 0:
            ruler_line.append('<span class="ruler-10th">|</span>')
        elif col_num % 5 == 0:
            ruler_line.append('<span class="ruler-5th">+</span>')
        else:
            ruler_line.append('<span class="ruler-regular">·</span>')
    
    return ''.join(numbers_line), ''.join(ruler_line)

def generate_hex_display(original_text, encoding_mode):
    hex_data = []
    lines = original_text.split('\n')
    for line in lines:
        upper, lower = [], []
        if encoding_mode == 'EBCDIC':
            try:
                ebcdic_bytes = line.encode('cp037')
            except UnicodeEncodeError:
                ebcdic_bytes = line.encode('cp037', errors='replace')
            for byte in ebcdic_bytes:
                hex_pair = f"{byte:02X}"
                upper.append(hex_pair[0])
                lower.append(hex_pair[1])
        else:
            for c in line:
                hex_pair = f"{ord(c):02X}"
                upper.append(hex_pair[0])
                lower.append(hex_pair[1])
        hex_data.append((''.join(upper), ''.join(lower)))
    return hex_data

def main():
    st.set_page_config(page_title="Text Analyzer - Hex Inspector", layout="wide")
    
    # Initialize session state for input_text if not already present
    if "input_text" not in st.session_state:
        st.session_state.input_text = "" # Initialize with empty or DEFAULT_TEXT

    # Professional styling
    st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 30px;
        font-size: 2.5rem;
        font-weight: 600;
    }
    .section-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        color: white;
        padding: 8px 16px;
        border-radius: 8px;
        margin: 20px 0 10px 0;
        font-weight: 600;
    }
    .input-container {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin-bottom: 20px;
    }
    .output-container {
        background: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .legend-box {
        background: #e3f2fd;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #1976d2;
        margin: 15px 0;
        font-family: 'Courier New', monospace;
        font-size: 14px;
    }
    .metrics-container {
        display: flex;
        justify-content: space-around;
        margin: 15px 0;
    }
    .metric-box {
        text-align: center;
        padding: 10px;
        background: #f0f2f6;
        border-radius: 8px;
        min-width: 100px;
    }
    .sticky-ruler-section {
        background: #e8f4f8;
        padding: 10px 15px;
        border-radius: 8px;
        border-left: 4px solid #1976d2;
        margin: 15px 0 10px 0;
        font-weight: 600;
        color: #1976d2;
    }
    .ruler-header {
        font-size: 16px;
        margin-bottom: 8px;
    }
    .scrollable-content {
        max-height: 600px;
        overflow-y: auto;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        margin-top: 10px;
    }
    .ruler-number-marker {
        color: #1f77b4;
        font-weight: bold;
        background: #fff3cd;
        padding: 0 1px;
        border-radius: 2px;
    }
    .ruler-10th {
        color: #d62728;
        font-weight: bold;
        font-size: 1.1em;
    }
    .ruler-5th {
        color: #2ca02c;
        font-weight: bold;
    }
    .ruler-regular {
        color: #666;
    }
    .ruler-container {
        font-family: 'Courier New', monospace;
        background: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        border: 1px solid #dee2e6;
        line-height: 1.3;
    }
    .data-line {
        font-family: 'Courier New', monospace;
        background: #ffffff;
        padding: 2px 10px;
        margin: 1px 0;
        border-left: 3px solid transparent;
    }
    .data-line:hover {
        background: #f8f9fa;
        border-left: 3px solid #007bff;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-title">🔍 Text Analyzer - Hex Inspector</h1>', unsafe_allow_html=True)

    # Sidebar controls with better organization
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        col1, col2 = st.columns(2)
        with col1:
            max_line_length = st.number_input(
                "Line Length", min_value=40, max_value=500, value=140, step=10
            )
        with col2:
            encoding_mode = st.selectbox("Encoding", ["ASCII", "EBCDIC"])
        
        st.markdown("### 🎯 Actions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Load Sample", use_container_width=True):
                st.session_state["input_text"] = DEFAULT_TEXT
        with col2:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state["input_text"] = ""
        
        analyze_button = st.button("🔍 Analyze Text", type="primary", use_container_width=True)
        
        st.markdown("### 📊 Legend")
        st.markdown("""
        <div class="legend-box">
        <strong>Symbol Guide:</strong><br>
        · = Space character<br>
        → = Tab character<br>
        ¶ = Newline character<br>
        ↴ = Carriage return<br>
        Control chars shown as Unicode symbols
        </div>
        """, unsafe_allow_html=True)

    # Input section with professional styling
    st.markdown('<div class="section-header">📝 Input Text</div>', unsafe_allow_html=True)
    
    text = st.text_area(
        label="Text input area for analysis",  # Descriptive label for accessibility
        label_visibility="hidden",  # Hide the label but keep it accessible
        height=200,
        key="input_text",
        placeholder="Paste or type your text here for analysis...",
        help="Enter text to analyze its printable characters and hex representation"
    )
    
    # Show input metrics
    if text:
        lines_count = len(text.split('\n'))
        chars_count = len(text)
        st.markdown(f"""
        <div class="metrics-container">
            <div class="metric-box">
                <strong>{lines_count}</strong><br>Lines
            </div>
            <div class="metric-box">
                <strong>{chars_count}</strong><br>Characters
            </div>
            <div class="metric-box">
                <strong>{max_line_length}</strong><br>Max Width
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Output section
    if analyze_button and text:
        st.markdown('<div class="section-header">📊 Analysis Results</div>', unsafe_allow_html=True)
        
        processed_text = replace_non_printable(text)
        ruler_numbers, ruler_line = generate_ruler(max_line_length)
        html_ruler_numbers, html_ruler_line = generate_html_ruler(max_line_length)
        hex_data = generate_hex_display(text, encoding_mode)
        processed_lines = processed_text.splitlines()  # Changed from split('\\n') to splitlines()
        
        # Truncate to first 9999 lines if needed
        if len(processed_lines) > 9999:
            st.warning("⚠️ Input contains more than 9999 lines. Displaying first 9999 lines only.")
            processed_lines = processed_lines[:9999]
            hex_data = hex_data[:9999] if hex_data else []

        def fit_line(line_content_to_fit):
            if len(line_content_to_fit) > max_line_length:
                return line_content_to_fit[:max_line_length]
            return line_content_to_fit.ljust(max_line_length)

        st.markdown("#### 📝 Analysis Output")
        
        # Display each line with its own ruler for perfect alignment
        for i, line_content in enumerate(processed_lines):
            line_num = i + 1
            fitted_line = fit_line(line_content)
            
            # Generate ruler specifically for this line length
            line_length = len(fitted_line)
            if line_length > 0:
                # Create the ruler display content with perfectly aligned labels
                # Account for line numbers up to 9999 (4 digits + "Line " + ":")
                ruler_display = []
                
                # Position numbers (every 10th position)
                ruler_numbers = generate_ruler(line_length)[0]
                ruler_display.append(f"Pos:      {ruler_numbers}")
                
                # Ruler markers with colors
                ruler_line = generate_ruler(line_length)[1]
                ruler_display.append(f"Cols:     {ruler_line}")
                
                # The actual data line - format for up to 4-digit line numbers
                line_label = f"Line {line_num}:"
                line_label = line_label.ljust(10)  # "Line 9999:" = 10 characters
                ruler_display.append(f"{line_label}{fitted_line}")
                
                # Hex data if available
                if i < len(hex_data):
                    hex_h, hex_l = hex_data[i]
                    fitted_hex_h = fit_line(hex_h)
                    fitted_hex_l = fit_line(hex_l)
                    ruler_display.append(f"Hex H:    {fitted_hex_h}")
                    ruler_display.append(f"Hex L:    {fitted_hex_l}")
                
                # Display this line's ruler and data together
                line_content_display = "\n".join(ruler_display)
                st.code(line_content_display, language=None)
                
                # Add some spacing between different lines
                if i < len(processed_lines) - 1:
                    st.markdown("<br>", unsafe_allow_html=True)
        
        # Download section - positioned after the analysis output
        st.markdown("---")  # Add a separator
        st.markdown("#### 📥 Export Results")
        
        # Create output sections for download with improved alignment
        output_sections = []
        for i, line in enumerate(processed_lines):
            line_num = i + 1
            fitted_line = fit_line(line)
            line_length = len(fitted_line)
            
            if line_length > 0:
                # Generate ruler for this specific line
                ruler_numbers, ruler_line = generate_ruler(line_length)
                
                # Use consistent 10-character labels for alignment (up to Line 9999:)
                line_label = f"Line {line_num}:"
                line_label = line_label.ljust(10)
                
                output_sections.append(f"=== Line {line_num} Analysis ===")
                output_sections.append(f"Pos:      {ruler_numbers}")
                output_sections.append(f"Cols:     {ruler_line}")
                output_sections.append(f"{line_label}{fitted_line}")
                
                if i < len(hex_data):
                    hex_h = fit_line(hex_data[i][0])
                    hex_l = fit_line(hex_data[i][1])
                    output_sections.append(f"Hex H:    {hex_h}")
                    output_sections.append(f"Hex L:    {hex_l}")
                
                output_sections.append("")  # Empty line between sections
        
        download_lines = [
            "=== TEXT ANALYZER REPORT ===",
            f"Encoding Mode: {encoding_mode}",
            f"Line Length: {max_line_length}",
            f"Total Lines Analyzed: {len(processed_lines)}",
            f"Total Characters: {len(text)}",
            "" if len(processed_lines) <= 9999 else "NOTE: Analysis limited to first 9999 lines",
            "",
            "LEGEND:",
            "Position Ruler: . = regular | + = every 5th | | = every 10th",
            "Numbers show column positions (1-based indexing)",
            "Special chars: · = Space | → = Tab | ¶ = Newline | ↴ = CR",
            "Actual periods remain as '.' - Hex value 2E",
            "Line numbers supported up to Line 9999:",
            "",
            "=== ANALYSIS OUTPUT ===",
            ""
        ] + output_sections
        
        download_content = '\n'.join(download_lines)
        st.download_button(
            "📥 Download Analysis Report",
            download_content,
            file_name=f"text_analysis_{encoding_mode.lower()}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    elif not text and analyze_button:
        st.warning("⚠️ Please enter some text to analyze.")
    
    else:
        # Show ruler preview when no analysis is running
        st.markdown('<div class="section-header">📏 Ruler Preview</div>', unsafe_allow_html=True)
        ruler_numbers, ruler_line = generate_ruler(max_line_length)
        st.code(f"{ruler_numbers}\n{ruler_line}", language=None)

    # Professional styling for monospace elements
    st.markdown("""
    <style>
    /* Remove all label and container related styles */
    .stTextArea {
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Direct textarea styling */
    .stTextArea textarea {
        font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', 'Courier New', monospace !important;
        font-size: 14px !important;
        line-height: 1.5 !important;
        border-radius: 8px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 12px !important;
        margin: 0 !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #1f77b4 !important;
        box-shadow: 0 0 0 3px rgba(31, 119, 180, 0.1) !important;
    }
    
    /* Code block styling */
    .stCodeBlock {
        font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', 'Courier New', monospace !important;
    }
    
    .stCodeBlock > div {
        background: #f8f9fa !important;
        border: 1px solid #e9ecef !important;
        border-radius: 8px !important;
        max-height: 600px !important;
        overflow: auto !important;
    }
    
    .stCodeBlock code {
        font-size: 13px !important;
        line-height: 1.4 !important;
        white-space: pre !important;
        overflow-x: auto !important;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px !important;
        border: none !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(90deg, #28a745, #20c997) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #f8f9fa !important;
    }
    
    /* Main container */
    .main .block-container {
        padding: 2rem 1rem !important;
        max-width: 100% !important;
    }
    
    /* Enhanced ruler and column highlighting */
    .stColumns > div:first-child {
        background: linear-gradient(135deg, #f0f8ff, #e8f4f8) !important;
        border-radius: 10px !important;
        padding: 15px !important;
        border: 2px solid #1976d2 !important;
        position: sticky !important;
        top: 20px !important;
        height: fit-content !important;
    }
    
    /* Content column styling */
    .stColumns > div:last-child {
        padding-left: 20px !important;
    }
    
    /* Code block styling with enhanced visibility */
    .stCodeBlock {
        font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', 'Courier New', monospace !important;
    }
    
    .stCodeBlock > div {
        background: #f8f9fa !important;
        border: 1px solid #e9ecef !important;
        border-radius: 8px !important;
        max-height: 500px !important;
        overflow: auto !important;
    }
    
    .stCodeBlock code {
        font-size: 13px !important;
        line-height: 1.4 !important;
        white-space: pre !important;
        overflow-x: auto !important;
    }
    
    /* Ruler column code block special styling */
    .stColumns > div:first-child .stCodeBlock > div {
        background: linear-gradient(to bottom, #f0f8ff, #e8f4f8) !important;
        border: 2px solid #1976d2 !important;
        max-height: 150px !important;
    }
    
    .stColumns > div:first-child .stCodeBlock code {
        color: #1976d2 !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
