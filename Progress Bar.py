import ui

class ProgressBar (ui.View):
    def __init__(self):
        pass
    def draw(self):
        pass
        width, height = ui.get_window_size()
        print('width: %d, height %d' % (width, height) )

        bar_height = 30
        bar_width = 520
        bar_x = 10
        bar_y = height / 2
        ui.set_color(0.5)
        ui.fill_rect(bar_x, bar_y, bar_width, bar_height)
 
#pb = ProgressBar()
pb = ui.load_view('Progress Bar')
pb.present('sheet')

#v = ui.load_view('Progress Bar')
#v = ui.load_view()

#v.present('sheet')

#progress = ui.Path()
#progress.line_width = 20.0
#progress.move_to(10, (540/2))
#progress.line_to((540-10), (540/2))
#progress.stroke()
