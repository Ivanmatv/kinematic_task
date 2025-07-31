import socket
import struct
from dataclasses import dataclass

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, 
    QVBoxLayout, QWidget, QHeaderView
)
from kinematic import forward_kinematics


@dataclass
class RobotData:
    timestamp: int
    theta: list[float]  # 6 углов в градусах


class MainWindow(QMainWindow):
    def __init__(self, results):
        super().__init__()
        self.setWindowTitle("Robot Kinematics Results")
        self.setGeometry(100, 100, 800, 400)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setRowCount(len(results))
        self.table.setHorizontalHeaderLabels([
            "Timestamp", "X Position", "Y Position", "Z Position"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for row, (ts, x, y, z) in enumerate(results):
            self.table.setItem(row, 0, QTableWidgetItem(str(ts)))
            self.table.setItem(row, 1, QTableWidgetItem(f"{x:.6f}"))
            self.table.setItem(row, 2, QTableWidgetItem(f"{y:.6f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{z:.6f}"))

        layout.addWidget(self.table)
        self.setCentralWidget(central_widget)


def main():
    SERVER_HOST = "localhost"
    SERVER_PORT = 8088

    # Создание UDP-сокета
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(b"get", (SERVER_HOST, SERVER_PORT))

        packets = []
        for _ in range(5):
            data, _ = sock.recvfrom(56)
            unpacked = struct.unpack('<Q6d', data)
            packets.append(RobotData(unpacked[0], list(unpacked[1:7])))

    # Расчет позиций
    results = []
    for packet in packets:
        position = forward_kinematics(packet.theta)
        results.append((packet.timestamp, *position))

    # Запуск GUI
    app = QApplication([])
    window = MainWindow(results)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
