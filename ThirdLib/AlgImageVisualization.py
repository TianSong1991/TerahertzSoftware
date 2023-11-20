# -*- coding: utf-8 -*-
"""
@Create Time: 2022/1/4 15:14
@Author: Kevin
@Python Version：3.7.6
"""
from mayavi.core.ui.api import MayaviScene, MlabSceneModel,SceneEditor
from traits.api import HasTraits, Instance
from traitsui.api import View, Item
import mayavi.mlab as mlab
from tvtk.util import ctf
from ThirdLib.AlgFunctions import ImageFunctions

#3d数据显示mayavi处理
class Visualization(HasTraits):
    def __init__(self,THzsig_intp,use_mayavi):
        self.THzsig_intp = THzsig_intp
        self.use_mayavi = use_mayavi
        self.volume = None
    scene = Instance(MlabSceneModel, ())
    def update(self,THzsig_intp,mode,Type):
        self.THzsig_intp = THzsig_intp
        self.mode = mode
        self.scene.mlab.clf()
        self.scene.scene_editor._tool_bar.tools[0].visible = False
        self.scene.scene_editor._tool_bar.tools[-1].visible = False
        self.scene.scene_editor._tool_bar.tools[-3].visible = False
        if self.use_mayavi == 1:
            if len(self.THzsig_intp) > 0:
                if Type == "volum":
                    self.volume = mlab.pipeline.volume(mlab.pipeline.scalar_field(self.THzsig_intp.transpose((2,0,1))))
                    c = ctf.save_ctfs(self.volume._volume_property)
                    max_range = 1000
                    c = ImageFunctions.obtain_alpha(c,max_range,self.mode)
                    ctf.load_ctfs(c, self.volume._volume_property)
                    self.volume.update_ctf = True
                    self.scene.mlab.gcf().scene.background = (0.9, 0.9, 0.9)
                else:
                    self.scene.mlab.volume_slice(self.THzsig_intp.transpose((2,0,1)), colormap=self.mode, plane_orientation='x_axes', slice_index=0)
                    self.scene.mlab.volume_slice(self.THzsig_intp.transpose((2,0,1)), colormap=self.mode, plane_orientation='y_axes', slice_index=0)
                    self.scene.mlab.volume_slice(self.THzsig_intp.transpose((2,0,1)), colormap=self.mode, plane_orientation='z_axes', slice_index=0)

    def updatealpha(self,alpha):
        if self.use_mayavi == 1:
            c = ctf.save_ctfs(self.volume._volume_property)
            minv, maxv = c['range']
            alphas = []
            value = alpha/100*(maxv-minv)+minv
            alphas.append([value, 0.01])
            alphas.append([maxv, 1])
            c['alpha'] = alphas
            ctf.load_ctfs(c, self.volume._volume_property)
            self.volume.update_ctf = True
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=250, width=300, show_label=False),
                resizable=True
                )