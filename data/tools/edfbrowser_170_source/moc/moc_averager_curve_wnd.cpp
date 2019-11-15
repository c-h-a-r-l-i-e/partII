/****************************************************************************
** Meta object code from reading C++ file 'averager_curve_wnd.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.13.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../averager_curve_wnd.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'averager_curve_wnd.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.13.1. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_UI_AverageCurveWindow_t {
    QByteArrayData data[6];
    char stringdata0[93];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_UI_AverageCurveWindow_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_UI_AverageCurveWindow_t qt_meta_stringdata_UI_AverageCurveWindow = {
    {
QT_MOC_LITERAL(0, 0, 21), // "UI_AverageCurveWindow"
QT_MOC_LITERAL(1, 22, 11), // "sliderMoved"
QT_MOC_LITERAL(2, 34, 0), // ""
QT_MOC_LITERAL(3, 35, 30), // "averager_curve_dialogDestroyed"
QT_MOC_LITERAL(4, 66, 10), // "export_edf"
QT_MOC_LITERAL(5, 77, 15) // "update_flywheel"

    },
    "UI_AverageCurveWindow\0sliderMoved\0\0"
    "averager_curve_dialogDestroyed\0"
    "export_edf\0update_flywheel"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_UI_AverageCurveWindow[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       4,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: name, argc, parameters, tag, flags
       1,    1,   34,    2, 0x08 /* Private */,
       3,    1,   37,    2, 0x08 /* Private */,
       4,    0,   40,    2, 0x08 /* Private */,
       5,    1,   41,    2, 0x08 /* Private */,

 // slots: parameters
    QMetaType::Void, QMetaType::Int,    2,
    QMetaType::Void, QMetaType::QObjectStar,    2,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int,    2,

       0        // eod
};

void UI_AverageCurveWindow::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<UI_AverageCurveWindow *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->sliderMoved((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 1: _t->averager_curve_dialogDestroyed((*reinterpret_cast< QObject*(*)>(_a[1]))); break;
        case 2: _t->export_edf(); break;
        case 3: _t->update_flywheel((*reinterpret_cast< int(*)>(_a[1]))); break;
        default: ;
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject UI_AverageCurveWindow::staticMetaObject = { {
    &QWidget::staticMetaObject,
    qt_meta_stringdata_UI_AverageCurveWindow.data,
    qt_meta_data_UI_AverageCurveWindow,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *UI_AverageCurveWindow::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *UI_AverageCurveWindow::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_UI_AverageCurveWindow.stringdata0))
        return static_cast<void*>(this);
    return QWidget::qt_metacast(_clname);
}

int UI_AverageCurveWindow::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QWidget::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 4)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 4;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 4)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 4;
    }
    return _id;
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
