from typing import List, Dict, Any
from nicegui import ui  # type: ignore
import json

# --- 1. DUMMY DATA (Enhanced for Multi-Sheet) ---
def get_dummy_validation_queue():
    return [
        {
            'id': 'STU-001', 'name': 'Esha Gupta', 'status': 'Pending',
            'sheets': [
                {
                    'class': 'Class 10',
                    'image': 'https://placehold.co/600x800/png?text=Class+10+Marklist',
                    'marks': [
                        {'subject': 'Mathematics', 'score': 95},
                        {'subject': 'Science', 'score': 88},
                        {'subject': 'Social Studies', 'score': 92},
                        {'subject': 'English', 'score': 85},
                    ]
                },
                {
                    'class': 'Class 12',
                    'image': 'https://placehold.co/600x800/png?text=Class+12+Marklist',
                    'marks': [
                        {'subject': 'Physics', 'score': 78},
                        {'subject': 'Chemistry', 'score': 82},
                        {'subject': 'Mathematics', 'score': 75},
                        {'subject': 'English', 'score': 80},
                    ]
                }
            ]
        },
        {
            'id': 'STU-002', 'name': 'Farhan Ali', 'status': 'Pending',
            'sheets': [
                {
                    'class': 'Class 12',
                    'image': 'https://placehold.co/600x800/png?text=Farhan+Class+12',
                    'marks': [
                        {'subject': 'Accountancy', 'score': 65},
                        {'subject': 'Business Studies', 'score': 70},
                        {'subject': 'Economics', 'score': 72},
                    ]
                }
            ]
        },
    ]

# Global state to track progress across the session
session_state = {
    'queue': [],
    'current_student_idx': 0,
    'current_sheet_idx': 0
}

def build_validate_tab() -> None:
    # Initialize Data
    session_state['queue'] = get_dummy_validation_queue()
    
    # --- UI REFERENCES ---
    dialog = ui.dialog().props('maximized transition-show=slide-up transition-hide=slide-down')
    content_area = None # Will hold the focus mode content
    
    # --- LOGIC HANDLERS ---
    
    def start_review():
        session_state['current_student_idx'] = 0
        session_state['current_sheet_idx'] = 0
        render_focus_mode()
        dialog.open()

    def exit_review():
        dialog.close()

    def next_step():
        """
        Logic: Save current sheet -> Next Sheet -> If no sheets left -> Next Student
        """
        s_idx = session_state['current_student_idx']
        sh_idx = session_state['current_sheet_idx']
        student = session_state['queue'][s_idx]
        
        # 1. Check if there are more sheets for this student
        if sh_idx < len(student['sheets']) - 1:
            session_state['current_sheet_idx'] += 1
            ui.notify(f"Saved {student['sheets'][sh_idx]['class']}. Loading next sheet...", color='positive')
            render_focus_mode()
        
        # 2. Check if there are more students
        elif s_idx < len(session_state['queue']) - 1:
            session_state['current_student_idx'] += 1
            session_state['current_sheet_idx'] = 0 # Reset sheet index for new student
            ui.notify(f"Completed {student['name']}. Loading next student...", color='positive')
            render_focus_mode()
        
        # 3. Done
        else:
            ui.notify("All validations completed!", type='positive')
            dialog.close()

    def prev_step():
        s_idx = session_state['current_student_idx']
        sh_idx = session_state['current_sheet_idx']

        if sh_idx > 0:
            session_state['current_sheet_idx'] -= 1
            render_focus_mode()
        elif s_idx > 0:
            session_state['current_student_idx'] -= 1
            # Go to last sheet of previous student
            prev_student = session_state['queue'][s_idx - 1]
            session_state['current_sheet_idx'] = len(prev_student['sheets']) - 1
            render_focus_mode()
        else:
            ui.notify('This is the first record.', type='warning')


    # --- RENDERER FOR FOCUS MODE ---
    def render_focus_mode():
        content_area.clear()
        
        # Get Current Context
        s_idx = session_state['current_student_idx']
        sh_idx = session_state['current_sheet_idx']
        student = session_state['queue'][s_idx]
        current_sheet = student['sheets'][sh_idx]
        
        # Calculate Progress
        students_left = len(session_state['queue']) - s_idx
        sheet_label = f"Sheet {sh_idx + 1} of {len(student['sheets'])}"

        with content_area:
            
            # 1. KEYBOARD SHORTCUTS
            # We bind to the specific container to ensure scope
            ui.keyboard(on_key=lambda e: next_step() if e.key == 'Enter' and not e.repeat else None)

            # 2. TOP NAV BAR (Control Center)
            with ui.row().style(
                'width: 100%; height: 64px; background: #fff; border-bottom: 1px solid #e0e0e0; '
                'align-items: center; padding: 0 24px; justify-content: space-between; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'
            ):
                # LEFT: Exit & Counter
                with ui.row().style('align-items: center; gap: 16px;'):
                    ui.button(icon='close', on_click=exit_review).props('flat round dense').tooltip('Exit Review')
                    with ui.column().style('gap: 0;'):
                        ui.label(f'{students_left} Students Remaining').style('font-size: 14px; font-weight: 600; color: #333;')
                        ui.label('Queue Status: Active').style('font-size: 11px; color: green;')

                # CENTER: Context
                with ui.column().style('align-items: center; gap: 0;'):
                    ui.label(student['name']).style('font-size: 18px; font-weight: 700; color: #1a1a1a;')
                    ui.label(f"{sheet_label} • {current_sheet['class']}").style('font-size: 12px; color: #666; font-weight: 500;')

                # RIGHT: Actions
                with ui.row().style('align-items: center; gap: 12px;'):
                    ui.button('Previous', on_click=prev_step).props('flat text-color=grey-8')
                    
                    # The Big Green Button
                    btn = ui.button('Approve & Next (Enter)', icon='check', on_click=next_step) \
                        .classes('shadow-1') \
                        .style('background-color: #00786f; color: white; font-weight: 600; padding: 0 20px; border-radius: 8px;')


            # 3. MAIN WORKSPACE (Split Layout)
            with ui.row().style('width: 100%; height: calc(100vh - 64px); gap: 0; flex-wrap: nowrap;'):
                
                # --- LEFT: IMAGE VIEWER (60%) ---
                with ui.column().style(
                    'width: 60%; height: 100%; background: #222; position: relative; '
                    'justify-content: center; align-items: center; overflow: hidden;'
                ):
                    # Simulated Zoom Controls
                    with ui.column().style('position: absolute; left: 16px; top: 50%; transform: translateY(-50%); gap: 8px; z-index: 10;'):
                        ui.button(icon='add').props('round dense color=grey-8 text-color=white').tooltip('Zoom In')
                        ui.button(icon='remove').props('round dense color=grey-8 text-color=white').tooltip('Zoom Out')

                    # The Image
                    ui.image(current_sheet['image']).style('max-width: 90%; max-height: 90%; object-fit: contain; box-shadow: 0 0 20px rgba(0,0,0,0.5);')

                # --- RIGHT: DATA ENTRY (40%) ---
                with ui.column().style('width: 40%; height: 100%; background: #fff; display: flex; flex-direction: column;'):
                    
                    # Class Tabs (Visual Context)
                    with ui.tabs().props('align="left" dense active-color="primary" indicator-color="primary"').style('width: 100%; border-bottom: 1px solid #eee; background: #fafafa;') as tabs:
                        # Create a tab for every sheet the student has
                        for sheet in student['sheets']:
                            t = ui.tab(sheet['class'])
                            if sheet['class'] == current_sheet['class']:
                                tabs.set_value(t) # Select current

                    # Scrollable Form Area
                    with ui.scroll_area().style('flex: 1; padding: 24px;'):
                        
                        ui.label('Verify Marks').classes('text-lg font-bold mb-4 text-gray-700')

                        # The Table
                        # We use a grid layout for better control than a standard table
                        with ui.element('div').style('display: grid; grid-template-columns: 2fr 1fr; gap: 16px; align-items: center;'):
                            
                            # Header
                            ui.label('Subject').classes('text-xs font-bold text-gray-400 uppercase')
                            ui.label('Score').classes('text-xs font-bold text-gray-400 uppercase')

                            # Rows
                            for mark in current_sheet['marks']:
                                # Subject Name (Read Only)
                                ui.label(mark['subject']).style('font-size: 15px; font-weight: 500; color: #333; padding-left: 8px;')
                                
                                # Input Field (Big & Bold)
                                ui.input(value=str(mark['score'])) \
                                    .props('outlined dense input-class="text-lg font-bold text-center"') \
                                    .style('width: 100%;')


    # --- BUILD THE DIALOG CONTAINER ---
    with dialog:
        # We use a raw div to ensure it fills the dialog window perfectly
        content_area = ui.element('div').style('width: 100%; height: 100%; background: white; display: flex; flex-direction: column;')


    # --- BUILD THE LANDING PAGE (QUEUE) ---
    with ui.column().style('width: 100%; height: 100%; gap: 20px;'):
        
        # 1. Header
        with ui.row().style('justify-content: space-between; align-items: center; width: 100%;'):
            with ui.column().style('gap: 4px;'):
                ui.label('Review Queue').style('font-size: 20px; font-weight: 600;')
                ui.label('24 Students pending manual review').style('color: #666; font-size: 13px;')
            
            ui.button('Start Review Session', icon='play_arrow', on_click=start_review) \
                .classes('btn-primary rounded-12') \
                .style('padding: 0 24px; height: 48px; font-size: 15px;')

        # 2. Queue List
        with ui.card().classes('tile').style('width: 100%; padding: 0;'):
            
            # Simple Header
            with ui.row().style('background: #f9fafb; padding: 12px 24px; border-bottom: 1px solid #eee;'):
                ui.label('Student Name').style('flex: 1; font-weight: 600; color: #555;')
                ui.label('Status').style('width: 150px; font-weight: 600; color: #555;')
                ui.label('Sheets Detected').style('width: 150px; font-weight: 600; color: #555;')

            # Rows
            for student in session_state['queue']:
                with ui.row().style('padding: 16px 24px; border-bottom: 1px solid #f0f0f0; align-items: center;'):
                    # Name
                    with ui.row().style('flex: 1; align-items: center; gap: 12px;'):
                        ui.avatar(student['name'][0]).classes('bg-grey-3 text-grey-8')
                        with ui.column().style('gap: 0;'):
                            ui.label(student['name']).style('font-weight: 500;')
                            ui.label(student['id']).style('font-size: 11px; color: #888;')
                    
                    # Status
                    ui.badge(student['status'], color='orange').props('outline')

                    # Sheets
                    ui.label(f"{len(student['sheets'])} Sheets").style('width: 150px; color: #444;')