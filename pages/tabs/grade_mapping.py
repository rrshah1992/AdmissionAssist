from nicegui import ui  # type: ignore


def build_grade_mapping_tab(board_options: list[str]) -> None:
    """Tab 1: board-wise score/grade to marks mapping (average logic)."""

    # in-memory rows for this tab
    rows_avg: list[dict] = []   # {'board', 'transcript', 'formula'}

    # wrapper row (card will be centered via margin: auto)
    with ui.row().style(
        'width: 100%; margin-top: 6px;'
    ):
        # Single card (now same width & alignment as Normalisation tab)
        with ui.card().classes('tile tile-fixed').style(
            'width: 100%; max-width: 760px; '
            'padding: 16px; '
            'height: calc(100vh - 290px); '
            'margin: 12px auto 0;'
        ):
            # flex column so the footer can stick to the bottom
            with ui.column().style(
                'width: 100%; height: 100%; display: flex; '
                'flex-direction: column; gap: 10px;'
            ):
                ui.label('Score calculation formula').style(
                    'font-size: 16px; font-weight: 600;'
                )

                # HEADER ROW
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

                    ui.label('Score as on transcript').style('flex: 1;')
                    ui.label('Score to consider').style('flex: 1;')
                    ui.label('')  # placeholder for actions

                # ---- placeholders for table container so helpers can see it ---
                table_container_avg = None  # will be set after definition

                # --- helpers ---------------------------------------------------
                def render_rows_avg() -> None:
                    nonlocal table_container_avg
                    if table_container_avg is None:
                        return
                    table_container_avg.clear()
                    if not rows_avg:
                        with table_container_avg:
                            ui.label(
                                'No rules added yet. Use “Add” above to '
                                'save your first score calculation rule.'
                            ).style(
                                'font-size: 13px; color: #777; '
                                'margin-top: 4px;'
                            )
                        return

                    with table_container_avg:
                        for i, row in enumerate(rows_avg):
                            with ui.row().style(
                                'width: 100%; gap: 12px; '
                                'align-items: center;'
                            ):
                                ui.label(row['board']).style(
                                    'min-width: 180px;'
                                )
                                ui.label(row['transcript']).style('flex: 1;')
                                ui.label(row['formula']).style('flex: 1;')

                                def open_edit(idx=i) -> None:
                                    open_edit_dialog_avg(idx)

                                def delete(idx=i) -> None:
                                    delete_row_avg(idx)

                                ui.button(
                                    icon='edit', on_click=open_edit
                                ).props('outline dense').classes('rounded-12')

                                ui.button(
                                    icon='delete', on_click=delete
                                ).props('outline dense').classes(
                                    'rounded-12'
                                ).style(
                                    'border-color: #b00020; '
                                    'color: #b00020;'
                                )

                def save_current_row() -> None:
                    rows_avg.append(
                        {
                            'board': board_select.value,
                            'transcript': transcript_input.value or '',
                            'formula': formula_input.value or '',
                        }
                    )
                    transcript_input.value = ''
                    formula_input.value = ''
                    render_rows_avg()

                def delete_row_avg(index: int) -> None:
                    rows_avg.pop(index)
                    render_rows_avg()

                def open_edit_dialog_avg(index: int) -> None:
                    row = rows_avg[index]
                    with ui.dialog() as dialog, ui.card().style(
                        'min-width: 480px;'
                    ):
                        ui.label('Edit configuration row').style(
                            'font-size: 16px; font-weight: 600;'
                        )
                        edit_board = ui.select(
                            board_options,
                            value=row['board'],
                            with_input=False,
                        )
                        edit_transcript = ui.input(
                            label='Score as on transcript',
                            value=row['transcript'],
                        )
                        edit_formula = ui.input(
                            label='Score to consider',
                            value=row['formula'],
                        )

                        with ui.row().style(
                            'justify-content: flex-end; gap: 8px; '
                            'margin-top: 12px;'
                        ):
                            ui.button(
                                'Cancel', on_click=dialog.close
                            ).props('flat')

                            def save_edit() -> None:
                                rows_avg[index] = {
                                    'board': edit_board.value,
                                    'transcript': edit_transcript.value or '',
                                    'formula': edit_formula.value or '',
                                }
                                dialog.close()
                                render_rows_avg()

                            ui.button(
                                'Save changes', on_click=save_edit
                            ).classes('btn-primary rounded-12')

                    dialog.open()

                # INPUT ROW + ADD BUTTON
                with ui.row().style(
                    'width: 100%; gap: 12px; align-items: flex-end;'
                ):
                    board_select = ui.select(
                        board_options,
                        value=board_options[0],
                        with_input=False,
                    ).style('min-width: 170px;')

                    transcript_input = ui.input(
                        placeholder='e.g. Class 12 Physics marks',
                    ).style('flex: 1;')

                    formula_input = ui.input(
                        placeholder='e.g. (marks / max_marks) * 100',
                    ).style('flex: 1;')

                    ui.button('Add', on_click=save_current_row) \
                        .props('outline') \
                        .classes('rounded-12') \
                        .style('min-width: 90px;')

                # SCROLLABLE TABLE AREA – TAKES AVAILABLE HEIGHT
                table_container_avg = ui.column().classes(
                    'tile-body'
                ).style(
                    'width: 100%; gap: 6px; margin-top: 8px; '
                    'flex: 1; min-height: 0; overflow-y: auto; '
                    'padding-right: 4px;'
                )

                # initial render (will show empty-state message)
                render_rows_avg()

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
