#include "measurement.h"
#include "ui_measurement.h"

Measurement::Measurement(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Measurement)
{
    ui->setupUi(this);
}

Measurement::~Measurement()
{
    delete ui;
}
