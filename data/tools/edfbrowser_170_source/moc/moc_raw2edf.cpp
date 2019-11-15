/****************************************************************************
** Meta object code from reading C++ file 'raw2edf.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.13.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../raw2edf.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'raw2edf.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.13.1. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_UI_RAW2EDFapp_t {
    QByteArrayData data[8];
    char stringdata0[131];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_UI_RAW2EDFapp_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_UI_RAW2EDFapp_t qt_meta_stringdata_UI_RAW2EDFapp = {
    {
QT_MOC_LITERAL(0, 0, 13), // "UI_RAW2EDFapp"
QT_MOC_LITERAL(1, 14, 15), // "gobuttonpressed"
QT_MOC_LITERAL(2, 30, 0), // ""
QT_MOC_LITERAL(3, 31, 17), // "savebuttonpressed"
QT_MOC_LITERAL(4, 49, 17), // "loadbuttonpressed"
QT_MOC_LITERAL(5, 67, 27), // "PhysicalDimensionLineEdited"
QT_MOC_LITERAL(6, 95, 17), // "sampleTypeChanged"
QT_MOC_LITERAL(7, 113, 17) // "helpbuttonpressed"

    },
    "UI_RAW2EDFapp\0gobuttonpressed\0\0"
    "savebuttonpressed\0loadbuttonpressed\0"
    "PhysicalDimensionLineEdited\0"
    "sampleTypeChanged\0helpbuttonpressed"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_UI_RAW2EDFapp[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       6,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: name, argc, parameters, tag, flags
       1,    0,   44,    2, 0x08 /* Private */,
       3,    0,   45,    2, 0x08 /* Private */,
       4,    0,   46,    2, 0x08 /* Private */,
       5,    1,   47,    2, 0x08 /* Private */,
       6,    1,   50,    2, 0x08 /* Private */,
       7,    0,   53,    2, 0x08 /* Private */,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::QString,    2,
    QMetaType::Void, QMetaType::Int,    2,
    QMetaType::Void,

       0        // eod
};

void UI_RAW2EDFapp::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<UI_RAW2EDFapp *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->gobuttonpressed(); break;
        case 1: _t->savebuttonpressed(); break;
        case 2: _t->loadbuttonpressed(); break;
        case 3: _t->PhysicalDimensionLineEdited((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 4: _t->sampleTypeChanged((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 5: _t->helpbuttonpressed(); break;
        default: ;
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject UI_RAW2EDFapp::staticMetaObject = { {
    &QObject::staticMetaObject,
    qt_meta_stringdata_UI_RAW2EDFapp.data,
    qt_meta_data_UI_RAW2EDFapp,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *UI_RAW2EDFapp::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *UI_RAW2EDFapp::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_UI_RAW2EDFapp.stringdata0))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int UI_RAW2EDFapp::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 6)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 6;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 6)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 6;
    }
    return _id;
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
