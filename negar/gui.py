def main():
    try:
        from negar_gui.gui import main
        main()
    except ModuleNotFoundError:
        print("Install `negar-gui` to have a GUI! :D")
        print("==>> pip install negar-gui")
        print("After installing negar-gui, `negar` would be an alias for `negar-gui`")