from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import jordan


desarrollo = False
simbol = False
decimales = False


class MainLayout(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.texto = ''

    
    def mostrar_desarrollo(self, instancia, valor):
        global desarrollo
        desarrollo = valor
        
    def simbolico(self,instancia,valor):
        global simbol
        simbol = valor
        
    def obtener_decimales(self,instancia,valor):
        global decimales
        decimales = valor
    
    def input_no_vacio(self, texto):
        if texto == '':
            return False
        else:
            return True
    
    def obtener_num_decimales(self,texto=''):
        ans = texto.split(' ')
        try:
            n = int(ans[1])
        except ValueError:
            return [False, 0]
        else:
            return [ans[0], n]
        
    
    def obtener_texto(self):
        self.texto = self.ids.input.text
    
    def iniciar_csv(self):
        global decimales, desarrollo, simbol
        input = self.texto
        if self.input_no_vacio(input) == False:
            self.imprimir_resultados('\n=== INGRESAR DATOS NO VACIOS ===\n')
        else:
            if decimales == True:
                lista = self.obtener_num_decimales(input)
                if lista[0] == False:
                    self.imprimir_resultados('\n=== PARAMETRO N INVALIDO ===\n')
                else:
                    jordan.iniciar_desde_csv(lista[0], desarrollo, simbol, lista[1])
                    self.imprimir_resultados(jordan.log)
            else:
                jordan.iniciar_desde_csv(input, desarrollo, simbol, 3)
                self.imprimir_resultados(jordan.log)
        
    
    def iniciar_datos(self):
        global decimales, desarrollo, simbol
        input = self.texto
        if self.input_no_vacio(input) == False:
            self.imprimir_resultados('\n=== INGRESAR DATOS NO VACIOS ===\n')
        else:
            if decimales == True:
                lista = self.obtener_num_decimales(input)
                if lista[0] == False:
                    self.imprimir_resultados('\n=== PARAMETRO N INVALIDO ===\n')
                else:
                    jordan.iniciar_desde_texto(lista[0], desarrollo, simbol, lista[1])
                    self.imprimir_resultados(jordan.log)
            else:
                jordan.iniciar_desde_texto(input, desarrollo, simbol, 3)
                self.imprimir_resultados(jordan.log)
    
    def limpiar(self):
        self.ids.resultado.text = ''
    
    def exportar_csv(self):
        self.ids.resultado.text += '\nPROXIMAMENTE\n'
    
    def exportar_txt(self):
        texto = self.ids.resultado.text
        with open('resultado.txt', 'x', encoding='UTF-8') as archivo:
            archivo.write(texto)
    
    def informacion(self):
        self.ids.resultado.text += '''
        
        ============ PROYECTO PORYGON ============
        
        Hecho por: Abdiel Hernandez
        
        Mira el programa y codigo en:
        https://github.com/abdzher/ProyectoPorygon
        
        '''

    def imprimir_resultados(self,texto):
        self.ids.resultado.text += texto
        

class MainApp(App):
    def build(self):
        return MainLayout()


if __name__ == '__main__':
    MainApp().run()