
#############################################################
# Username : ronshuvy
# Full Name : Ron Shuvy
# ID : 206330193
#############################################################

import turtle

def draw_petal():
    """ Draws single petal """
    turtle.down()
    turtle.forward(30)
    turtle.right(45)
    turtle.forward(30)
    turtle.right(135)
    turtle.forward(30)
    turtle.right(45)
    turtle.forward(30)
    turtle.right(135)

def draw_flower():
    """ Draws single flower """
    turtle.down()
    # draws the first petal
    turtle.left(45)
    draw_petal()
    # draws the second petal
    turtle.left(90)
    draw_petal()
    # draws the third petal
    turtle.left(90)
    draw_petal()
    # draws the fourth petal
    turtle.left(90)
    draw_petal()
    # draws the plant strem
    turtle.left(135)
    turtle.forward(150)

def draw_flower_and_advance():
    """ Draws single flower and advances the turtle for the next draw """
    draw_flower()
    # positions the turtle for the next draw
    turtle.right(90)
    turtle.up()
    turtle.forward(150)
    turtle.right(90)
    turtle.forward(150)
    turtle.left(90)
    turtle.down()

def draw_flower_bed():
    """ Draws 3 flowers """
    # moves to the starting point
    turtle.up()
    turtle.forward(200)
    turtle.left(180)
    turtle.down()
    # draws 3 flowers
    draw_flower_and_advance()
    draw_flower_and_advance()
    draw_flower_and_advance()

if __name__ == "__main__" :

    draw_flower_bed()
    turtle.done()
