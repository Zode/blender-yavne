# TODO: Y.A.V.N.E. - Actualización completa para Blender 4.5+

## 📋 Resumen General
Este documento detalla todos los cambios necesarios para actualizar Y.A.V.N.E. a Blender 4.5+ con todas las mejoras y optimizaciones posibles.

## ✅ Cambios ya realizados
- [x] Actualizado `bl_info` versión a (2, 1, 1) y Blender a (4, 5, 0)
- [x] Reemplazado módulo `imp` por `importlib` en `__init__.py`
- [x] Eliminada propiedad `use_auto_smooth` de preferences.py
- [x] Actualizado panel.py para remover UI de auto_smooth

## 🔧 Cambios pendientes críticos

### 1. **operators.py - Actualización de manejo de normales**

#### ❌ PROBLEMA: Métodos inexistentes en Blender 4.5
```python
# Línea 979: calc_normals_split() NO EXISTE en Mesh de Blender 4.5
# Línea 1014-1015: has_custom_normals y create_normals_split() NO EXISTEN
```

#### ✅ SOLUCIÓN:
```python
# REEMPLAZAR líneas 978-980 con:
# En Blender 4.5+ las normales se manejan automáticamente
overlay.show_edge_sharp = True

# REEMPLAZAR líneas 1014-1017 con:
# Blender 4.5 maneja automáticamente las normales personalizadas
mesh.normals_split_custom_set([(n.x, n.y, n.z) for n in split_normals])
```

### 2. **operators.py - Actualización de GPU API**

#### ⚠️ ADVERTENCIA: API GPU cambió en Blender 4.0+
```python
# Línea 547, 557: gpu.shader.from_builtin() puede estar deprecado
```

#### ✅ SOLUCIÓN:
```python
# Verificar y actualizar a nueva API si es necesario:
# Blender 4.0+ usa gpu.shader.from_builtin('UNIFORM_COLOR') 
# pero podría cambiar a gpu.shader.from_builtin('3D_UNIFORM_COLOR')
```

### 3. **operators.py - Optimización de __init__ y __del__**

#### ⚠️ MEJORA: Añadir super().__init__() correctamente
```python
# Líneas 51-57 y 855-860: __init__ debe llamar super() con *args, **kwargs
# Líneas 862-867: __del__ verifica innecesariamente hasattr(super(), '__del__')
```

#### ✅ SOLUCIÓN:
```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.addon = None
    self.ensure_custom_layers()

def __del__(self):
    # Solo llamar si existe el método en la clase padre
    if hasattr(super().__class__, '__del__'):
        super().__del__()
```

## 🚀 Mejoras y optimizaciones adicionales

### 4. **Modernización del código Python**

#### a) Usar anotaciones de tipo (Type Hints)
```python
# utils.py
from typing import List, Set, Optional, Tuple
import mathutils

def split_loops(
    vert: 'bmesh.types.BMVert', 
    angle: float = math.pi, 
    use_flat_faces: bool = False
) -> List[List['bmesh.types.BMLoop']]:
    ...
```

#### b) Usar f-strings en lugar de concatenación
```python
# Cambiar esto:
'Maximum angle between faces to be considered as smooth'
# Por esto:
f'Maximum angle between faces to be considered as smooth'
```

### 5. **Mejorar manejo de errores**

#### Añadir try-except en operaciones críticas:
```python
def execute(self, context):
    try:
        mesh = context.edit_object.data
        # ... código ...
    except AttributeError as e:
        self.report({'ERROR'}, f"No mesh object selected: {e}")
        return {'CANCELLED'}
    except Exception as e:
        self.report({'ERROR'}, f"Unexpected error: {e}")
        return {'CANCELLED'}
```

### 6. **Optimización de multiprocessing**

#### ⚠️ PROBLEMA: Línea 990 desactiva multiprocessing en POSIX
```python
# operators.py línea 990
if len(bm.verts) > 5000 and os.name not in {'nt', 'posix'}:
```

#### ✅ SOLUCIÓN:
```python
# Usar concurrent.futures en lugar de multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed

# O mejor aún, usar ThreadPoolExecutor para evitar problemas de serialización
from concurrent.futures import ThreadPoolExecutor
```

### 7. **Actualizar documentación y comentarios**

#### Añadir docstrings con formato Google/NumPy:
```python
def split_loops(vert, angle=math.pi, use_flat_faces=False):
    """Split vertex linked loops into groups based on edge properties.
    
    Args:
        vert: Common vertex shared by loops
        angle: Face edge angle threshold in radians
        use_flat_faces: Flag controlling if vertex normals are split
                       along flat shaded face boundaries
    
    Returns:
        List of grouped loops
    
    Example:
        >>> loops = split_loops(vertex, math.pi/2)
    """
```

### 8. **Mejorar el sistema de custom data layers**

#### Verificar si los layers existen antes de acceder:
```python
def ensure_custom_layers(self):
    """Ensure necessary custom data layers exist."""
    mesh = bpy.context.edit_object.data
    bm = bmesh.from_edit_mesh(mesh)
    
    # Usar get() para evitar KeyError
    vert_int_layers = bm.verts.layers.int
    if not vert_int_layers.get('vertex-normal-weight'):
        vert_int_layers.new('vertex-normal-weight')
```

### 9. **Actualizar panel.py para nueva UI**

#### Cambiar location de Tool Shelf (deprecado) a Sidebar:
```python
bl_space_type = 'VIEW_3D'
bl_region_type = 'UI'  # En lugar de 'TOOLS'
bl_category = "Edit"   # O crear nueva categoría "YAVNE"
```

### 10. **Añadir validación de versión**

#### En __init__.py añadir verificación:
```python
def register():
    # Verificar versión de Blender
    if bpy.app.version < (4, 5, 0):
        raise Exception("Y.A.V.N.E. requiere Blender 4.5 o superior")
```

## 📝 Archivos a modificar

1. **operators.py** - CRÍTICO
   - [ ] Eliminar calc_normals_split() (línea 979)
   - [ ] Eliminar has_custom_normals y create_normals_split() (líneas 1014-1015)
   - [ ] Actualizar GPU shaders si es necesario
   - [ ] Mejorar __init__ y __del__
   - [ ] Añadir manejo de errores

2. **panel.py** - MEDIO
   - [ ] Actualizar bl_region_type a 'UI'
   - [ ] Considerar nueva organización de UI

3. **utils.py** - BAJO
   - [ ] Añadir type hints
   - [ ] Optimizar funciones

4. **preferences.py** - COMPLETO ✅
   - [x] Ya actualizado

5. **__init__.py** - COMPLETO ✅
   - [x] Ya actualizado

## 🧪 Testing necesario

1. **Probar cada operador individualmente:**
   - [ ] ManageVertexNormalWeight
   - [ ] ManageFaceNormalInfluence
   - [ ] GetNormalVector
   - [ ] SetNormalVector
   - [ ] MergeVertexNormals
   - [ ] TransferShading
   - [ ] UpdateVertexNormals

2. **Verificar:**
   - [ ] Custom data layers se crean correctamente
   - [ ] GPU drawing funciona
   - [ ] Multiprocessing no causa crashes
   - [ ] UI aparece en el lugar correcto

## 📌 Prioridad de implementación

1. **CRÍTICO** - Arreglar métodos de normales inexistentes
2. **ALTO** - Actualizar GPU API si es necesario
3. **MEDIO** - Mejorar manejo de errores
4. **BAJO** - Optimizaciones y modernización del código

## 🎯 Resultado esperado

Después de implementar todos estos cambios, Y.A.V.N.E. será:
- ✅ Totalmente compatible con Blender 4.5+
- ✅ Más robusto con mejor manejo de errores
- ✅ Más eficiente con código optimizado
- ✅ Más mantenible con mejor documentación
- ✅ Preparado para futuras versiones de Blender

---
**Autor:** JordanRO2
**Fecha:** 2024
**Versión objetivo:** Y.A.V.N.E. 2.2.0 para Blender 4.5+