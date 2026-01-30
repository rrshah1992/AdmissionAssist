# pages/tabs/normalisation.py
from typing import List, Dict
from nicegui import ui  # type: ignore


def build_normalisation_tab(board_options: List[str]) -> None:
    """
    Tab 3: Normalisation configuration.

    Mirrors your existing UI:
    - Single centered tile
    - Board dropdown + modifier input
    - Scrollable saved rows area
    - Footer buttons with ... stubs
    """

    # in-memory list of saved rows for this tab only
    rows_norm: List[Dict[str, str]] = []  # {'board', 'modifier'}

    # Single tile centered, same height logic as Average tiles
    with ui.card().classes('tile tile-fixed').style(
        'width: 100%; max-width: 760px; padding: 16px; '
        'height: calc(100vh - 290px); margin: 12px auto 0;'
    ):
        # flex column so footer stays at bottom
        with ui.column().style(
            'width: 100%; height: 100%; display: flex; '
            'flex-direction: column; gap: 10px;'
        ):

            # HEADER ROW (match left tile structure)
            with ui.row().style(
                'width: 100%; font-size: 13px; font-weight: 600; '
                'color: #555; align-items: center;'
            ):
                with ui.row().style(
                    'min-width: 180px; align-items: center; gap: 6px;'
                ):
                    ui.label('Board')
                    ui.button(
                        'Add new',
                        on_click=lambda: ui.notify('Add board (stub)'),
                    ).props('flat dense').style('font-size: 11px;')

                ui.label('Modification to calculated average').style(
                    'flex: 1; min-width: 0;'
                )
                ui.label('').style('width: 80px;')  # aligns with + button

            # INPUT ROW + + BUTTON
            with ui.row().style(
                'width: 100%; gap: 12px; align-items: flex-end; '
                'flex-wrap: nowrap;'
            ):
                default_board = board_options[0] if board_options else None
                norm_board_select = ui.select(
                    board_options,
                    value=default_board,
                    with_input=False,
                ).style('min-width: 180px; flex: 0 0 180px;')

                modifier_input = ui.input(
                    placeholder='e.g. +5, *0.9, cap at 95, etc.'
                ).style('flex: 1; min-width: 0;')

                # forward declaration so the function exists when called
                def render_rows_norm() -> None:
                    ...

                def save_norm_row() -> None:
                    rows_norm.append(
                        {
                            'board': norm_board_select.value,
                            'modifier': modifier_input.value or '',
                        }
                    )
                    modifier_input.value = ''
                    render_rows_norm()

                ui.button('Add', on_click=save_norm_row) \
                    .props('outline') \
                    .classes('rounded-12') \
                    .style('min-width: 90px;')

            # ✅ SAVED ROWS AREA: ONLY THIS SCROLLS
            table_container_norm = ui.column().classes('tile-body').style(
                'flex: 1; min-height: 0; width: 100%; '
                'overflow-y: auto; gap: 6px; margin-top: 8px; '
                'padding-right: 4px;'
            )

            def delete_row_norm(index: int) -> None:
                rows_norm.pop(index)
                render_rows_norm()

            def render_rows_norm() -> None:
                table_container_norm.clear()
                with table_container_norm:
                    if not rows_norm:
                        ui.label('No rows saved yet.').style(
                            'font-size: 13px; color: #777; margin-top: 4px;'
                        )
                        return

                    for i, row in enumerate(rows_norm):
                        with ui.row().style(
                            'width: 100%; gap: 12px; align-items: center;'
                        ):
                            ui.label(row['board']).style('min-width: 180px;')
                            ui.label(row['modifier']).style(
                                'flex: 1; min-width: 0;'
                            )

                            # Edit (stub)
                            ui.button(
                                icon='edit',
                                on_click=lambda idx=i: ui.notify(
                                    f'Edit {idx} (stub)'
                                ),
                            ).props('outline dense').classes('rounded-12')

                            # Delete
                            ui.button(
                                icon='delete',
                                on_click=lambda idx=i: delete_row_norm(idx),
                            ).props('outline dense').classes('rounded-12') \
                             .style(
                                 'border-color: #b00020; color: #b00020;'
                             )

            # initial render -> empty state
            render_rows_norm()

            # helper text
            ui.label(
                'Export currently set configuration.'
            ).style('font-size: 12px; color: #666; margin-top: 6px;')

            # FOOTER – STICKS TO BOTTOM (thanks to flex column)
            with ui.row().classes('tile-footer'):
                ui.button(
                    'Download current config',
                    icon='download',
                    on_click=...
                ).props('outline').classes('btn-secondary rounded-12')
