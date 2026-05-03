# 🚀 Guía Rápida: Setup en GitHub

## Paso 1: Crear Repositorio en GitHub

1. Ve a https://github.com
2. Click en "New repository"
3. Nombre: `ml-pipeline-cicd`
4. Descripción: "Automated ML Pipeline with MLflow and GitHub Actions"
5. Público o Privado según preferencia
6. **NO** marcar "Initialize with README"
7. Click "Create repository"

## Paso 2: Subir el Proyecto

En tu terminal local:

```bash
# Navegar al proyecto
cd ml-pipeline-project

# Inicializar git (si no está ya)
git init

# Agregar todos los archivos
git add .

# Primer commit
git commit -m "Initial commit: ML pipeline with CI/CD"

# Conectar con GitHub (reemplazar con tu URL)
git remote add origin https://github.com/TU_USUARIO/ml-pipeline-cicd.git

# Subir al repositorio
git branch -M main
git push -u origin main
```

## Paso 3: Verificar GitHub Actions

1. Ve a tu repositorio en GitHub
2. Click en la pestaña "Actions"
3. Deberías ver el workflow "ML Pipeline CI/CD" ejecutándose
4. Click en el run para ver detalles
5. Una vez completado, descarga los artifacts generados

## Paso 4: Ver Artifacts

1. En la página del workflow run
2. Scroll hacia abajo hasta "Artifacts"
3. Descarga:
   - `mlflow-artifacts` (datos de tracking)
   - `trained-model` (modelo entrenado)

## Paso 5: Habilitar MLflow (Opcional)

Si tienes un entorno con MLflow disponible:

```bash
# Instalar MLflow
pip install mlflow

# Descomentar en requirements.txt
# Editar: mlflow>=2.5.0 (quitar el #)

# Ejecutar pipeline
make train

# Ver UI de MLflow
mlflow ui
# Acceder a: http://localhost:5000
```

## Configuración Adicional

### Secrets de GitHub (si necesario)

Para proyectos que requieren credenciales:

1. Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Agregar: `MLFLOW_TRACKING_URI`, `AWS_ACCESS_KEY`, etc.

### Branch Protection

Para proyectos en equipo:

1. Settings → Branches
2. Add rule para `main`
3. Marcar: "Require status checks to pass"
4. Seleccionar el workflow de ML Pipeline

## Triggers del CI/CD

El workflow se ejecuta automáticamente en:

- ✅ Push a branch `main` o `develop`
- ✅ Pull Requests hacia `main`
- ✅ Manual desde GitHub Actions tab

## Solución de Problemas

### Error: "no matching distribution found for mlflow"

Solución: El proyecto funciona sin MLflow usando JSON como fallback. Para usar MLflow, asegúrate de tener Python 3.8+ y pip actualizado.

### Error: "GitHub Actions failed"

1. Verifica que requirements.txt esté actualizado
2. Revisa los logs en la pestaña Actions
3. Asegúrate de que todos los archivos estén en el repositorio

### Dataset no descarga

No hay problema - el proyecto genera automáticamente un dataset sintético si la descarga falla.

## Verificación Final

Checklist antes de presentar:

- [ ] Repositorio creado y público
- [ ] Código subido completamente
- [ ] GitHub Actions ejecutado exitosamente
- [ ] Artifacts disponibles para descarga
- [ ] README.md visible en la página principal
- [ ] EVIDENCIA.md incluida

## URL para Entregar

Una vez configurado, tu URL será:

```
https://github.com/TU_USUARIO/ml-pipeline-cicd
```

---

**¡Listo para presentar!** 🎉
