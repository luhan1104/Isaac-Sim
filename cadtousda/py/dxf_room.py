import sys
import ezdxf

def create_tag(filepath):
    doc = ezdxf.readfile(filepath)

    msp = doc.modelspace()

    ref = doc.blocks.new(name='REF')
    ref.add_circle((0,0), 37.5)
    msp.add_blockref('REF', (9500, 7500))

    tag1 = doc.blocks.new(name='TAG5X5')
    tag1.add_lwpolyline([(0, 0), (0, 148), (148, 148), (148, 0), (0, 0)])
    msp.add_blockref('TAG5X5', (3000, 5000), dxfattribs={
            'rotation': 30
            })
    msp.add_blockref('TAG5X5', (9500, 5000))

    tag2 = doc.blocks.new(name='TAG2XN')
    tag2.add_lwpolyline([(0, 0), (0, 57), (480, 57), (480, 0), (0, 0)])
    msp.add_blockref('TAG2XN', (6000, 5000))
    msp.add_blockref('TAG2XN', (13000, 5000), dxfattribs={
            'rotation': 90
            })
    

    doc.saveas(filepath)


if __name__ == "__main__":
    n = len(sys.argv)
    if n < 1:
        filepath = "/home/liufeng/isaac_test/cadtousda/dxf/room.dxf"
    else:
        filepath = sys.argv[1]
    create_tag(filepath)