bl_info = {
    "name": "Clean up F-Curve Modifier",
    "author": "Your Name",
    "version": (1, 1),
    "blender": (4, 2, 0),
    "location": "Graph Editor > Channel",
    "description": "Deletes all F-Curve modifiers from selected channels. 日本語: Fカーブモディファイアを全て削除",
    "warning": "",
    "wiki_url": "",
    "category": "Animation",
}

import bpy

# アドオンのメイン機能となるオペレータークラス
class GRAPH_OT_remove_all_fcurve_modifiers(bpy.types.Operator):
    bl_idname = "graph.remove_all_fcurve_modifiers"
    bl_label = "Clean up F-Curve Modifier"
    bl_description = "Deletes all F-Curve modifiers from selected channels."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        fcurves = context.selected_editable_fcurves
        
        if not fcurves:
            self.report({'WARNING'}, "No F-Curves selected in the Graph Editor.")
            return {'CANCELLED'}
        
        for fcurve in fcurves:
            while fcurve.modifiers:
                fcurve.modifiers.remove(fcurve.modifiers[0])
        
        self.report({'INFO'}, f"Successfully removed all modifiers from {len(fcurves)} F-Curves.")
        
        if context.area.type == 'GRAPH_EDITOR':
            context.area.tag_redraw()
            
        return {'FINISHED'}

# グラフエディタの「チャンネル」メニューに項目を追加する関数
def menu_func(self, context):
    # UIの言語が日本語かどうかをチェック
    if bpy.app.translations.locale == 'ja_JP':
        op_text = "Fカーブモディファイアを全て削除"
    else:
        op_text = "Clean up F-Curve Modifier"
    
    self.layout.operator(
        GRAPH_OT_remove_all_fcurve_modifiers.bl_idname,
        text=op_text
    )

def register():
    bpy.utils.register_class(GRAPH_OT_remove_all_fcurve_modifiers)
    bpy.types.GRAPH_MT_channel.append(menu_func)

def unregister():
    bpy.utils.unregister_class(GRAPH_OT_remove_all_fcurve_modifiers)
    bpy.types.GRAPH_MT_channel.remove(menu_func)

if __name__ == "__main__":
    register()