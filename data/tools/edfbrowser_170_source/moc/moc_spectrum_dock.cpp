/****************************************************************************
** Meta object code from reading C++ file 'spectrum_dock.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.13.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../spectrum_dock.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'spectrum_dock.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.13.1. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_UI_SpectrumDockWindow_t {
    QByteArrayData data[14];
    char stringdata0[222];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_UI_SpectrumDockWindow_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_UI_SpectrumDockWindow_t qt_meta_stringdata_UI_SpectrumDockWindow = {
    {
QT_MOC_LITERAL(0, 0, 21), // "UI_SpectrumDockWindow"
QT_MOC_LITERAL(1, 22, 12), // "update_curve"
QT_MOC_LITERAL(2, 35, 0), // ""
QT_MOC_LITERAL(3, 36, 11), // "sliderMoved"
QT_MOC_LITERAL(4, 48, 17), // "sqrtButtonClicked"
QT_MOC_LITERAL(5, 66, 17), // "vlogButtonClicked"
QT_MOC_LITERAL(6, 84, 21), // "colorBarButtonClicked"
QT_MOC_LITERAL(7, 106, 12), // "print_to_txt"
QT_MOC_LITERAL(8, 119, 12), // "setdashboard"
QT_MOC_LITERAL(9, 132, 15), // "update_flywheel"
QT_MOC_LITERAL(10, 148, 19), // "dftsz_value_changed"
QT_MOC_LITERAL(11, 168, 17), // "windowBox_changed"
QT_MOC_LITERAL(12, 186, 19), // "overlap_box_changed"
QT_MOC_LITERAL(13, 206, 15) // "open_close_dock"

    },
    "UI_SpectrumDockWindow\0update_curve\0\0"
    "sliderMoved\0sqrtButtonClicked\0"
    "vlogButtonClicked\0colorBarButtonClicked\0"
    "print_to_txt\0setdashboard\0update_flywheel\0"
    "dftsz_value_changed\0windowBox_changed\0"
    "overlap_box_changed\0open_close_dock"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_UI_SpectrumDockWindow[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
      12,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: name, argc, parameters, tag, flags
       1,    0,   74,    2, 0x08 /* Private */,
       3,    1,   75,    2, 0x08 /* Private */,
       4,    1,   78,    2, 0x08 /* Private */,
       5,    1,   81,    2, 0x08 /* Private */,
       6,    1,   84,    2, 0x08 /* Private */,
       7,    0,   87,    2, 0x08 /* Private */,
       8,    0,   88,    2, 0x08 /* Private */,
       9,    1,   89,    2, 0x08 /* Private */,
      10,    1,   92,    2, 0x08 /* Private */,
      11,    1,   95,    2, 0x08 /* Private */,
      12,    1,   98,    2, 0x08 /* Private */,
      13,    1,  101,    2, 0x08 /* Private */,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int,    2,
    QMetaType::Void, QMetaType::Bool,    2,
    QMetaType::Void, QMetaType::Bool,    2,
    QMetaType::Void, QMetaType::Bool,    2,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int,    2,
    QMetaType::Void, QMetaType::Int,    2,
    QMetaType::Void, QMetaType::Int,    2,
    QMetaType::Void, QMetaType::Int,    2,
    QMetaType::Void, QMetaType::Bool,    2,

       0        // eod
};

void UI_SpectrumDockWindow::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<UI_SpectrumDockWindow *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->update_curve(); break;
        case 1: _t->sliderMoved((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 2: _t->sqrtButtonClicked((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 3: _t->vlogButtonClicked((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 4: _t->colorBarButtonClicked((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 5: _t->print_to_txt(); break;
        case 6: _t->setdashboard(); break;
        case 7: _t->update_flywheel((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 8: _t->dftsz_value_changed((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 9: _t->windowBox_changed((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 10: _t->overlap_box_changed((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 11: _t->open_close_dock((*reinterpret_cast< bool(*)>(_a[1]))); break;
        default: ;
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject UI_SpectrumDockWindow::staticMetaObject = { {
    &QObject::staticMetaObject,
    qt_meta_stringdata_UI_SpectrumDockWindow.data,
    qt_meta_data_UI_SpectrumDockWindow,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *UI_SpectrumDockWindow::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *UI_SpectrumDockWindow::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_UI_SpectrumDockWindow.stringdata0))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int UI_SpectrumDockWindow::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 12)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 12;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 12)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 12;
    }
    return _id;
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
