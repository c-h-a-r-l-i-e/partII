/****************************************************************************
** Meta object code from reading C++ file 'z_score_dialog.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.13.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../z_score_dialog.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'z_score_dialog.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.13.1. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_UI_ZScoreWindow_t {
    QByteArrayData data[12];
    char stringdata0[214];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_UI_ZScoreWindow_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_UI_ZScoreWindow_t qt_meta_stringdata_UI_ZScoreWindow = {
    {
QT_MOC_LITERAL(0, 0, 15), // "UI_ZScoreWindow"
QT_MOC_LITERAL(1, 16, 18), // "startButtonClicked"
QT_MOC_LITERAL(2, 35, 0), // ""
QT_MOC_LITERAL(3, 36, 28), // "get_annotationsButtonClicked"
QT_MOC_LITERAL(4, 65, 17), // "jumpButtonClicked"
QT_MOC_LITERAL(5, 83, 21), // "ZscoreDialogDestroyed"
QT_MOC_LITERAL(6, 105, 19), // "RadioButtonsClicked"
QT_MOC_LITERAL(7, 125, 20), // "defaultButtonClicked"
QT_MOC_LITERAL(8, 146, 12), // "markersMoved"
QT_MOC_LITERAL(9, 159, 21), // "addTraceButtonClicked"
QT_MOC_LITERAL(10, 181, 16), // "shift_page_right"
QT_MOC_LITERAL(11, 198, 15) // "shift_page_left"

    },
    "UI_ZScoreWindow\0startButtonClicked\0\0"
    "get_annotationsButtonClicked\0"
    "jumpButtonClicked\0ZscoreDialogDestroyed\0"
    "RadioButtonsClicked\0defaultButtonClicked\0"
    "markersMoved\0addTraceButtonClicked\0"
    "shift_page_right\0shift_page_left"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_UI_ZScoreWindow[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
      10,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: name, argc, parameters, tag, flags
       1,    0,   64,    2, 0x08 /* Private */,
       3,    0,   65,    2, 0x08 /* Private */,
       4,    0,   66,    2, 0x08 /* Private */,
       5,    1,   67,    2, 0x08 /* Private */,
       6,    1,   70,    2, 0x08 /* Private */,
       7,    0,   73,    2, 0x08 /* Private */,
       8,    0,   74,    2, 0x08 /* Private */,
       9,    0,   75,    2, 0x08 /* Private */,
      10,    0,   76,    2, 0x08 /* Private */,
      11,    0,   77,    2, 0x08 /* Private */,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::QObjectStar,    2,
    QMetaType::Void, QMetaType::Bool,    2,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,

       0        // eod
};

void UI_ZScoreWindow::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<UI_ZScoreWindow *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->startButtonClicked(); break;
        case 1: _t->get_annotationsButtonClicked(); break;
        case 2: _t->jumpButtonClicked(); break;
        case 3: _t->ZscoreDialogDestroyed((*reinterpret_cast< QObject*(*)>(_a[1]))); break;
        case 4: _t->RadioButtonsClicked((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 5: _t->defaultButtonClicked(); break;
        case 6: _t->markersMoved(); break;
        case 7: _t->addTraceButtonClicked(); break;
        case 8: _t->shift_page_right(); break;
        case 9: _t->shift_page_left(); break;
        default: ;
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject UI_ZScoreWindow::staticMetaObject = { {
    &QObject::staticMetaObject,
    qt_meta_stringdata_UI_ZScoreWindow.data,
    qt_meta_data_UI_ZScoreWindow,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *UI_ZScoreWindow::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *UI_ZScoreWindow::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_UI_ZScoreWindow.stringdata0))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int UI_ZScoreWindow::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 10)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 10;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 10)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 10;
    }
    return _id;
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
