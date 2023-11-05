import ezdxf

def create_scene(filepath):
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    doc.header['$INSUNITS'] = 6
    
    # scene_out = doc.blocks.new(name='SCENE')
    # # scene_out.add_lwpolyline([(-5020, 5020), (5020, 5020), 
    # #                           (5020, -5020), (-5020, -5020), 
    # #                           (-5020, 4900), (-5000, 4900),
    # #                           (-5000, -5000), (5000, -5000),
    # #                           (5000, 5000), (-5020, 5000),
    # #                           (-5020, 5020)])
    
    # scene_out.add_lwpolyline([(-5.02, 5.02), (5.02, 5.02), 
    #                           (5.02, -5.02), (-5.02, -5.02), 
    #                           (-5.02, 4.9), (-5.0, 4.9),
    #                           (-5.0, -5.0), (5.0, -5.0),
    #                           (5.0, 5.0), (-5.02, 5.0),
    #                           (-5.02, 5.02)])
    points = [(-5.02, 5.02), (5.02, 5.02), 
                (5.02, -5.02), (-5.02, -5.02), 
                (-5.02, 4.9), (-5.0, 4.9),
                (-5.0, -5.0), (5.0, -5.0),
                (5.0, 5.0), (-5.02, 5.0),
                (-5.02, 5.02)]
    
    msp.add_lwpolyline(points)

    msp.add_line((1,4),(3,4))

    # scene_in = doc.blocks.new(name='SCENEIN')
    # scene_in.add_lwpolyline([(5000, 5000), (5000, -5000), (-5000, -5000), (-5000, 5000), (5000, 5000)])


    tag = doc.blocks.new(name='TAG5X5')
    tag.add_lwpolyline([(0, 0), (0, 0.148), (0.148, 0.148), (0.148, 0), (0, 0)])

    # msp.add_blockref('SCENE', (0, 0))
    # # msp.add_blockref('SCENEOUT', (0, 0))
    # # msp.add_blockref('SCENEIN', (0, 0))

    msp.add_blockref('TAG5X5', (1, 1))
    msp.add_blockref('TAG5X5', (1, 2))

    doc.saveas(filepath)


if __name__ == "__main__":
    filepath = "/home/liufeng/isaac_test/lh/python_usd/demo.dxf"
    create_scene(filepath)