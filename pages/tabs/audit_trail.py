from nicegui import ui  # type: ignore

# --- DUMMY AUDIT DATA ---
# In a real app, this would fetch from a database based on the selected student ID
AUDIT_LOGS = {
    'REG005': """
## Audit Report: Esha Gupta (REG005)
**Date:** 29 Jan 2026, 14:30

### 1. Extraction Phase
* **Source File:** `Marksheet_Scan_001.jpg`
* **OCR Engine:** Tesseract v5.0 + Custom Model
* **Confidence Score:** **98.5%** (High)
* **Anomalies:** None detected.

### 2. Calculation Rules Applied
* **Board Detected:** CBSE (Class 12)
* **Rule [CBSE-A1]:** Grade 'A1' mapped to **95.0** (Standard Scale)
* **Rule [CBSE-B2]:** Grade 'B2' mapped to **75.0**
* **Subject Selection Strategy:** "Best 5" (English + Top 4 Technical)
    * *Excluded:* Physical Education (Score: 88) - Reason: Non-technical elective.

### 3. Final Score Calculation
> **Aggregate Score:** 94.2%
* **Normalization Factor:** 1.0 (No adjustments applied)
* **Status:** <span style="color:green; font-weight:bold">QUALIFIED</span>
""",
    'REG001': """
## Audit Report: Alice Kumar (REG001)
**Date:** 28 Jan 2026, 09:15

### 1. Extraction Phase
* **Source File:** `Alice_Transcript.pdf`
* **Confidence Score:** **82.0%** (Review Required)

### 2. Calculation Rules Applied
* **Board Detected:** IB Diploma
* **Subject Selection Strategy:** "Best 5"
    * *Note:* IB scale converted using 2024 mapping table.

### 3. Final Score Calculation
> **Aggregate Score:** 88.5%
""",
}

def build_audit_tab():
    # State
    selected_student = {'value': 'REG005'} # Default to Esha

    # Layout
    with ui.column().style('width: 100%; height: 100%; gap: 0;'):
        
        # --- TOP BAR ---
        with ui.row().style('width: 100%; justify-content: space-between; align-items: center; padding-bottom: 20px;'):
            ui.label('Audit Trail').style('font-size: 20px; font-weight: 600; color: #1a1a1a;')
            
            # Export Button
            ui.button('Export Full Audit Log', icon='download', on_click=lambda: ui.notify('Downloading Audit_Log_Full.csv...')) \
                .classes('btn-secondary rounded-12') \
                .style('border: 1px solid #e0e0e0;')

        # --- SEARCH & FILTER ---
        with ui.row().style('width: 100%; margin-bottom: 20px; align-items: center; gap: 12px;'):
            # Searchable Dropdown
            options = {
                'REG005': 'Esha Gupta (REG005)',
                'REG001': 'Alice Kumar (REG001)',
                'REG002': 'Bob Sharma (REG002)',
            }
            
            select = ui.select(
                options=options, 
                value='REG005',
                with_input=True, # Makes it searchable
                label='Search Student (Name or ID)'
            ).style('width: 400px;').props('outlined dense options-dense behavior="menu"')
            
        
        # --- REPORT VIEWER (The "Document") ---
        # We use a card to frame it like a paper report
        with ui.card().classes('tile').style(
            'flex: 1; width: 100%; padding: 40px; overflow-y: auto; '
            'border: 1px solid #e0e0e0; box-shadow: none;'
        ):
            # Container for the Markdown content
            log_container = ui.element('div').style('max-width: 800px; margin: 0 auto; width: 100%;')
            
            def render_log():
                log_container.clear()
                student_id = select.value
                content = AUDIT_LOGS.get(student_id, f"## No logs found for {student_id}")
                
                with log_container:
                    # Render the Markdown with GitHub-like styling
                    ui.markdown(content).style(
                        'font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; '
                        'line-height: 1.6; color: #333;'
                    )

            # Bind the render to the selection change
            select.on_value_change(render_log)
            
            # Initial Render
            render_log()