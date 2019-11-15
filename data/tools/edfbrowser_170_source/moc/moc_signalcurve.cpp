/****************************************************************************
** Meta object code from reading C++ file 'signalcurve.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.13.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../signalcurve.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'signalcurve.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.13.1. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_SignalCurve_t {
    QByteArrayData data[11];
    char stringdata0[158];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_SignalCurve_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_SignalCurve_t qt_meta_stringdata_SignalCurve = {
    {
QT_MOC_LITERAL(0, 0, 11), // "SignalCurve"
QT_MOC_LITERAL(1, 12, 20), // "extra_button_clicked"
QT_MOC_LITERAL(2, 33, 0), // ""
QT_MOC_LITERAL(3, 34, 16), // "dashBoardClicked"
QT_MOC_LITERAL(4, 51, 14), // "markerHasMoved"
QT_MOC_LITERAL(5, 66, 13), // "exec_sidemenu"
QT_MOC_LITERAL(6, 80, 12), // "print_to_pdf"
QT_MOC_LITERAL(7, 93, 14), // "print_to_image"
QT_MOC_LITERAL(8, 108, 16), // "print_to_printer"
QT_MOC_LITERAL(9, 125, 14), // "print_to_ascii"
QT_MOC_LITERAL(10, 140, 17) // "send_button_event"

    },
    "SignalCurve\0extra_button_clicked\0\0"
    "dashBoardClicked\0markerHasMoved\0"
    "exec_sidemenu\0print_to_pdf\0print_to_image\0"
    "print_to_printer\0print_to_ascii\0"
    "send_button_event"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_SignalCurve[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       9,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       3,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    0,   59,    2, 0x06 /* Public */,
       3,    0,   60,    2, 0x06 /* Public */,
       4,    0,   61,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
       5,    0,   62,    2, 0x08 /* Private */,
       6,    0,   63,    2, 0x08 /* Private */,
       7,    0,   64,    2, 0x08 /* Private */,
       8,    0,   65,    2, 0x08 /* Private */,
       9,    0,   66,    2, 0x08 /* Private */,
      10,    0,   67,    2, 0x08 /* Private */,

 // signals: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,

       0        // eod
};

void SignalCurve::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<SignalCurve *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->extra_button_clicked(); break;
        case 1: _t->dashBoardClicked(); break;
        case 2: _t->markerHasMoved(); break;
        case 3: _t->exec_sidemenu(); break;
        case 4: _t->print_to_pdf(); break;
        case 5: _t->print_to_image(); break;
        case 6: _t->print_to_printer(); break;
        case 7: _t->print_to_ascii(); break;
        case 8: _t->send_button_event(); break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (SignalCurve::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&SignalCurve::extra_button_clicked)) {
                *result = 0;
                return;
            }
        }
        {
            using _t = void (SignalCurve::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&SignalCurve::dashBoardClicked)) {
                *result = 1;
                return;
            }
        }
        {
            using _t = void (SignalCurve::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&SignalCurve::markerHasMoved)) {
                *result = 2;
                return;
            }
        }
    }
    Q_UNUSED(_a);
}

QT_INIT_METAOBJECT const QMetaObject SignalCurve::staticMetaObject = { {
    &QWidget::staticMetaObject,
    qt_meta_stringdata_SignalCurve.data,
    qt_meta_data_SignalCurve,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *SignalCurve::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *SignalCurve::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_SignalCurve.stringdata0))
        return static_cast<void*>(this);
    return QWidget::qt_metacast(_clname);
}

int SignalCurve::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QWidget::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 9)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 9;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 9)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 9;
    }
    return _id;
}

// SIGNAL 0
void SignalCurve::extra_button_clicked()
{
    QMetaObject::activate(this, &staticMetaObject, 0, nullptr);
}

// SIGNAL 1
void SignalCurve::dashBoardClicked()
{
    QMetaObject::activate(this, &staticMetaObject, 1, nullptr);
}

// SIGNAL 2
void SignalCurve::markerHasMoved()
{
    QMetaObject::activate(this, &staticMetaObject, 2, nullptr);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
