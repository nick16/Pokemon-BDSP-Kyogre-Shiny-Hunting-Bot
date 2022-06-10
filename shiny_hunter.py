from gi.repository import Gdk


# Check if Kyogre on screen is of a Pinkish color.
def shiny(r,g,b):
    if r >= 162 and r <= 231:
        if g >= 28 and g <= 113:
            if b >= 182 and b <= 255:
                return True
    return False

# If the bot gets stuck in some setting in the Switch home ui
def stuck(r,g,b):
    # Feel free to add colors to this if the controller ends up somewhere you dont want it.
    # At the moment this is checking the Switch menu's grey colors.
    if (r == 71 or r == 40) and \
       (g == 71 or g == 42) and \
       (b == 71 or b == 44):
        return True
    return False

# Checks the color at pixel (x,y) if its shiny or not.
def checkColor(x,y):
    w = Gdk.get_default_root_window()
    pb = Gdk.pixbuf_get_from_window(w, x, y, 1, 1)
    r,g,b = pb.get_pixels()
    print(f'COLOR: rgb{(r,g,b)} | xy{x,y}')

    if shiny(r,g,b):
        print('SHINY')
        return "shiny"
    elif stuck(r,g,b):
        print('STUCK')
        return 'stuck'
    else:
        print('not shiny')
        return 'not_shiny'
