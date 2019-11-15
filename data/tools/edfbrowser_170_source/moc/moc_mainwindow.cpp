/****************************************************************************
** Meta object code from reading C++ file 'mainwindow.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.13.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../mainwindow.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'mainwindow.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.13.1. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_UI_Mainwindow_t {
    QByteArrayData data[120];
    char stringdata0[2196];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_UI_Mainwindow_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_UI_Mainwindow_t qt_meta_stringdata_UI_Mainwindow = {
    {
QT_MOC_LITERAL(0, 0, 13), // "UI_Mainwindow"
QT_MOC_LITERAL(1, 14, 18), // "remove_all_signals"
QT_MOC_LITERAL(2, 33, 0), // ""
QT_MOC_LITERAL(3, 34, 36), // "edfplus_remove_duplicate_anno..."
QT_MOC_LITERAL(4, 71, 17), // "video_player_seek"
QT_MOC_LITERAL(5, 89, 25), // "video_player_toggle_pause"
QT_MOC_LITERAL(6, 115, 13), // "open_new_file"
QT_MOC_LITERAL(7, 129, 14), // "show_file_info"
QT_MOC_LITERAL(8, 144, 22), // "close_file_action_func"
QT_MOC_LITERAL(9, 167, 8), // "QAction*"
QT_MOC_LITERAL(10, 176, 15), // "close_all_files"
QT_MOC_LITERAL(11, 192, 12), // "exit_program"
QT_MOC_LITERAL(12, 205, 23), // "signalproperties_dialog"
QT_MOC_LITERAL(13, 229, 23), // "filterproperties_dialog"
QT_MOC_LITERAL(14, 253, 18), // "add_signals_dialog"
QT_MOC_LITERAL(15, 272, 17), // "show_about_dialog"
QT_MOC_LITERAL(16, 290, 16), // "set_display_time"
QT_MOC_LITERAL(17, 307, 13), // "set_page_div2"
QT_MOC_LITERAL(18, 321, 14), // "set_page_mult2"
QT_MOC_LITERAL(19, 336, 26), // "set_display_time_whole_rec"
QT_MOC_LITERAL(20, 363, 13), // "set_amplitude"
QT_MOC_LITERAL(21, 377, 18), // "set_amplitude_div2"
QT_MOC_LITERAL(22, 396, 19), // "set_amplitude_mult2"
QT_MOC_LITERAL(23, 416, 19), // "fit_signals_to_pane"
QT_MOC_LITERAL(24, 436, 21), // "fit_signals_dc_offset"
QT_MOC_LITERAL(25, 458, 11), // "former_page"
QT_MOC_LITERAL(26, 470, 15), // "shift_page_left"
QT_MOC_LITERAL(27, 486, 16), // "shift_page_right"
QT_MOC_LITERAL(28, 503, 13), // "playback_file"
QT_MOC_LITERAL(29, 517, 13), // "stop_playback"
QT_MOC_LITERAL(30, 531, 9), // "next_page"
QT_MOC_LITERAL(31, 541, 13), // "shift_page_up"
QT_MOC_LITERAL(32, 555, 15), // "shift_page_down"
QT_MOC_LITERAL(33, 571, 8), // "zoomback"
QT_MOC_LITERAL(34, 580, 7), // "forward"
QT_MOC_LITERAL(35, 588, 17), // "show_splashscreen"
QT_MOC_LITERAL(36, 606, 15), // "export_to_ascii"
QT_MOC_LITERAL(37, 622, 23), // "check_edf_compatibility"
QT_MOC_LITERAL(38, 646, 14), // "add_new_filter"
QT_MOC_LITERAL(39, 661, 19), // "add_plif_ecg_filter"
QT_MOC_LITERAL(40, 681, 14), // "add_fir_filter"
QT_MOC_LITERAL(41, 696, 16), // "add_spike_filter"
QT_MOC_LITERAL(42, 713, 18), // "remove_all_filters"
QT_MOC_LITERAL(43, 732, 27), // "remove_all_plif_ecg_filters"
QT_MOC_LITERAL(44, 760, 22), // "remove_all_fir_filters"
QT_MOC_LITERAL(45, 783, 24), // "remove_all_spike_filters"
QT_MOC_LITERAL(46, 808, 14), // "jump_to_dialog"
QT_MOC_LITERAL(47, 823, 13), // "jump_to_start"
QT_MOC_LITERAL(48, 837, 11), // "jump_to_end"
QT_MOC_LITERAL(49, 849, 21), // "jump_to_time_millisec"
QT_MOC_LITERAL(50, 871, 16), // "show_annotations"
QT_MOC_LITERAL(51, 888, 19), // "show_options_dialog"
QT_MOC_LITERAL(52, 908, 13), // "get_long_time"
QT_MOC_LITERAL(53, 922, 5), // "char*"
QT_MOC_LITERAL(54, 928, 16), // "nk2edf_converter"
QT_MOC_LITERAL(55, 945, 12), // "set_timesync"
QT_MOC_LITERAL(56, 958, 22), // "set_timesync_reference"
QT_MOC_LITERAL(57, 981, 23), // "recent_file_action_func"
QT_MOC_LITERAL(58, 1005, 18), // "sync_by_crosshairs"
QT_MOC_LITERAL(59, 1024, 12), // "save_montage"
QT_MOC_LITERAL(60, 1037, 12), // "load_montage"
QT_MOC_LITERAL(61, 1050, 12), // "view_montage"
QT_MOC_LITERAL(62, 1063, 17), // "show_this_montage"
QT_MOC_LITERAL(63, 1081, 9), // "show_help"
QT_MOC_LITERAL(64, 1091, 17), // "show_kb_shortcuts"
QT_MOC_LITERAL(65, 1109, 12), // "print_to_edf"
QT_MOC_LITERAL(66, 1122, 29), // "set_user_defined_display_time"
QT_MOC_LITERAL(67, 1152, 12), // "print_to_bdf"
QT_MOC_LITERAL(68, 1165, 20), // "print_to_img_640x480"
QT_MOC_LITERAL(69, 1186, 20), // "print_to_img_800x600"
QT_MOC_LITERAL(70, 1207, 21), // "print_to_img_1024x768"
QT_MOC_LITERAL(71, 1229, 22), // "print_to_img_1280x1024"
QT_MOC_LITERAL(72, 1252, 22), // "print_to_img_1600x1200"
QT_MOC_LITERAL(73, 1275, 20), // "convert_ascii_to_edf"
QT_MOC_LITERAL(74, 1296, 19), // "convert_fino_to_edf"
QT_MOC_LITERAL(75, 1316, 19), // "convert_wave_to_edf"
QT_MOC_LITERAL(76, 1336, 23), // "convert_fm_audio_to_edf"
QT_MOC_LITERAL(77, 1360, 22), // "convert_mortara_to_edf"
QT_MOC_LITERAL(78, 1383, 21), // "convert_nexfin_to_edf"
QT_MOC_LITERAL(79, 1405, 14), // "edfd_converter"
QT_MOC_LITERAL(80, 1420, 12), // "slider_moved"
QT_MOC_LITERAL(81, 1433, 19), // "convert_emsa_to_edf"
QT_MOC_LITERAL(82, 1453, 17), // "bdf2edf_converter"
QT_MOC_LITERAL(83, 1471, 21), // "set_dc_offset_to_zero"
QT_MOC_LITERAL(84, 1493, 17), // "annotation_editor"
QT_MOC_LITERAL(85, 1511, 9), // "save_file"
QT_MOC_LITERAL(86, 1521, 21), // "unisens2edf_converter"
QT_MOC_LITERAL(87, 1543, 20), // "BI98002edf_converter"
QT_MOC_LITERAL(88, 1564, 18), // "export_annotations"
QT_MOC_LITERAL(89, 1583, 19), // "load_predefined_mtg"
QT_MOC_LITERAL(90, 1603, 24), // "edit_predefined_montages"
QT_MOC_LITERAL(91, 1628, 18), // "show_spectrum_dock"
QT_MOC_LITERAL(92, 1647, 11), // "page_3cmsec"
QT_MOC_LITERAL(93, 1659, 12), // "page_25mmsec"
QT_MOC_LITERAL(94, 1672, 12), // "page_50mmsec"
QT_MOC_LITERAL(95, 1685, 14), // "reduce_signals"
QT_MOC_LITERAL(96, 1700, 11), // "edit_header"
QT_MOC_LITERAL(97, 1712, 25), // "biosemi2bdfplus_converter"
QT_MOC_LITERAL(98, 1738, 18), // "import_annotations"
QT_MOC_LITERAL(99, 1757, 11), // "open_stream"
QT_MOC_LITERAL(100, 1769, 16), // "start_stop_video"
QT_MOC_LITERAL(101, 1786, 18), // "stop_video_generic"
QT_MOC_LITERAL(102, 1805, 22), // "live_stream_timer_func"
QT_MOC_LITERAL(103, 1828, 21), // "video_poll_timer_func"
QT_MOC_LITERAL(104, 1850, 28), // "playback_realtime_timer_func"
QT_MOC_LITERAL(105, 1879, 16), // "organize_signals"
QT_MOC_LITERAL(106, 1896, 10), // "Escape_fun"
QT_MOC_LITERAL(107, 1907, 31), // "export_ecg_rr_interval_to_ascii"
QT_MOC_LITERAL(108, 1939, 21), // "convert_binary_to_edf"
QT_MOC_LITERAL(109, 1961, 22), // "convert_manscan_to_edf"
QT_MOC_LITERAL(110, 1984, 21), // "convert_scpecg_to_edf"
QT_MOC_LITERAL(111, 2006, 18), // "convert_mit_to_edf"
QT_MOC_LITERAL(112, 2025, 19), // "convert_biox_to_edf"
QT_MOC_LITERAL(113, 2045, 19), // "video_process_error"
QT_MOC_LITERAL(114, 2065, 22), // "QProcess::ProcessError"
QT_MOC_LITERAL(115, 2088, 14), // "vlc_sock_error"
QT_MOC_LITERAL(116, 2103, 28), // "QAbstractSocket::SocketError"
QT_MOC_LITERAL(117, 2132, 23), // "export_filtered_signals"
QT_MOC_LITERAL(118, 2156, 19), // "video_player_faster"
QT_MOC_LITERAL(119, 2176, 19) // "video_player_slower"

    },
    "UI_Mainwindow\0remove_all_signals\0\0"
    "edfplus_remove_duplicate_annotations\0"
    "video_player_seek\0video_player_toggle_pause\0"
    "open_new_file\0show_file_info\0"
    "close_file_action_func\0QAction*\0"
    "close_all_files\0exit_program\0"
    "signalproperties_dialog\0filterproperties_dialog\0"
    "add_signals_dialog\0show_about_dialog\0"
    "set_display_time\0set_page_div2\0"
    "set_page_mult2\0set_display_time_whole_rec\0"
    "set_amplitude\0set_amplitude_div2\0"
    "set_amplitude_mult2\0fit_signals_to_pane\0"
    "fit_signals_dc_offset\0former_page\0"
    "shift_page_left\0shift_page_right\0"
    "playback_file\0stop_playback\0next_page\0"
    "shift_page_up\0shift_page_down\0zoomback\0"
    "forward\0show_splashscreen\0export_to_ascii\0"
    "check_edf_compatibility\0add_new_filter\0"
    "add_plif_ecg_filter\0add_fir_filter\0"
    "add_spike_filter\0remove_all_filters\0"
    "remove_all_plif_ecg_filters\0"
    "remove_all_fir_filters\0remove_all_spike_filters\0"
    "jump_to_dialog\0jump_to_start\0jump_to_end\0"
    "jump_to_time_millisec\0show_annotations\0"
    "show_options_dialog\0get_long_time\0"
    "char*\0nk2edf_converter\0set_timesync\0"
    "set_timesync_reference\0recent_file_action_func\0"
    "sync_by_crosshairs\0save_montage\0"
    "load_montage\0view_montage\0show_this_montage\0"
    "show_help\0show_kb_shortcuts\0print_to_edf\0"
    "set_user_defined_display_time\0"
    "print_to_bdf\0print_to_img_640x480\0"
    "print_to_img_800x600\0print_to_img_1024x768\0"
    "print_to_img_1280x1024\0print_to_img_1600x1200\0"
    "convert_ascii_to_edf\0convert_fino_to_edf\0"
    "convert_wave_to_edf\0convert_fm_audio_to_edf\0"
    "convert_mortara_to_edf\0convert_nexfin_to_edf\0"
    "edfd_converter\0slider_moved\0"
    "convert_emsa_to_edf\0bdf2edf_converter\0"
    "set_dc_offset_to_zero\0annotation_editor\0"
    "save_file\0unisens2edf_converter\0"
    "BI98002edf_converter\0export_annotations\0"
    "load_predefined_mtg\0edit_predefined_montages\0"
    "show_spectrum_dock\0page_3cmsec\0"
    "page_25mmsec\0page_50mmsec\0reduce_signals\0"
    "edit_header\0biosemi2bdfplus_converter\0"
    "import_annotations\0open_stream\0"
    "start_stop_video\0stop_video_generic\0"
    "live_stream_timer_func\0video_poll_timer_func\0"
    "playback_realtime_timer_func\0"
    "organize_signals\0Escape_fun\0"
    "export_ecg_rr_interval_to_ascii\0"
    "convert_binary_to_edf\0convert_manscan_to_edf\0"
    "convert_scpecg_to_edf\0convert_mit_to_edf\0"
    "convert_biox_to_edf\0video_process_error\0"
    "QProcess::ProcessError\0vlc_sock_error\0"
    "QAbstractSocket::SocketError\0"
    "export_filtered_signals\0video_player_faster\0"
    "video_player_slower"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_UI_Mainwindow[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
     114,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: name, argc, parameters, tag, flags
       1,    0,  584,    2, 0x0a /* Public */,
       3,    0,  585,    2, 0x0a /* Public */,
       4,    1,  586,    2, 0x0a /* Public */,
       5,    0,  589,    2, 0x0a /* Public */,
       6,    0,  590,    2, 0x08 /* Private */,
       7,    0,  591,    2, 0x08 /* Private */,
       8,    1,  592,    2, 0x08 /* Private */,
      10,    0,  595,    2, 0x08 /* Private */,
      11,    0,  596,    2, 0x08 /* Private */,
      12,    0,  597,    2, 0x08 /* Private */,
      13,    0,  598,    2, 0x08 /* Private */,
      14,    0,  599,    2, 0x08 /* Private */,
      15,    0,  600,    2, 0x08 /* Private */,
      16,    1,  601,    2, 0x08 /* Private */,
      17,    0,  604,    2, 0x08 /* Private */,
      18,    0,  605,    2, 0x08 /* Private */,
      19,    0,  606,    2, 0x08 /* Private */,
      20,    1,  607,    2, 0x08 /* Private */,
      21,    0,  610,    2, 0x08 /* Private */,
      22,    0,  611,    2, 0x08 /* Private */,
      23,    0,  612,    2, 0x08 /* Private */,
      24,    0,  613,    2, 0x08 /* Private */,
      25,    0,  614,    2, 0x08 /* Private */,
      26,    0,  615,    2, 0x08 /* Private */,
      27,    0,  616,    2, 0x08 /* Private */,
      28,    0,  617,    2, 0x08 /* Private */,
      29,    0,  618,    2, 0x08 /* Private */,
      30,    0,  619,    2, 0x08 /* Private */,
      31,    0,  620,    2, 0x08 /* Private */,
      32,    0,  621,    2, 0x08 /* Private */,
      33,    0,  622,    2, 0x08 /* Private */,
      34,    0,  623,    2, 0x08 /* Private */,
      35,    0,  624,    2, 0x08 /* Private */,
      36,    0,  625,    2, 0x08 /* Private */,
      37,    0,  626,    2, 0x08 /* Private */,
      38,    0,  627,    2, 0x08 /* Private */,
      39,    0,  628,    2, 0x08 /* Private */,
      40,    0,  629,    2, 0x08 /* Private */,
      41,    0,  630,    2, 0x08 /* Private */,
      42,    0,  631,    2, 0x08 /* Private */,
      43,    0,  632,    2, 0x08 /* Private */,
      44,    0,  633,    2, 0x08 /* Private */,
      45,    0,  634,    2, 0x08 /* Private */,
      46,    0,  635,    2, 0x08 /* Private */,
      47,    0,  636,    2, 0x08 /* Private */,
      48,    0,  637,    2, 0x08 /* Private */,
      49,    1,  638,    2, 0x08 /* Private */,
      50,    0,  641,    2, 0x08 /* Private */,
      51,    0,  642,    2, 0x08 /* Private */,
      52,    1,  643,    2, 0x08 /* Private */,
      54,    0,  646,    2, 0x08 /* Private */,
      55,    1,  647,    2, 0x08 /* Private */,
      56,    1,  650,    2, 0x08 /* Private */,
      57,    1,  653,    2, 0x08 /* Private */,
      58,    0,  656,    2, 0x08 /* Private */,
      59,    0,  657,    2, 0x08 /* Private */,
      60,    0,  658,    2, 0x08 /* Private */,
      61,    0,  659,    2, 0x08 /* Private */,
      62,    0,  660,    2, 0x08 /* Private */,
      63,    0,  661,    2, 0x08 /* Private */,
      64,    0,  662,    2, 0x08 /* Private */,
      65,    0,  663,    2, 0x08 /* Private */,
      66,    0,  664,    2, 0x08 /* Private */,
      67,    0,  665,    2, 0x08 /* Private */,
      68,    0,  666,    2, 0x08 /* Private */,
      69,    0,  667,    2, 0x08 /* Private */,
      70,    0,  668,    2, 0x08 /* Private */,
      71,    0,  669,    2, 0x08 /* Private */,
      72,    0,  670,    2, 0x08 /* Private */,
      73,    0,  671,    2, 0x08 /* Private */,
      74,    0,  672,    2, 0x08 /* Private */,
      75,    0,  673,    2, 0x08 /* Private */,
      76,    0,  674,    2, 0x08 /* Private */,
      77,    0,  675,    2, 0x08 /* Private */,
      78,    0,  676,    2, 0x08 /* Private */,
      79,    0,  677,    2, 0x08 /* Private */,
      80,    1,  678,    2, 0x08 /* Private */,
      81,    0,  681,    2, 0x08 /* Private */,
      82,    0,  682,    2, 0x08 /* Private */,
      83,    0,  683,    2, 0x08 /* Private */,
      84,    0,  684,    2, 0x08 /* Private */,
      85,    0,  685,    2, 0x08 /* Private */,
      86,    0,  686,    2, 0x08 /* Private */,
      87,    0,  687,    2, 0x08 /* Private */,
      88,    0,  688,    2, 0x08 /* Private */,
      89,    1,  689,    2, 0x08 /* Private */,
      90,    0,  692,    2, 0x08 /* Private */,
      91,    0,  693,    2, 0x08 /* Private */,
      92,    0,  694,    2, 0x08 /* Private */,
      93,    0,  695,    2, 0x08 /* Private */,
      94,    0,  696,    2, 0x08 /* Private */,
      95,    0,  697,    2, 0x08 /* Private */,
      96,    0,  698,    2, 0x08 /* Private */,
      97,    0,  699,    2, 0x08 /* Private */,
      98,    0,  700,    2, 0x08 /* Private */,
      99,    0,  701,    2, 0x08 /* Private */,
     100,    0,  702,    2, 0x08 /* Private */,
     101,    1,  703,    2, 0x08 /* Private */,
     102,    0,  706,    2, 0x08 /* Private */,
     103,    0,  707,    2, 0x08 /* Private */,
     104,    0,  708,    2, 0x08 /* Private */,
     105,    0,  709,    2, 0x08 /* Private */,
     106,    0,  710,    2, 0x08 /* Private */,
     107,    0,  711,    2, 0x08 /* Private */,
     108,    0,  712,    2, 0x08 /* Private */,
     109,    0,  713,    2, 0x08 /* Private */,
     110,    0,  714,    2, 0x08 /* Private */,
     111,    0,  715,    2, 0x08 /* Private */,
     112,    0,  716,    2, 0x08 /* Private */,
     113,    1,  717,    2, 0x08 /* Private */,
     115,    1,  720,    2, 0x08 /* Private */,
     117,    0,  723,    2, 0x08 /* Private */,
     118,    0,  724,    2, 0x08 /* Private */,
     119,    0,  725,    2, 0x08 /* Private */,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int,    2,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, 0x80000000 | 9,    2,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, 0x80000000 | 9,    2,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, 0x80000000 | 9,    2,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::LongLong,    2,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::LongLong, 0x80000000 | 53,    2,
    QMetaType::Void,
    QMetaType::Void, 0x80000000 | 9,    2,
    QMetaType::Void, 0x80000000 | 9,    2,
    QMetaType::Void, 0x80000000 | 9,    2,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int,    2,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, 0x80000000 | 9,    2,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int,    2,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, 0x80000000 | 114,    2,
    QMetaType::Void, 0x80000000 | 116,    2,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,

       0        // eod
};

void UI_Mainwindow::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<UI_Mainwindow *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->remove_all_signals(); break;
        case 1: _t->edfplus_remove_duplicate_annotations(); break;
        case 2: _t->video_player_seek((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 3: _t->video_player_toggle_pause(); break;
        case 4: _t->open_new_file(); break;
        case 5: _t->show_file_info(); break;
        case 6: _t->close_file_action_func((*reinterpret_cast< QAction*(*)>(_a[1]))); break;
        case 7: _t->close_all_files(); break;
        case 8: _t->exit_program(); break;
        case 9: _t->signalproperties_dialog(); break;
        case 10: _t->filterproperties_dialog(); break;
        case 11: _t->add_signals_dialog(); break;
        case 12: _t->show_about_dialog(); break;
        case 13: _t->set_display_time((*reinterpret_cast< QAction*(*)>(_a[1]))); break;
        case 14: _t->set_page_div2(); break;
        case 15: _t->set_page_mult2(); break;
        case 16: _t->set_display_time_whole_rec(); break;
        case 17: _t->set_amplitude((*reinterpret_cast< QAction*(*)>(_a[1]))); break;
        case 18: _t->set_amplitude_div2(); break;
        case 19: _t->set_amplitude_mult2(); break;
        case 20: _t->fit_signals_to_pane(); break;
        case 21: _t->fit_signals_dc_offset(); break;
        case 22: _t->former_page(); break;
        case 23: _t->shift_page_left(); break;
        case 24: _t->shift_page_right(); break;
        case 25: _t->playback_file(); break;
        case 26: _t->stop_playback(); break;
        case 27: _t->next_page(); break;
        case 28: _t->shift_page_up(); break;
        case 29: _t->shift_page_down(); break;
        case 30: _t->zoomback(); break;
        case 31: _t->forward(); break;
        case 32: _t->show_splashscreen(); break;
        case 33: _t->export_to_ascii(); break;
        case 34: _t->check_edf_compatibility(); break;
        case 35: _t->add_new_filter(); break;
        case 36: _t->add_plif_ecg_filter(); break;
        case 37: _t->add_fir_filter(); break;
        case 38: _t->add_spike_filter(); break;
        case 39: _t->remove_all_filters(); break;
        case 40: _t->remove_all_plif_ecg_filters(); break;
        case 41: _t->remove_all_fir_filters(); break;
        case 42: _t->remove_all_spike_filters(); break;
        case 43: _t->jump_to_dialog(); break;
        case 44: _t->jump_to_start(); break;
        case 45: _t->jump_to_end(); break;
        case 46: _t->jump_to_time_millisec((*reinterpret_cast< long long(*)>(_a[1]))); break;
        case 47: _t->show_annotations(); break;
        case 48: _t->show_options_dialog(); break;
        case 49: { long long _r = _t->get_long_time((*reinterpret_cast< char*(*)>(_a[1])));
            if (_a[0]) *reinterpret_cast< long long*>(_a[0]) = std::move(_r); }  break;
        case 50: _t->nk2edf_converter(); break;
        case 51: _t->set_timesync((*reinterpret_cast< QAction*(*)>(_a[1]))); break;
        case 52: _t->set_timesync_reference((*reinterpret_cast< QAction*(*)>(_a[1]))); break;
        case 53: _t->recent_file_action_func((*reinterpret_cast< QAction*(*)>(_a[1]))); break;
        case 54: _t->sync_by_crosshairs(); break;
        case 55: _t->save_montage(); break;
        case 56: _t->load_montage(); break;
        case 57: _t->view_montage(); break;
        case 58: _t->show_this_montage(); break;
        case 59: _t->show_help(); break;
        case 60: _t->show_kb_shortcuts(); break;
        case 61: _t->print_to_edf(); break;
        case 62: _t->set_user_defined_display_time(); break;
        case 63: _t->print_to_bdf(); break;
        case 64: _t->print_to_img_640x480(); break;
        case 65: _t->print_to_img_800x600(); break;
        case 66: _t->print_to_img_1024x768(); break;
        case 67: _t->print_to_img_1280x1024(); break;
        case 68: _t->print_to_img_1600x1200(); break;
        case 69: _t->convert_ascii_to_edf(); break;
        case 70: _t->convert_fino_to_edf(); break;
        case 71: _t->convert_wave_to_edf(); break;
        case 72: _t->convert_fm_audio_to_edf(); break;
        case 73: _t->convert_mortara_to_edf(); break;
        case 74: _t->convert_nexfin_to_edf(); break;
        case 75: _t->edfd_converter(); break;
        case 76: _t->slider_moved((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 77: _t->convert_emsa_to_edf(); break;
        case 78: _t->bdf2edf_converter(); break;
        case 79: _t->set_dc_offset_to_zero(); break;
        case 80: _t->annotation_editor(); break;
        case 81: _t->save_file(); break;
        case 82: _t->unisens2edf_converter(); break;
        case 83: _t->BI98002edf_converter(); break;
        case 84: _t->export_annotations(); break;
        case 85: _t->load_predefined_mtg((*reinterpret_cast< QAction*(*)>(_a[1]))); break;
        case 86: _t->edit_predefined_montages(); break;
        case 87: _t->show_spectrum_dock(); break;
        case 88: _t->page_3cmsec(); break;
        case 89: _t->page_25mmsec(); break;
        case 90: _t->page_50mmsec(); break;
        case 91: _t->reduce_signals(); break;
        case 92: _t->edit_header(); break;
        case 93: _t->biosemi2bdfplus_converter(); break;
        case 94: _t->import_annotations(); break;
        case 95: _t->open_stream(); break;
        case 96: _t->start_stop_video(); break;
        case 97: _t->stop_video_generic((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 98: _t->live_stream_timer_func(); break;
        case 99: _t->video_poll_timer_func(); break;
        case 100: _t->playback_realtime_timer_func(); break;
        case 101: _t->organize_signals(); break;
        case 102: _t->Escape_fun(); break;
        case 103: _t->export_ecg_rr_interval_to_ascii(); break;
        case 104: _t->convert_binary_to_edf(); break;
        case 105: _t->convert_manscan_to_edf(); break;
        case 106: _t->convert_scpecg_to_edf(); break;
        case 107: _t->convert_mit_to_edf(); break;
        case 108: _t->convert_biox_to_edf(); break;
        case 109: _t->video_process_error((*reinterpret_cast< QProcess::ProcessError(*)>(_a[1]))); break;
        case 110: _t->vlc_sock_error((*reinterpret_cast< QAbstractSocket::SocketError(*)>(_a[1]))); break;
        case 111: _t->export_filtered_signals(); break;
        case 112: _t->video_player_faster(); break;
        case 113: _t->video_player_slower(); break;
        default: ;
        }
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        switch (_id) {
        default: *reinterpret_cast<int*>(_a[0]) = -1; break;
        case 6:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< QAction* >(); break;
            }
            break;
        case 13:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< QAction* >(); break;
            }
            break;
        case 17:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< QAction* >(); break;
            }
            break;
        case 51:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< QAction* >(); break;
            }
            break;
        case 52:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< QAction* >(); break;
            }
            break;
        case 53:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< QAction* >(); break;
            }
            break;
        case 85:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< QAction* >(); break;
            }
            break;
        case 110:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< QAbstractSocket::SocketError >(); break;
            }
            break;
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject UI_Mainwindow::staticMetaObject = { {
    &QMainWindow::staticMetaObject,
    qt_meta_stringdata_UI_Mainwindow.data,
    qt_meta_data_UI_Mainwindow,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *UI_Mainwindow::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *UI_Mainwindow::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_UI_Mainwindow.stringdata0))
        return static_cast<void*>(this);
    return QMainWindow::qt_metacast(_clname);
}

int UI_Mainwindow::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QMainWindow::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 114)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 114;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 114)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 114;
    }
    return _id;
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
