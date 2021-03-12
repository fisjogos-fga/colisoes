import pyxel
import pymunk
import string


class Game:
    def __init__(self):
        self.input = Input(0, 186, on_clear=self.parse)
        self.paused = True
        self.space = pymunk.Space()

        # Crie objetos no mundo. Objetos A e B que participam da colisão.
        # Se sobrar tempo, crie paredes para manter estes objetos confinados 
        # à área da tela.
        ...  

    def update(self):
        """
        Atualiza o estado do jogo.
        """
        self.input.update()

        if pyxel.btn(pyxel.KEY_CONTROL) and pyxel.btnp(pyxel.KEY_SPACE):
            self.paused = not self.paused

        # Atualize a física do espaço se não estiver pausado.
        ...  

    def draw(self):
        """
        Desenha elementos na tela.
        """
        pyxel.cls(0)
        self.input.draw()

        # Desenhe os dois objetos do espaço. Se sobrar tempo, também implemente
        # funções para mostrar a velocidade e massa dos objetos do mundo.
        ...  

    def run(self):
        """
        Inicializa loop principal do jogo.
        """
        pyxel.run(self.update, self.draw)

    def define(self, name, value):
        print(f"Redefinindo valor: {name} = {value}")

        # Utilize o comando dado para modificar o valor das massas e
        # velocidades dos objetos A e B.
        ...

    # Todas as funções com o nome do tipo command_<comando> implementam
    # comandos que podem ser digitados da tela do jogo. O método abaixo
    # implementa o comando "restart"
    def command_restart(self):
        print("Reiniciando!")
        
        # Reinicie as velocidades e posições dos objetos.
        ...  

    def command_go(self):
        self.paused = False

    def command_pause(self):
        self.paused = True

    def parse(self, src):
        """
        Processa comandos do tipo <var> = <valor>

        Comandos bem sucedidos executam o método define(nome, valor).

            ATENÇÃO: Este código é necessário para fazer a demonstração funcionar, 
            mas não precisa dar muita atenção a ele na aula de hoje. Sempre fique a 
            vontade para estudá-lo depois :)
        """
        name, eq, value = map(str.strip, src.partition("="))

        if not eq:
            cmd = getattr(self, "command_" + name, None)
            if cmd:
                return cmd()
            self.input.error = f"comando nao reconhecido: {name}!"

        if not name or not eq or not name.isalpha():
            self.input.error = "comando invalido!"
            return

        try:
            value = float(value)
        except ValueError:
            self.input.error = f"digite um valor numerico, não {value}"

        self.define(name, value)



class Input:
    """
    A classe Input implementa uma caixa de entrada de texto primitiva que pode
    responder a comandos quando o usuário digita um texto e pressiona <enter>.

        ATENÇÃO: Este código é necessário para fazer a demonstração funcionar, 
        mas não precisa dar muita atenção a ele na aula de hoje. Sempre fique a 
        vontade para estudá-lo depois :)
    """
    COLOR_BG = pyxel.COLOR_GRAY
    COLOR_TEXT = pyxel.COLOR_BLACK
    COLOR_ERROR = pyxel.COLOR_RED
    COLOR_CURSOR = pyxel.COLOR_WHITE
    CHARS = {
        pyxel.KEY_SPACE: " ",
        pyxel.KEY_COMMA: ",",
        pyxel.KEY_SEMICOLON: ";",
        pyxel.KEY_EQUAL: "=",
        pyxel.KEY_MINUS: "-",
        pyxel.KEY_PERIOD: ".",
        # ...
    }
    CHARS.update(
        {getattr(pyxel, "KEY_" + k.upper()): k for k in string.ascii_lowercase}
    )
    CHARS.update({getattr(pyxel, "KEY_" + k.upper()): k for k in "0123456789"})

    def __init__(self, x, y, width=None, value="", on_clear=None):
        self.x = x
        self.y = y
        self.width = width
        self.value = value
        self.on_clear = on_clear
        self.error = ""
        self._idx = 0

    def update(self):
        self._idx += 1
        for key, char in self.CHARS.items():
            if pyxel.btnp(key):
                self.value += char
                self.error = ""
        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            if self.error:
                self.error = ""
            else:
                self.value = self.value[:-1]
        if pyxel.btnp(pyxel.KEY_ENTER):
            if self.error:
                self.error = ""
            elif self.on_clear:
                self.on_clear(self.value)
            self.value = ""

    def draw(self):
        width = self.width or pyxel.width - self.x
        pyxel.rect(self.x, self.y, width, 10, self.COLOR_BG)
        if (self._idx // 5) % 2 == 0:
            pyxel.text(self.x + 5, self.y + 3, ">", self.COLOR_CURSOR)

        if self.error:
            st, color = self.error, self.COLOR_ERROR
        else:
            st, color = self.value, self.COLOR_TEXT
        pyxel.text(self.x + 15, self.y + 3, st, color)


# Inicializa o jogo
pyxel.init(256, 196, caption="Uma colisão simples")
game = Game()
game.run()