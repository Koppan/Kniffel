#include "setup_window.h"
#include "ui_setup_window.h"

Setup_Window::Setup_Window(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::Setup_Window)
{
    ui->setupUi(this);
}

Setup_Window::~Setup_Window()
{
    delete ui;
}

