/****************************************************************************
** Meta object code from reading C++ file 'edit_predefined_mtg.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.13.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../edit_predefined_mtg.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'edit_predefined_mtg.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.13.1. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_UI_edit_predefined_mtg_window_t {
    QByteArrayData data[6];
    char stringdata0[79];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_UI_edit_predefined_mtg_window_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_UI_edit_predefined_mtg_window_t qt_meta_stringdata_UI_edit_predefined_mtg_window = {
    {
QT_MOC_LITERAL(0, 0, 29), // "UI_edit_predefined_mtg_window"
QT_MOC_LITERAL(1, 30, 10), // "rowClicked"
QT_MOC_LITERAL(2, 41, 0), // ""
QT_MOC_LITERAL(3, 42, 16), // "QListWidgetItem*"
QT_MOC_LITERAL(4, 59, 7), // "adEntry"
QT_MOC_LITERAL(5, 67, 11) // "removeEntry"

    },
    "UI_edit_predefined_mtg_window\0rowClicked\0"
    "\0QListWidgetItem*\0adEntry\0removeEntry"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_UI_edit_predefined_mtg_window[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       3,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: name, argc, parameters, tag, flags
       1,    1,   29,    2, 0x08 /* Private */,
       4,    0,   32,    2, 0x08 /* Private */,
       5,    0,   33,    2, 0x08 /* Private */,

 // slots: parameters
    QMetaType::Void, 0x80000000 | 3,    2,
    QMetaType::Void,
    QMetaType::Void,

       0        // eod
};

void UI_edit_predefined_mtg_window::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<UI_edit_predefined_mtg_window *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->rowClicked((*reinterpret_cast< QListWidgetItem*(*)>(_a[1]))); break;
        case 1: _t->adEntry(); break;
        case 2: _t->removeEntry(); break;
        default: ;
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject UI_edit_predefined_mtg_window::staticMetaObject = { {
    &QObject::staticMetaObject,
    qt_meta_stringdata_UI_edit_predefined_mtg_window.data,
    qt_meta_data_UI_edit_predefined_mtg_window,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *UI_edit_predefined_mtg_window::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *UI_edit_predefined_mtg_window::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_UI_edit_predefined_mtg_window.stringdata0))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int UI_edit_predefined_mtg_window::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 3)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 3;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 3)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 3;
    }
    return _id;
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
