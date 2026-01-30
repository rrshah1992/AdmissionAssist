# pages/tabs/run_jobs.py
from nicegui import ui  # type: ignore

# --- 1. DATA ALIGNMENT ---
# Updated states to match your specific requirements
def get_dummy_students():
    return [
        {'id': 'REG001', 'email': 'alice@univ.edu', 'timestamp': '14 Jan 2026, 12:46 pm', 'program': 'UG', 'status': 'New'},
        {'id': 'REG002', 'email': 'bob@univ.edu', 'timestamp': '14 Jan 2026, 12:48 pm', 'program': 'UG', 'status': 'Digitized'},
        {'id': 'REG003', 'email': 'chitra@univ.edu', 'timestamp': '14 Jan 2026, 01:15 pm', 'program': 'PhD', 'status': 'Scored'},
        {'id': 'REG004', 'email': 'dev@univ.edu', 'timestamp': '14 Jan 2026, 02:00 pm', 'program': 'UG', 'status': 'Failed'},
        {'id': 'REG005', 'email': 'esha@univ.edu', 'timestamp': '14 Jan 2026, 02:30 pm', 'program': 'UG', 'status': 'New'},
        {'id': 'REG006', 'email': 'farhan@univ.edu', 'timestamp': '14 Jan 2026, 03:00 pm', 'program': 'UG', 'status': 'Digitized'},
    ]

def build_run_jobs_tab() -> ui.table:
    # State for current filter
    current_filter = {'status': 'All'} 
    
    # Process Data for Metrics
    all_rows = get_dummy_students()
    counts = {
        'New': len([r for r in all_rows if r['status'] == 'New']),
        'Digitized': len([r for r in all_rows if r['status'] == 'Digitized']),
        'Scored': len([r for r in all_rows if r['status'] == 'Scored']),
        'Failed': len([r for r in all_rows if r['status'] == 'Failed']),
    }

    # Styles for the metric cards
    card_style = (
        'flex: 1; padding: 16px; border-radius: 12px; cursor: pointer; '
        'transition: all 0.2s; border: 1px solid #e0e0e0; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'
    )
    
    # Active state style (visual feedback when selected)
    active_style = 'border: 2px solid #00786f; background-color: #f0fdfc;'

    with ui.column().style('width: 100%; height: 100%; gap: 20px;'):
        
        # --- 1. METRIC CARDS (FILTER ROWS) ---
        with ui.row().style('width: 100%; gap: 16px; margin-bottom: 8px;'):
            
            # We create a dictionary to hold references to the cards so we can update their styles
            cards = {}

            def filter_by_status(status):
                # Toggle logic: if clicking the same status, reset to All
                if current_filter['status'] == status:
                    current_filter['status'] = 'All'
                else:
                    current_filter['status'] = status
                
                # Update Table
                if current_filter['status'] == 'All':
                    table.rows = all_rows
                else:
                    table.rows = [r for r in all_rows if r['status'] == current_filter['status']]
                table.update()

                # Update Card Styles (Highlight active)
                for s, card_col in cards.items():
                    # Reset all
                    card_col.style(replace=card_style)
                    if s == current_filter['status']:
                         card_col.style(add=active_style)

            # Helper to build a card
            def build_card(label, count, color, status_key):
                with ui.column().classes('bg-white').style(card_style) as card:
                    cards[status_key] = card # Register for styling
                    ui.label(label).style('font-size: 13px; color: #666; font-weight: 500;')
                    with ui.row().style('align-items: center; justify-content: space-between; width: 100%;'):
                        ui.label(str(count)).style('font-size: 24px; font-weight: 700; color: #333;')
                        # Status Indicator Dot
                        ui.element('div').style(f'width: 8px; height: 8px; border-radius: 50%; background-color: {color};')
                
                # Make interactive
                card.on('click', lambda: filter_by_status(status_key))

            # Render the 4 cards
            build_card('New Applications (Apps submitted but not processed)', counts['New'], '#3b82f6', 'New')       # Blue
            build_card('Digitized (Data read and waiting for review)', counts['Digitized'], '#f59e0b', 'Digitized')  # Orange
            build_card('Scored (Apps processes entirely)', counts['Scored'], '#10b981', 'Scored')           # Green
            build_card('Failed', counts['Failed'], '#ef4444', 'Failed')           # Red


        # --- 2. TABLE SECTION ---
        with ui.card().classes('tile tile-fixed').style('width: 100%; flex: 1; padding: 0; overflow: hidden; display: flex; flex-direction: column;'):
            
            # Toolbar inside the card
            with ui.row().style('padding: 16px; border-bottom: 1px solid #eee; width: 100%; justify-content: space-between; align-items: center;'):
                ui.label('Applications List').style('font-size: 16px; font-weight: 600;')
                
                # Search Bar
                search_input = ui.input(placeholder='Search by ID or Email') \
                    .props('dense outlined append-icon=search rounded') \
                    .style('width: 300px;')

            columns = [
                {'name': 'id', 'label': 'Student ID', 'field': 'id', 'align': 'left', 'sortable': True},
                {'name': 'email', 'label': 'Student Email', 'field': 'email', 'align': 'left', 'sortable': True},
                {'name': 'timestamp', 'label': 'Submitted At', 'field': 'timestamp', 'align': 'left', 'sortable': True},
                {'name': 'program', 'label': 'Program', 'field': 'program', 'align': 'left', 'sortable': True},
                {'name': 'status', 'label': 'Extraction Status', 'field': 'status', 'align': 'left', 'sortable': True},
            ]

            table = ui.table(
                columns=columns, 
                rows=all_rows, 
                selection='multiple',
                pagination=10
            ).classes('w-full').props('flat')
            
            # Customize the header to look like the screenshot (lighter gray)
            table.add_slot('header', r'''
                <q-tr :props="props" style="background-color: #f8f9fa; color: #444;">
                    <q-th auto-width />
                    <q-th v-for="col in props.cols" :key="col.name" :props="props">
                        {{ col.label }}
                    </q-th>
                </q-tr>
            ''')
            
            # Status badge formatting via slot
            table.add_slot('body-cell-status', r'''
                <q-td :props="props">
                    <q-badge :color="props.value === 'Scored' ? 'green' : (props.value === 'Failed' ? 'red' : (props.value === 'Digitized' ? 'orange' : 'blue'))" 
                             text-color="white" 
                             :label="props.value" />
                </q-td>
            ''')

            table.style('flex: 1; border: none;')

            # Search Logic linked to current filtered set
            def on_search():
                term = search_input.value.lower()
                # Base set depends on selected metric card
                base_set = all_rows if current_filter['status'] == 'All' else [r for r in all_rows if r['status'] == current_filter['status']]
                
                filtered = [
                    row for row in base_set
                    if term in row['id'].lower() or term in row['email'].lower()
                ]
                table.rows = filtered
                table.update()

            search_input.on('input', on_search)

    return table