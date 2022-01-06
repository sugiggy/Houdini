import toolutils
scene = toolutils.sceneViewer()
flipbook_options = scene.flipbookSettings().stash()
flipbook_options.useResolution(0)
scene.flipbook(scene.curViewport(),flipbook_options)
