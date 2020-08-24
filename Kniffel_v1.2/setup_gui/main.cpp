#include "setup_window.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    Setup_Window w;
    w.show();
    return a.exec();
}
