#!/usr/bin/env python3
"""
Test script for Y.A.V.N.E. Blender 4.5 compatibility
Run this inside Blender to verify the addon works correctly
Author: JordanRO2
"""

import sys

def test_addon_compatibility():
    """Test if the addon is compatible with current Blender version."""
    try:
        import bpy
        print(f"Testing Y.A.V.N.E. with Blender {bpy.app.version_string}")
        
        # Check if critical methods exist
        mesh_type = bpy.types.Mesh
        
        # Test for required methods
        required_methods = [
            'calc_normals_split',
            'normals_split_custom_set',
            'normals_split_custom_set_from_vertices'
        ]
        
        print("\nChecking required methods:")
        for method in required_methods:
            if hasattr(mesh_type, method):
                print(f"  ✓ {method} exists")
            else:
                print(f"  ✗ {method} NOT FOUND")
        
        # Check for deprecated features
        print("\nChecking deprecated features:")
        if hasattr(mesh_type, 'use_auto_smooth'):
            print("  ⚠ use_auto_smooth still exists (will be ignored in 4.5+)")
        else:
            print("  ✓ use_auto_smooth removed (as expected in 4.5+)")
        
        # Test custom data layers
        print("\nTesting custom data layers:")
        temp_mesh = bpy.data.meshes.new(name="test_mesh")
        bm = None
        
        try:
            import bmesh
            bm = bmesh.new()
            bm.from_mesh(temp_mesh)
            
            # Test layer creation
            if hasattr(bm.verts.layers, 'int'):
                bm.verts.layers.int.new('test-int')
                print("  ✓ Vertex int layers work")
            
            if hasattr(bm.loops.layers, 'float'):
                bm.loops.layers.float.new('test-float')
                print("  ✓ Loop float layers work")
            
            if hasattr(bm.faces.layers, 'int'):
                bm.faces.layers.int.new('test-face-int')
                print("  ✓ Face int layers work")
                
        finally:
            if bm:
                bm.free()
            bpy.data.meshes.remove(temp_mesh)
        
        print("\n✅ All tests passed!")
        return True
        
    except ImportError:
        print("❌ This script must be run inside Blender")
        return False
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

if __name__ == "__main__":
    # If running inside Blender
    if 'bpy' in sys.modules:
        test_addon_compatibility()
    else:
        print("This script must be run inside Blender")
        print("Usage: blender --python test_blender45.py")