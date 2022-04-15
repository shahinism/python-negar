def main():
    try:
        from negar_gui import gui
        gui.main()
    except ModuleNotFoundError:
        print("Install `negar-gui` to have a GUI! :D")
        print("==>> pip install negar-gui")
        print("After installing negar-gui, `negar` would be an alias for `negar-gui`")

if __name__=="__main__":
    main()
