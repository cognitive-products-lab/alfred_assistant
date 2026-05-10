# ============================================================
# ALFRED - check_tools.ps1
# Verification de la presence de tous les outils necessaires
# ============================================================
# UTILISATION :
#   cd D:\PROJET_ALFRED\ALFRED_PC
#   .\scripts\check_tools.ps1
#
# Ce script verifie :
#   1. Python (version minimale 3.11)
#   2. pip
#   3. Git
#   4. VS Code
#   5. PowerShell (version minimale 5.1)
#   6. L'environnement virtuel .venv
#   7. Les packages Python requis (requirements.txt)
#   8. Les outils de securite (bandit, pip-audit)
#   9. Les outils de test (pytest)
#  10. Les fichiers et dossiers cles du projet
# ============================================================

# -- Compteurs globaux -----------------------------------------
$totalChecks  = 0
$passedChecks = 0
$failedChecks = 0
$warnings     = 0

# -- Fonctions d'affichage -------------------------------------
function Write-Header($title) {
    Write-Host ""
    Write-Host "-------------------------------------------------" -ForegroundColor DarkCyan
    Write-Host "  $title" -ForegroundColor Cyan
    Write-Host "-------------------------------------------------" -ForegroundColor DarkCyan
}

function Write-OK($label, $detail = "") {
    $script:totalChecks++
    $script:passedChecks++
    $info = if ($detail) { " ($detail)" } else { "" }
    Write-Host "  [OK] $label$info" -ForegroundColor Green
}

function Write-FAIL($label, $hint = "") {
    $script:totalChecks++
    $script:failedChecks++
    Write-Host "  [ECHEC] $label" -ForegroundColor Red
    if ($hint) {
        Write-Host "     -> $hint" -ForegroundColor DarkRed
    }
}

function Write-WARN($label, $hint = "") {
    $script:totalChecks++
    $script:warnings++
    Write-Host "  [AVERT] $label" -ForegroundColor Yellow
    if ($hint) {
        Write-Host "     -> $hint" -ForegroundColor DarkYellow
    }
}

# ============================================================
# BANNIERE
# ============================================================
Write-Host ""
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "         ALFRED - Verification des outils           " -ForegroundColor Cyan
Write-Host "     Local-first | Security by Design               " -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Date    : $(Get-Date -Format 'dd/MM/yyyy HH:mm')" -ForegroundColor DarkGray
Write-Host "  Dossier : $(Get-Location)" -ForegroundColor DarkGray

# -- Verifier qu'on est au bon endroit ------------------------
$currentDir = Split-Path -Leaf (Get-Location)
if ($currentDir -ne "ALFRED_PC") {
    Write-Host ""
    Write-Host "  ATTENTION : Lance ce script depuis D:\PROJET_ALFRED\ALFRED_PC\" -ForegroundColor Yellow
    Write-Host "     Dossier actuel : $currentDir" -ForegroundColor Yellow
    $confirm = Read-Host "  Continuer quand meme ? (o/n)"
    if ($confirm -ne "o") { exit }
}

# ============================================================
# 1. OUTILS SYSTEME
# ============================================================
Write-Header "1/6 - Outils systeme"

# Python
try {
    $pyVersion = python --version 2>&1
    if ($pyVersion -match "Python (\d+)\.(\d+)") {
        $major = [int]$Matches[1]
        $minor = [int]$Matches[2]
        if ($major -ge 3 -and $minor -ge 11) {
            Write-OK "Python" "$pyVersion"
        } else {
            Write-FAIL "Python version insuffisante : $pyVersion" "Minimum requis : Python 3.11 - https://www.python.org/downloads/"
        }
    }
} catch {
    Write-FAIL "Python introuvable" "Installer Python 3.11+ depuis https://www.python.org/downloads/"
}

# pip
try {
    $pipVersion = pip --version 2>&1
    if ($pipVersion -match "pip") {
        Write-OK "pip" "$($pipVersion -split ' ')[1]"
    } else {
        Write-FAIL "pip introuvable"
    }
} catch {
    Write-FAIL "pip introuvable" "Reinstaller Python avec l'option 'Add pip' cochee"
}

# Git
try {
    $gitVersion = git --version 2>&1
    if ($gitVersion -match "git version") {
        Write-OK "Git" "$gitVersion"
    } else {
        Write-FAIL "Git introuvable"
    }
} catch {
    Write-FAIL "Git introuvable" "Installer Git depuis https://git-scm.com/download/win"
}

# VS Code
try {
    $codeVersion = code --version 2>&1
    if ($codeVersion) {
        Write-OK "VS Code" "v$($codeVersion[0])"
    } else {
        Write-WARN "VS Code non detecte dans le PATH" "Installer VS Code depuis https://code.visualstudio.com/ ou ajouter au PATH"
    }
} catch {
    Write-WARN "VS Code non detecte dans le PATH" "Peut etre installe sans etre accessible via 'code'"
}

# PowerShell
$psVersion = $PSVersionTable.PSVersion
if ($psVersion.Major -ge 5) {
    Write-OK "PowerShell" "v$($psVersion.Major).$($psVersion.Minor)"
} else {
    Write-FAIL "PowerShell version insuffisante : v$($psVersion.Major)" "Minimum requis : 5.1"
}

# ============================================================
# 2. ENVIRONNEMENT VIRTUEL PYTHON
# ============================================================
Write-Header "2/6 - Environnement virtuel Python"

if (Test-Path ".venv") {
    Write-OK "Dossier .venv present"
    if (Test-Path ".venv\Scripts\python.exe") {
        Write-OK ".venv\Scripts\python.exe"
    } else {
        Write-FAIL ".venv\Scripts\python.exe manquant" "Recreer : python -m venv .venv"
    }
    if (Test-Path ".venv\Scripts\Activate.ps1") {
        Write-OK ".venv\Scripts\Activate.ps1"
    } else {
        Write-FAIL ".venv\Scripts\Activate.ps1 manquant"
    }
} else {
    Write-FAIL "Environnement virtuel .venv absent" "Creer : python -m venv .venv"
}

# ============================================================
# 3. PACKAGES PYTHON REQUIS
# ============================================================
Write-Header "3/6 - Packages Python (requirements.txt)"

$requiredPackages = @(
    @{ name = "python-dotenv";    import = "dotenv"      },
    @{ name = "pydantic";         import = "pydantic"    },
    @{ name = "cryptography";     import = "cryptography"},
    @{ name = "bcrypt";           import = "bcrypt"      },
    @{ name = "PyJWT";            import = "jwt"         },
    @{ name = "bandit";           import = $null         },
    @{ name = "pip-audit";        import = $null         },
    @{ name = "pytest";           import = "pytest"      },
    @{ name = "pytest-cov";       import = $null         },
    @{ name = "python-dateutil";  import = "dateutil"    }
)

$pythonExe = if (Test-Path ".venv\Scripts\python.exe") { ".venv\Scripts\python.exe" } else { "python" }

foreach ($pkg in $requiredPackages) {
    if ($pkg.import) {
        $result = & $pythonExe -c "import $($pkg.import)" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-OK $pkg.name
        } else {
            Write-FAIL "$($pkg.name) non installe" "pip install $($pkg.name)"
        }
    } else {
        $pipList = & $pythonExe -m pip show $pkg.name 2>&1
        if ($pipList -match "Name:") {
            Write-OK $pkg.name
        } else {
            Write-FAIL "$($pkg.name) non installe" "pip install $($pkg.name)"
        }
    }
}

# ============================================================
# 4. FICHIERS RACINE DU PROJET
# ============================================================
Write-Header "4/6 - Fichiers racine du projet"

$rootFiles = @(
    @{ path = "requirements.txt";  critical = $true  },
    @{ path = "paths.py";          critical = $true  },
    @{ path = ".env";              critical = $true  },
    @{ path = ".env.example";      critical = $false },
    @{ path = ".gitignore";        critical = $false },
    @{ path = "README.md";         critical = $false },
    @{ path = "pyproject.toml";    critical = $false }
)

foreach ($f in $rootFiles) {
    if (Test-Path $f.path) {
        Write-OK $f.path
    } elseif ($f.critical) {
        Write-FAIL "$($f.path) MANQUANT" "Fichier critique - consulter le guide bootstrap"
    } else {
        Write-WARN "$($f.path) absent" "Non bloquant mais recommande"
    }
}

# ============================================================
# 5. STRUCTURE DES DOSSIERS CLES
# ============================================================
Write-Header "5/6 - Structure des dossiers cles"

$keyDirs = @(
    "src", "config", "data", "logs", "assets",
    "knowledges", "tests", "scripts", "auth",
    "src\core", "src\input", "src\output",
    "src\memory", "src\knowledge", "src\security",
    "src\v1", "src\v2", "src\v3", "src\v4",
    "config\v1", "config\v2", "config\v3", "config\v4", "config\security",
    "data\memory", "data\profile", "data\security",
    "data\v2", "data\v3", "data\v4",
    "knowledges\human", "knowledges\professional", "knowledges\lifestyle"
)

foreach ($dir in $keyDirs) {
    if (Test-Path $dir) {
        Write-OK $dir
    } else {
        Write-WARN "$dir absent" "Lancer bootstrap_project.ps1 pour creer l'arborescence"
    }
}

$keyFiles = @(
    "src\main.py",
    "src\__init__.py",
    "src\security\__init__.py",
    "config\settings.json",
    "config\security\security_settings.json",
    "data\user_memory.json",
    "knowledges\manifest.json"
)

foreach ($f in $keyFiles) {
    if (Test-Path $f) {
        Write-OK $f
    } else {
        Write-WARN "$f absent" "Creer via bootstrap_project.ps1 ou manuellement"
    }
}

# ============================================================
# 6. OUTILS DE SECURITE & AUDIT
# ============================================================
Write-Header "6/6 - Outils de securite et audit"

# bandit
try {
    $banditOut = & $pythonExe -m bandit --version 2>&1
    if ($banditOut -match "bandit") {
        Write-OK "bandit (scan securite code)" "$banditOut"
    } else {
        Write-FAIL "bandit non fonctionnel" "pip install bandit"
    }
} catch {
    Write-FAIL "bandit introuvable" "pip install bandit"
}

# pip-audit
try {
    $auditOut = & $pythonExe -m pip_audit --version 2>&1
    if ($auditOut -match "\d") {
        Write-OK "pip-audit (audit dependances)" "v$auditOut"
    } else {
        Write-FAIL "pip-audit non fonctionnel" "pip install pip-audit"
    }
} catch {
    Write-FAIL "pip-audit introuvable" "pip install pip-audit"
}

# pytest
try {
    $pytestOut = & $pythonExe -m pytest --version 2>&1
    if ($pytestOut -match "pytest") {
        Write-OK "pytest (tests)" "$pytestOut"
    } else {
        Write-FAIL "pytest non fonctionnel" "pip install pytest"
    }
} catch {
    Write-FAIL "pytest introuvable" "pip install pytest"
}

# .env dans .gitignore
if (Test-Path ".gitignore") {
    $gitIgnoreContent = Get-Content ".gitignore" -Raw
    if ($gitIgnoreContent -match "\.env") {
        Write-OK ".env exclu du versioning (.gitignore)"
    } else {
        Write-WARN ".env non explicitement exclu du .gitignore" "Ajouter '.env' dans .gitignore IMMEDIATEMENT"
    }
}

# ============================================================
# RESUME FINAL
# ============================================================
Write-Host ""
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "              RESUME DE LA VERIFICATION             " -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Total verifications : $totalChecks" -ForegroundColor White
Write-Host "  [OK]    Succes      : $passedChecks" -ForegroundColor Green
Write-Host "  [AVERT] Avertiss.   : $warnings" -ForegroundColor Yellow
Write-Host "  [ECHEC] Echecs      : $failedChecks" -ForegroundColor Red
Write-Host ""

if ($failedChecks -eq 0 -and $warnings -eq 0) {
    Write-Host "  Environnement parfait - Pret pour le developpement !" -ForegroundColor Green
} elseif ($failedChecks -eq 0) {
    Write-Host "  Environnement fonctionnel avec $warnings avertissement(s) mineurs." -ForegroundColor Yellow
    Write-Host "  Tu peux commencer - corrige les avertissements quand tu peux." -ForegroundColor Yellow
} else {
    Write-Host "  $failedChecks outil(s) manquant(s) - Corrige les ECHECS avant de continuer." -ForegroundColor Red
    Write-Host "  Consulte les hints ci-dessus pour chaque echec." -ForegroundColor DarkRed
}

Write-Host ""
Write-Host "  Prochaine etape : .\scripts\bootstrap_project.ps1" -ForegroundColor DarkGray
Write-Host ""