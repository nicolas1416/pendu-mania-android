"""Personnalise le projet Android généré : icône, plein écran."""
import glob, os
from PIL import Image

RES = "android/app/src/main/res"
TAILLES = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
icone = Image.open("outils/icone.png").convert("RGBA")
premier = Image.open("outils/icone_premier_plan.png").convert("RGBA")
for dens, t in TAILLES.items():
    dossier = os.path.join(RES, "mipmap-" + dens)
    os.makedirs(dossier, exist_ok=True)
    petit = icone.resize((t, t), Image.LANCZOS)
    petit.save(os.path.join(dossier, "ic_launcher.png"))
    petit.save(os.path.join(dossier, "ic_launcher_round.png"))
    premier.resize((t * 9 // 4, t * 9 // 4), Image.LANCZOS).save(os.path.join(dossier, "ic_launcher_foreground.png"))

fond = os.path.join(RES, "values", "ic_launcher_background.xml")
with open(fond, "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
            '    <color name="ic_launcher_background">#4A3B2F</color>\n</resources>\n')

activite = glob.glob("android/app/src/main/java/**/MainActivity.java", recursive=True)[0]
with open(activite, "w", encoding="utf-8") as f:
    f.write('''package fr.pendumania.jeu;

import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.core.view.WindowInsetsControllerCompat;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) {
            WindowInsetsControllerCompat c = WindowCompat.getInsetsController(getWindow(), getWindow().getDecorView());
            c.hide(WindowInsetsCompat.Type.systemBars());
            c.setSystemBarsBehavior(WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
        }
    }
}
''')
print("Projet Android personnalisé :", activite)
