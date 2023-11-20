from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics


def FixString(control):
    tmp = control.text()
    strLen = len(tmp)
    metrics = QFontMetrics(control.font())
    maxWidth = control.maximumWidth()
    control.setToolTip(tmp)
    if metrics.width(tmp) <= maxWidth:
        return
    prev = 0
    strs = []
    for i in range(0, strLen):
        if metrics.width(tmp[prev:i]) >= maxWidth:
            strs.append(tmp[prev:i - 1])
            prev = i - 1
    strs.append(tmp[prev:])
    result = ""
    for i in strs:
        result = result + i + "\r\n"
    control.setText(result.rstrip("\r\n"))
