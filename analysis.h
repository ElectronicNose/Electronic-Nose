#ifndef ANALYSIS_H
#define ANALYSIS_H

#include <QMainWindow>

namespace Ui {
class Analysis;
}

class Analysis : public QMainWindow
{
    Q_OBJECT

public:
    explicit Analysis(QWidget *parent = 0);
    ~Analysis();

private:
    Ui::Analysis *ui;
};

#endif // ANALYSIS_H
