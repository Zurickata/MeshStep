# meshstep.pro
# Usamos += para evitar errores con \ y espacios invisibles

SOURCES += app/interface/main_window.py
SOURCES += app/interface/options_dialog.py
SOURCES += app/interface/manual_dialog.py
SOURCES += app/logic/mesh_generator.py
SOURCES += app/visualization/RefinementViewer.py
SOURCES += app/logic/main_window_logic.py
SOURCES += app/interface/panel_derecho.py

TRANSLATIONS = translations/meshstep_en.ts \
               translations/meshstep_es.ts