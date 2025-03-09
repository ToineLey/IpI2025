import termios
import sys
import tty
import select


def getch(timeout=0.05):  # Timeout en secondes
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        # Utilisation de select pour attendre l'entrée avec un timeout
        ready, _, _ = select.select([sys.stdin], [], [], timeout)
        if ready:
            return sys.stdin.read(1)  # Si une touche est appuyée
        else:
            return ''  # Si rien n'est appuyé après le timeout
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
