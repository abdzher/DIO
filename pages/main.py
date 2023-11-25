import flet as ft
import numpy as np

from programs.texts import Indicator
from programs.texts import TXT
from programs.datacheck import Data

import asyncio as asy

indicator = Indicator()


async def main(page: ft.Page):
    
    async def show_info1(e):
        await page.show_dialog_async(info1_dialog)
        await page.update_async()
        
    async def show_egg(e):
        if e == 0:
            algo = TXT.eg_nekoarc
        elif e == 1:
            algo = TXT.eg_hola
        elif e == 2:
            algo = TXT.eg_pastel
        alertegg = ft.AlertDialog(
            title = ft.Text(value = "Me encontraste...", 
                      style=ft.TextThemeStyle.TITLE_MEDIUM),
            content=ft.Text(value=algo, 
                        style=ft.TextThemeStyle.BODY_MEDIUM)
            )
        await page.show_dialog_async(alertegg)
        await page.update_async()
        
            
    
    async def show_window_changes(e: ft.ControlEvent):
        main_page.width = page.window_width
        main_page.height = page.window_height - 100
        print(page.window_width, page.window_height)
        print(main_page.width, main_page.height)
        await page.update_async()
        
    ############ COMMA FUNCTIONS
    async def comma_data(e):
        await page.show_dialog_async(comma_dialog)
        await page.update_async()

    async def comma_data_accept(e):
        indicator.dtype = "comma"
        row3_tf.value = comma_field.value
        await page.close_dialog_async()
        await page.update_async()
    
    async def show_info_comma(e):
        await page.close_dialog_async()
        await page.update_async()
        await asy.sleep(0.2)
        await page.show_dialog_async(info_comma)
        await page.update_async()
    
    ############ ECUATION FUNCTIONS
    async def ecuation_data(e):
        await page.show_dialog_async(ecuation_dialog)
        await page.update_async()

    async def ecuation_data_accept(e):
        indicator.dtype = "ecuation"
        row3_tf.value = ecuation_field.value
        await page.close_dialog_async()
        await page.update_async()
    
    async def show_info_ecuation(e):
        await page.close_dialog_async()
        await page.update_async()
        await asy.sleep(0.2)
        await page.show_dialog_async(info_ecuation)
        await page.update_async()
        
    ############ CSV FUNCTIONS
    async def get_file(_):
        await get_file_dialog.pick_files_async(
            allow_multiple=False,
            dialog_title="Elija su archivo CSV.",
            allowed_extensions=["csv"],
            file_type=ft.FilePickerFileType.CUSTOM,
            )
        
    async def get_file_result(e: ft.FilePickerResultEvent):
        if e.files:
            selected_files.value = (
                ", ".join(map(lambda f: f.name, e.files)) 
            )
            indicator.file = list(map(lambda f: f.path, e.files))[0]
            print(indicator.file)
            indicator.file = fr"{indicator.file}"
            print(indicator.file)
        else:
            selected_files.value = "Ningun archivo seleccionado."
        await selected_files.update_async()

    async def csv_data(e):
        await page.show_dialog_async(csv_dialog)
        await page.update_async()

    async def csv_data_accept(e):
        indicator.dtype = "csv"
        row3_tf.value = selected_files.value
        await page.close_dialog_async()
        await page.update_async()
    
    async def show_info_csv(e):
        await page.close_dialog_async()
        await page.update_async()
        await asy.sleep(0.2)
        await page.show_dialog_async(info_csv)
        await page.update_async()
    
    
    # ======= START FUNCTIONS
    async def start_press(e):
        prog_bar_column.controls.clear()
        await page.update_async()
        prog_bar_column.height = 45
        prog_bar_column.controls.append(ft.Text("Se esta procesando su informacion"))
        prog_bar_column.controls.append(ft.ProgressBar(width=400, color="amber", bgcolor="#eeeeee"))
        await page.update_async()
        
        data = await start_proc()
        
        if type(data) == str:
            await show_error(data)
        elif type(data) == type(None):
            print('Se ha llamado al error exitosamente')
        elif type(data.data) == type(np.empty(1)):
            #print(data.data)
            await show_error('passed')
            controls = await data.solve()
            #print(controls)
            prog_bar_column.controls.extend(controls)
            prog_bar_column.height = page.window_height - 150
            await page.update_async()
            ##############################################################################
            # -2, 1, 2 ; -3, 4, 12; 0 , 1, 6 ; 3 ,-1, 21 ; 3 ,-1, 5 ; 3 ,-6, 0
            # -2, 1, 2 ; -3, 4, 12; 0 , 1, 6 ; 3 ,-1, 21 ; 1 ,-1, 5 ; 3 ,-6, 0
        else:
            print("CRITICAL ERROR: no data capture")
            
            
    
    async def start_proc():
        passed = False
        dtype = indicator.dtype
        
        
        if dtype == "ecuation" or dtype == "comma":
            pdata = row3_tf.value
            passed = True
        else:
            pdata = indicator.file
            if pdata == "\...": 
                return "nodataerror"
            else:
                passed = True
        
        egg_list = ["nekoarc", "hola","pastel"]  
        if pdata in egg_list:
            passed = False
            await show_egg(egg_list.index(pdata))
            return "easteregg"
            
        
        if passed == True:
            passed = False
            try:
                ndec = int(row3_ndec.value.replace(' ',""))
                maxiterat = int(row3_niter.value.replace(' ',""))
            except ValueError:
                return "valndec"
            else:
                if ndec < 0 or maxiterat < 0: return "minndec"
                else: passed = True
        
        if passed == True:
            frac = row3_frac.value
            iterat = row3_showit.value
            data = Data(pdata, dtype, ndec, frac, iterat, maxiterat)
            check = await data.check_data()
            if check[0] == True:
                await show_internal_error(check[1])
            elif check[0] == False:
                data.data = check[1]
                return data
            else:
                print('CRTICAL ERROR: NO CHECKED DATA')
                return 'ERROR NO CHECKED DATA'

            
        
    
    async def show_error(error):
        prog_bar_column.controls.clear()
        error_text = ft.Text(
                "generic text",
                size=30,
                color=ft.colors.WHITE,
                bgcolor=ft.colors.RED_700,
                weight=ft.FontWeight.W_100,
            )
        if error == "nodataerror":
            error_text.value = "ERROR: No hay datos seleccionados."
            prog_bar_column.controls.append(error_text)
            await page.update_async()
        elif error == "valndec":
            error_text.value = "ERROR: No se indico un numero de decimales o el maximo de iteraciones entero."
            prog_bar_column.controls.append(error_text)
            await page.update_async()
        elif error == "minndec":
            error_text.value = "ERROR: El numero de decimales o el maximo de iteraciones elegidos es negativo."
            prog_bar_column.controls.append(error_text)
            await page.update_async()
        elif error == "passed":
            error_text.value = "POSTIVO: Informacion leida correctamente."
            error_text.bgcolor = ft.colors.GREEN
            prog_bar_column.controls.append(error_text)
            await page.update_async()
        elif error == "easteregg":
            error_text.value = "Aún hay más..."
            error_text.bgcolor = ft.colors.AMBER
            prog_bar_column.controls.append(error_text)
            await page.update_async()
            
    
    async def show_internal_error(error):
        prog_bar_column.controls.clear()
        prog_bar_column.controls.append(error)
        await page.update_async()
    
    
    
    
    # ================== APPBAR =======================
    appbar = ft.AppBar(
        leading = ft.Icon(ft.icons.TABLE_CHART),
        #leading= ft.Image(src = "icon.ico"),
        leading_width=50,
        title = ft.Text("DIO: Tableu Solver"),
        bgcolor = ft.colors.LIGHT_BLUE_700
    )
    
    
    
    
    
    
    # ================= MAIN COLUMN ===================
    
    
    # ========= ELEMENTS =========
    
    # ROW1 ====
    #  Welcome text
    welcome_text = ft.Text(
        value = TXT.ext_welcome,
        style = ft.TextThemeStyle.TITLE_MEDIUM,
        text_align=ft.TextAlign.JUSTIFY,
        size=20,
        max_lines=2
        )
    ft.Text()
    # ROW 2 ====
    # Instruction 1
    instruction1 = ft.Text(
        value = TXT.ext_inst1,
        style = ft.TextThemeStyle.BODY_MEDIUM,
        size=16
        )
    
    info1 = ft.Container(
        ft.Icon(name = ft.icons.HELP, color=ft.colors.LIGHT_BLUE_700, size=20),
        on_click=show_info1
    )
    
    info1_dialog = ft.AlertDialog(
        title=ft.Text(value = TXT.info1_title, 
                      style=ft.TextThemeStyle.TITLE_MEDIUM),
        content=ft.Text(value=TXT.info1_info, 
                        style=ft.TextThemeStyle.BODY_MEDIUM)
    )
    
    row2 = ft.Row(
        controls=[instruction1,info1],
        width = page.window_width
    )
    
    # ROW 3 ====
    
    row3_tf = ft.TextField(
        label="Datos", 
        read_only=True, 
        value="Sus datos apareceran aqui.",
        autocorrect=False,
        multiline=True,
        min_lines=4
        )


    # COMMA ==
    row3_bt_comma = ft.ElevatedButton("Datos separados con coma.", on_click=comma_data)
    
    info_comma = ft.AlertDialog(
        title=ft.Text(value = TXT.comma_info_title, 
                      style=ft.TextThemeStyle.TITLE_MEDIUM),
        content=ft.Text(value=TXT.comma_info_text, 
                        style=ft.TextThemeStyle.BODY_MEDIUM)
    )
    
    comma_field = ft.TextField(label="Datos",value="Escriba",multiline=True)
    
    comma_dialog = ft.AlertDialog(
        title=ft.Text(TXT.comma_dial_title),
        content = comma_field,
        actions=[
            ft.TextButton("Ayuda", on_click=show_info_comma),
            ft.TextButton("Añadir datos", on_click=comma_data_accept),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    # COMMA ==
    
    # ECUCATION ==
    row3_bt_ect = ft.ElevatedButton("Introducir datos algebraicos.", on_click=ecuation_data)
    
    info_ecuation = ft.AlertDialog(
        title=ft.Text(value = TXT.ect_info_title, 
                      style=ft.TextThemeStyle.TITLE_MEDIUM),
        content=ft.Text(value=TXT.ect_info_text, 
                        style=ft.TextThemeStyle.BODY_MEDIUM)
    )
    
    ecuation_field = ft.TextField(label="Datos",value="NO IMPLEMENTADO AUN",multiline=True)
    
    ecuation_dialog = ft.AlertDialog(
        title=ft.Text(TXT.ect_dial_title),
        content = ecuation_field,
        actions=[
            ft.TextButton("Ayuda", on_click=show_info_ecuation),
            ft.TextButton("Añadir datos", on_click=ecuation_data_accept),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    # ecuation_dialog = 
    
    # ECUCATION ==
    
    # CSV ==
    row3_bt_file = ft.ElevatedButton("Elegir un archivo CSV.", on_click=csv_data)
    
    info_csv = ft.AlertDialog(
        title=ft.Text(value = TXT.csv_info_title, 
                      style=ft.TextThemeStyle.TITLE_MEDIUM),
        content=ft.Text(value=TXT.csv_info_text, 
                        style=ft.TextThemeStyle.BODY_MEDIUM)
    )

    get_file_dialog = ft.FilePicker(on_result=get_file_result)
    selected_files = ft.Text()
    page.overlay.append(get_file_dialog)
    
    csv_dialog = ft.AlertDialog(
        title = ft.Text(TXT.csv_dial_title),
        content = ft.Column([
            ft.ElevatedButton(
                "Subir archivo", 
                icon = ft.icons.FILE_UPLOAD,
                on_click= get_file
                ),
            selected_files
            ],
            height=50),
        actions=[
            ft.TextButton("Ayuda", on_click=show_info_csv),
            ft.TextButton("Añadir datos", on_click=csv_data_accept),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    # CSV ==
    
    row3_ndec = ft.TextField(label="Numero de decimales:", 
                             border=ft.InputBorder.UNDERLINE,
                             dense= False,
                             value="3")
    
    row3_niter = ft.TextField(label="Numero maximo de iteraciones:", 
                             border=ft.InputBorder.UNDERLINE,
                             dense= False,
                             value="999")
    
    row3_frac = ft.Checkbox(label = "¿Se usan fracciones?      ", value = False)
    
    row3_showit = ft.Checkbox(label="Mostrar todas las iteraciones", value=False)
    
    start_button = ft.FilledButton(
        content=ft.Row([ft.Icon(ft.icons.PLAY_ARROW, size=38),
                        ft.Text("INICIAR", size=22, text_align=ft.TextAlign.START)],
                       height=80,
                       alignment=ft.MainAxisAlignment.CENTER),
        style=ft.ButtonStyle(
            overlay_color=ft.colors.LIGHT_BLUE_100,
            bgcolor=ft.colors.LIGHT_BLUE_700,
            shape=ft.StadiumBorder()
        ),
        on_click = start_press
    )
    
    # row3_bt_ect
    row3 = ft.Row(
        controls=[
                  row3_tf,
                  ft.Column(
                      controls=[
                          ft.Row([row3_niter, row3_bt_file, row3_bt_comma]),
                          ft.Row([row3_ndec, row3_frac, row3_showit])
                      ]
                  ),
                  start_button
                 ],
        width=page.window_width
    )
    
    
    # ======== PROGRESS BAR =====

    prog_bar_column = ft.Column(
        height = 0,
        width = page.window_width,
        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        scroll = ft.ScrollMode.ALWAYS,
        
    )
    
    
    
    # ========= DEFINITION =======
    main_page_elements = [welcome_text, row2, row3, prog_bar_column]
    
    main_page = ft.Column(
        controls = main_page_elements,
        width = page.window_width,
        height = page.window_height - 100,
        scroll = ft.ScrollMode.AUTO,
        spacing = 20
    )
    
    
    
    
    
    
    
    
    # ================== MAIN STACK ===================
    main_layout = ft.Stack([main_page])
    
    
    
    
    
    page.on_window_event = show_window_changes
    
    # ================== ASYNC CALLS ===================
    await page.add_async(appbar, main_layout)
    


ft.app(target=main)