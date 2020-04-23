from game_class import *

def main():

    g = Game()
    g.show_start_screen()

    while g.running:
        g.new()
        g.show_go_screen()

    pg.quit()

if __name__ == '__main__':
    main()
