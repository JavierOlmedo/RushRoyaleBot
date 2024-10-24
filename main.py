import os
from source.app import App

if __name__ == "__main__":
    try:
        os.system("cls||clear")
        app = App()
        app.mainloop()

    except KeyboardInterrupt:
        print("[-] User aborted App!")
        app.destroy()
        