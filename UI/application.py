import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from dynamics.pendulum import *
from dynamics.solver import *

qss = """
        QMenuBar {
            background-color: #616161;
        }
        QMenuBar::item {
            color:  #FAFAFA;
            background: #616161;
        }
        QMenuBar::item:selected{
            background: #757575;
        }

        QMenu {
            color:  #FAFAFA;
            background-color: #424242;
        }
        QMenu::item{
            padding: 3px 20px 3px 20px;
            width: 150px;
        }
        QMenu::item:selected {
            background-color: #616161;
            border-radius: 5px;
        }

        QMainWindow {
            background-color: #212121;
            margin: 0px;
            padding: 0px;
        }
    """

class App(QMainWindow):
    """
    This program is the internal development tool that is based on PyQt5.
    """

    def __init__(self):
        "Initialise the application."
        super().__init__()        
        # Define the title of the application
        self.title = 'Dynamics  -  Nonlinear Dynamic Simulation'
        
        # Run the UI initialisation 
        self.initUI()

    def initUI(self):
        "UI initialisation method."
        # Set the application title
        self.setWindowTitle(self.title)

        # Set Layout
        self.layout()

        # Set Menu Bar
        self.menu()
        
        # Resize the window size
        self.resize(1280,720)
        # Center the window
        self.center()

        # Simulation state
        self.state = 0  # 0: Resetted; 1: Paused; 2: Running

        # Show the window
        self.show()

    def center(self):
        "Method to centre the window"
        # Get the geometry of the main window
        qr = self.frameGeometry()
        # Get the centre point (cp) of the screen resolution of the monitor
        cp = QDesktopWidget().availableGeometry().center()
        # Set the centre point of the frame as the centre point of the monitor
        qr.moveCenter(cp)
        # Move the window accordingly
        self.move(qr.topLeft())

    def menu(self):
        "Method to create menu of the application."
        # Initialise menu bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        editMenu = menubar.addMenu('Edit')
        viewMenu = menubar.addMenu('View')

        # Add actions to menu bar
        fileMenu.addAction(self.menu_run())
        fileMenu.addAction(self.menu_import())
        fileMenu.addSeparator()
        fileMenu.addAction(self.menu_exit())
        editMenu.addAction(QAction('Copy', self))
        viewMenu.addAction(QAction('Toggle Full Screen', self))
        
    def menu_run(self):
        "Method to create new action on the menu."
        # Initialise and setup the new action
        newAct = QAction('Run', self)
        newAct.setShortcut('Ctrl+A')
        newAct.triggered.connect(self.slot_simulation)

        return newAct

    def menu_import(self):
        "Method to create import action on the menu."
        # Initialise and setup the import action
        importAct = QAction('Import...', self)
        importAct.setShortcut('Ctrl+I')
        importAct.triggered.connect(self.slot_import_data)

        return importAct 

    def menu_exit(self):
        "Method to create exit action on the menu."
        # Initialise and setup the exit action
        exitAct = QAction('Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(qApp.quit)

        return exitAct

    def layout(self):
        "Method to define layout of the application."
        # Create centre widget
        wid_centre = QWidget(self)
        self.setCentralWidget(wid_centre)

        # Initialise the horizontal box layout
        hbox = QHBoxLayout()
        hbox.addWidget(self.sidebar())
        # hbox.addStretch(1)
        hbox.addWidget(self.simulation())
        # hbox.addStretch(1)
        hbox.addWidget(self.input_container())
        # hbox.addStretch(1)
        hbox.setContentsMargins(0,0,0,0)
        
        wid_centre.setLayout(hbox)
        # wid_centre.setStyleSheet(
        #     """
        #         .QWidget {
        #             border-width: 1px;
        #             border-color: #339;
        #             border-style: solid;
        #         }
        #     """
        # )

    def simulation(self):
        "Method to define simulation plot of the application."
        # Create simulation widget
        simulation = QWidget()
        self.simulation_layout = QGridLayout()

        # Create Plot Widget
        self.simulation_plot = pg.PlotWidget(useOpenGL=True)
        self.simulation_plot.plot([], [], pen="w", symbol='o')

        # Plot settings
        self.simulation_plot.setBackground("#212121")
        self.simulation_plot.setAspectLocked(ratio=1)
        
        # Update results Layout
        self.simulation_layout.addWidget(self.simulation_plot)
        self.simulation_layout.setContentsMargins(40,30,40,30)
        simulation.setLayout(self.simulation_layout)

        return simulation

    def sidebar(self):
        "Method to define sidebar of the application."
        # Create sidebar widget
        sidebar = QWidget()
        
        # Initialise Vertical Box Layout
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel('A'))
        vbox.addWidget(QLabel('B'))
        vbox.addWidget(QLabel('C'))
        vbox.addWidget(QLabel('D'))
        vbox.addStretch(1)
        vbox.setAlignment(Qt.AlignCenter)

        # Update sidebar
        sidebar.setLayout(vbox)

        # Styling sidebar
        sidebar.setFixedWidth(50)
        sidebar.setStyleSheet(
            """
                .QWidget {
                    background-color: #424242;
                    margin: 0px;
                }
                .QLabel {
                    color: white;
                }
            """
        )

        return sidebar

    def input_container(self):
        "Method to define input container of the application."
        # Create input widget
        wid_input = QWidget()

        # Initialise Form Layout for input parameters
        wid_param = QGroupBox("Parameters")
        param_form = QFormLayout()
        self.disp_init_spin = QDoubleSpinBox()
        self.disp_init_spin.setDecimals(3)
        self.velo_init_spin = QDoubleSpinBox()
        self.velo_init_spin.setDecimals(3)
        self.mass_spin = QDoubleSpinBox()
        self.mass_spin.setDecimals(3)
        self.mass_spin.setValue(1)
        self.drag_coeff_spin = QDoubleSpinBox()
        self.drag_coeff_spin.setDecimals(3)
        self.drag_coeff_spin.setValue(0)
        self.length_spin = QDoubleSpinBox()
        self.length_spin.setDecimals(3)
        self.length_spin.setValue(1)
        self.time_step_spin = QDoubleSpinBox()
        self.time_step_spin.setDecimals(6)
        self.time_step_spin.setValue(1e-3)
        self.solver = QComboBox()
        self.solver.addItems(["Euler", "Modified Euler", "RK2", "RK4"])
        param_form.addRow(QLabel("Initial Displacement (rad)"), self.disp_init_spin)
        param_form.addRow(QLabel("Initial Velocity (rad/s)"), self.velo_init_spin)
        param_form.addRow(QLabel("Mass (kg)"), self.mass_spin)
        param_form.addRow(QLabel("coefficient of Drag"), self.drag_coeff_spin)
        param_form.addRow(QLabel("Length (m)"), self.length_spin)
        param_form.addRow(QLabel("Time Step (s)"), self.time_step_spin)
        param_form.addRow(QLabel("Numerical Solver"), self.solver)
        # Update wid_param
        wid_param.setLayout(param_form)

        # Create Form group box
        plot_gbox = QGroupBox("Plot")
        plot_layout = QVBoxLayout()
        # plot_layout.setAlignment(Qt.AlignHCenter)
        self.Time_setting = QCheckBox('Show Time', self)
        self.Time_setting.setCheckState(2)
        self.Acc_setting = QCheckBox('Show Acceleration', self)
        self.Acc_setting.setCheckState(2)
        self.Velo_setting = QCheckBox('Show Velocity', self)
        self.Velo_setting.setCheckState(2)
        self.Disp_setting = QCheckBox('Show Displacement', self)
        self.Disp_setting.setCheckState(2)
        self.Energy_setting = QCheckBox('Show Energy', self)
        self.Energy_setting.setCheckState(2)
        self.disp_indi_setting = QCheckBox('Displacement Indicator', self)
        self.disp_indi_setting.setCheckState(2)
        self.velo_indi_setting = QCheckBox('Velocity Indicator', self)
        self.velo_indi_setting.setCheckState(2)
        self.support_setting = QCheckBox('Support', self)
        self.support_setting.setCheckState(2)
        self.grid_setting = QCheckBox('Grid On', self)
        self.grid_setting.setCheckState(0)
        plot_layout.addWidget(self.Time_setting)
        plot_layout.addWidget(self.Acc_setting)
        plot_layout.addWidget(self.Velo_setting)
        plot_layout.addWidget(self.Disp_setting)
        plot_layout.addWidget(self.Energy_setting)
        plot_layout.addWidget(self.disp_indi_setting)
        plot_layout.addWidget(self.velo_indi_setting)
        plot_layout.addWidget(self.support_setting)
        plot_layout.addWidget(self.grid_setting)
        plot_gbox.setLayout(plot_layout)
        plot_gbox.setFixedHeight(300)

        # Setup buttoms
        runButton = QPushButton("Run / Pause")
        runButton.clicked.connect(self.slot_run_pause)
        resetButton = QPushButton("Reset")

        # Initialise the vertical box layout
        vbox = QVBoxLayout()
        vbox.addWidget(wid_param)
        vbox.addWidget(plot_gbox)
        vbox.addStretch(1)
        vbox.addWidget(runButton)
        vbox.addWidget(resetButton)

        # Update input widget
        wid_input.setLayout(vbox)
        wid_input.setFixedWidth(350)
        wid_input.setFixedHeight(650)
        wid_input.setStyleSheet(
            """
                .QWidget {
                    margin: 0px;
                }
                .QLabel {
                    color: white;
                }
                .QGroupBox {
                    color: white;
                }
                .QCheckBox {
                    color: white;
                    margin-left: 40px;
                }
            """
        )

        return wid_input

    def slot_run_pause(self):
        "Methdo (slot) to run and pause the simulation."
        # When status is 0, i.e. initialise simulation
        if self.state == 0:
            # Define problem
            problem = PendulumProblem()
            problem.initialise(
                initial_displacement=[self.disp_init_spin.value()],
                initial_velocity=[self.velo_init_spin.value()],
                time_step=self.time_step_spin.value()
                )
            problem.setup(
                mass=self.mass_spin.value(),
                drag_coeff=self.drag_coeff_spin.value(),
                length=self.length_spin.value()
                )
        
            # Select solver
            if self.solver.currentText() == "Euler":
                solver = Euler()
            elif self.solver.currentText() == "Modified Euler":
                solver = ImprovedEuler()
            elif self.solver.currentText() == "RK2":
                solver = RungeKuttaTwo()
            elif self.solver.currentText() == "RK4":
                solver = RungeKuttaFour()

            # Define Simulation
            self.simulation = PendulumModel(problem, solver)
            # Set up timer
            self.timer = QTimer()
            # timer.setSingleShot(False)
            self.timer.timeout.connect(self.slot_simulation)
            self.timer.start(0)
            self.update()

    def slot_simulation(self):
        "Method (slot) to simulation."
        # Iterate the simulation
        self.simulation.iterate()
        # Extract displacement, velocity and time
        displacement = self.simulation.displacement
        velocity = self.simulation.velocity
        time = self.simulation.time
        length = self.length_spin.value()

        # Calculate the position
        position_x = self.length_spin.value() * np.sin(displacement)
        position_y = -1 * self.length_spin.value() * np.cos(displacement)

        # Update plot
        self.simulation_plot.clear()
        self.simulation_plot.plot(
            [0,position_x], [0,position_y], pen="w", symbol='o')
        
        # Support plot
        if self.support_setting.checkState():
            self.simulation_plot.plot(
                [0, 0], [0, -length], pen=pg.mkPen('w', width=0.5, style=Qt.DashLine)
            )
        
        # Plot Text
        

        # Plot settings
        self.simulation_plot.setBackground("#212121")
        self.simulation_plot.setRange(xRange=(-length,length), yRange=(-length,length))
        # self.simulation_plot.setAspectLocked(ratio=1)

    
    def slot_import_data(self):
        "Method (slot) to import selected data file."
        # Set up options for 
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileName(self,"Import...", "", \
            "All Files (*);;Python Files (*.py)", options=options)
        if files:
            # Statusbar indicates the data is successfully imported
            self.statusBar().showMessage("File is successfully imported.")
            self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qss) 
    ex = App()
    sys.exit(app.exec_())