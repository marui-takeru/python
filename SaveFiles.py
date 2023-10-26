# bpyインポート
import bpy

def delete_all_objects():
    # 全シーンオブジェクトを削除する
    for item in bpy.context.scene.objects:
        bpy.context.scene.objects.unlink(item)
    # 全データオブジェクトを削除する
    for item in bpy.data.objects:
        bpy.data.objects.remove(item)
    # 全メッシュデータを削除する
    for item in bpy.data.meshes:
        bpy.data.meshes.remove(item)
    # 全マテリアルデータを削除する
    for item in bpy.data.materials:
        bpy.data.materials.remove(item)
    return

# Cubeオブジェクトの削除
bpy.context.scene.collection.children['Collection'].objects.unlink(bpy.data.objects['Cube'])

# Cameraオブジェクトの削除
bpy.context.scene.collection.children['Collection'].objects.unlink(bpy.data.objects['Camera'])

# Lightオブジェクトの削除
bpy.context.scene.collection.children['Collection'].objects.unlink(bpy.data.objects['Light'])


# gltfデータの読み込み
gltf_path='/Users/takerumarui/Desktop/ccc_google_3.gltf'
bpy.ops.import_scene.gltf(filepath=gltf_path)

# objデータの出力
obj_path='/Users/takerumarui/Desktop/ccc_google_3.obj'
bpy.ops.export_scene.obj(filepath=obj_path)



# 3Dモデルの削除
# bpy.context.scene.objects.unlink(bpy.context.scene.objects)

