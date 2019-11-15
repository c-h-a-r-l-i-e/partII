/****************************************************************************
** Meta object code from reading C++ file 'signals_dialog.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.13.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../signals_dialog.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'signals_dialog.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.13.1. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_UI_Signalswindow_t {
    QByteArrayData data[12];
    char stringdata0[211];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_UI_Signalswindow_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_UI_Signalswindow_t qt_meta_stringdata_UI_Signalswindow = {
    {
QT_MOC_LITERAL(0, 0, 16), // "UI_Signalswindow"
QT_MOC_LITERAL(1, 17, 12), // "show_signals"
QT_MOC_LITERAL(2, 30, 0), // ""
QT_MOC_LITERAL(3, 31, 22), // "SelectAllButtonClicked"
QT_MOC_LITERAL(4, 54, 20), // "DisplayButtonClicked"
QT_MOC_LITERAL(5, 75, 24), // "DisplayCompButtonClicked"
QT_MOC_LITERAL(6, 100, 16), // "AddButtonClicked"
QT_MOC_LITERAL(7, 117, 21), // "SubtractButtonClicked"
QT_MOC_LITERAL(8, 139, 19), // "RemoveButtonClicked"
QT_MOC_LITERAL(9, 159, 18), // "ColorButtonClicked"
QT_MOC_LITERAL(10, 178, 14), // "SpecialButton*"
QT_MOC_LITERAL(11, 193, 17) // "HelpButtonClicked"

    },
    "UI_Signalswindow\0show_signals\0\0"
    "SelectAllButtonClicked\0DisplayButtonClicked\0"
    "DisplayCompButtonClicked\0AddButtonClicked\0"
    "SubtractButtonClicked\0RemoveButtonClicked\0"
    "ColorButtonClicked\0SpecialButton*\0"
    "HelpButtonClicked"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_UI_Signalswindow[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       9,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: name, argc, parameters, tag, flags
       1,    1,   59,    2, 0x08 /* Private */,
       3,    0,   62,    2, 0x08 /* Private */,
       4,    0,   63,    2, 0x08 /* Private */,
       5,    0,   64,    2, 0x08 /* Private */,
       6,    0,   65,    2, 0x08 /* Private */,
       7,    0,   66,    2, 0x08 /* Private */,
       8,    0,   67,    2, 0x08 /* Private */,
       9,    1,   68,    2, 0x08 /* Private */,
      11,    0,   71,    2, 0x08 /* Private */,

 // slots: parameters
    QMetaType::Void, QMetaType::Int,    2,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, 0x80000000 | 10,    2,
    QMetaType::Void,

       0        // eod
};

void UI_Signalswindow::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<UI_Signalswindow *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->show_signals((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 1: _t->SelectAllButtonClicked(); break;
        case 2: _t->DisplayButtonClicked(); break;
        case 3: _t->DisplayCompButtonClicked(); break;
        case 4: _t->AddButtonClicked(); break;
        case 5: _t->SubtractButtonClicked(); break;
        case 6: _t->RemoveButtonClicked(); break;
        case 7: _t->ColorButtonClicked((*reinterpret_cast< SpecialButton*(*)>(_a[1]))); break;
        case 8: _t->HelpButtonClicked(); break;
        default: ;
        }
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        switch (_id) {
        default: *reinterpret_cast<int*>(_a[0]) = -1; break;
        case 7:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< SpecialButton* >(); break;
            }
            break;
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject UI_Signalswindow::staticMetaObject = { {
    &QObject::staticMetaObject,
    qt_meta_stringdata_UI_Signalswindow.data,
    qt_meta_data_UI_Signalswindow,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *UI_Signalswindow::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *UI_Signalswindow::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_UI_Signalswindow.stringdata0))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int UI_Signalswindow::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 9)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 9;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 9)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 9;
    }
    return _id;
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
