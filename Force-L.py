import sys

import matplotlib
import numpy as np
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QDoubleSpinBox, QWidget, QPushButton, QCheckBox
from matplotlib import animation, pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtCore import Qt
from scipy.integrate import ode

matplotlib.use('Qt5Agg')


class interface(QMainWindow):
    def __init__(self):
        super().__init__()
        global q, v, B, E, xInp, yInp, zInp, velX, velY, velZ, En
        q = 1
        B = 1
        E = 1
        v = 1
        xInp = 0
        yInp = 0
        zInp = 0
        velX = 1
        velY = 1
        velZ = 1
        En = 0

        self.setGeometry(100, 100, 700, 500)
        self.setWindowTitle = 'Движение частицы'

        self.layout = QVBoxLayout()

        self.chkBx = QCheckBox('Bx')
        self.chkBx.toggled.connect(self.btnch)
        self.chkBy = QCheckBox('By')
        self.chkBy.toggled.connect(self.btnch)
        self.chkBz = QCheckBox('Bz')
        self.chkBz.toggled.connect(self.btnch)


        self.chkEx = QCheckBox('Ex')
        self.chkEx.toggled.connect(self.btnch)
        self.chkEy = QCheckBox('Ey')
        self.chkEy.toggled.connect(self.btnch)
        self.chkEz = QCheckBox('Ez')
        self.chkEz.toggled.connect(self.btnch)

        self.widget1 = QDoubleSpinBox()
        self.widget2 = QDoubleSpinBox()
        self.widget3 = QDoubleSpinBox()

        self.widget1.setValue(1)
        self.widget2.setValue(1)
        self.widget3.setValue(1)

        self.widgetInputX = QDoubleSpinBox()
        self.widgetInputY = QDoubleSpinBox()
        self.widgetInputZ = QDoubleSpinBox()

        self.widgetVelX = QDoubleSpinBox()
        self.widgetVelY = QDoubleSpinBox()
        self.widgetVelZ = QDoubleSpinBox()

        self.widgetVelX.setValue(1)
        self.widgetVelY.setValue(1)
        self.widgetVelZ.setValue(1)

        self.btn1 = QPushButton('Построение графика')
        self.btn1.pressed.connect(self.btn_cl1)
        self.layout.addWidget(self.widget1)
        self.layout.addWidget(self.widget2)
        self.layout.addWidget(self.widget3)

        self.layout.addWidget(self.widgetInputX)
        self.layout.addWidget(self.widgetInputY)
        self.layout.addWidget(self.widgetInputZ)

        self.layout.addWidget(self.widgetVelX)
        self.layout.addWidget(self.widgetVelY)
        self.layout.addWidget(self.widgetVelZ)

        self.layout.addWidget(self.chkBx)
        self.layout.addWidget(self.chkBy)
        self.layout.addWidget(self.chkBz)

        self.layout.addWidget(self.chkEx)
        self.layout.addWidget(self.chkEy)
        self.layout.addWidget(self.chkEz)

        self.widgetInputX.setRange(-100, 100)
        self.widgetInputY.setRange(-100, 100)
        self.widgetInputZ.setRange(-100, 100)

        self.widgetVelX.setRange(-100, 100)
        self.widgetVelY.setRange(-100, 100)
        self.widgetVelZ.setRange(-100, 100)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.widget1.setRange(-100, 100)
        self.widget2.setRange(-100, 100)
        self.widget3.setRange(-100, 100)
        self.widget1.setPrefix("q = ")
        self.widget1.setSingleStep(0.1)
        self.widget1.valueChanged.connect(self.gl1)

        self.layout.addWidget(self.btn1)
        self.widget2.setPrefix("B = ")
        self.widget2.setSingleStep(0.1)
        self.widget2.valueChanged.connect(self.gl2)
        self.widget3.setPrefix("E = ")
        self.widget3.setSingleStep(0.1)
        self.widget3.valueChanged.connect(self.gl3)

        # Ввод Начальных координат точки
        self.widgetInputX.setPrefix("x0 = ")
        self.widgetInputX.setSingleStep(0.1)
        self.widgetInputX.valueChanged.connect(self.glSetX)

        self.widgetInputY.setPrefix("y0 = ")
        self.widgetInputY.setSingleStep(0.1)
        self.widgetInputY.valueChanged.connect(self.glSetY)

        self.widgetInputZ.setPrefix("z0 = ")
        self.widgetInputZ.setSingleStep(0.1)
        self.widgetInputZ.valueChanged.connect(self.glSetZ)

        # Ввод начальных скоростей точки
        self.widgetVelX.setPrefix("vx0 = ")
        self.widgetVelX.setSingleStep(0.1)
        self.widgetVelX.valueChanged.connect(self.glSetVelX)

        self.widgetVelY.setPrefix("vy0 = ")
        self.widgetVelY.setSingleStep(0.1)
        self.widgetVelY.valueChanged.connect(self.glSetVelY)

        self.widgetVelZ.setPrefix("vz0 = ")
        self.widgetVelZ.setSingleStep(0.1)
        self.widgetVelZ.valueChanged.connect(self.glSetVelZ)



        self.setCentralWidget(self.widget)
        self.show()

    def btn_cl1(self):
        self.chile_Win = Main_win()
        self.chile_Win.show()


    def gl1(self, i):
        global q
        q = i

    def gl2(self, i):
        global B
        B = i

    def gl3(self, i):
        global E
        E = i

    def gl4(self, i):
        global v
        v = i
    
    def glSetX(self, i):
        global xInp
        xInp = i

    def glSetY(self, i):
        global yInp
        yInp = i

    def glSetZ(self, i):
        global zInp
        zInp = i
    
    def glSetVelX(self, i):
        global velX
        velX = i

    def glSetVelY(self, i):
        global velY
        velY = i

    def glSetVelZ(self, i):
        global velZ
        velZ = i

    def btnch(self):
        global Bn, En
        if self.chkBx.isChecked():
            Bn = 1
        if self.chkBy.isChecked():
            Bn = 2
        if self.chkBz.isChecked():
            Bn = 3
        if self.chkEx.isChecked():
            En = 1
        if self.chkEy.isChecked():
            En = 2
        if self.chkEz.isChecked():
            En = 3

class Main_win(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left = 650
        self.top = 140
        self.title = 'Движение частицы'
        self.width = 640
        self.height = 480
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.m = PlotCanvas(self, width=4, height=3)
        self.m.move(0, 0)

        self.show()


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d')

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.updateGeometry(self)
        self.plot(fig)

    def plot(self, fig):
        global Bn
        def newton(t, Y, q, m, B, E):
            global En
            x, y, z = Y[0], Y[1], Y[2]
            u, v, w = Y[3], Y[4], Y[5]

            alpha = q / m  # ERROR: ВОЗМОЖНО ДЕЛЕНИЕ НА НОЛЬ. ПРОГРАММА ПАДАЕТ, ЕСЛИ v = 0
            if q < 0:
                En = En * -1
            if En == 1 or En == -1:
                if Bn == 1:
                    return np.array([u, v, w, E * En, alpha * B * w + E * 0, -alpha * B * v + E * 0])  # если В вдоль X
                elif Bn == 2:
                    return np.array([u, v, w, -alpha * B * w + E * En, E * 0, alpha * B * u + E * 0])  # если вдоль У
                elif Bn == 3:
                    return np.array([u, v, w, alpha * B * v + E*En, -alpha * B * u + E*0, E*0])# если В вдоль Z
            if En == 2 or En == -2:
                if Bn == 1:
                    return np.array([u, v, w, E * 0, alpha * B * w + E * En, -alpha * B * v + E * 0])  # если В вдоль X
                elif Bn == 2:
                    return np.array([u, v, w, -alpha * B * w + E * 0, E * En, alpha * B * u + E * 0])  # если вдоль У
                elif Bn == 3:
                    return np.array([u, v, w, alpha * B * v + E*0, -alpha * B * u + E*En, E*0])# если В вдоль Z
            if En == 3 or En == -3:
                if Bn == 1:
                    return np.array([u, v, w, E * 0, alpha * B * w + E * 0, -alpha * B * v + E * En])  # если В вдоль X
                elif Bn == 2:
                    return np.array([u, v, w, -alpha * B * w + E * 0, E * 0, alpha * B * u + E * En])  # если вдоль У
                elif Bn == 3:
                    return np.array([u, v, w, alpha * B * v + E*0, -alpha * B * u + E*0, E*En])# если В вдоль Z
            if En == 0:
                if Bn == 1:
                    return np.array([u, v, w, E * 0, alpha * B * w + E * 0, -alpha * B * v + E * 0])  # если В вдоль X
                elif Bn == 2:
                    return np.array([u, v, w, -alpha * B * w + E * 0, E * 0, alpha * B * u + E * 0])  # если вдоль У
                elif Bn == 3:
                    return np.array([u, v, w, alpha * B * v + E*0, -alpha * B * u + E*0, E*0])# если В вдоль Z



        r = ode(newton).set_integrator('dopri5')

        t0 = 0
        x0 = np.array([xInp, yInp, zInp])
        v0 = np.array([velX, velY, velZ])
        initial_conditions = np.concatenate((x0, v0))

        r.set_initial_value(initial_conditions, t0).set_f_params(q, v, B, E)

        positions = []
        t1 = 50
        dt = 0.05
        while r.successful() and r.t < t1:
            r.integrate(r.t + dt)
            positions.append(r.y[:3])

        positions = np.array(positions)

        B1 = np.array([x0[0], x0[1], x0[2]])
        E1 = np.array([x0[0], x0[1], x0[2]])
        if En == 1 and E < 0:
            E2 = np.array([-60, 0, 0])
        elif En == 1 and E >= 0:
            E2 = np.array([60, 0, 0])
        elif En==2 and E < 0:
            E2 = np.array([0, -60, 0])
        elif En==2 and E >= 0:
            E2 = np.array([0, 60, 0])
        elif En==3 and E < 0:
            E2 = np.array([0, 0, -60])
        elif En==3 and E >= 0:
            E2 = np.array([0, 0, 60])
        else:
            E2 = np.array([0, 0, 0])

        if Bn == 1 and B < 0:
            B2 = np.array([-60, 0, 0])
        elif Bn == 1 and B >= 0:
            B2 = np.array([60, 0, 0])
        elif Bn==2 and B < 0:
            B2 = np.array([0, -60, 0])
        elif Bn==2 and B >= 0:
            B2 = np.array([0, 60, 0])
        elif Bn==3 and B < 0:
            B2 = np.array([0, 0, -60])
        elif Bn==3 and B >= 0:
            B2 = np.array([0, 0, 60])
        else:
            B2 = np.array([0, 0, 0])
        B_axis = np.vstack((B1, B1 + B2))
        E_axis = np.vstack((E1, E1 + E2))
        FRAMES = 50

        def init():
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('y')
            self.ax.set_zlabel('z')

        def animate(i):
            current_index = int(positions.shape[0] / FRAMES * i)
            self.ax.cla()
            self.ax.plot3D(positions[:current_index, 0],
                      positions[:current_index, 1],
                      positions[:current_index, 2])
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('y')
            self.ax.set_zlabel('z')
            self.ax.set_title('Динамичское движение частицы')
            if En == Bn and ((E > 0 and B > 0) or (E < 0 and B < 0)):
                self.ax.plot3D(B_axis[:, 0], B_axis[:, 1], B_axis[:, 2])
                self.ax.text3D((E1 + E2)[0], (E1 + E2)[1], (E1 + E2)[2], "E and B field")
            else:
                self.ax.plot3D(B_axis[:, 0], B_axis[:, 1], B_axis[:, 2])
                self.ax.plot3D(E_axis[:, 0], E_axis[:, 1], E_axis[:, 2])
                self.ax.text3D((E1 + E2)[0], (E1 + E2)[1], (E1 + E2)[2], "E field")
                self.ax.text3D((B1 + B2)[0], (B1 + B2)[1], (B1 + B2)[2], "B field")

        self.anim = animation.FuncAnimation(fig, animate, init_func=init,
                                       frames=FRAMES, interval=100, repeat=0)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = interface()
    sys.exit(app.exec())
