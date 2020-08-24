#ifndef SETUP_WINDOW_H
#define SETUP_WINDOW_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class Setup_Window; }
QT_END_NAMESPACE

class Setup_Window : public QMainWindow
{
    Q_OBJECT

public:
    Setup_Window(QWidget *parent = nullptr);
    ~Setup_Window();

private:
    Ui::Setup_Window *ui;
};
#endif // SETUP_WINDOW_H
