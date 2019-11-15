/****************************************************************************
** Meta object code from reading C++ file 'header_editor.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.13.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../header_editor.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'header_editor.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.13.1. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_UI_headerEditorWindow_t {
    QByteArrayData data[10];
    char stringdata0[153];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_UI_headerEditorWindow_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_UI_headerEditorWindow_t qt_meta_stringdata_UI_headerEditorWindow = {
    {
QT_MOC_LITERAL(0, 0, 21), // "UI_headerEditorWindow"
QT_MOC_LITERAL(1, 22, 9), // "open_file"
QT_MOC_LITERAL(2, 32, 0), // ""
QT_MOC_LITERAL(3, 33, 8), // "save_hdr"
QT_MOC_LITERAL(4, 42, 11), // "read_header"
QT_MOC_LITERAL(5, 54, 10), // "closeEvent"
QT_MOC_LITERAL(6, 65, 12), // "QCloseEvent*"
QT_MOC_LITERAL(7, 78, 25), // "calculate_chars_left_name"
QT_MOC_LITERAL(8, 104, 30), // "calculate_chars_left_recording"
QT_MOC_LITERAL(9, 135, 17) // "helpbuttonpressed"

    },
    "UI_headerEditorWindow\0open_file\0\0"
    "save_hdr\0read_header\0closeEvent\0"
    "QCloseEvent*\0calculate_chars_left_name\0"
    "calculate_chars_left_recording\0"
    "helpbuttonpressed"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_UI_headerEditorWindow[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       8,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: name, argc, parameters, tag, flags
       1,    0,   54,    2, 0x08 /* Private */,
       3,    0,   55,    2, 0x08 /* Private */,
       4,    0,   56,    2, 0x08 /* Private */,
       5,    1,   57,    2, 0x08 /* Private */,
       7,    1,   60,    2, 0x08 /* Private */,
       7,    1,   63,    2, 0x08 /* Private */,
       8,    1,   66,    2, 0x08 /* Private */,
       9,    0,   69,    2, 0x08 /* Private */,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, 0x80000000 | 6,    2,
    QMetaType::Void, QMetaType::Int,    2,
    QMetaType::Int, QMetaType::QString,    2,
    QMetaType::Int, QMetaType::QString,    2,
    QMetaType::Void,

       0        // eod
};

void UI_headerEditorWindow::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<UI_headerEditorWindow *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->open_file(); break;
        case 1: _t->save_hdr(); break;
        case 2: _t->read_header(); break;
        case 3: _t->closeEvent((*reinterpret_cast< QCloseEvent*(*)>(_a[1]))); break;
        case 4: _t->calculate_chars_left_name((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 5: { int _r = _t->calculate_chars_left_name((*reinterpret_cast< const QString(*)>(_a[1])));
            if (_a[0]) *reinterpret_cast< int*>(_a[0]) = std::move(_r); }  break;
        case 6: { int _r = _t->calculate_chars_left_recording((*reinterpret_cast< const QString(*)>(_a[1])));
            if (_a[0]) *reinterpret_cast< int*>(_a[0]) = std::move(_r); }  break;
        case 7: _t->helpbuttonpressed(); break;
        default: ;
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject UI_headerEditorWindow::staticMetaObject = { {
    &QDialog::staticMetaObject,
    qt_meta_stringdata_UI_headerEditorWindow.data,
    qt_meta_data_UI_headerEditorWindow,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *UI_headerEditorWindow::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *UI_headerEditorWindow::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_UI_headerEditorWindow.stringdata0))
        return static_cast<void*>(this);
    return QDialog::qt_metacast(_clname);
}

int UI_headerEditorWindow::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QDialog::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 8)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 8;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 8)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 8;
    }
    return _id;
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
