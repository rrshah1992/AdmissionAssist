# pages/tabs/subject_mapping.py
from typing import List, Dict, Any
from nicegui import ui  # type: ignore


def build_subject_mapping_tab(board_options: List[str], subject_options: List[str]) -> None:
    """
    Tab 2: Subject selection rule editor.

    Layout follows the provided wireframe:
    - Header: board + class/level + Save / Preview
    - TOTAL SUBJECTS & AGGREGATION section
    - PRE-FILTERS section
    - PHASES section
    """

    # ---- simple in-memory state ---------------------------------------------
# ---- PATCH 1: DATA STATE (Preserves logic, enables "English" mapping) ----
    classes = ['9', '10', '11', '12']

    # 1. Configuration State (Stores the final output)
    config_state = {
        'total_subjects': 5,
        'agg_method': 'Average %',  # Default
        'board': board_options[0] if board_options else 'CBSE',
        'class': '10'
    }

    # 2. Pre-Filters (Simplified for Natural Language)
    # Old format: {'field': 'has_theory', 'op': '=', 'value': 'True'}
    # New format: {'action': 'Include only', 'condition': 'Theory is present'}
    filters: List[Dict[str, str]] = []

    # 3. Phases (Preserves your "Group", "Fill", "Sub-group" logic)
    phases: List[Dict[str, Any]] = [
        {
            'type': 'group_pick', # Mandatory Rule
            'min': 1, 'max': 1, 
            'subjects': ['Mathematics']
        },
        {
            'type': 'sub_group',  # Sub-Group Rule
            'name': 'Science', 
            'subjects': ['Physics', 'Chemistry'], 
            'method': 'Average'
        },
        {
            'type': 'fill_top',   # Remaining Rule
            'limit': 3, 
            'sort': 'Percentage'
        }
    ]

    # ---- main tile ----------------------------------------------------------
    with ui.card().classes('tile tile-fixed').style(
        'width: 100%; max-width: 1160px; '
        'padding: 16px; '
        'height: calc(100vh - 290px); '
        'margin: 12px auto 0;'
    ):
        with ui.column().style(
            'width: 100%; height: 100%; display: flex; '
            'flex-direction: column; gap: 12px;'
        ):
            # title
            ui.label('Subject selection rule editor').style(
                'font-size: 16px; font-weight: 600;'
            )

            # -----------------------------------------------------------------
            # HEADER: Board / Class / Save / Preview
            # -----------------------------------------------------------------
            with ui.row().style(
                'width: 100%; align-items: center; gap: 12px;'
            ):
                default_board = board_options[0] if board_options else None
                default_class = '10'

                ui.label('Board:').style('font-weight: 500;')
                board_select = ui.select(
                    board_options,
                    value=default_board,
                    with_input=False,
                ).style('min-width: 160px;')

                ui.label('Class / Level:').style('font-weight: 500;')
                class_select = ui.select(
                    classes,
                    value=default_class,
                    with_input=False,
                ).style('min-width: 120px;')

                with ui.row().style('margin-left: auto; gap: 8px;'):
                    def save_rule() -> None:
                        ui.notify(
                            f'Saved rule for {board_select.value} '
                            f'Class {class_select.value}'
                        )


            # -----------------------------------------------------------------
            # SCROLLABLE BODY: all sections live here
            # -----------------------------------------------------------------
            body = ui.column().style(
                'flex: 1; min-height: 0; overflow-y: auto; '
                'width: 100%; gap: 12px; padding-right: 4px;'
            )

            # ---- PATCH 2: NATURAL LANGUAGE RENDERER ----
            with body:
                
                # STYLES: Define the "Fill-in-the-blank" look
                input_style = 'border-bottom: 2px solid #e0e0e0; background: #f9f9f9; padding: 0 4px; border-radius: 4px 4px 0 0;'
                sentence_style = 'font-size: 15px; font-weight: 500; color: #333; align-items: center; gap: 8px;'

                # -------------------------------------------------------------
                # SECTION 1: TOTAL & AGGREGATION
                # -------------------------------------------------------------
                with ui.card().style('width: 100%; padding: 20px; box-shadow: none; border: 1px solid #e0e0e0; background: #fafafa;'):
                    with ui.row().style(sentence_style):
                        ui.label('Calculate Final Score using')
                        ui.select(['Average %', 'Sum of Marks'], value=config_state['agg_method']) \
                            .props('dense borderless options-dense').style(input_style + 'min-width: 140px;')
                        
                        ui.label('of the best')
                        ui.number(value=config_state['total_subjects'], min=1, max=10) \
                            .props('dense borderless').style(input_style + 'max-width: 60px; text-align: center;')
                        
                        ui.label('subjects.')

                # -------------------------------------------------------------
                # SECTION 2: PRE-FILTERS (Sentence Builder)
                # -------------------------------------------------------------
                ui.label('1. Pre-Filters (Eligible Subjects)').style('font-size: 13px; font-weight: 700; color: #555; text-transform: uppercase; margin-top: 12px;')
                
                # Container for filter rows
                filter_list = ui.column().style('width: 100%; gap: 8px;')

                def render_filters():
                    filter_list.clear()
                    with filter_list:
                        # A. Existing Filters
                        for i, f in enumerate(filters):
                            with ui.row().style('width: 100%; align-items: center; gap: 10px; background: #fff; border: 1px solid #eee; padding: 8px 16px; border-radius: 8px;'):
                                ui.icon('filter_alt', size='18px').classes('text-grey-5')
                                # Read-only sentence view
                                ui.label(f"{f['action']} subjects where {f['condition']}").style('flex: 1; font-size: 14px; color: #333;')
                                ui.button(icon='close', on_click=lambda idx=i: remove_filter(idx)).props('flat dense round size=sm color=grey')

                        # B. "Add New" Builder Row
                        with ui.row().style('width: 100%; align-items: center; gap: 8px; padding-top: 4px;'):
                            ui.label('Rule:').style('font-size: 13px; font-weight: 600; color: #777;')
                            
                            # Sentence Parts
                            act = ui.select(['Include only', 'Exclude'], value='Include only').props('dense borderless options-dense').style(input_style + 'width: 120px;')
                            ui.label('subjects where')
                            cond = ui.select(['Theory is Present', 'Language is Blocked', 'Is a Language'], value='Theory is Present').props('dense borderless options-dense').style(input_style + 'width: 180px;')
                            
                            # Add Button
                            ui.button('Add', icon='add', on_click=lambda: add_filter(act.value, cond.value)) \
                                .classes('rounded-12').props('unelevated color=grey-2 text-color=grey-9 dense').style('margin-left: auto;')

                def add_filter(a, c):
                    filters.append({'action': a, 'condition': c})
                    render_filters()

                def remove_filter(idx):
                    filters.pop(idx)
                    render_filters()

                render_filters()

                # -------------------------------------------------------------
                # SECTION 3: PHASES (Logic Processor)
                # -------------------------------------------------------------
                ui.label('2. Selection Logic (Processed in Order)').style('font-size: 13px; font-weight: 700; color: #555; text-transform: uppercase; margin-top: 12px;')
                
                phases_container = ui.column().style('width: 100%; gap: 12px;')

                def render_phases():
                    phases_container.clear()
                    with phases_container:
                        for i, phase in enumerate(phases):
                            with ui.row().style('width: 100%; align-items: center; gap: 12px; background: #fff; border: 1px solid #e0e0e0; padding: 12px 16px; border-radius: 12px; transition: all 0.2s;'):
                                
                                # Index Bubble
                                ui.label(str(i + 1)).style('background: #eee; color: #555; width: 24px; height: 24px; border-radius: 50%; text-align: center; line-height: 24px; font-size: 12px; font-weight: 700;')

                                # --- LOGIC BRANCHING FOR "ENGLISH" SENTENCES ---
                                
                                # 1. MANDATORY RULE
                                if phase['type'] == 'group_pick':
                                    with ui.row().style(sentence_style + 'flex: 1; flex-wrap: wrap;'):
                                        ui.label('Must select')
                                        ui.number(value=phase['min'], min=0, max=10, on_change=lambda e, p=phase: p.update({'min': int(e.value or 0)})).props('dense borderless').style(input_style + 'max-width: 50px; text-align: center;')
                                        ui.label('to')
                                        ui.number(value=phase['max'], min=0, max=10, on_change=lambda e, p=phase: p.update({'max': int(e.value or 0)})).props('dense borderless').style(input_style + 'max-width: 50px; text-align: center;')
                                        ui.label('subjects from')
                                        
                                        # Simple text input for subjects (e.g., "Maths, Physics")
                                        def update_subs(e, p=phase): p['subjects'] = [x.strip() for x in (e.value or '').split(',')]
                                        ui.input(value=', '.join(phase['subjects']), on_change=lambda e: update_subs(e)).props('dense borderless placeholder="e.g. Maths"').style(input_style + 'min-width: 180px; color: #00786f; font-weight: 600;')

                                # 2. SUB-GROUP RULE
                                elif phase['type'] == 'sub_group':
                                    with ui.row().style(sentence_style + 'flex: 1; flex-wrap: wrap;'):
                                        ui.label('Create Group called')
                                        ui.input(value=phase.get('name', ''), on_change=lambda e, p=phase: p.update({'name': e.value})).props('dense borderless placeholder="Name"').style(input_style + 'width: 120px; color: #00786f; font-weight: 600;')
                                        ui.label('from')
                                        
                                        def update_grp(e, p=phase): p['subjects'] = [x.strip() for x in (e.value or '').split(',')]
                                        ui.input(value=', '.join(phase.get('subjects', [])), on_change=lambda e: update_grp(e)).props('dense borderless placeholder="Sub1, Sub2"').style(input_style + 'min-width: 160px;')
                                        
                                        ui.label('using')
                                        ui.select(['Average', 'Sum', 'Best of'], value=phase.get('method', 'Average'), on_change=lambda e, p=phase: p.update({'method': e.value})).props('dense borderless options-dense').style(input_style + 'width: 100px;')

                                # 3. REMAINING RULE
                                # 3. REMAINING RULE (Updated: No number input)
                                elif phase['type'] == 'fill_top':
                                    with ui.row().style(sentence_style + 'flex: 1; flex-wrap: wrap;'):
                                        ui.label('Select remaining subjects sorted by')
                                        
                                        ui.select(
                                            ['Percentage', 'Marks', 'Name'], 
                                            value=phase.get('sort', 'Percentage'), 
                                            on_change=lambda e, p=phase: p.update({'sort': e.value})
                                        ).props('dense borderless options-dense').style(input_style + 'min-width: 120px;')

                                # Delete Button
                                ui.button(icon='delete', on_click=lambda idx=i: delete_phase(idx)).props('flat dense round color=red-4 size=sm')

                def delete_phase(idx):
                    phases.pop(idx)
                    render_phases()

                def add_phase(type_key):
                    # Default templates for new rules
                    if type_key == 'group_pick': new = {'type': 'group_pick', 'min': 1, 'max': 1, 'subjects': []}
                    elif type_key == 'sub_group': new = {'type': 'sub_group', 'name': 'New Group', 'subjects': [], 'method': 'Average'}
                    elif type_key == 'fill_top': new = {'type': 'fill_top', 'limit': 3, 'sort': 'Percentage'}
                    phases.append(new)
                    render_phases()

                render_phases()

                # --- BUTTONS ROW (At the bottom) ---
                with ui.row().style('gap: 12px; margin-top: 12px; padding-bottom: 24px;'):
                    ui.button('Must Select...', on_click=lambda: add_phase('group_pick')).classes('rounded-12').props('outline color=grey-7 size=sm')
                    ui.button('Create Group...', on_click=lambda: add_phase('sub_group')).classes('rounded-12').props('outline color=grey-7 size=sm')
                    ui.button('Select Remaining...', on_click=lambda: add_phase('fill_top')).classes('rounded-12').props('outline color=grey-7 size=sm')



