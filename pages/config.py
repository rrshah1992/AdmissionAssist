# pages/config.py
from nicegui import ui  # type: ignore
from datetime import datetime

# Import tab builders
from pages.tabs.grade_mapping import build_grade_mapping_tab
from pages.tabs.subject_selection import build_subject_mapping_tab
from pages.tabs.normalisation import build_normalisation_tab
from pages.tabs.run_jobs import build_run_jobs_tab
from pages.tabs.validate_ai import build_validate_tab
from pages.tabs.history import build_history_tab  # <--- NEW IMPORT
from pages.tabs.audit_trail import build_audit_tab # <--- Add this  

BOARD_OPTIONS = ['CBSE', 'IB', 'State Board']
SUBJECT_OPTIONS = ['Mathematics', 'Physics', 'Chemistry', 'English']


@ui.page('/config')
def config_page() -> None:
    ui.colors(primary='#007878')

    # State for the Run Jobs status
    job_status = {'state': 'idle', 'label': 'Ready to execute', 'color': 'text-blue-600'}

    # ------------------------------------------------------------------ #
    # 0. HEADER BAR                                                      #
    # ------------------------------------------------------------------ #
    with ui.element('div').classes('app-header'):
        with ui.element('div').classes('app-header-inner'):
            # LEFT: logo
            with ui.row().style('align-items: center; gap: 12px;'):
                ui.image('/assets/plaksha-logo.png').style('height: 40px; width: auto;')

            # CENTER: title
            ui.label('Score Calculation Manager').style(
                'font-size: 20px; font-weight: 600; color: #333;'
            )

            # RIGHT: user chip + logout
            with ui.row().style('justify-content: flex-end; align-items: center; gap: 10px;'):
                with ui.row().style('align-items: center; gap: 8px;'):
                    ui.avatar().props('icon=person size=32px').classes('bg-grey-3 text-grey-8')
                    with ui.column().style('gap: 0; line-height: 1.2;'):
                        ui.label('Admin User').style('font-size: 13px; font-weight: 600;')

                ui.button(icon='logout', on_click=lambda: ui.run_javascript("window.location.href='./'")) \
                    .props('flat round dense text-color=grey-7')

    # ------------------------------------------------------------------ #
    # 1. MAIN LAYOUT                                                     #
    # ------------------------------------------------------------------ #
    with ui.row().style(
        'width: 100%; height: calc(100vh - 65px); '
        'flex-wrap: nowrap; gap: 0;'
    ):

        # ======================= LEFT SIDEBAR ======================= #
        with ui.column().style(
            'width: 250px; height: 100%; background: #fff; '
            'border-right: 1px solid #e0e0e0; padding: 24px 0;'
        ):
            
            # 1. Custom Header Builder (Icon + Bold Text + Spacing)
            def nav_group_header(text, icon_name):
                with ui.row().style('width: 100%; align-items: center; padding: 24px 0 8px 24px; gap: 10px;'):
                    ui.icon(icon_name).style('font-size: 20px; color: #333;')
                    ui.label(text).style('font-size: 15px; font-weight: 700; color: #1a1a1a;')

            # 2. Tabs Container
            # We use a specific class 'nested-tabs' to target styles if needed, 
            # but inline styles work best for immediate precision.
            with ui.tabs().props('vertical indicator-color="transparent"').classes('w-full') as tabs:
                
                # --- GROUP 1: APPLICATIONS ---
                nav_group_header('Applications', 'dashboard')
                
                # Note: 'pl-14' = padding-left ~56px to align text under the header label, not the icon
                tab_style = 'justify-content: flex-start; padding-left: 54px; min-height: 36px; font-weight: 500; font-size: 14px;'
                
                run_jobs_tab = ui.tab('Applications List').style(tab_style)
                validate_tab = ui.tab('Digitisation Review').style(tab_style)

                # --- GROUP 2: SETTINGS ---
                nav_group_header('Settings', 'settings')
                
                grade_tab = ui.tab('Grade Scales').style(tab_style)
                subject_tab = ui.tab('Subject Selection').style(tab_style)
                norm_tab = ui.tab('Board Normalisation').style(tab_style)

                # --- GROUP 3: SYSTEM LOGS ---
                nav_group_header('System Logs', 'dns')
                
                history_tab = ui.tab('Process Logs').style(tab_style)
                audit_tab = ui.tab('Audit Trail').style(tab_style)

            ui.space()
            
            # Version info at bottom
            with ui.column().style('padding: 24px;'):
                ui.separator().style('margin-bottom: 12px;')
                ui.label('v1.0.8').style('font-size: 11px; color: #aaa;')

        # ======================= RIGHT CONTENT ======================= #
        with ui.column().style(
            'flex: 1; height: 100%; padding: 0 32px; overflow: hidden; position: relative;'
        ):
            
            # --- 1.1 DYNAMIC HEADER ACTION AREA ---
            action_container = ui.row().style(
                'width: 100%; justify-content: flex-end; align-items: center; '
                'padding-top: 20px; padding-bottom: 10px; gap: 12px; min-height: 68px;'
            )

            # References to hold data from builder functions
            jobs_table_ref = None

            # --- 1.2 TAB PANELS ---
            with ui.tab_panels(tabs, value=run_jobs_tab, animated=False).style(
                'width: 100%; height: calc(100% - 80px); background: transparent;'
            ):
                
                # 1. Run Jobs
                with ui.tab_panel(run_jobs_tab).style('padding: 0;'):
                    with ui.column().style('height: 100%; width: 100%;'):
                        jobs_table_ref = build_run_jobs_tab()

                # 2. Validate AI
                with ui.tab_panel(validate_tab).style('padding: 0;'):
                    with ui.column().style('height: 100%; width: 100%;'):
                        build_validate_tab()

                # 3. Grade mapping
                with ui.tab_panel(grade_tab).style('padding: 0;'):
                    with ui.column().style('height: 100%; width: 100%;'):
                        build_grade_mapping_tab(BOARD_OPTIONS)

                # 4. Subject selection
                with ui.tab_panel(subject_tab).style('padding: 0;'):
                    with ui.column().style('height: 100%; width: 100%;'):
                        build_subject_mapping_tab(BOARD_OPTIONS, SUBJECT_OPTIONS)

                # 5. Normalisation
                with ui.tab_panel(norm_tab).style('padding: 0;'):
                    with ui.column().style('height: 100%; width: 100%;'):
                        build_normalisation_tab(BOARD_OPTIONS)

                # 6. Job History (Updated)
                with ui.tab_panel(history_tab).style('padding: 0;'):
                    with ui.column().style('height: 100%; width: 100%;'):
                        build_history_tab()

                # 7. Audit Trail (Active)
                with ui.tab_panel(audit_tab).style('padding: 0;'):
                    with ui.column().style('height: 100%; width: 100%;'):
                        build_audit_tab() # <--- CALL THE BUILDER

    # ------------------------------------------------------------------ #
    # 2. DYNAMIC HEADER LOGIC                                            #
    # ------------------------------------------------------------------ #
    
    def render_header_actions():
        """Clears and rebuilds the top-right button area based on active tab."""
        action_container.clear()
        
        current_tab = tabs.value

        # --- CASE A: RUN JOBS TAB ---
        if current_tab == run_jobs_tab:
            with action_container:
                # Vertical stack: Label on top, Button below
                with ui.column().style('align-items: flex-end; gap: 2px;'):
                    
                    # Status Label (Dynamic Color)
                    status_label = ui.label(job_status['label']).classes(f"text-xs font-bold {job_status['color']}")

                    def execute_jobs():
                        if not jobs_table_ref: 
                            return
                        selected = jobs_table_ref.selected
                        if not selected:
                            ui.notify('No students selected!', type='warning')
                            return
                        
                        # Simulate running state
                        job_status['state'] = 'running'
                        job_status['label'] = 'Processing jobs...'
                        job_status['color'] = 'text-amber-500' # Yellow
                        render_header_actions()
                        
                        # Simulate finish
                        def finish():
                            job_status['state'] = 'executed'
                            job_status['label'] = 'Execution Successful'
                            job_status['color'] = 'text-green-600' # Green
                            render_header_actions()
                            ui.notify(f'Processed {len(selected)} jobs', type='positive')
                        
                        ui.timer(2.0, finish, once=True)

                    ui.button('Execute Extraction', icon='play_arrow', on_click=execute_jobs) \
                        .classes('btn-primary rounded-12') \
                        .style('padding: 0 20px; background-color: #007878;')

        # --- CASE B: CONFIGURATION TABS ---
        elif current_tab in [grade_tab, subject_tab, norm_tab]:
            with action_container:
                last_saved_label = ui.label('Not saved yet').style('font-size: 12px; color: #666;')
                
                def save_configuration() -> None:
                    now = datetime.now().strftime('%d %b, %I:%M %p')
                    last_saved_label.text = f'Saved · {now}'
                    ui.notify('Configuration successfully saved', type='positive')

                ui.button('Save Changes', icon='save', on_click=save_configuration) \
                    .classes('btn-primary rounded-12') \
                    .style('padding: 0 20px;')
        
        # --- CASE C: VALIDATE & HISTORY ---
        else:
            # History is read-only, Validate has its own controls.
            pass

    # Listener
    tabs.on_value_change(lambda e: render_header_actions())
    
    # Initial render
    render_header_actions()