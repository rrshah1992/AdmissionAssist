from nicegui import ui, app   # type: ignore
import pages.config   # registers /config route

app.add_static_files('/assets', 'assets')

def go_to_config():
    ui.run_javascript("window.location.href='./config'")

def handle_sso_login():
    ui.notify('Redirecting to organization login…')

ui.add_css("""
body {
    margin: 0;
    overflow-x: hidden;
    overflow-y: auto;
    background: #f6f7f9;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.rounded-12 { border-radius: 12px; overflow: hidden; }

/* --- BUTTONS & TABS: Remove Auto-Caps --- */
.q-btn, .q-tab, .q-tab__label {
    text-transform: none !important;
    letter-spacing: normal !important;
}

/* Buttons */
.btn-primary {
    background-color: #00786f !important;
    color: #ffffff;
    font-weight: 600;
}
.btn-primary:hover { background-color: #00453f; }

.btn-secondary {
    background-color: #ffffff;
    color: #00786f;
    font-weight: 600;
}
.btn-secondary:hover { background-color: #e6f4f3; }
           
/* Header & Tiles (Shared) */
.app-header {
  position: sticky; top: 0; z-index: 1000; width: 100%;
  background: #ffffff;
  border-bottom: 1px solid rgba(0,0,0,.06);
  box-shadow: 0 4px 12px -6px rgba(0,0,0,.1);
}
.app-header-inner {
  width: 100%; padding: 10px 24px;
  display: grid; grid-template-columns: auto 1fr auto;
  align-items: center;
}
.tile {
  background: #fff;
  border: 1px solid rgba(0,0,0,.06);
  border-radius: 14px;
  box-shadow: 0 10px 22px rgba(0,0,0,.08);
}
.tile-fixed {
  height: calc(100vh - 140px);
  display: flex; flex-direction: column;
}
.tile-body { flex: 1 1 auto; overflow-y: auto; padding-right: 4px; }
.tile-footer {
  margin-top: 10px; padding-top: 10px;
  border-top: 1px solid rgba(0,0,0,.06);
  display: flex; gap: 12px; align-items: center;
}

/* Quasar Overrides */
html, body, .q-layout, .q-page, .q-tab-panels, .q-panel-parent {
  background: #f6f7f9 !important;
}

/* --- SIDEBAR NAVIGATION STYLES --- */
.side-nav-tabs .q-tab {
    padding: 0 16px;
    min-height: 40px;
    border-radius: 8px;
    margin-bottom: 4px;
    color: #5f6368;
    width: 100%; /* Ensure tab takes full width of sidebar */
}

/* IMPORTANT: Target the inner content to Left Align the icon and text */
.side-nav-tabs .q-tab__content { 
    justify-content: flex-start !important; 
    width: 100%;
}

.side-nav-tabs .q-tab__label { 
    font-size: 14px; 
    font-weight: 500;
    padding-left: 8px; /* Add slight gap between icon and text */
}

.side-nav-tabs .q-tab--active { 
    background-color: #e6f4f3; 
    color: #00786f; 
}

/* Hide the underlining slider */
.side-nav-tabs .q-tab__indicator { display: none; }
""", shared=True)

@ui.page('/')
def login_page():
    ui.colors(primary='#007878')
    with ui.row().style('height: 100vh; width: 100%; margin: 0; padding: 0;'):
        
        # LEFT PANEL (Vertically Centered)
        with ui.column().classes('justify-center').style(
            'flex: 1; padding: 48px; max-width: 480px; height: 100vh;'
        ):
            # Logo
            ui.image('/assets/plaksha-logo.png').style('height: 60px; width: 200px; margin-left: -20px;')
            
            # Text block
            ui.label('Score Manager').style('font-size: 32px; font-weight: 600; margin-top: 24px;')
            ui.label('Login to continue').style('font-size: 16px; color: #666; margin-bottom: 24px;')

            # Inputs
            ui.input(placeholder='Email').style('width: 100%; max-width: 320px;')
            ui.input(placeholder='Password', password=True).style('width: 100%; max-width: 320px;')

            # Button
            ui.button('Enter Configuration', icon='settings', on_click=go_to_config) \
                .classes('btn-primary rounded-12').style('width: 100%; max-width: 320px; height: 44px; margin-top: 16px;')

            # SSO Link
            ui.button('Use organization account', on_click=handle_sso_login) \
                .classes('btn-secondary rounded-12').style('width: 100%; max-width: 320px; margin-top: 8px;')

        # RIGHT PANEL
        with ui.element('div').classes('rounded-12').style(
            'flex: 1; height: calc(100vh - 40px); margin: 20px 20px 20px 0; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.1);'
        ):
            ui.image('/assets/login-hero.jpg').style('width: 100%; height: 100%; object-fit: cover;')

#ui.run(port=8080, on_air=True)
ui.run(port=8080)