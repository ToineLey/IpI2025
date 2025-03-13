import termios
import sys
import tty
import select


def getch():  # Timeout en secondes
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        # Utilisation de select pour attendre l'entrée avec un timeout
        ready, _, _ = select.select([sys.stdin], [], [], 0.0005)
        if ready:
            return sys.stdin.read(1)  # Si une touche est appuyée
        else:
            return ''  # Si rien n'est appuyé après le timeout
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
