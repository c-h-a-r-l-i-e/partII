/****************************************************************************
** Meta object code from reading C++ file 'nk2edf.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.13.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../nk2edf.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'nk2edf.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.13.1. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_UI_NK2EDFwindow_t {
    QByteArrayData data[6];
    char stringdata0[61];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_UI_NK2EDFwindow_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_UI_NK2EDFwindow_t qt_meta_stringdata_UI_NK2EDFwindow = {
    {
QT_MOC_LITERAL(0, 0, 15), // "UI_NK2EDFwindow"
QT_MOC_LITERAL(1, 16, 16), // "SelectFileButton"
QT_MOC_LITERAL(2, 33, 0), // ""
QT_MOC_LITERAL(3, 34, 14), // "convert_nk2edf"
QT_MOC_LITERAL(4, 49, 5), // "FILE*"
QT_MOC_LITERAL(5, 55, 5) // "char*"

    },
    "UI_NK2EDFwindow\0SelectFileButton\0\0"
    "convert_nk2edf\0FILE*\0char*"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_UI_NK2EDFwindow[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       2,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: name, argc, parameters, tag, flags
       1,    0,   24,    2, 0x08 /* Private */,
       3,    8,   25,    2, 0x08 /* Private */,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Int, 0x80000000 | 4, 0x80000000 | 4, 0x80000000 | 4, QMetaType::Int, QMetaType::Int, QMetaType::Int, 0x80000000 | 5, QMetaType::Int,    2,    2,    2,    2,    2,    2,    2,    2,

       0        // eod
};

void UI_NK2EDFwindow::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<UI_NK2EDFwindow *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->SelectFileButton(); break;
        case 1: { int _r = _t->convert_nk2edf((*reinterpret_cast< FILE*(*)>(_a[1])),(*reinterpret_cast< FILE*(*)>(_a[2])),(*reinterpret_cast< FILE*(*)>(_a[3])),(*reinterpret_cast< int(*)>(_a[4])),(*reinterpret_cast< int(*)>(_a[5])),(*reinterpret_cast< int(*)>(_a[6])),(*reinterpret_cast< char*(*)>(_a[7])),(*reinterpret_cast< int(*)>(_a[8])));
            if (_a[0]) *reinterpret_cast< int*>(_a[0]) = std::move(_r); }  break;
        default: ;
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject UI_NK2EDFwindow::staticMetaObject = { {
    &QObject::staticMetaObject,
    qt_meta_stringdata_UI_NK2EDFwindow.data,
    qt_meta_data_UI_NK2EDFwindow,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *UI_NK2EDFwindow::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *UI_NK2EDFwindow::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_UI_NK2EDFwindow.stringdata0))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int UI_NK2EDFwindow::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 2)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 2;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 2)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 2;
    }
    return _id;
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
