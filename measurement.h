#ifndef MEASUREMENT_H
#define MEASUREMENT_H

#include <QWidget>

namespace Ui {
class Measurement;
}

class Measurement : public QWidget
{
    Q_OBJECT

public:
    explicit Measurement(QWidget *parent = 0);
    ~Measurement();

private:
    Ui::Measurement *ui;
};

#endif // MEASUREMENT_H
