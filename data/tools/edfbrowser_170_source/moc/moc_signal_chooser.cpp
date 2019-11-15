/****************************************************************************
** Meta object code from reading C++ file 'signal_chooser.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.13.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../signal_chooser.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'signal_chooser.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.13.1. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_UI_SignalChooser_t {
    QByteArrayData data[8];
    char stringdata0[95];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_UI_SignalChooser_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_UI_SignalChooser_t qt_meta_stringdata_UI_SignalChooser = {
    {
QT_MOC_LITERAL(0, 0, 16), // "UI_SignalChooser"
QT_MOC_LITERAL(1, 17, 13), // "call_sidemenu"
QT_MOC_LITERAL(2, 31, 0), // ""
QT_MOC_LITERAL(3, 32, 16), // "QListWidgetItem*"
QT_MOC_LITERAL(4, 49, 8), // "signalUp"
QT_MOC_LITERAL(5, 58, 10), // "signalDown"
QT_MOC_LITERAL(6, 69, 12), // "signalDelete"
QT_MOC_LITERAL(7, 82, 12) // "signalInvert"

    },
    "UI_SignalChooser\0call_sidemenu\0\0"
    "QListWidgetItem*\0signalUp\0signalDown\0"
    "signalDelete\0signalInvert"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_UI_SignalChooser[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       5,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: name, argc, parameters, tag, flags
       1,    1,   39,    2, 0x08 /* Private */,
       4,    0,   42,    2, 0x08 /* Private */,
       5,    0,   43,    2, 0x08 /* Private */,
       6,    0,   44,    2, 0x08 /* Private */,
       7,    0,   45,    2, 0x08 /* Private */,

 // slots: parameters
    QMetaType::Void, 0x80000000 | 3,    2,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,

       0        // eod
};

void UI_SignalChooser::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<UI_SignalChooser *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->call_sidemenu((*reinterpret_cast< QListWidgetItem*(*)>(_a[1]))); break;
        case 1: _t->signalUp(); break;
        case 2: _t->signalDown(); break;
        case 3: _t->signalDelete(); break;
        case 4: _t->signalInvert(); break;
        default: ;
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject UI_SignalChooser::staticMetaObject = { {
    &QObject::staticMetaObject,
    qt_meta_stringdata_UI_SignalChooser.data,
    qt_meta_data_UI_SignalChooser,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *UI_SignalChooser::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *UI_SignalChooser::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_UI_SignalChooser.stringdata0))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int UI_SignalChooser::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 5)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 5;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 5)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 5;
    }
    return _id;
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
