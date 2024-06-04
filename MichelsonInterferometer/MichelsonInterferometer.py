from tkinter import *
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import math

plt.ion()  # Open the interactive mode.
mpl.use('TkAgg')  # Tkinter & matplotlib linker.

# Control
window = Tk()

fig = Figure()
image = fig.add_subplot()
label = [Label(), Label(), Label(), Label()]
scale = [[Scale(), Scale()],
         [Scale(), Scale()],
         [Scale()],
         [Scale(), Scale()]]

# Data
distance = 0
distance_accuracy = IntVar()
delta_distance = 0

focal = 200
focal_part_1 = DoubleVar()
angle_part_2 = DoubleVar()

wavelength_1 = 0
wavelength_1_part_1 = DoubleVar()
wavelength_1_part_2 = DoubleVar()

wavelength_2 = 0
wavelength_2_part_1 = DoubleVar()
wavelength_2_part_2 = DoubleVar()

VALUE_RANGE = 20
ACCURACY = 500


# These are functions using in the APP.
def WindowCreate():
    window.title("迈克尔逊干涉仪实验仿真")
    window.geometry("1500x750")
    window.resizable(False, False)


def WindowInitialize():
    global label
    global distance_accuracy

    window.bind('<MouseWheel>', DistanceRefresh)
    window.bind('<ButtonRelease>', WavelengthAndFocalRefresh)

    # Scales control wavelength 1.
    scale[0][0] = Scale(window, length=1000, orient=HORIZONTAL, activebackground='red', from_=0, to=999,
                        digits=3, resolution=1, label='波长1(整数部分)', variable=wavelength_1_part_1)
    scale[0][0].place(x=0, y=0)
    scale[0][1] = Scale(window, length=200, orient=HORIZONTAL, activebackground='red', from_=0, to=0.99,
                        digits=2, resolution=0.01, label='波长1(小数部分)', variable=wavelength_1_part_2)
    scale[0][1].place(x=1100, y=0)

    # Scales control wavelength 2.
    scale[1][0] = Scale(window, length=1000, orient=HORIZONTAL, activebackground='red', from_=0, to=999,
                        digits=3, resolution=1, label='波长2(整数部分)', variable=wavelength_2_part_1)
    scale[1][0].place(x=0, y=80)
    scale[1][1] = Scale(window, length=200, orient=HORIZONTAL, activebackground='red', from_=0, to=0.99,
                        digits=2, resolution=0.01, label='波长2(小数部分)', variable=wavelength_2_part_2)
    scale[1][1].place(x=1100, y=80)

    # Scale controls accuracy of distance.
    scale[2][0] = Scale(window, length=200, orient=HORIZONTAL, activebackground='red', from_=1, to=5,
                        digits=1, resolution=1, label='距离(滚轮控制精度)', variable=distance_accuracy)
    scale[2][0].place(x=0, y=160)

    # Scales control angle.
    scale[3][0] = Scale(window, length=400, orient=HORIZONTAL, activebackground='red', from_=1, to=200,
                        digits=3, resolution=1, label='焦距(整数部分)/mm', variable=focal_part_1)
    scale[3][0].place(x=0, y=240)
    scale[3][0].set(100)
    scale[3][1] = Scale(window, length=200, orient=HORIZONTAL, activebackground='red', from_=0, to=0.9,
                        digits=1, resolution=0.1, label='焦距(小数部分)/mm', variable=angle_part_2)
    scale[3][1].place(x=0, y=320)

    # Label shows the distance.
    label[0] = Label(window, text="{:.2f}".format(wavelength_1) + 'nm', font=("", 20))
    label[0].place(x=1350, y=30)
    label[1] = Label(window, text="{:.2f}".format(wavelength_2) + 'nm', font=("", 20))
    label[1].place(x=1350, y=110)
    label[2] = Label(window, text="{:.5f}".format(distance) + 'mm', font=("", 20))
    label[2].place(x=250, y=190)
    label[3] = Label(window, text="{:.1f}".format(focal) + 'mm', font=("", 20))
    label[3].place(x=250, y=350)

    fig_frame = Frame(window, width=500, height=500)
    fig_frame.place(x=500, y=200)
    canvas = FigureCanvasTkAgg(fig, fig_frame)
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=YES)
    toolbar = NavigationToolbar2Tk(canvas, fig_frame, pack_toolbar=False)
    toolbar.update()
    toolbar.pack(side=RIGHT)


def WavelengthAndFocalRefresh(event):
    # Check the change of wavelength and focal length.
    global label
    global wavelength_1
    global wavelength_2
    global focal

    wavelength_1 = wavelength_1_part_1.get() + wavelength_1_part_2.get()
    wavelength_2 = wavelength_2_part_1.get() + wavelength_2_part_2.get()
    focal = focal_part_1.get() + angle_part_2.get()

    label[0].config(text="{:.2f}".format(wavelength_1) + 'nm')
    label[1].config(text="{:.2f}".format(wavelength_2) + 'nm')
    label[3].config(text="{:.1f}".format(focal) + 'mm')

    if 1000 <= event.x <= 1500 and 250 <= event.y <= 750:
        # In the area of the interference image.
        pass

    ImageRefresh()


def DistanceRefresh(event):
    # Check the change of distance.
    global distance
    global delta_distance

    delta_distance = 10 ** (-1 * distance_accuracy.get())

    if event.delta > 0:
        distance += delta_distance
    else:
        distance -= delta_distance
        if distance < 0:
            distance = 0

    distance = float('%.5f' % distance)
    label[2].config(text="{:.5f}".format(distance) + 'mm')

    ImageRefresh()


def ImageRefresh():
    wavelength_A = wavelength_1 * 10 ** -6
    wavelength_B = wavelength_2 * 10 ** -6
    if wavelength_A != 0:
        x_A, y_A = np.meshgrid(np.linspace(-VALUE_RANGE, VALUE_RANGE, ACCURACY),
                               np.linspace(-VALUE_RANGE, VALUE_RANGE, ACCURACY))
        r_A = np.sqrt(x_A ** 2 + y_A ** 2)
        A = np.cos(math.pi * (2 * distance * np.cos(np.arcsin(np.sin(np.arctan(r_A / focal))))) / wavelength_A) ** 2
    else:
        A = 0
    if wavelength_B != 0:
        x_B, y_B = np.meshgrid(np.linspace(-VALUE_RANGE, VALUE_RANGE, ACCURACY),
                               np.linspace(-VALUE_RANGE, VALUE_RANGE, ACCURACY))
        r_B = np.sqrt(x_B ** 2 + y_B ** 2)
        B = np.cos(math.pi * (2 * distance * np.cos(np.arcsin(np.sin(np.arctan(r_B / focal))))) / wavelength_B) ** 2
    else:
        B = 0

    if wavelength_A != 0 or wavelength_B != 0:
        image.imshow(A/2.0+B/2.0)
    fig.canvas.draw()
    image.cla()


WindowCreate()
WindowInitialize()
window.mainloop()
