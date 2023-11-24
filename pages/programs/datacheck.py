import asyncio
from fractions import Fraction
import numpy as np
import flet as ft
import pandas as pd
import csv
import aiofiles

#class Tx(ft.Text):
#    def __init__(self, text):
#        self.value = text
#        self.size = 14

class Tb(ft.DataTable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.id = id
        #self.df = df
    
    #def copytable(self):
        #self.df.to_clipboard()   
    
        
        

# cd D:\pyproj\fletmainproj\code\pages
# flet run main.py
# cd D:\pyproj\fletmainproj\jordanvenv
# Scripts\activate


class Data():
    def __init__(self, data, type, ndec, frac, iterat, maxiterat):
        self.data = data
        self.type = type
        self.ndec = ndec
        self.frac = frac
        self.iterat = iterat
             
        self.state = ''
        self.array = np.empty(1)
        self.checked = False
        
        self.log = []
        self.nacol = []
        self.narow = []
        
        self.df = None
        self.id = 0
        
        self.df_hist = []
        
        self.numiter = 0
        self.maxiterat = maxiterat 
        
        self.text_error = ft.Text(
                "generic text",
                size=22,
                color=ft.colors.WHITE,
                bgcolor=ft.colors.RED_700,
                weight=ft.FontWeight.W_100,
            )
        
    
    async def check_data(self):
        p = False
        # Check data correct.
        if self.type == "comma":
            comma = self.data
            result = await self.__process_data(comma, "comma")
            p = True
            
        elif self.type == "csv":
            route = self.data
            result = await self.__process_data(route, "csv")
            p = True
            
        if p == True:
            # Error management
            if type(result) == type(np.empty(1)):
                # NOW DATA IS IN A NUMPY'S ARRAY
                self.checked = True
                self.array = result
                return [False, result]
            elif result == "numnofloat": 
                text_error = self.text_error
                text_error.value = "ERROR: Los datos introducidos deberian ser reales, pero estos no coinciden con el tipo de dato indicado."
                return [True, text_error]
            elif result == "numnofrac":
                text_error = self.text_error
                text_error.value = "ERROR: Los datos introducidos deberian ser fracciones, pero estos no coinciden con el tipo de dato indicado."
                return [True, text_error]
            elif result == "nosamedim":
                text_error = self.text_error
                text_error.value = "ERROR: Los datos indicados generan una matriz de dimensiones no conformables."
                return [True, text_error]
            elif result == 'zeroonfrac':
                text_error = self.text_error
                text_error.value = "ERROR: No se puede contener valores que contengan como denominador el cero."
                return [True, text_error]
            elif result == "nofracindicated":
                text_error = self.text_error
                text_error.value = "CRITICAL ERROR: NO FRACTION TRUE OR FALSE INDICATED."
                return [True, text_error]
            else: 
                text_error = self.text_error
                text_error.value = "CRITICAL ERROR: MISSING DATA."
                return [True, text_error]
            
        #elif self.type == "ecuation":
        #    pass
        
        else:
            print("ERROR MISSING DATA TYPE")
              
        
        
    
    async def __process_data(self, data: str, dtype):
        
        if dtype == "comma":
            new_data = data.replace(' ','')
            new_data = new_data.replace('\n','')
            new_data = new_data.split(';')
            mid_data = []
            for row in new_data:
                mid_data.append(row.split(','))
                
        elif dtype == "csv":
            mid_data = []
        
            async with aiofiles.open(data, "r", newline="", encoding="utf-8") as file:
                lines = await file.readlines()
                table = csv.reader(lines)

                for row in table:
                    new_row = [str(x) for x in row]
                    mid_data.append(new_row)
            
        final_data = []
        for row in mid_data:
            new_row = []
            for num in row:
                if self.frac == False:
                    try:
                        new_row.append(float(num))
                    except ValueError:
                        return "numnofloat"
                    else:
                        pass
                elif self.frac == True:
                    try:
                        new_row.append(Fraction(num))
                    except ValueError:
                        return "numnofrac"
                    except  ZeroDivisionError:
                        return "zeroonfrac"
                    else:
                        pass
                else:
                    return "nofracindicated"
            final_data.append(new_row)
        
        try:
            final_data = np.array(final_data)
        except ValueError:
            return "nosamedim"
        else:
            return final_data
    
    
    async def solve(self):
        if self.checked != True:
            return "No se puede ejecutar"
        else:
            self.shape = self.array.shape
            self.m = self.shape[0] - 1
            self.n = self.shape[1] - 1
            self.log.append(ft.Text("El proceso será iniciado", size=18, selectable=True))
            self.log.append(ft.Text(f"El tamaño de la matriz es de {self.m+1}x{self.n+1}, y su tableu inicial es el siguiente:", size=14, selectable=True))
            
            # Get dataframe with data and cols, rows names
            if self.type == "csv" or self.type == "comma":
                # Create DataFrame
                self.df = pd.DataFrame(self.array)
                # Reindexing
                self.df = self.df.rename(
                    columns = lambda x: "-X" + f"{x+1}" if x < self.n else "1", 
                    index = lambda x: "Y" + f"{x+1}" if x < self.m else "Z")
                # Round decimals if fraction == False
                if self.frac == False: self.df.round(self.ndec)
                # Get row names and col names
                self.nacol = list(self.df.columns)
                self.narow = list(self.df.index)

                self.df_hist.append(pd.DataFrame(self.df))
                self.log.append(self.__gettable())
                
                # Now begins solution:
                
                # Get negative Z index
                index = await self.__issolved()
                if index == -1:
                    self.log.append(await self.__getwarning("alreadysolution"))
                else:
                    # continuar
                    pivote = await self.__getpivot(index)
                    if pivote == (-1, -1):
                        self.log.append(await self.__getwarning("allneg"))
                    else:
                        if self.iterat == True:
                            self.log.append(ft.Text(f"Iteración número: {self.numiter} \nEl pivote elegido se encuentra en ({pivote[0]},{pivote[1]}), con valor de {self.array[pivote]}", size=14, selectable=True))
                        result = await self.__resolve(pivote)
                        self.log.append(result)
                        
                        while self.numiter <= self.maxiterat:
                            index = await self.__issolved()
                            if index == -1:
                                self.log.append(await self.__showresult())
                                self.log.append(self.__gettable())
                                break
                            else:
                                pivote = await self.__getpivot(index)
                                if self.iterat == True:
                                    self.log.append(ft.Text(f"Iteración número: {self.numiter} \nEl pivote elegido se encuentra en ({pivote[0]},{pivote[1]}), con valor de {self.array[pivote]}", size=14, selectable=True))
                                result = await self.__resolve(pivote)
                                self.log.append(result)
                        self.log.append(ft.Text(f"Se ha llegado al número máximo de iteraciones.", size=14, selectable=True))    
                                
                        
            print(self.log)
            return self.log
                
    
    async def __showresult(self):
        return ft.Text(
            f"Solución encontrada en 1 iteración." if self.numiter == 1 else f"Solución encontrada en {self.numiter} iteraciones.",
            max_lines=2,
            bgcolor=ft.colors.GREEN_ACCENT_700,
            color=ft.colors.BLACK,
            size=20,
            text_align=ft.TextAlign.CENTER
        )   
    
    
    async def __resolve(self, pv):
        r, s = pv[0], pv[1]
        clone = np.copy(self.array)
        pivote = self.array[r,s]
        
        self.array[r,s] = 1/pivote
        
        for i in range(0, self.m + 1):
            if i == r: continue
            self.array[i,s] = - clone[i,s]/pivote
        
        for j in range(0, self.n + 1):
            if j == s: continue
            self.array[r,j] = clone[r,j]/pivote
        
        for i in range(0, self.m + 1):
            if i == r: continue
            else:
                for j in range(0, self.n + 1):
                    if j == s: continue
                    else: self.array[i,j] = clone[i,j] - ((clone[i,s]*clone[r,j])/pivote)
        
        nacol = str(self.nacol[s])
        print(nacol)
        narow = self.narow[r]
        nacol = nacol[1:len(nacol)]
        self.narow[r] = nacol
        self.nacol[s] = "-" + narow
        
        await self.__modifdf()
        
        if self.iterat == True:
            return self.__gettable()
        else:
            return ft.Text(f"Se encontró solución para la iteración {self.numiter}")

        
        
    
    async def __modifdf(self):
        self.df = pd.DataFrame(
            self.array,
            index = self.narow,
            columns = self.nacol
        )
        
    
    async def __getpivot(self, column):
        self.numiter += 1
        nmax = 99999999999999999999999999
        values = []
        for i, j in enumerate(self.array[:,column]):
            if j <= 0: values.append(nmax)
            else: values.append(self.array[i,self.n]/j)
        if min(values) == nmax: 
            return (-1, -1)
        else: 
            r = values.index(min(values))
            return (r, column)
                
                
    async def __issolved(self):
        index = -1
        for i, j in enumerate(self.array[self.m,:]):
            if j < 0:
                index = i
                break
        return index


    async def __getwarning(self, error):
        if error == "alreadysolution":
            wtext = "Advertencia: Los valores positivos en la ultima fila\nindican que no es necesario buscar solucion."
        elif error == "allneg":
            wtext = "Advertencia: Todos los valores en la columna son negativos,\nrevisar que el despeje para el tableu sea correcto."
        return ft.Text(
            wtext,
            max_lines=2,
            bgcolor=ft.colors.AMBER,
            color=ft.colors.BLACK,
            size=20,
            text_align=ft.TextAlign.CENTER
        )   
    
         
    def __gettable(self):
        # Round decimals
        if self.frac == False:
            dataframe = self.df.round(self.ndec)
        else:
            dataframe = self.df
        # Create table
        table = Tb(columns=[], rows=[],
                             column_spacing=20,
                             border=ft.border.all(1.5, ft.colors.BROWN_900),
                             border_radius=4,
                             divider_thickness=0,
                             vertical_lines=ft.border.BorderSide(1.5, ft.colors.BROWN_900),
                             horizontal_lines=ft.border.BorderSide(1.5, ft.colors.BROWN_900),
                             heading_row_height=30,
                             data_row_max_height=40,
                             #df = df,
                             #id = self.id
                             )
        # Create columns                                                     #, on_click = table.copytable
        new_columns=[ft.DataColumn(ft.Container(ft.Icon(ft.icons.COPY, size=14)))]
        for i in self.nacol:
            new_columns.append(ft.DataColumn(ft.Text(f"{i}", text_align=ft.TextAlign.CENTER, selectable=True)))
        table.columns = new_columns
        # Add rows
        for index, row in dataframe.iterrows():
            cells = [ft.DataCell(ft.Text(f"{index}", text_align=ft.TextAlign.START , selectable=True))]
            for i in range(self.n+1):
                cells.append(ft.DataCell(ft.Text(f"{row.iloc[i]}", text_align=ft.TextAlign.START , selectable=True)))
            table.rows.append(ft.DataRow(cells))
        # Manage ids
        #self.id += 1
        # Return table
        return table
            


            
        

if __name__ == "__main__":
    mode = 2
    if mode == 0:
        data = Data(
            data = """
            2, 1, 2 ;
            -3, 4, 12;
            0 , 1, 6 ;
            3 ,-1, 6 ;
            3 ,-1, 5 ;
            1 ,-1, 5 ;
            3 ,-6, 0
            """,
            type="comma", #csv ecuation,
            ndec=3,
            frac=True,
            iterat=True
        )
        
    elif mode == 1:
        data = Data(
            data = """
            2 ,-1, 2 ;
            -3,-4, 12;
            0 ,-1, 6 ;
            3 ,-1, 6 ;
            3 ,-1, 5 ;
            1 ,-1, 5 ;
            3 ,-6, 0
            """,
            type="comma", #csv ecuation,
            ndec=3,
            frac=False,
            iterat=True
        )
    
    if mode == 2:
        data = Data(
            data = """
            -2, 1, 2 ;
            -3, 4, 12;
            0 , 1, 6 ;
            3 ,-1, 6 ;
            3 ,-1, 5 ;
            1 ,-1, 5 ;
            3 ,-6, 0
            """,
            type="comma", #csv ecuation,
            ndec=3,
            frac=True,
            iterat=True
        )
    
    asyncio.run(data.check_data())
    
    asyncio.run(data.solve())
    
    def main(page: ft.Page):
        page.add(ft.Column(data.log, scroll=True))
        
    ft.app(target=main)

    
