/****************************************************************************
** Meta object code from reading C++ file 'import_annotations.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.13.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../import_annotations.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'import_annotations.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.13.1. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_UI_ImportAnnotationswindow_t {
    QByteArrayData data[8];
    char stringdata0[152];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_UI_ImportAnnotationswindow_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_UI_ImportAnnotationswindow_t qt_meta_stringdata_UI_ImportAnnotationswindow = {
    {
QT_MOC_LITERAL(0, 0, 26), // "UI_ImportAnnotationswindow"
QT_MOC_LITERAL(1, 27, 19), // "ImportButtonClicked"
QT_MOC_LITERAL(2, 47, 0), // ""
QT_MOC_LITERAL(3, 48, 29), // "descriptionRadioButtonClicked"
QT_MOC_LITERAL(4, 78, 20), // "DCEventSignalChanged"
QT_MOC_LITERAL(5, 99, 23), // "DurationCheckBoxChanged"
QT_MOC_LITERAL(6, 123, 10), // "TabChanged"
QT_MOC_LITERAL(7, 134, 17) // "helpbuttonpressed"

    },
    "UI_ImportAnnotationswindow\0"
    "ImportButtonClicked\0\0descriptionRadioButtonClicked\0"
    "DCEventSignalChanged\0DurationCheckBoxChanged\0"
    "TabChanged\0helpbuttonpressed"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_UI_ImportAnnotationswindow[] = {

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
       3,    1,   45,    2, 0x08 /* Private */,
       4,    1,   48,    2, 0x08 /* Private */,
       5,    1,   51,    2, 0x08 /* Private */,
       6,    1,   54,    2, 0x08 /* Private */,
       7,    0,   57,    2, 0x08 /* Private */,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void, QMetaType::Bool,    2,
    QMetaType::Void, QMetaType::Int,    2,
    QMetaType::Void, QMetaType::Int,    2,
    QMetaType::Void, QMetaType::Int,    2,
    QMetaType::Void,

       0        // eod
};

void UI_ImportAnnotationswindow::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<UI_ImportAnnotationswindow *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->ImportButtonClicked(); break;
        case 1: _t->descriptionRadioButtonClicked((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 2: _t->DCEventSignalChanged((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 3: _t->DurationCheckBoxChanged((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 4: _t->TabChanged((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 5: _t->helpbuttonpressed(); break;
        default: ;
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject UI_ImportAnnotationswindow::staticMetaObject = { {
    &QObject::staticMetaObject,
    qt_meta_stringdata_UI_ImportAnnotationswindow.data,
    qt_meta_data_UI_ImportAnnotationswindow,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *UI_ImportAnnotationswindow::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *UI_ImportAnnotationswindow::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_UI_ImportAnnotationswindow.stringdata0))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int UI_ImportAnnotationswindow::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
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