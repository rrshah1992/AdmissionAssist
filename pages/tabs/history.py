# pages/tabs/history.py
from nicegui import ui  # type: ignore

def get_dummy_history():
    return [
        {'job_id': 'JOB-2024-005', 'user': 'Admin User', 'status': 'Completed', 'timestamp': '12 Jan 2024, 02:30 PM', 'records': 45},
        {'job_id': 'JOB-2024-004', 'user': 'Admin User', 'status': 'Completed', 'timestamp': '12 Jan 2024, 10:15 AM', 'records': 12},
        {'job_id': 'JOB-2024-003', 'user': 'Sarah Smith', 'status': 'Failed', 'timestamp': '11 Jan 2024, 04:45 PM', 'records': 0},
        {'job_id': 'JOB-2024-002', 'user': 'Admin User', 'status': 'Completed', 'timestamp': '11 Jan 2024, 09:00 AM', 'records': 150},
        {'job_id': 'JOB-2024-001', 'user': 'John Doe', 'status': 'Completed', 'timestamp': '10 Jan 2024, 11:20 AM', 'records': 22},
    ]

def build_history_tab() -> None:
    """
    Builds the Job History tab with a single data table.
    """
    
    # Use the same tile style as other tabs for consistency
    with ui.card().classes('tile tile-fixed').style(
        'width: 100%; max-width: 1200px; padding: 24px; margin: 12px auto 0; display: flex; flex-direction: column;'
    ):
        # Header
        with ui.row().style('width: 100%; justify-content: space-between; align-items: center; margin-bottom: 16px;'):
            ui.label('Job Execution Logs').style('font-size: 18px; font-weight: 600; color: #333;')
            
            # Simple refresh button stub
            ui.button(icon='refresh', on_click=lambda: ui.notify('Refreshed logs')).props('flat round dense color=grey-7')

        # Table
        columns = [
            {'name': 'job_id', 'label': 'Job ID', 'field': 'job_id', 'align': 'left', 'sortable': True},
            {'name': 'user', 'label': 'Executed By', 'field': 'user', 'align': 'left', 'sortable': True},
            {'name': 'status', 'label': 'Status', 'field': 'status', 'align': 'left', 'sortable': True},
            {'name': 'records', 'label': 'Records Processed', 'field': 'records', 'align': 'right', 'sortable': True},
            {'name': 'timestamp', 'label': 'Timestamp', 'field': 'timestamp', 'align': 'right', 'sortable': True},
        ]
        
        rows = get_dummy_history()
        
        # We use slots to color the status column
        with ui.table(columns=columns, rows=rows, pagination=10).classes('w-full').props('flat bordered') as table:
            
            # Custom rendering for the 'status' column to add colors
            table.add_slot('body-cell-status', '''
                <q-td :props="props">
                    <q-chip 
                        dense 
                        flat 
                        :color="props.value === 'Completed' ? 'green-1' : (props.value === 'Failed' ? 'red-1' : 'grey-1')"
                        :text-color="props.value === 'Completed' ? 'green-8' : (props.value === 'Failed' ? 'red-8' : 'grey-8')"
                    >
                        {{ props.value }}
                    </q-chip>
                </q-td>
            ''')
            
            # Make table scrollable filling the remaining height
            table.style('flex: 1; min-height: 0; overflow-y: auto;')