/****************************************************************************
** Meta object code from reading C++ file 'adjustfiltersettings.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.13.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../adjustfiltersettings.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'adjustfiltersettings.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.13.1. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_AdjustFilterSettings_t {
    QByteArrayData data[8];
    char stringdata0[141];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_AdjustFilterSettings_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_AdjustFilterSettings_t qt_meta_stringdata_AdjustFilterSettings = {
    {
QT_MOC_LITERAL(0, 0, 20), // "AdjustFilterSettings"
QT_MOC_LITERAL(1, 21, 20), // "freqbox1valuechanged"
QT_MOC_LITERAL(2, 42, 0), // ""
QT_MOC_LITERAL(3, 43, 20), // "freqbox2valuechanged"
QT_MOC_LITERAL(4, 64, 20), // "orderboxvaluechanged"
QT_MOC_LITERAL(5, 85, 18), // "stepsizeboxchanged"
QT_MOC_LITERAL(6, 104, 16), // "filterboxchanged"
QT_MOC_LITERAL(7, 121, 19) // "removeButtonClicked"

    },
    "AdjustFilterSettings\0freqbox1valuechanged\0"
    "\0freqbox2valuechanged\0orderboxvaluechanged\0"
    "stepsizeboxchanged\0filterboxchanged\0"
    "removeButtonClicked"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_AdjustFilterSettings[] = {

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
       1,    1,   44,    2, 0x08 /* Private */,
       3,    1,   47,    2, 0x08 /* Private */,
       4,    1,   50,    2, 0x08 /* Private */,
       5,    1,   53,    2, 0x08 /* Private */,
       6,    1,   56,    2, 0x08 /* Private */,
       7,    0,   59,    2, 0x08 /* Private */,

 // slots: parameters
    QMetaType::Void, QMetaType::Double,    2,
    QMetaType::Void, QMetaType::Double,    2,
    QMetaType::Void, QMetaType::Int,    2,
    QMetaType::Void, QMetaType::Int,    2,
    QMetaType::Void, QMetaType::Int,    2,
    QMetaType::Void,

       0        // eod
};

void AdjustFilterSettings::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<AdjustFilterSettings *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->freqbox1valuechanged((*reinterpret_cast< double(*)>(_a[1]))); break;
        case 1: _t->freqbox2valuechanged((*reinterpret_cast< double(*)>(_a[1]))); break;
        case 2: _t->orderboxvaluechanged((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 3: _t->stepsizeboxchanged((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 4: _t->filterboxchanged((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 5: _t->removeButtonClicked(); break;
        default: ;
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject AdjustFilterSettings::staticMetaObject = { {
    &QObject::staticMetaObject,
    qt_meta_stringdata_AdjustFilterSettings.data,
    qt_meta_data_AdjustFilterSettings,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *AdjustFilterSettings::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *AdjustFilterSettings::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_AdjustFilterSettings.stringdata0))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int AdjustFilterSettings::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
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
